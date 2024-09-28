# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cloud_message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import transport_pb2 as transport__pb2
import cloud_provisioning_requests_pb2 as cloud__provisioning__requests__pb2
import cloud_provisioning_events_pb2 as cloud__provisioning__events__pb2
import cloud_device_events_pb2 as cloud__device__events__pb2
import cloud_device_requests_pb2 as cloud__device__requests__pb2
import cloud_metadata_events_pb2 as cloud__metadata__events__pb2
import cloud_room_requests_pb2 as cloud__room__requests__pb2
import cloud_video_settings_requests_pb2 as cloud__video__settings__requests__pb2
import cloud_device_settings_requests_pb2 as cloud__device__settings__requests__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cloud_message.proto',
  package='logi.proto',
  syntax='proto3',
  serialized_options=_b('\n%com.logitech.vc.raiden.proto.messages'),
  serialized_pb=_b('\n\x13\x63loud_message.proto\x12\nlogi.proto\x1a\x0ftransport.proto\x1a!cloud_provisioning_requests.proto\x1a\x1f\x63loud_provisioning_events.proto\x1a\x19\x63loud_device_events.proto\x1a\x1b\x63loud_device_requests.proto\x1a\x1b\x63loud_metadata_events.proto\x1a\x19\x63loud_room_requests.proto\x1a#cloud_video_settings_requests.proto\x1a$cloud_device_settings_requests.proto\"\xbf\x02\n\x11LogiRaidenMessage\x12\"\n\x06header\x18\x01 \x01(\x0b\x32\x12.logi.proto.Header\x12\x34\n\x06source\x18\x02 \x01(\x0e\x32$.logi.proto.LogiRaidenMessage.Source\x12\x17\n\x0finternal_api_id\x18\x03 \x01(\x05\x12(\n\x07request\x18\x04 \x01(\x0b\x32\x15.logi.proto.LRRequestH\x00\x12*\n\x08response\x18\x05 \x01(\x0b\x32\x16.logi.proto.LRResponseH\x00\x12$\n\x05\x65vent\x18\x06 \x01(\x0b\x32\x13.logi.proto.LREventH\x00\"0\n\x06Source\x12\x0f\n\x0bUNAVAILABLE\x10\x00\x12\n\n\x06\x43LIENT\x10\x01\x12\t\n\x05PROXY\x10\x02\x42\t\n\x07payload\"\x87\x07\n\tLRRequest\x12\x44\n\x16provision_host_request\x18\x01 \x01(\x0b\x32\".logi.proto.LRProvisionHostRequestH\x00\x12H\n\x18\x64\x65provision_host_request\x18\x02 \x01(\x0b\x32$.logi.proto.LRDeprovisionHostRequestH\x00\x12Q\n\x1dget_provisioning_data_request\x18\x03 \x01(\x0b\x32(.logi.proto.LRGetProvisioningDataRequestH\x00\x12Z\n\"set_cloud_connection_state_request\x18\x04 \x01(\x0b\x32,.logi.proto.LRSetCloudConnectionStateRequestH\x00\x12V\n check_for_product_update_request\x18\x05 \x01(\x0b\x32*.logi.proto.LRCheckForProductUpdateRequestH\x00\x12^\n$set_firmware_update_schedule_request\x18\x06 \x01(\x0b\x32..logi.proto.LRSetFirmwareUpdateScheduleRequestH\x00\x12X\n!bulk_set_room_information_request\x18\x07 \x01(\x0b\x32+.logi.proto.LRBulkSetRoomInformationRequestH\x00\x12`\n%set_right_sight_configuration_request\x18\x08 \x01(\x0b\x32/.logi.proto.LRSetRightSightConfigurationRequestH\x00\x12T\n\x1fset_room_occupancy_mode_request\x18\t \x01(\x0b\x32).logi.proto.LRSetRoomOccupancyModeRequestH\x00\x12\x66\n(set_device_display_configuration_request\x18\n \x01(\x0b\x32\x32.logi.proto.LRSetDeviceDisplayConfigurationRequestH\x00\x42\t\n\x07payload\"\x9c\x07\n\nLRResponse\x12\x46\n\x17provision_host_response\x18\x01 \x01(\x0b\x32#.logi.proto.LRProvisionHostResponseH\x00\x12J\n\x19\x64\x65provision_host_response\x18\x02 \x01(\x0b\x32%.logi.proto.LRDeprovisionHostResponseH\x00\x12S\n\x1eget_provisioning_data_response\x18\x03 \x01(\x0b\x32).logi.proto.LRGetProvisioningDataResponseH\x00\x12\\\n#set_cloud_connection_state_response\x18\x04 \x01(\x0b\x32-.logi.proto.LRSetCloudConnectionStateResponseH\x00\x12X\n!check_for_product_update_response\x18\x05 \x01(\x0b\x32+.logi.proto.LRCheckForProductUpdateResponseH\x00\x12`\n%set_firmware_update_schedule_response\x18\x06 \x01(\x0b\x32/.logi.proto.LRSetFirmwareUpdateScheduleResponseH\x00\x12Z\n\"bulk_set_room_information_response\x18\x07 \x01(\x0b\x32,.logi.proto.LRBulkSetRoomInformationResponseH\x00\x12\x62\n&set_right_sight_configuration_response\x18\x08 \x01(\x0b\x32\x30.logi.proto.LRSetRightSightConfigurationResponseH\x00\x12V\n set_room_occupancy_mode_response\x18\t \x01(\x0b\x32*.logi.proto.LRSetRoomOccupancyModeResponseH\x00\x12h\n)set_device_display_configuration_response\x18\n \x01(\x0b\x32\x33.logi.proto.LRSetDeviceDisplayConfigurationResponseH\x00\x42\t\n\x07payload\"\xbc\x02\n\x07LREvent\x12Y\n!provisioning_data_available_event\x18\x01 \x01(\x0b\x32,.logi.proto.LRProvisioningDataAvailableEventH\x00\x12\x42\n\x15product_updated_event\x18\x02 \x01(\x0b\x32!.logi.proto.LRProductUpdatedEventH\x00\x12\x44\n\x16metadata_updated_event\x18\x03 \x01(\x0b\x32\".logi.proto.LRMetadataUpdatedEventH\x00\x12\x41\n\x14\x64\x65provisioning_event\x18\x04 \x01(\x0b\x32!.logi.proto.LRDeprovisioningEventH\x00\x42\t\n\x07payloadB\'\n%com.logitech.vc.raiden.proto.messagesb\x06proto3')
  ,
  dependencies=[transport__pb2.DESCRIPTOR,cloud__provisioning__requests__pb2.DESCRIPTOR,cloud__provisioning__events__pb2.DESCRIPTOR,cloud__device__events__pb2.DESCRIPTOR,cloud__device__requests__pb2.DESCRIPTOR,cloud__metadata__events__pb2.DESCRIPTOR,cloud__room__requests__pb2.DESCRIPTOR,cloud__video__settings__requests__pb2.DESCRIPTOR,cloud__device__settings__requests__pb2.DESCRIPTOR,])



_LOGIRAIDENMESSAGE_SOURCE = _descriptor.EnumDescriptor(
  name='Source',
  full_name='logi.proto.LogiRaidenMessage.Source',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNAVAILABLE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLIENT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROXY', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=568,
  serialized_end=616,
)
_sym_db.RegisterEnumDescriptor(_LOGIRAIDENMESSAGE_SOURCE)


_LOGIRAIDENMESSAGE = _descriptor.Descriptor(
  name='LogiRaidenMessage',
  full_name='logi.proto.LogiRaidenMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='logi.proto.LogiRaidenMessage.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='logi.proto.LogiRaidenMessage.source', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='internal_api_id', full_name='logi.proto.LogiRaidenMessage.internal_api_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='request', full_name='logi.proto.LogiRaidenMessage.request', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='logi.proto.LogiRaidenMessage.response', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='event', full_name='logi.proto.LogiRaidenMessage.event', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LOGIRAIDENMESSAGE_SOURCE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='payload', full_name='logi.proto.LogiRaidenMessage.payload',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=308,
  serialized_end=627,
)


_LRREQUEST = _descriptor.Descriptor(
  name='LRRequest',
  full_name='logi.proto.LRRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='provision_host_request', full_name='logi.proto.LRRequest.provision_host_request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deprovision_host_request', full_name='logi.proto.LRRequest.deprovision_host_request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='get_provisioning_data_request', full_name='logi.proto.LRRequest.get_provisioning_data_request', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_cloud_connection_state_request', full_name='logi.proto.LRRequest.set_cloud_connection_state_request', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='check_for_product_update_request', full_name='logi.proto.LRRequest.check_for_product_update_request', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_firmware_update_schedule_request', full_name='logi.proto.LRRequest.set_firmware_update_schedule_request', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bulk_set_room_information_request', full_name='logi.proto.LRRequest.bulk_set_room_information_request', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_right_sight_configuration_request', full_name='logi.proto.LRRequest.set_right_sight_configuration_request', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_room_occupancy_mode_request', full_name='logi.proto.LRRequest.set_room_occupancy_mode_request', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_device_display_configuration_request', full_name='logi.proto.LRRequest.set_device_display_configuration_request', index=9,
      number=10, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='payload', full_name='logi.proto.LRRequest.payload',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=630,
  serialized_end=1533,
)


_LRRESPONSE = _descriptor.Descriptor(
  name='LRResponse',
  full_name='logi.proto.LRResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='provision_host_response', full_name='logi.proto.LRResponse.provision_host_response', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deprovision_host_response', full_name='logi.proto.LRResponse.deprovision_host_response', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='get_provisioning_data_response', full_name='logi.proto.LRResponse.get_provisioning_data_response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_cloud_connection_state_response', full_name='logi.proto.LRResponse.set_cloud_connection_state_response', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='check_for_product_update_response', full_name='logi.proto.LRResponse.check_for_product_update_response', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_firmware_update_schedule_response', full_name='logi.proto.LRResponse.set_firmware_update_schedule_response', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bulk_set_room_information_response', full_name='logi.proto.LRResponse.bulk_set_room_information_response', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_right_sight_configuration_response', full_name='logi.proto.LRResponse.set_right_sight_configuration_response', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_room_occupancy_mode_response', full_name='logi.proto.LRResponse.set_room_occupancy_mode_response', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_device_display_configuration_response', full_name='logi.proto.LRResponse.set_device_display_configuration_response', index=9,
      number=10, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='payload', full_name='logi.proto.LRResponse.payload',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1536,
  serialized_end=2460,
)


_LREVENT = _descriptor.Descriptor(
  name='LREvent',
  full_name='logi.proto.LREvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='provisioning_data_available_event', full_name='logi.proto.LREvent.provisioning_data_available_event', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_updated_event', full_name='logi.proto.LREvent.product_updated_event', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata_updated_event', full_name='logi.proto.LREvent.metadata_updated_event', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deprovisioning_event', full_name='logi.proto.LREvent.deprovisioning_event', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='payload', full_name='logi.proto.LREvent.payload',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=2463,
  serialized_end=2779,
)

_LOGIRAIDENMESSAGE.fields_by_name['header'].message_type = transport__pb2._HEADER
_LOGIRAIDENMESSAGE.fields_by_name['source'].enum_type = _LOGIRAIDENMESSAGE_SOURCE
_LOGIRAIDENMESSAGE.fields_by_name['request'].message_type = _LRREQUEST
_LOGIRAIDENMESSAGE.fields_by_name['response'].message_type = _LRRESPONSE
_LOGIRAIDENMESSAGE.fields_by_name['event'].message_type = _LREVENT
_LOGIRAIDENMESSAGE_SOURCE.containing_type = _LOGIRAIDENMESSAGE
_LOGIRAIDENMESSAGE.oneofs_by_name['payload'].fields.append(
  _LOGIRAIDENMESSAGE.fields_by_name['request'])
_LOGIRAIDENMESSAGE.fields_by_name['request'].containing_oneof = _LOGIRAIDENMESSAGE.oneofs_by_name['payload']
_LOGIRAIDENMESSAGE.oneofs_by_name['payload'].fields.append(
  _LOGIRAIDENMESSAGE.fields_by_name['response'])
_LOGIRAIDENMESSAGE.fields_by_name['response'].containing_oneof = _LOGIRAIDENMESSAGE.oneofs_by_name['payload']
_LOGIRAIDENMESSAGE.oneofs_by_name['payload'].fields.append(
  _LOGIRAIDENMESSAGE.fields_by_name['event'])
_LOGIRAIDENMESSAGE.fields_by_name['event'].containing_oneof = _LOGIRAIDENMESSAGE.oneofs_by_name['payload']
_LRREQUEST.fields_by_name['provision_host_request'].message_type = cloud__provisioning__requests__pb2._LRPROVISIONHOSTREQUEST
_LRREQUEST.fields_by_name['deprovision_host_request'].message_type = cloud__provisioning__requests__pb2._LRDEPROVISIONHOSTREQUEST
_LRREQUEST.fields_by_name['get_provisioning_data_request'].message_type = cloud__provisioning__requests__pb2._LRGETPROVISIONINGDATAREQUEST
_LRREQUEST.fields_by_name['set_cloud_connection_state_request'].message_type = cloud__provisioning__requests__pb2._LRSETCLOUDCONNECTIONSTATEREQUEST
_LRREQUEST.fields_by_name['check_for_product_update_request'].message_type = cloud__device__requests__pb2._LRCHECKFORPRODUCTUPDATEREQUEST
_LRREQUEST.fields_by_name['set_firmware_update_schedule_request'].message_type = cloud__device__requests__pb2._LRSETFIRMWAREUPDATESCHEDULEREQUEST
_LRREQUEST.fields_by_name['bulk_set_room_information_request'].message_type = cloud__room__requests__pb2._LRBULKSETROOMINFORMATIONREQUEST
_LRREQUEST.fields_by_name['set_right_sight_configuration_request'].message_type = cloud__video__settings__requests__pb2._LRSETRIGHTSIGHTCONFIGURATIONREQUEST
_LRREQUEST.fields_by_name['set_room_occupancy_mode_request'].message_type = cloud__room__requests__pb2._LRSETROOMOCCUPANCYMODEREQUEST
_LRREQUEST.fields_by_name['set_device_display_configuration_request'].message_type = cloud__device__settings__requests__pb2._LRSETDEVICEDISPLAYCONFIGURATIONREQUEST
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['provision_host_request'])
_LRREQUEST.fields_by_name['provision_host_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['deprovision_host_request'])
_LRREQUEST.fields_by_name['deprovision_host_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['get_provisioning_data_request'])
_LRREQUEST.fields_by_name['get_provisioning_data_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['set_cloud_connection_state_request'])
_LRREQUEST.fields_by_name['set_cloud_connection_state_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['check_for_product_update_request'])
_LRREQUEST.fields_by_name['check_for_product_update_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['set_firmware_update_schedule_request'])
_LRREQUEST.fields_by_name['set_firmware_update_schedule_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['bulk_set_room_information_request'])
_LRREQUEST.fields_by_name['bulk_set_room_information_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['set_right_sight_configuration_request'])
_LRREQUEST.fields_by_name['set_right_sight_configuration_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['set_room_occupancy_mode_request'])
_LRREQUEST.fields_by_name['set_room_occupancy_mode_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRREQUEST.oneofs_by_name['payload'].fields.append(
  _LRREQUEST.fields_by_name['set_device_display_configuration_request'])
_LRREQUEST.fields_by_name['set_device_display_configuration_request'].containing_oneof = _LRREQUEST.oneofs_by_name['payload']
_LRRESPONSE.fields_by_name['provision_host_response'].message_type = cloud__provisioning__requests__pb2._LRPROVISIONHOSTRESPONSE
_LRRESPONSE.fields_by_name['deprovision_host_response'].message_type = cloud__provisioning__requests__pb2._LRDEPROVISIONHOSTRESPONSE
_LRRESPONSE.fields_by_name['get_provisioning_data_response'].message_type = cloud__provisioning__requests__pb2._LRGETPROVISIONINGDATARESPONSE
_LRRESPONSE.fields_by_name['set_cloud_connection_state_response'].message_type = cloud__provisioning__requests__pb2._LRSETCLOUDCONNECTIONSTATERESPONSE
_LRRESPONSE.fields_by_name['check_for_product_update_response'].message_type = cloud__device__requests__pb2._LRCHECKFORPRODUCTUPDATERESPONSE
_LRRESPONSE.fields_by_name['set_firmware_update_schedule_response'].message_type = cloud__device__requests__pb2._LRSETFIRMWAREUPDATESCHEDULERESPONSE
_LRRESPONSE.fields_by_name['bulk_set_room_information_response'].message_type = cloud__room__requests__pb2._LRBULKSETROOMINFORMATIONRESPONSE
_LRRESPONSE.fields_by_name['set_right_sight_configuration_response'].message_type = cloud__video__settings__requests__pb2._LRSETRIGHTSIGHTCONFIGURATIONRESPONSE
_LRRESPONSE.fields_by_name['set_room_occupancy_mode_response'].message_type = cloud__room__requests__pb2._LRSETROOMOCCUPANCYMODERESPONSE
_LRRESPONSE.fields_by_name['set_device_display_configuration_response'].message_type = cloud__device__settings__requests__pb2._LRSETDEVICEDISPLAYCONFIGURATIONRESPONSE
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['provision_host_response'])
_LRRESPONSE.fields_by_name['provision_host_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['deprovision_host_response'])
_LRRESPONSE.fields_by_name['deprovision_host_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['get_provisioning_data_response'])
_LRRESPONSE.fields_by_name['get_provisioning_data_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['set_cloud_connection_state_response'])
_LRRESPONSE.fields_by_name['set_cloud_connection_state_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['check_for_product_update_response'])
_LRRESPONSE.fields_by_name['check_for_product_update_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['set_firmware_update_schedule_response'])
_LRRESPONSE.fields_by_name['set_firmware_update_schedule_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['bulk_set_room_information_response'])
_LRRESPONSE.fields_by_name['bulk_set_room_information_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['set_right_sight_configuration_response'])
_LRRESPONSE.fields_by_name['set_right_sight_configuration_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['set_room_occupancy_mode_response'])
_LRRESPONSE.fields_by_name['set_room_occupancy_mode_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LRRESPONSE.oneofs_by_name['payload'].fields.append(
  _LRRESPONSE.fields_by_name['set_device_display_configuration_response'])
_LRRESPONSE.fields_by_name['set_device_display_configuration_response'].containing_oneof = _LRRESPONSE.oneofs_by_name['payload']
_LREVENT.fields_by_name['provisioning_data_available_event'].message_type = cloud__provisioning__events__pb2._LRPROVISIONINGDATAAVAILABLEEVENT
_LREVENT.fields_by_name['product_updated_event'].message_type = cloud__device__events__pb2._LRPRODUCTUPDATEDEVENT
_LREVENT.fields_by_name['metadata_updated_event'].message_type = cloud__metadata__events__pb2._LRMETADATAUPDATEDEVENT
_LREVENT.fields_by_name['deprovisioning_event'].message_type = cloud__provisioning__events__pb2._LRDEPROVISIONINGEVENT
_LREVENT.oneofs_by_name['payload'].fields.append(
  _LREVENT.fields_by_name['provisioning_data_available_event'])
_LREVENT.fields_by_name['provisioning_data_available_event'].containing_oneof = _LREVENT.oneofs_by_name['payload']
_LREVENT.oneofs_by_name['payload'].fields.append(
  _LREVENT.fields_by_name['product_updated_event'])
_LREVENT.fields_by_name['product_updated_event'].containing_oneof = _LREVENT.oneofs_by_name['payload']
_LREVENT.oneofs_by_name['payload'].fields.append(
  _LREVENT.fields_by_name['metadata_updated_event'])
_LREVENT.fields_by_name['metadata_updated_event'].containing_oneof = _LREVENT.oneofs_by_name['payload']
_LREVENT.oneofs_by_name['payload'].fields.append(
  _LREVENT.fields_by_name['deprovisioning_event'])
_LREVENT.fields_by_name['deprovisioning_event'].containing_oneof = _LREVENT.oneofs_by_name['payload']
DESCRIPTOR.message_types_by_name['LogiRaidenMessage'] = _LOGIRAIDENMESSAGE
DESCRIPTOR.message_types_by_name['LRRequest'] = _LRREQUEST
DESCRIPTOR.message_types_by_name['LRResponse'] = _LRRESPONSE
DESCRIPTOR.message_types_by_name['LREvent'] = _LREVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LogiRaidenMessage = _reflection.GeneratedProtocolMessageType('LogiRaidenMessage', (_message.Message,), dict(
  DESCRIPTOR = _LOGIRAIDENMESSAGE,
  __module__ = 'cloud_message_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LogiRaidenMessage)
  ))
_sym_db.RegisterMessage(LogiRaidenMessage)

LRRequest = _reflection.GeneratedProtocolMessageType('LRRequest', (_message.Message,), dict(
  DESCRIPTOR = _LRREQUEST,
  __module__ = 'cloud_message_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRRequest)
  ))
_sym_db.RegisterMessage(LRRequest)

LRResponse = _reflection.GeneratedProtocolMessageType('LRResponse', (_message.Message,), dict(
  DESCRIPTOR = _LRRESPONSE,
  __module__ = 'cloud_message_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LRResponse)
  ))
_sym_db.RegisterMessage(LRResponse)

LREvent = _reflection.GeneratedProtocolMessageType('LREvent', (_message.Message,), dict(
  DESCRIPTOR = _LREVENT,
  __module__ = 'cloud_message_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.LREvent)
  ))
_sym_db.RegisterMessage(LREvent)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)