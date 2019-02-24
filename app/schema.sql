DROP TABLE IF EXISTS sensors;
DROP TABLE IF EXISTS readings;

CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    port INTEGER UNIQUE NOT NULL,
    V_high REAL NOT NULL,
    V_low REAL NOT NULL,
    pump_pin INTEGER NOT NULL
);

CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    voltage REAL NOT NULL,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id)
);
