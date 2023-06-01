# Apache Beam pipeline to analyze London bicycle hiring dataset with GCP Dataflow

This repository contains an Apache Beam pipeline that was used to analyze [London bicycle hiring data set](https://console.cloud.google.com/marketplace/product/greater-london-authority/london-bicycles) using GCP Dataflow.

The pipeline will source the full data set, containing 83205227 bicycle hiring events, from Google Bigquery. All subsequent data transformations, such as cleaning the station IDs, counting the number of bike hires per station and calculating total distance covered per station, are performed by the Apache Beam pipeline. The pipeline will output the total number of bicycle hires for all combinations of bicycle stations, as well as the total distance covered by all those bicyle hire events.
An overview of all pipeline processing steps as executed on GCP Dataflow can be seen in the following pipeline [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph).

<p align="center">
  <img src="img/pipeline_dag.png" alt="Apache Beam pipeline to analyze London bicyle sharing data set" style="height: 70%; width:70%;"/>
</p>
