import asyncio
from datetime import timedelta
from typing import List

from temporalio import workflow

from temporal_batch_processing.src.models.batch_completion import BatchCompletion

with workflow.unsafe.imports_passed_through():
    from temporal_batch_processing.src.models.file_metadata import FileMetadata
    from temporal_batch_processing.src.models.partition_info import PartitionInfo
    from temporal_batch_processing.src.models.partition_workflow_input import PartitionWorkflowInput
    from temporal_batch_processing.src.models.partition_workflow_progress import PartitionWorkflowProgress
    from temporal_batch_processing.src.activities import list_files_activity, create_partitions_activity, \
        fetch_files_metadata_activity, cleanup_temporary_table_activity, read_orders_activity, enrich_orders_activity
    from temporal_batch_processing.src.models.batch_processing_request import BatchProcessingRequest

TIMEOUT = timedelta(minutes=5)


@workflow.defn
class BatchWorkflow:

    @workflow.run
    async def process_batch(self,
                            file_info: FileMetadata,
                            start_offset: int,
                            limit: int) -> None:
        orders = await workflow.execute_activity(
            read_orders_activity,
            args=[file_info, start_offset, limit],
            start_to_close_timeout=TIMEOUT
        )

        await workflow.execute_activity(
            enrich_orders_activity,
            args=[orders],
            start_to_close_timeout=TIMEOUT
        )

        info = workflow.info()
        if info.parent and info.parent.workflow_id:
            parent = workflow.get_external_workflow_handle_for(
                workflow=PartitionWorkflow.process_partition,
                workflow_id=info.parent.workflow_id
            )

            await parent.signal(PartitionWorkflow.report_completion,
                                BatchCompletion(start_offset, len(orders.requests)))


@workflow.defn
class PartitionWorkflow:

    @workflow.init
    def __init__(self, partition_input: PartitionWorkflowInput) -> None:
        self._in_process_records = partition_input.in_process_records.copy()
        self._progress = partition_input.progress
        self._batch_size = partition_input.batch_size

    @workflow.run
    async def process_partition(self, partition_input: PartitionWorkflowInput) -> None:

        current_offset = partition_input.start_offset

        while True:

            await workflow.wait_condition(
                lambda: len(self._in_process_records) < partition_input.sliding_window_size
            )

            await self._report_progress(workflow.info())

            if current_offset >= partition_input.end_offset:
                await workflow.wait_condition(lambda: len(self._in_process_records) == 0)
                await self._report_progress(workflow.info())
                break

            batch_end = min(current_offset + partition_input.batch_size, partition_input.end_offset)
            batch_ids = {i for i in range(current_offset, batch_end)}

            self._in_process_records.update(batch_ids)

            await workflow.start_child_workflow(
                BatchWorkflow.process_batch,
                args=[partition_input.file_info, current_offset, len(batch_ids)],
                id=f"{workflow.info().workflow_id}/batch_{current_offset}",
                parent_close_policy=workflow.ParentClosePolicy.ABANDON,
            )

            current_offset = batch_end

    async def _report_progress(self, info):
        if info.parent and info.parent.workflow_id:
            parent = workflow.get_external_workflow_handle_for(
                workflow=MainWorkflow.run,
                workflow_id=info.parent.workflow_id
            )
            await parent.signal(
                MainWorkflow.report_progress,
                PartitionWorkflowProgress(
                    child_id=info.workflow_id,
                    completed=self._progress
                )
            )

    @workflow.signal
    async def report_completion(self, batch_completion: BatchCompletion) -> None:
        reported_records = set(range(batch_completion.start, batch_completion.start + batch_completion.limit))
        self._in_process_records -= reported_records
        self._progress += len(reported_records)


@workflow.defn
class MainWorkflow:

    def __init__(self):
        self._completion_by_partition = {}

    @workflow.run
    async def run(self, batch_request: BatchProcessingRequest) -> None:
        partitions = await self._create_partitions(batch_request)
        partition_handles = []

        for i, partition in enumerate(partitions):
            child_id = f"{workflow.info().workflow_id}/{i}"
            partition_input = PartitionWorkflowInput(
                file_info=partition.file_info,
                start_offset=partition.start_offset,
                end_offset=partition.end_offset,
                batch_size=batch_request.batching_options.batch_size,
                sliding_window_size=batch_request.batching_options.sliding_window_size,
            )

            self._completion_by_partition[child_id] = {
                "completed": 0,
                "total": partition.end_offset - partition.start_offset
            }

            handle = await workflow.start_child_workflow(
                workflow=PartitionWorkflow.process_partition,
                args=[partition_input],
                id=child_id
            )

            partition_handles.append(handle)

        await asyncio.gather(*partition_handles)

        clean_up_activities = []

        for partition in partitions:
            activity = workflow.execute_activity(
                cleanup_temporary_table_activity,
                args=[partition.file_info.table_name],
                start_to_close_timeout=TIMEOUT
            )
            clean_up_activities.append(activity)

        await asyncio.gather(*clean_up_activities)

        await workflow.wait_condition(workflow.all_handlers_finished)

    @staticmethod
    async def _create_partitions(batch_request: BatchProcessingRequest) -> List[PartitionInfo]:

        input_files: List[str] = await workflow.execute_activity(list_files_activity,
                                                                 args=[batch_request.files_path],
                                                                 start_to_close_timeout=TIMEOUT)

        files_metadata: List[FileMetadata] = await workflow.execute_activity(fetch_files_metadata_activity,
                                                                             args=[batch_request.files_path,
                                                                                   input_files],
                                                                             start_to_close_timeout=TIMEOUT)

        partitions: List[PartitionInfo] = await workflow.execute_activity(
            create_partitions_activity,
            args=[files_metadata, batch_request.batching_options.partition_size],
            start_to_close_timeout=TIMEOUT)

        return partitions

    @workflow.signal
    async def report_progress(self, progress: PartitionWorkflowProgress) -> None:
        self._completion_by_partition[progress.child_id]["completed"] = progress.completed

    @workflow.query
    def get_progress(self) -> dict:
        total_orders = sum([v["total"] for v in self._completion_by_partition.values()])
        completed = sum([v["completed"] for v in self._completion_by_partition.values()])
        percentage = 100 * (completed / total_orders)
        aggregated = {"total_orders": total_orders,
                      "completed_orders": completed,
                      "progress_percentage": int(percentage)}
        result = {**self._completion_by_partition, **aggregated}
        return result
