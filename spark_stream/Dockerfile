FROM bitnami/spark:latest
USER root
RUN install_packages python3-pip
RUN pip3 install kafka-python pyspark psycopg2
COPY spark_stream.py /app/spark_stream.py
CMD ["spark-submit", "/app/spark_stream.py"]
