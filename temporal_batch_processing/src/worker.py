import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from temporal_batch_processing.src.activities import list_files_activity, fetch_files_metadata_activity, \
    create_partitions_activity, cleanup_temporary_table_activity, enrich_orders_activity, read_orders_activity
from temporal_batch_processing.src.workflows import MainWorkflow, PartitionWorkflow, BatchWorkflow
from temporal_batch_processing.src.models.config import Config, get_config


async def worker_fn(config: Config):
    client = await Client.connect(config.temporal_server)
    worker = Worker(
        client,
        task_queue=config.task_queue,
        workflows=[MainWorkflow,
                   PartitionWorkflow,
                   BatchWorkflow],
        activities=[list_files_activity,
                    fetch_files_metadata_activity,
                    create_partitions_activity,
                    read_orders_activity,
                    enrich_orders_activity,
                    cleanup_temporary_table_activity],
    )
    await worker.run()


def run():
    worker_config = get_config()
    print(f"Starting worker with config: {worker_config}")
    asyncio.run(worker_fn(worker_config))
