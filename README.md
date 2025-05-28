# Temporal Batch Processing Example

This project demonstrates how to implement a batch-processing workflow using temporal.io and DuckDB. The implementation is based on a real-life use case, with some simplifications to keep the example concise and clear.

## Project Overview

For a full description of this project, you are welcome to read the accompanying [medium blogpost](https://medium.com/riskified-technology/a-story-of-million-rows-building-a-lightweight-batch-pipeline-with-temporal-and-duckdb-3c0a8aa88cca).

## Running Integration Tests

Before everything, run `poetry install` to setup the project. To run the integration tests, you'll need to start several services in separate terminal windows:

1. Start the Temporal server:
```bash
poetry run temporal-server
```

2. Start the Temporal worker:
```bash
poetry run temporal-worker
```

3. Start the fake S3 service:
```bash
poetry run fake-s3
```

4. Run the tests:
```bash
poetry run pytest
```
