CREATE TABLE IF NOT EXISTS sensor_data (
    sensor_id INT,
    temperature DOUBLE PRECISION,
    timestamp TIMESTAMPTZ
);
SELECT create_hypertable('sensor_data', 'timestamp', if_not_exists => TRUE);
