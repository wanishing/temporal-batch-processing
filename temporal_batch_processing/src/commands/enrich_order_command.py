import grpc

from temporal_batch_processing.src.generated_protos.order_pb2 import EnrichOrderRequests
from temporal_batch_processing.src.generated_protos.order_pb2_grpc import OrderServiceStub
from temporal_batch_processing.src.models.config import Config


class EnrichOrdersCommand:

    def __init__(self, order_service_client: OrderServiceStub):
        self.order_service_client = order_service_client

    @classmethod
    def build(cls, config: Config):
        channel = grpc.insecure_channel(f"{config.order_service_host}:{config.order_service_port}")
        return cls(order_service_client=OrderServiceStub(channel))

    def run(self, requests: EnrichOrderRequests):
        for request in requests.requests:
            self.order_service_client.EnrichOrder(request)
