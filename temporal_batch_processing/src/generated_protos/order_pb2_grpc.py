"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from . import order_pb2 as order__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in order_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class OrderServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EnrichOrder = channel.unary_unary('/order.OrderService/EnrichOrder', request_serializer=order__pb2.EnrichOrderRequest.SerializeToString, response_deserializer=order__pb2.EnrichOrderResponse.FromString, _registered_method=True)

class OrderServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EnrichOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_OrderServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'EnrichOrder': grpc.unary_unary_rpc_method_handler(servicer.EnrichOrder, request_deserializer=order__pb2.EnrichOrderRequest.FromString, response_serializer=order__pb2.EnrichOrderResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('order.OrderService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('order.OrderService', rpc_method_handlers)

class OrderService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EnrichOrder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/EnrichOrder', order__pb2.EnrichOrderRequest.SerializeToString, order__pb2.EnrichOrderResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)