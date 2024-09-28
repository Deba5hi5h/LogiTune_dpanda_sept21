# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cloud_device_settings_requests.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2
import device_settings_requests_pb2 as device__settings__requests__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cloud_device_settings_requests.proto',
  package='logi.proto',
  syntax='proto3',
  serialized_options=_b('\n,com.logitech.vc.raiden.proto.device.messages'),
  serialized_pb=_b('\n$cloud_device_settings_requests.proto\x12\nlogi.proto\x1a\x0c\x63ommon.proto\x1a\x1e\x64\x65vice_settings_requests.proto\"\x85\x01\n&LRSetDeviceDisplayConfigurationRequest\x12\x41\n\x07request\x18\x01 \x01(\x0b\x32\x30.logi.proto.SetDeviceDisplayConfigurationRequest\x12\x18\n\x10issued_timestamp\x18\x02 \x01(\x04\"]\n\'LRSetDeviceDisplayConfigurationResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x0f\n\x07success\x18\x02 \x01(\x08\x42.\n,com.logitech.vc.raiden.proto.device.messagesb\x06proto3')
  ,
  dependencies=[common__pb2.DESCRIPTOR,device__settings__requests__pb2.DESCRIPTOR,])




_LRSETDEVICEDISPLAYCONFIGURATIONREQUEST = _descriptor.Descriptor(
  name='LRSetDeviceDisplayConfigurationRequest',
  full_name='logi.proto.LRSetDeviceDisplayConfigurationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='logi.proto.LRSetDeviceDisplayConfigurationRequest.request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issued_timestamp', full_name='logi.proto.LRSetDeviceDisplayConfigurationRequest.issued_timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
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
  serialized_start=99,
  serialized_end=232,
)


_LRSETDEVICEDISPLAYCONFIGURATIONRESPONSE = _descriptor.Descriptor(
  name='LRSetDeviceDisplayConfigurationResponse',
  full_name='logi.proto.LRSetDeviceDisplayConfigurationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRSetDeviceDisplayConfigurationResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='logi.proto.LRSetDeviceDisplayConfigurationResponse.success', index=1,
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
  serialized_start=234,
  serialized_end=327,
)

_LRSETDEVICEDISPLAYCONFIGURATIONREQUEST.fields_by_name['request'].message_type = device__settings__requests__pb2._SETDEVICEDISPLAYCONFIGURATIONREQUEST
_LRSETDEVICEDISPLAYCONFIGURATIONRESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
DESCRIPTOR.message_types_by_name['LRSetDeviceDisplayConfigurationRequest'] = _LRSETDEVICEDISPLAYCONFIGURATIONREQUEST
DESCRIPTOR.message_types_by_name['LRSetDeviceDisplayConfigurationResponse'] = _LRSETDEVICEDISPLAYCONFIGURATIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LRSetDeviceDisplayConfigurationRequest = _reflection.GeneratedProtocolMessageType('LRSetDeviceDisplayConfigurationRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRSETDEVICEDISPLAYCONFIGURATIONREQUEST,
  __module__ = 'cloud_device_settings_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRSetDeviceDisplayConfigurationRequest)
  ))
_sym_db.RegisterMessage(LRSetDeviceDisplayConfigurationRequest)

LRSetDeviceDisplayConfigurationResponse = _reflection.GeneratedProtocolMessageType('LRSetDeviceDisplayConfigurationResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRSETDEVICEDISPLAYCONFIGURATIONRESPONSE,
  __module__ = 'cloud_device_settings_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRSetDeviceDisplayConfigurationResponse)
  ))
_sym_db.RegisterMessage(LRSetDeviceDisplayConfigurationResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
