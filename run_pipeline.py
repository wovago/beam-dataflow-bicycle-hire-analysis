import argparse
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from geopy import distance

# Minimal query to retrieve data only, all data transforms will be handled by beam
rides_query = """
SELECT *
FROM [bigquery-public-data:london_bicycles.cycle_hire]
"""

# Minimal query to retrieve data only, all data transforms will be handled by beam
stations_query = """
SELECT *
FROM [bigquery-public-data:london_bicycles.cycle_stations]
"""


def create_tuples(element, lookup_table, max_station_id=852):
    """Function that will lookup and harmonize station IDs"""
    ids = {"start": None, "end": None}
    for s in ["start", "end"]:
        if element[f"{s}_station_id"] is None:
            if element[f"{s}_station_logical_terminal"] in lookup_table:
                ids[s] = lookup_table[element[f"{s}_station_logical_terminal"]]
        elif element[f"{s}_station_id"] <= max_station_id:
            ids[s] = element[f"{s}_station_id"]
        elif element[f"{s}_station_id"] > max_station_id:
            if element[f"{s}_station_id"] in lookup_table:
                ids[s] = lookup_table[element[f"{s}_station_id"]]
    return (tuple([ids["start"], ids["end"]]), 1)


def calculate_distance(element, lookup_table):
    """Function that will compute geodesic distance between two stations"""
    start_id = element[0][0]
    end_id = element[0][1]
    counts = element[1]
    if start_id in lookup_table and end_id in lookup_table:
        start_lat = lookup_table[start_id]["latitude"]
        start_long = lookup_table[start_id]["longitude"]
        end_lat = lookup_table[end_id]["latitude"]
        end_long = lookup_table[end_id]["longitude"]

        dist = distance.distance((start_lat, start_long), (end_lat, end_long)).km
        total_dist = counts * dist
        return beam.Row(
            start_station_id=int(start_id),
            end_station_id=int(end_id),
            amount_of_rides=int(counts),
            total_distance_between_stations=float(total_dist),
        )


def run(argv=None):
    """Main entry point that defines and runs the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        dest="output",
        required=True,
        help="Output file to write results to",
    )
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(
        pipeline_args, job_name="count-number-of-bike-rides", save_main_session=True
    )

    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Create lookup table that maps station name to normalized ID
        station_ids = beam.pvalue.AsDict(
            pipeline
            | "Retrieve station id data"
            >> beam.io.ReadFromBigQuery(
                query=stations_query, method=beam.io.ReadFromBigQuery.Method.DIRECT_READ
            )
            | "Create tuple"
            >> beam.Map(lambda x: (int(x["terminal_name"]), int(x["id"])))
        )

        # Create lookup table that maps station ID to coordinates
        coordinates = beam.pvalue.AsDict(
            pipeline
            | "Retrieve station data"
            >> beam.io.ReadFromBigQuery(
                query=stations_query, method=beam.io.ReadFromBigQuery.Method.DIRECT_READ
            )
            | "Select mapping fields"
            >> beam.Map(
                lambda x: beam.Row(
                    id=int(x["id"]),
                    coordinates={
                        "latitude": float(x["latitude"]),
                        "longitude": float(x["longitude"]),
                    },
                )
            )
        )

        # Main pipeline that will vlean station IDs, count amount of bikerides 
        # and compute total distance
        amount_of_rides = (
            pipeline
            | "Retrieve bikeride data"
            >> beam.io.ReadFromBigQuery(
                query=rides_query, method=beam.io.ReadFromBigQuery.Method.DIRECT_READ
            )
            | "Extract name fields" >> beam.Map(create_tuples, lookup_table=station_ids)
            | "Filter incomplete tuples" >> beam.Filter(lambda x: all(x))
            | "Group and sum" >> beam.CombinePerKey(sum)
            | "Calculate distance"
            >> beam.Map(calculate_distance, lookup_table=coordinates)
            | "Filter Records with missing coordinates" >> beam.Filter(lambda x: x)
            | "Format distance record"
            >> beam.Map(
                lambda x: "{},{},{},{}".format(
                    x.start_station_id,
                    x.end_station_id,
                    x.amount_of_rides,
                    x.total_distance_between_stations,
                )
            )
            | "Write total distance to file"
            >> beam.io.WriteToText(known_args.output)
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
