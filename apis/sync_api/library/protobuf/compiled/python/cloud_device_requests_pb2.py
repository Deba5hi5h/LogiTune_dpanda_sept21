# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cloud_device_requests.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2
import product_state_structures_pb2 as product__state__structures__pb2
import update_schedule_structures_pb2 as update__schedule__structures__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cloud_device_requests.proto',
  package='logi.proto',
  syntax='proto3',
  serialized_options=_b('\n,com.logitech.vc.raiden.proto.device.messages'),
  serialized_pb=_b('\n\x1b\x63loud_device_requests.proto\x12\nlogi.proto\x1a\x0c\x63ommon.proto\x1a\x1eproduct_state_structures.proto\x1a update_schedule_structures.proto\"\xc7\x01\n\"LRSetFirmwareUpdateScheduleRequest\x12\x14\n\x0cproduct_uuid\x18\x01 \x01(\t\x12\x30\n\rproduct_model\x18\x02 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12\x35\n\x10scheduled_update\x18\x03 \x01(\x0b\x32\x1b.logi.proto.ScheduledUpdate\x12\"\n\x1areporting_interval_seconds\x18\x04 \x01(\r\"Y\n#LRSetFirmwareUpdateScheduleResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x0f\n\x07success\x18\x02 \x01(\x08\"\xbb\x01\n\x1eLRCheckForProductUpdateRequest\x12\x12\n\nupdate_now\x18\x01 \x01(\x08\x12\x14\n\x0cproduct_uuid\x18\x02 \x01(\t\x12\x30\n\rproduct_model\x18\x03 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12\x19\n\x11\x65xpiration_millis\x18\x04 \x01(\x04\x12\"\n\x1areporting_interval_seconds\x18\x05 \x01(\r\"U\n\x1fLRCheckForProductUpdateResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x0f\n\x07success\x18\x02 \x01(\x08\x42.\n,com.logitech.vc.raiden.proto.device.messagesb\x06proto3')
  ,
  dependencies=[common__pb2.DESCRIPTOR,product__state__structures__pb2.DESCRIPTOR,update__schedule__structures__pb2.DESCRIPTOR,])




_LRSETFIRMWAREUPDATESCHEDULEREQUEST = _descriptor.Descriptor(
  name='LRSetFirmwareUpdateScheduleRequest',
  full_name='logi.proto.LRSetFirmwareUpdateScheduleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.LRSetFirmwareUpdateScheduleRequest.product_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.LRSetFirmwareUpdateScheduleRequest.product_model', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheduled_update', full_name='logi.proto.LRSetFirmwareUpdateScheduleRequest.scheduled_update', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reporting_interval_seconds', full_name='logi.proto.LRSetFirmwareUpdateScheduleRequest.reporting_interval_seconds', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=124,
  serialized_end=323,
)


_LRSETFIRMWAREUPDATESCHEDULERESPONSE = _descriptor.Descriptor(
  name='LRSetFirmwareUpdateScheduleResponse',
  full_name='logi.proto.LRSetFirmwareUpdateScheduleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRSetFirmwareUpdateScheduleResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='logi.proto.LRSetFirmwareUpdateScheduleResponse.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=325,
  serialized_end=414,
)


_LRCHECKFORPRODUCTUPDATEREQUEST = _descriptor.Descriptor(
  name='LRCheckForProductUpdateRequest',
  full_name='logi.proto.LRCheckForProductUpdateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_now', full_name='logi.proto.LRCheckForProductUpdateRequest.update_now', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.LRCheckForProductUpdateRequest.product_uuid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.LRCheckForProductUpdateRequest.product_model', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expiration_millis', full_name='logi.proto.LRCheckForProductUpdateRequest.expiration_millis', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reporting_interval_seconds', full_name='logi.proto.LRCheckForProductUpdateRequest.reporting_interval_seconds', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=417,
  serialized_end=604,
)


_LRCHECKFORPRODUCTUPDATERESPONSE = _descriptor.Descriptor(
  name='LRCheckForProductUpdateResponse',
  full_name='logi.proto.LRCheckForProductUpdateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRCheckForProductUpdateResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='logi.proto.LRCheckForProductUpdateResponse.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=606,
  serialized_end=691,
)

_LRSETFIRMWAREUPDATESCHEDULEREQUEST.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_LRSETFIRMWAREUPDATESCHEDULEREQUEST.fields_by_name['scheduled_update'].message_type = update__schedule__structures__pb2._SCHEDULEDUPDATE
_LRSETFIRMWAREUPDATESCHEDULERESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_LRCHECKFORPRODUCTUPDATEREQUEST.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_LRCHECKFORPRODUCTUPDATERESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
DESCRIPTOR.message_types_by_name['LRSetFirmwareUpdateScheduleRequest'] = _LRSETFIRMWAREUPDATESCHEDULEREQUEST
DESCRIPTOR.message_types_by_name['LRSetFirmwareUpdateScheduleResponse'] = _LRSETFIRMWAREUPDATESCHEDULERESPONSE
DESCRIPTOR.message_types_by_name['LRCheckForProductUpdateRequest'] = _LRCHECKFORPRODUCTUPDATEREQUEST
DESCRIPTOR.message_types_by_name['LRCheckForProductUpdateResponse'] = _LRCHECKFORPRODUCTUPDATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LRSetFirmwareUpdateScheduleRequest = _reflection.GeneratedProtocolMessageType('LRSetFirmwareUpdateScheduleRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRSETFIRMWAREUPDATESCHEDULEREQUEST,
  __module__ = 'cloud_device_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRSetFirmwareUpdateScheduleRequest)
  ))
_sym_db.RegisterMessage(LRSetFirmwareUpdateScheduleRequest)

LRSetFirmwareUpdateScheduleResponse = _reflection.GeneratedProtocolMessageType('LRSetFirmwareUpdateScheduleResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRSETFIRMWAREUPDATESCHEDULERESPONSE,
  __module__ = 'cloud_device_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRSetFirmwareUpdateScheduleResponse)
  ))
_sym_db.RegisterMessage(LRSetFirmwareUpdateScheduleResponse)

LRCheckForProductUpdateRequest = _reflection.GeneratedProtocolMessageType('LRCheckForProductUpdateRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRCHECKFORPRODUCTUPDATEREQUEST,
  __module__ = 'cloud_device_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRCheckForProductUpdateRequest)
  ))
_sym_db.RegisterMessage(LRCheckForProductUpdateRequest)

LRCheckForProductUpdateResponse = _reflection.GeneratedProtocolMessageType('LRCheckForProductUpdateResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRCHECKFORPRODUCTUPDATERESPONSE,
  __module__ = 'cloud_device_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRCheckForProductUpdateResponse)
  ))
_sym_db.RegisterMessage(LRCheckForProductUpdateResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)