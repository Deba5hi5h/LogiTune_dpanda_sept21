# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: firmware_requests.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2
import firmware_structures_pb2 as firmware__structures__pb2
import product_state_structures_pb2 as product__state__structures__pb2
import update_schedule_structures_pb2 as update__schedule__structures__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='firmware_requests.proto',
  package='logi.proto',
  syntax='proto3',
  serialized_options=_b('\n#com.logitech.vc.sync.proto.messages'),
  serialized_pb=_b('\n\x17\x66irmware_requests.proto\x12\nlogi.proto\x1a\x0c\x63ommon.proto\x1a\x19\x66irmware_structures.proto\x1a\x1eproduct_state_structures.proto\x1a update_schedule_structures.proto\"4\n GetFirmwareUpdateProgressRequest\x12\x10\n\x08reserved\x18\x01 \x01(\x08\"{\n!GetFirmwareUpdateProgressResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x33\n\x07updates\x18\x02 \x03(\x0b\x32\".logi.proto.FirmwareUpdateProgress\";\n#GetLatestFirmwareByProductIdRequest\x12\x14\n\x0cproduct_uuid\x18\x01 \x01(\t\"\xaa\x02\n$GetLatestFirmwareByProductIdResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x14\n\x0cproduct_uuid\x18\x02 \x01(\t\x12\'\n\x1flatest_firmware_package_version\x18\x03 \x01(\t\x12&\n\x1elatest_firmware_published_date\x18\x04 \x01(\r\x12)\n!latest_firmware_release_notes_uri\x18\x05 \x01(\t\x12M\n\x1flatest_device_firmware_versions\x18\x06 \x03(\x0b\x32$.logi.proto.LatestDeviceFirmwareInfo\",\n\x18UpdateAllFirmwareRequest\x12\x10\n\x08reserved\x18\x01 \x01(\x08\"s\n\x19UpdateAllFirmwareResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x33\n\x07updates\x18\x02 \x03(\x0b\x32\".logi.proto.FirmwareUpdateProgress\"r\n UpdateFirmwareByProductIdRequest\x12\x14\n\x0cproduct_uuid\x18\x01 \x01(\t\x12 \n\x18\x66irmware_package_version\x18\x02 \x01(\t\x12\x16\n\x0ewindows_update\x18\x03 \x01(\x08\"z\n!UpdateFirmwareByProductIdResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x32\n\x06update\x18\x02 \x01(\x0b\x32\".logi.proto.FirmwareUpdateProgress\"\xa1\x01\n SetFirmwareUpdateScheduleRequest\x12\x14\n\x0cproduct_uuid\x18\x01 \x01(\t\x12\x30\n\rproduct_model\x18\x02 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12\x35\n\x10scheduled_update\x18\x03 \x01(\x0b\x32\x1b.logi.proto.ScheduledUpdate\"\xc5\x01\n!SetFirmwareUpdateScheduleResponse\x12!\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x11.logi.proto.Error\x12\x14\n\x0cproduct_uuid\x18\x02 \x01(\t\x12\x30\n\rproduct_model\x18\x03 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12\x35\n\x10scheduled_update\x18\x04 \x01(\x0b\x32\x1b.logi.proto.ScheduledUpdate\"\xe2\x03\n\x0f\x46irmwareRequest\x12\\\n$get_firmware_update_progress_request\x18\x01 \x01(\x0b\x32,.logi.proto.GetFirmwareUpdateProgressRequestH\x00\x12\x64\n)get_latest_firmware_by_product_id_request\x18\x02 \x01(\x0b\x32/.logi.proto.GetLatestFirmwareByProductIdRequestH\x00\x12U\n\x1dupdate_firmware_by_id_request\x18\x03 \x01(\x0b\x32,.logi.proto.UpdateFirmwareByProductIdRequestH\x00\x12K\n\x1bupdate_all_firmware_request\x18\x04 \x01(\x0b\x32$.logi.proto.UpdateAllFirmwareRequestH\x00\x12\\\n$set_firmware_update_schedule_request\x18\x05 \x01(\x0b\x32,.logi.proto.SetFirmwareUpdateScheduleRequestH\x00\x42\t\n\x07request\"\xee\x03\n\x10\x46irmwareResponse\x12^\n%get_firmware_update_progress_response\x18\x02 \x01(\x0b\x32-.logi.proto.GetFirmwareUpdateProgressResponseH\x00\x12\x66\n*get_latest_firmware_by_product_id_response\x18\x03 \x01(\x0b\x32\x30.logi.proto.GetLatestFirmwareByProductIdResponseH\x00\x12W\n\x1eupdate_firmware_by_id_response\x18\x04 \x01(\x0b\x32-.logi.proto.UpdateFirmwareByProductIdResponseH\x00\x12M\n\x1cupdate_all_firmware_response\x18\x05 \x01(\x0b\x32%.logi.proto.UpdateAllFirmwareResponseH\x00\x12^\n%set_firmware_update_schedule_response\x18\x06 \x01(\x0b\x32-.logi.proto.SetFirmwareUpdateScheduleResponseH\x00\x42\n\n\x08responseB%\n#com.logitech.vc.sync.proto.messagesb\x06proto3')
  ,
  dependencies=[common__pb2.DESCRIPTOR,firmware__structures__pb2.DESCRIPTOR,product__state__structures__pb2.DESCRIPTOR,update__schedule__structures__pb2.DESCRIPTOR,])




_GETFIRMWAREUPDATEPROGRESSREQUEST = _descriptor.Descriptor(
  name='GetFirmwareUpdateProgressRequest',
  full_name='logi.proto.GetFirmwareUpdateProgressRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reserved', full_name='logi.proto.GetFirmwareUpdateProgressRequest.reserved', index=0,
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
  serialized_start=146,
  serialized_end=198,
)


_GETFIRMWAREUPDATEPROGRESSRESPONSE = _descriptor.Descriptor(
  name='GetFirmwareUpdateProgressResponse',
  full_name='logi.proto.GetFirmwareUpdateProgressResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.GetFirmwareUpdateProgressResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updates', full_name='logi.proto.GetFirmwareUpdateProgressResponse.updates', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=200,
  serialized_end=323,
)


_GETLATESTFIRMWAREBYPRODUCTIDREQUEST = _descriptor.Descriptor(
  name='GetLatestFirmwareByProductIdRequest',
  full_name='logi.proto.GetLatestFirmwareByProductIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.GetLatestFirmwareByProductIdRequest.product_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=325,
  serialized_end=384,
)


_GETLATESTFIRMWAREBYPRODUCTIDRESPONSE = _descriptor.Descriptor(
  name='GetLatestFirmwareByProductIdResponse',
  full_name='logi.proto.GetLatestFirmwareByProductIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.GetLatestFirmwareByProductIdResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.GetLatestFirmwareByProductIdResponse.product_uuid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='latest_firmware_package_version', full_name='logi.proto.GetLatestFirmwareByProductIdResponse.latest_firmware_package_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='latest_firmware_published_date', full_name='logi.proto.GetLatestFirmwareByProductIdResponse.latest_firmware_published_date', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='latest_firmware_release_notes_uri', full_name='logi.proto.GetLatestFirmwareByProductIdResponse.latest_firmware_release_notes_uri', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='latest_device_firmware_versions', full_name='logi.proto.GetLatestFirmwareByProductIdResponse.latest_device_firmware_versions', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=387,
  serialized_end=685,
)


_UPDATEALLFIRMWAREREQUEST = _descriptor.Descriptor(
  name='UpdateAllFirmwareRequest',
  full_name='logi.proto.UpdateAllFirmwareRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reserved', full_name='logi.proto.UpdateAllFirmwareRequest.reserved', index=0,
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
  serialized_start=687,
  serialized_end=731,
)


_UPDATEALLFIRMWARERESPONSE = _descriptor.Descriptor(
  name='UpdateAllFirmwareResponse',
  full_name='logi.proto.UpdateAllFirmwareResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.UpdateAllFirmwareResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updates', full_name='logi.proto.UpdateAllFirmwareResponse.updates', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=733,
  serialized_end=848,
)


_UPDATEFIRMWAREBYPRODUCTIDREQUEST = _descriptor.Descriptor(
  name='UpdateFirmwareByProductIdRequest',
  full_name='logi.proto.UpdateFirmwareByProductIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.UpdateFirmwareByProductIdRequest.product_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='firmware_package_version', full_name='logi.proto.UpdateFirmwareByProductIdRequest.firmware_package_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='windows_update', full_name='logi.proto.UpdateFirmwareByProductIdRequest.windows_update', index=2,
      number=3, type=8, cpp_type=7, label=1,
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
  serialized_start=850,
  serialized_end=964,
)


_UPDATEFIRMWAREBYPRODUCTIDRESPONSE = _descriptor.Descriptor(
  name='UpdateFirmwareByProductIdResponse',
  full_name='logi.proto.UpdateFirmwareByProductIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.UpdateFirmwareByProductIdResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='logi.proto.UpdateFirmwareByProductIdResponse.update', index=1,
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
  serialized_start=966,
  serialized_end=1088,
)


_SETFIRMWAREUPDATESCHEDULEREQUEST = _descriptor.Descriptor(
  name='SetFirmwareUpdateScheduleRequest',
  full_name='logi.proto.SetFirmwareUpdateScheduleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.SetFirmwareUpdateScheduleRequest.product_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.SetFirmwareUpdateScheduleRequest.product_model', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheduled_update', full_name='logi.proto.SetFirmwareUpdateScheduleRequest.scheduled_update', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=1091,
  serialized_end=1252,
)


_SETFIRMWAREUPDATESCHEDULERESPONSE = _descriptor.Descriptor(
  name='SetFirmwareUpdateScheduleResponse',
  full_name='logi.proto.SetFirmwareUpdateScheduleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errors', full_name='logi.proto.SetFirmwareUpdateScheduleResponse.errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.SetFirmwareUpdateScheduleResponse.product_uuid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.SetFirmwareUpdateScheduleResponse.product_model', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheduled_update', full_name='logi.proto.SetFirmwareUpdateScheduleResponse.scheduled_update', index=3,
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
  ],
  serialized_start=1255,
  serialized_end=1452,
)


_FIRMWAREREQUEST = _descriptor.Descriptor(
  name='FirmwareRequest',
  full_name='logi.proto.FirmwareRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='get_firmware_update_progress_request', full_name='logi.proto.FirmwareRequest.get_firmware_update_progress_request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='get_latest_firmware_by_product_id_request', full_name='logi.proto.FirmwareRequest.get_latest_firmware_by_product_id_request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_firmware_by_id_request', full_name='logi.proto.FirmwareRequest.update_firmware_by_id_request', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_all_firmware_request', full_name='logi.proto.FirmwareRequest.update_all_firmware_request', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_firmware_update_schedule_request', full_name='logi.proto.FirmwareRequest.set_firmware_update_schedule_request', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
      name='request', full_name='logi.proto.FirmwareRequest.request',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1455,
  serialized_end=1937,
)


_FIRMWARERESPONSE = _descriptor.Descriptor(
  name='FirmwareResponse',
  full_name='logi.proto.FirmwareResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='get_firmware_update_progress_response', full_name='logi.proto.FirmwareResponse.get_firmware_update_progress_response', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='get_latest_firmware_by_product_id_response', full_name='logi.proto.FirmwareResponse.get_latest_firmware_by_product_id_response', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_firmware_by_id_response', full_name='logi.proto.FirmwareResponse.update_firmware_by_id_response', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_all_firmware_response', full_name='logi.proto.FirmwareResponse.update_all_firmware_response', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_firmware_update_schedule_response', full_name='logi.proto.FirmwareResponse.set_firmware_update_schedule_response', index=4,
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
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='response', full_name='logi.proto.FirmwareResponse.response',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1940,
  serialized_end=2434,
)

_GETFIRMWAREUPDATEPROGRESSRESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_GETFIRMWAREUPDATEPROGRESSRESPONSE.fields_by_name['updates'].message_type = firmware__structures__pb2._FIRMWAREUPDATEPROGRESS
_GETLATESTFIRMWAREBYPRODUCTIDRESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_GETLATESTFIRMWAREBYPRODUCTIDRESPONSE.fields_by_name['latest_device_firmware_versions'].message_type = firmware__structures__pb2._LATESTDEVICEFIRMWAREINFO
_UPDATEALLFIRMWARERESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_UPDATEALLFIRMWARERESPONSE.fields_by_name['updates'].message_type = firmware__structures__pb2._FIRMWAREUPDATEPROGRESS
_UPDATEFIRMWAREBYPRODUCTIDRESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_UPDATEFIRMWAREBYPRODUCTIDRESPONSE.fields_by_name['update'].message_type = firmware__structures__pb2._FIRMWAREUPDATEPROGRESS
_SETFIRMWAREUPDATESCHEDULEREQUEST.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_SETFIRMWAREUPDATESCHEDULEREQUEST.fields_by_name['scheduled_update'].message_type = update__schedule__structures__pb2._SCHEDULEDUPDATE
_SETFIRMWAREUPDATESCHEDULERESPONSE.fields_by_name['errors'].message_type = common__pb2._ERROR
_SETFIRMWAREUPDATESCHEDULERESPONSE.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_SETFIRMWAREUPDATESCHEDULERESPONSE.fields_by_name['scheduled_update'].message_type = update__schedule__structures__pb2._SCHEDULEDUPDATE
_FIRMWAREREQUEST.fields_by_name['get_firmware_update_progress_request'].message_type = _GETFIRMWAREUPDATEPROGRESSREQUEST
_FIRMWAREREQUEST.fields_by_name['get_latest_firmware_by_product_id_request'].message_type = _GETLATESTFIRMWAREBYPRODUCTIDREQUEST
_FIRMWAREREQUEST.fields_by_name['update_firmware_by_id_request'].message_type = _UPDATEFIRMWAREBYPRODUCTIDREQUEST
_FIRMWAREREQUEST.fields_by_name['update_all_firmware_request'].message_type = _UPDATEALLFIRMWAREREQUEST
_FIRMWAREREQUEST.fields_by_name['set_firmware_update_schedule_request'].message_type = _SETFIRMWAREUPDATESCHEDULEREQUEST
_FIRMWAREREQUEST.oneofs_by_name['request'].fields.append(
  _FIRMWAREREQUEST.fields_by_name['get_firmware_update_progress_request'])
_FIRMWAREREQUEST.fields_by_name['get_firmware_update_progress_request'].containing_oneof = _FIRMWAREREQUEST.oneofs_by_name['request']
_FIRMWAREREQUEST.oneofs_by_name['request'].fields.append(
  _FIRMWAREREQUEST.fields_by_name['get_latest_firmware_by_product_id_request'])
_FIRMWAREREQUEST.fields_by_name['get_latest_firmware_by_product_id_request'].containing_oneof = _FIRMWAREREQUEST.oneofs_by_name['request']
_FIRMWAREREQUEST.oneofs_by_name['request'].fields.append(
  _FIRMWAREREQUEST.fields_by_name['update_firmware_by_id_request'])
_FIRMWAREREQUEST.fields_by_name['update_firmware_by_id_request'].containing_oneof = _FIRMWAREREQUEST.oneofs_by_name['request']
_FIRMWAREREQUEST.oneofs_by_name['request'].fields.append(
  _FIRMWAREREQUEST.fields_by_name['update_all_firmware_request'])
_FIRMWAREREQUEST.fields_by_name['update_all_firmware_request'].containing_oneof = _FIRMWAREREQUEST.oneofs_by_name['request']
_FIRMWAREREQUEST.oneofs_by_name['request'].fields.append(
  _FIRMWAREREQUEST.fields_by_name['set_firmware_update_schedule_request'])
_FIRMWAREREQUEST.fields_by_name['set_firmware_update_schedule_request'].containing_oneof = _FIRMWAREREQUEST.oneofs_by_name['request']
_FIRMWARERESPONSE.fields_by_name['get_firmware_update_progress_response'].message_type = _GETFIRMWAREUPDATEPROGRESSRESPONSE
_FIRMWARERESPONSE.fields_by_name['get_latest_firmware_by_product_id_response'].message_type = _GETLATESTFIRMWAREBYPRODUCTIDRESPONSE
_FIRMWARERESPONSE.fields_by_name['update_firmware_by_id_response'].message_type = _UPDATEFIRMWAREBYPRODUCTIDRESPONSE
_FIRMWARERESPONSE.fields_by_name['update_all_firmware_response'].message_type = _UPDATEALLFIRMWARERESPONSE
_FIRMWARERESPONSE.fields_by_name['set_firmware_update_schedule_response'].message_type = _SETFIRMWAREUPDATESCHEDULERESPONSE
_FIRMWARERESPONSE.oneofs_by_name['response'].fields.append(
  _FIRMWARERESPONSE.fields_by_name['get_firmware_update_progress_response'])
_FIRMWARERESPONSE.fields_by_name['get_firmware_update_progress_response'].containing_oneof = _FIRMWARERESPONSE.oneofs_by_name['response']
_FIRMWARERESPONSE.oneofs_by_name['response'].fields.append(
  _FIRMWARERESPONSE.fields_by_name['get_latest_firmware_by_product_id_response'])
_FIRMWARERESPONSE.fields_by_name['get_latest_firmware_by_product_id_response'].containing_oneof = _FIRMWARERESPONSE.oneofs_by_name['response']
_FIRMWARERESPONSE.oneofs_by_name['response'].fields.append(
  _FIRMWARERESPONSE.fields_by_name['update_firmware_by_id_response'])
_FIRMWARERESPONSE.fields_by_name['update_firmware_by_id_response'].containing_oneof = _FIRMWARERESPONSE.oneofs_by_name['response']
_FIRMWARERESPONSE.oneofs_by_name['response'].fields.append(
  _FIRMWARERESPONSE.fields_by_name['update_all_firmware_response'])
_FIRMWARERESPONSE.fields_by_name['update_all_firmware_response'].containing_oneof = _FIRMWARERESPONSE.oneofs_by_name['response']
_FIRMWARERESPONSE.oneofs_by_name['response'].fields.append(
  _FIRMWARERESPONSE.fields_by_name['set_firmware_update_schedule_response'])
_FIRMWARERESPONSE.fields_by_name['set_firmware_update_schedule_response'].containing_oneof = _FIRMWARERESPONSE.oneofs_by_name['response']
DESCRIPTOR.message_types_by_name['GetFirmwareUpdateProgressRequest'] = _GETFIRMWAREUPDATEPROGRESSREQUEST
DESCRIPTOR.message_types_by_name['GetFirmwareUpdateProgressResponse'] = _GETFIRMWAREUPDATEPROGRESSRESPONSE
DESCRIPTOR.message_types_by_name['GetLatestFirmwareByProductIdRequest'] = _GETLATESTFIRMWAREBYPRODUCTIDREQUEST
DESCRIPTOR.message_types_by_name['GetLatestFirmwareByProductIdResponse'] = _GETLATESTFIRMWAREBYPRODUCTIDRESPONSE
DESCRIPTOR.message_types_by_name['UpdateAllFirmwareRequest'] = _UPDATEALLFIRMWAREREQUEST
DESCRIPTOR.message_types_by_name['UpdateAllFirmwareResponse'] = _UPDATEALLFIRMWARERESPONSE
DESCRIPTOR.message_types_by_name['UpdateFirmwareByProductIdRequest'] = _UPDATEFIRMWAREBYPRODUCTIDREQUEST
DESCRIPTOR.message_types_by_name['UpdateFirmwareByProductIdResponse'] = _UPDATEFIRMWAREBYPRODUCTIDRESPONSE
DESCRIPTOR.message_types_by_name['SetFirmwareUpdateScheduleRequest'] = _SETFIRMWAREUPDATESCHEDULEREQUEST
DESCRIPTOR.message_types_by_name['SetFirmwareUpdateScheduleResponse'] = _SETFIRMWAREUPDATESCHEDULERESPONSE
DESCRIPTOR.message_types_by_name['FirmwareRequest'] = _FIRMWAREREQUEST
DESCRIPTOR.message_types_by_name['FirmwareResponse'] = _FIRMWARERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetFirmwareUpdateProgressRequest = _reflection.GeneratedProtocolMessageType('GetFirmwareUpdateProgressRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETFIRMWAREUPDATEPROGRESSREQUEST,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.GetFirmwareUpdateProgressRequest)
  ))
_sym_db.RegisterMessage(GetFirmwareUpdateProgressRequest)

GetFirmwareUpdateProgressResponse = _reflection.GeneratedProtocolMessageType('GetFirmwareUpdateProgressResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETFIRMWAREUPDATEPROGRESSRESPONSE,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.GetFirmwareUpdateProgressResponse)
  ))
_sym_db.RegisterMessage(GetFirmwareUpdateProgressResponse)

GetLatestFirmwareByProductIdRequest = _reflection.GeneratedProtocolMessageType('GetLatestFirmwareByProductIdRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETLATESTFIRMWAREBYPRODUCTIDREQUEST,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.GetLatestFirmwareByProductIdRequest)
  ))
_sym_db.RegisterMessage(GetLatestFirmwareByProductIdRequest)

GetLatestFirmwareByProductIdResponse = _reflection.GeneratedProtocolMessageType('GetLatestFirmwareByProductIdResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETLATESTFIRMWAREBYPRODUCTIDRESPONSE,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.GetLatestFirmwareByProductIdResponse)
  ))
_sym_db.RegisterMessage(GetLatestFirmwareByProductIdResponse)

UpdateAllFirmwareRequest = _reflection.GeneratedProtocolMessageType('UpdateAllFirmwareRequest', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEALLFIRMWAREREQUEST,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.UpdateAllFirmwareRequest)
  ))
_sym_db.RegisterMessage(UpdateAllFirmwareRequest)

UpdateAllFirmwareResponse = _reflection.GeneratedProtocolMessageType('UpdateAllFirmwareResponse', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEALLFIRMWARERESPONSE,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.UpdateAllFirmwareResponse)
  ))
_sym_db.RegisterMessage(UpdateAllFirmwareResponse)

UpdateFirmwareByProductIdRequest = _reflection.GeneratedProtocolMessageType('UpdateFirmwareByProductIdRequest', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEFIRMWAREBYPRODUCTIDREQUEST,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.UpdateFirmwareByProductIdRequest)
  ))
_sym_db.RegisterMessage(UpdateFirmwareByProductIdRequest)

UpdateFirmwareByProductIdResponse = _reflection.GeneratedProtocolMessageType('UpdateFirmwareByProductIdResponse', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEFIRMWAREBYPRODUCTIDRESPONSE,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.UpdateFirmwareByProductIdResponse)
  ))
_sym_db.RegisterMessage(UpdateFirmwareByProductIdResponse)

SetFirmwareUpdateScheduleRequest = _reflection.GeneratedProtocolMessageType('SetFirmwareUpdateScheduleRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETFIRMWAREUPDATESCHEDULEREQUEST,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.SetFirmwareUpdateScheduleRequest)
  ))
_sym_db.RegisterMessage(SetFirmwareUpdateScheduleRequest)

SetFirmwareUpdateScheduleResponse = _reflection.GeneratedProtocolMessageType('SetFirmwareUpdateScheduleResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETFIRMWAREUPDATESCHEDULERESPONSE,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.SetFirmwareUpdateScheduleResponse)
  ))
_sym_db.RegisterMessage(SetFirmwareUpdateScheduleResponse)

FirmwareRequest = _reflection.GeneratedProtocolMessageType('FirmwareRequest', (_message.Message,), dict(
  DESCRIPTOR = _FIRMWAREREQUEST,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.FirmwareRequest)
  ))
_sym_db.RegisterMessage(FirmwareRequest)

FirmwareResponse = _reflection.GeneratedProtocolMessageType('FirmwareResponse', (_message.Message,), dict(
  DESCRIPTOR = _FIRMWARERESPONSE,
  __module__ = 'firmware_requests_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.FirmwareResponse)
  ))
_sym_db.RegisterMessage(FirmwareResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
