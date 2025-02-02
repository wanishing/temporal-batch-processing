"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class EnrichOrderRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ORDER_ID_FIELD_NUMBER: builtins.int
    EMAIL_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    order_id: builtins.str
    email: builtins.str
    created_at: builtins.str

    def __init__(self, *, order_id: builtins.str=..., email: builtins.str=..., created_at: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing.Literal['created_at', b'created_at', 'email', b'email', 'order_id', b'order_id']) -> None:
        ...
global___EnrichOrderRequest = EnrichOrderRequest

@typing.final
class EnrichOrderRequests(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    REQUESTS_FIELD_NUMBER: builtins.int

    @property
    def requests(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___EnrichOrderRequest]:
        ...

    def __init__(self, *, requests: collections.abc.Iterable[global___EnrichOrderRequest] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing.Literal['requests', b'requests']) -> None:
        ...
global___EnrichOrderRequests = EnrichOrderRequests

@typing.final
class EnrichOrderResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ORDER_ID_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    order_id: builtins.str
    status: builtins.str
    message: builtins.str

    def __init__(self, *, order_id: builtins.str=..., status: builtins.str=..., message: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing.Literal['message', b'message', 'order_id', b'order_id', 'status', b'status']) -> None:
        ...
global___EnrichOrderResponse = EnrichOrderResponse