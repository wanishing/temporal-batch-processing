from concurrent import futures

import grpc

from temporal_batch_processing.src.generated_protos.order_pb2 import EnrichOrderResponse
from temporal_batch_processing.src.generated_protos.order_pb2_grpc import OrderServiceServicer, \
    add_OrderServiceServicer_to_server


class FakeOrderService(OrderServiceServicer):

    def __init__(self):
        self.requests = set()

    def EnrichOrder(self, request, context) -> EnrichOrderResponse:
        """Standard gRPC uses (request, context) signature"""
        print(f'Received request: {request}')
        self.requests.add(request.order_id)
        return EnrichOrderResponse(order_id=request.order_id,
                                   status="ENRICHED",
                                   message="Order enriched successfully")

    def assert_requested(self, expected_count):
        assert len(self.requests) == expected_count, \
            f"Expected {expected_count} unique requests, got {len(self.requests)}"


def run():
    print(f"Starting Order Service")
    service = FakeOrderService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_OrderServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:7070')
    server.start()
    print(f"Server started on port 7070")
    server.wait_for_termination()
