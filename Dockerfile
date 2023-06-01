# Use Apache Beam base image
FROM apache/beam_python3.11_sdk:2.47.0

# Install additional Python library 
RUN pip install geopy==2.3.0

# Set the entrypoint to the Apache Beam SDK launcher
ENTRYPOINT ["/opt/apache/beam/boot"]

