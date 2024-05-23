DEFINE ticker = 'SBER';

CREATE STREAM IF NOT EXISTS stream_${ticker} (
   ts TIMESTAMP,
   ts_str STRING,
   symbol STRING,
   open DOUBLE,
   high DOUBLE,
   low DOUBLE,
   close DOUBLE,
   volume DOUBLE
) WITH (
   KAFKA_TOPIC='${ticker}',
   VALUE_FORMAT='JSON',
   TIMESTAMP='ts'
);

SELECT ts_str, MIN(symbol) AS symbol, AS_VALUE(ts_str) AS ts_string, 
AVG(open) as avg_open, AVG(close) AS avg_close FROM stream_${ticker}
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY ts_str
EMIT FINAL;
