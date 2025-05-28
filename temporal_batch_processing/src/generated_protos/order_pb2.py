"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 29, 0, "", "order.proto"
)
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0border.proto\x12\x05order"I\n\x12EnrichOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\r\n\x05email\x18\x02 \x01(\t\x12\x12\n\ncreated_at\x18\x03 \x01(\t"B\n\x13EnrichOrderRequests\x12+\n\x08requests\x18\x01 \x03(\x0b2\x19.order.EnrichOrderRequest"H\n\x13EnrichOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t2V\n\x0cOrderService\x12F\n\x0bEnrichOrder\x12\x19.order.EnrichOrderRequest\x1a\x1a.order.EnrichOrderResponse"\x00b\x06proto3'
)
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "order_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_ENRICHORDERREQUEST"]._serialized_start = 22
    _globals["_ENRICHORDERREQUEST"]._serialized_end = 95
    _globals["_ENRICHORDERREQUESTS"]._serialized_start = 97
    _globals["_ENRICHORDERREQUESTS"]._serialized_end = 163
    _globals["_ENRICHORDERRESPONSE"]._serialized_start = 165
    _globals["_ENRICHORDERRESPONSE"]._serialized_end = 237
    _globals["_ORDERSERVICE"]._serialized_start = 239
    _globals["_ORDERSERVICE"]._serialized_end = 325
