# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cloud_provisioning_requests.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2
import configuration_structures_pb2 as configuration__structures__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cloud_provisioning_requests.proto',
  package='logi.proto',
  syntax='proto3',
  serialized_options=_b('\n2com.logitech.vc.raiden.proto.provisioning.messages'),
  serialized_pb=_b('\n!cloud_provisioning_requests.proto\x12\nlogi.proto\x1a\x0c\x63ommon.proto\x1a\x1e\x63onfiguration_structures.proto\"y\n\x16LRProvisionHostRequest\x12\x1e\n\x16json_provisioning_data\x18\x01 \x01(\t\x12?\n\x0emerge_strategy\x18\x02 \x01(\x0e\x32\'.logi.proto.LRProvisioningMergeStrategy\"M\n\x17LRProvisionHostResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x0f\n\x07success\x18\x02 \x01(\x08\",\n\x18LRDeprovisionHostRequest\x12\x10\n\x08reserved\x18\x01 \x01(\x08\"O\n\x19LRDeprovisionHostResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x0f\n\x07success\x18\x02 \x01(\x08\"0\n\x1cLRGetProvisioningDataRequest\x12\x10\n\x08reserved\x18\x01 \x01(\x08\"\x99\x01\n\x1dLRGetProvisioningDataResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x16\n\x0eis_provisioned\x18\x02 \x01(\x08\x12\x1d\n\x15is_connected_to_cloud\x18\x03 \x01(\x08\x12\x1e\n\x16json_provisioning_data\x18\x04 \x01(\t\"A\n LRSetCloudConnectionStateRequest\x12\x1d\n\x15is_connected_to_cloud\x18\x01 \x01(\x08\"}\n!LRSetCloudConnectionStateResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x35\n\x10host_information\x18\x02 \x01(\x0b\x32\x1b.logi.proto.HostInformation*u\n\x1bLRProvisioningMergeStrategy\x12,\n(LR_PROVISIONING_MERGE_STRATEGY_OVERWRITE\x10\x00\x12(\n$LR_PROVISIONING_MERGE_STRATEGY_MERGE\x10\x01\x42\x34\n2com.logitech.vc.raiden.proto.provisioning.messagesb\x06proto3')
  ,
  dependencies=[common__pb2.DESCRIPTOR,configuration__structures__pb2.DESCRIPTOR,])

_LRPROVISIONINGMERGESTRATEGY = _descriptor.EnumDescriptor(
  name='LRProvisioningMergeStrategy',
  full_name='logi.proto.LRProvisioningMergeStrategy',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LR_PROVISIONING_MERGE_STRATEGY_OVERWRITE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LR_PROVISIONING_MERGE_STRATEGY_MERGE', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=824,
  serialized_end=941,
)
_sym_db.RegisterEnumDescriptor(_LRPROVISIONINGMERGESTRATEGY)

LRProvisioningMergeStrategy = enum_type_wrapper.EnumTypeWrapper(_LRPROVISIONINGMERGESTRATEGY)
LR_PROVISIONING_MERGE_STRATEGY_OVERWRITE = 0
LR_PROVISIONING_MERGE_STRATEGY_MERGE = 1



_LRPROVISIONHOSTREQUEST = _descriptor.Descriptor(
  name='LRProvisionHostRequest',
  full_name='logi.proto.LRProvisionHostRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='json_provisioning_data', full_name='logi.proto.LRProvisionHostRequest.json_provisioning_data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='merge_strategy', full_name='logi.proto.LRProvisionHostRequest.merge_strategy', index=1,
      number=2, type=14, cpp_type=8, label=1,
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
  serialized_start=95,
  serialized_end=216,
)


_LRPROVISIONHOSTRESPONSE = _descriptor.Descriptor(
  name='LRProvisionHostResponse',
  full_name='logi.proto.LRProvisionHostResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRProvisionHostResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='logi.proto.LRProvisionHostResponse.success', index=1,
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
  serialized_start=218,
  serialized_end=295,
)


_LRDEPROVISIONHOSTREQUEST = _descriptor.Descriptor(
  name='LRDeprovisionHostRequest',
  full_name='logi.proto.LRDeprovisionHostRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reserved', full_name='logi.proto.LRDeprovisionHostRequest.reserved', index=0,
      number=1, type=8, cpp_type=7, label=1,
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
  serialized_start=297,
  serialized_end=341,
)


_LRDEPROVISIONHOSTRESPONSE = _descriptor.Descriptor(
  name='LRDeprovisionHostResponse',
  full_name='logi.proto.LRDeprovisionHostResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRDeprovisionHostResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='logi.proto.LRDeprovisionHostResponse.success', index=1,
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
  serialized_start=343,
  serialized_end=422,
)


_LRGETPROVISIONINGDATAREQUEST = _descriptor.Descriptor(
  name='LRGetProvisioningDataRequest',
  full_name='logi.proto.LRGetProvisioningDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reserved', full_name='logi.proto.LRGetProvisioningDataRequest.reserved', index=0,
      number=1, type=8, cpp_type=7, label=1,
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
  serialized_start=424,
  serialized_end=472,
)


_LRGETPROVISIONINGDATARESPONSE = _descriptor.Descriptor(
  name='LRGetProvisioningDataResponse',
  full_name='logi.proto.LRGetProvisioningDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRGetProvisioningDataResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_provisioned', full_name='logi.proto.LRGetProvisioningDataResponse.is_provisioned', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_connected_to_cloud', full_name='logi.proto.LRGetProvisioningDataResponse.is_connected_to_cloud', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='json_provisioning_data', full_name='logi.proto.LRGetProvisioningDataResponse.json_provisioning_data', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=475,
  serialized_end=628,
)


_LRSETCLOUDCONNECTIONSTATEREQUEST = _descriptor.Descriptor(
  name='LRSetCloudConnectionStateRequest',
  full_name='logi.proto.LRSetCloudConnectionStateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_connected_to_cloud', full_name='logi.proto.LRSetCloudConnectionStateRequest.is_connected_to_cloud', index=0,
      number=1, type=8, cpp_type=7, label=1,
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
  serialized_start=630,
  serialized_end=695,
)


_LRSETCLOUDCONNECTIONSTATERESPONSE = _descriptor.Descriptor(
  name='LRSetCloudConnectionStateResponse',
  full_name='logi.proto.LRSetCloudConnectionStateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.LRSetCloudConnectionStateResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host_information', full_name='logi.proto.LRSetCloudConnectionStateResponse.host_information', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=697,
  serialized_end=822,
)

_LRPROVISIONHOSTREQUEST.fields_by_name['merge_strategy'].enum_type = _LRPROVISIONINGMERGESTRATEGY
_LRPROVISIONHOSTRESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_LRDEPROVISIONHOSTRESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_LRGETPROVISIONINGDATARESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_LRSETCLOUDCONNECTIONSTATERESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_LRSETCLOUDCONNECTIONSTATERESPONSE.fields_by_name['host_information'].message_type = configuration__structures__pb2._HOSTINFORMATION
DESCRIPTOR.message_types_by_name['LRProvisionHostRequest'] = _LRPROVISIONHOSTREQUEST
DESCRIPTOR.message_types_by_name['LRProvisionHostResponse'] = _LRPROVISIONHOSTRESPONSE
DESCRIPTOR.message_types_by_name['LRDeprovisionHostRequest'] = _LRDEPROVISIONHOSTREQUEST
DESCRIPTOR.message_types_by_name['LRDeprovisionHostResponse'] = _LRDEPROVISIONHOSTRESPONSE
DESCRIPTOR.message_types_by_name['LRGetProvisioningDataRequest'] = _LRGETPROVISIONINGDATAREQUEST
DESCRIPTOR.message_types_by_name['LRGetProvisioningDataResponse'] = _LRGETPROVISIONINGDATARESPONSE
DESCRIPTOR.message_types_by_name['LRSetCloudConnectionStateRequest'] = _LRSETCLOUDCONNECTIONSTATEREQUEST
DESCRIPTOR.message_types_by_name['LRSetCloudConnectionStateResponse'] = _LRSETCLOUDCONNECTIONSTATERESPONSE
DESCRIPTOR.enum_types_by_name['LRProvisioningMergeStrategy'] = _LRPROVISIONINGMERGESTRATEGY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LRProvisionHostRequest = _reflection.GeneratedProtocolMessageType('LRProvisionHostRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRPROVISIONHOSTREQUEST,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRProvisionHostRequest)
  ))
_sym_db.RegisterMessage(LRProvisionHostRequest)

LRProvisionHostResponse = _reflection.GeneratedProtocolMessageType('LRProvisionHostResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRPROVISIONHOSTRESPONSE,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRProvisionHostResponse)
  ))
_sym_db.RegisterMessage(LRProvisionHostResponse)

LRDeprovisionHostRequest = _reflection.GeneratedProtocolMessageType('LRDeprovisionHostRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRDEPROVISIONHOSTREQUEST,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRDeprovisionHostRequest)
  ))
_sym_db.RegisterMessage(LRDeprovisionHostRequest)

LRDeprovisionHostResponse = _reflection.GeneratedProtocolMessageType('LRDeprovisionHostResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRDEPROVISIONHOSTRESPONSE,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRDeprovisionHostResponse)
  ))
_sym_db.RegisterMessage(LRDeprovisionHostResponse)

LRGetProvisioningDataRequest = _reflection.GeneratedProtocolMessageType('LRGetProvisioningDataRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRGETPROVISIONINGDATAREQUEST,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRGetProvisioningDataRequest)
  ))
_sym_db.RegisterMessage(LRGetProvisioningDataRequest)

LRGetProvisioningDataResponse = _reflection.GeneratedProtocolMessageType('LRGetProvisioningDataResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRGETPROVISIONINGDATARESPONSE,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRGetProvisioningDataResponse)
  ))
_sym_db.RegisterMessage(LRGetProvisioningDataResponse)

LRSetCloudConnectionStateRequest = _reflection.GeneratedProtocolMessageType('LRSetCloudConnectionStateRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRSETCLOUDCONNECTIONSTATEREQUEST,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRSetCloudConnectionStateRequest)
  ))
_sym_db.RegisterMessage(LRSetCloudConnectionStateRequest)

LRSetCloudConnectionStateResponse = _reflection.GeneratedProtocolMessageType('LRSetCloudConnectionStateResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRSETCLOUDCONNECTIONSTATERESPONSE,
  __module__ = 'cloud_provisioning_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRSetCloudConnectionStateResponse)
  ))
_sym_db.RegisterMessage(LRSetCloudConnectionStateResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
