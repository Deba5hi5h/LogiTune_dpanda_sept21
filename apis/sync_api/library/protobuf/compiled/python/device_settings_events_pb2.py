# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: device_settings_events.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import device_settings_structures_pb2 as device__settings__structures__pb2
import product_state_structures_pb2 as product__state__structures__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='device_settings_events.proto',
  package='logi.proto',
  syntax='proto3',
  serialized_options=_b('\n#com.logitech.vc.sync.proto.messages'),
  serialized_pb=_b('\n\x1c\x64\x65vice_settings_events.proto\x12\nlogi.proto\x1a device_settings_structures.proto\x1a\x1eproduct_state_structures.proto\"\xb0\x01\n&DeviceDisplayConfigurationChangedEvent\x12\x13\n\x0b\x64\x65vice_uuid\x18\x01 \x01(\t\x12\x30\n\rproduct_model\x18\x02 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12?\n\x15\x64isplay_configuration\x18\x03 \x01(\x0b\x32 .logi.proto.DisplayConfiguration\"\xbf\x01\n)DeviceConnectionConfigurationChangedEvent\x12\x13\n\x0b\x64\x65vice_uuid\x18\x01 \x01(\t\x12\x30\n\rproduct_model\x18\x02 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12K\n\x18\x63onnection_configuration\x18\x03 \x01(\x0b\x32).logi.proto.DeviceConnectionConfiguration\"\xb9\x01\n)DeviceWhiteboardConfigurationChangedEvent\x12\x13\n\x0b\x64\x65vice_uuid\x18\x01 \x01(\t\x12\x30\n\rproduct_model\x18\x02 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12\x45\n\x18whiteboard_configuration\x18\x03 \x01(\x0b\x32#.logi.proto.WhiteboardConfiguration\"\x9c\x01\n\x1f\x44\x65viceAudioSettingsChangedEvent\x12\x14\n\x0cproduct_uuid\x18\x01 \x01(\t\x12\x30\n\rproduct_model\x18\x02 \x01(\x0e\x32\x19.logi.proto.Product.Model\x12\x31\n\x0e\x61udio_settings\x18\x03 \x01(\x0b\x32\x19.logi.proto.AudioSettings\"\xc4\x03\n\x13\x44\x65viceSettingsEvent\x12h\n*device_display_configuration_changed_event\x18\x01 \x01(\x0b\x32\x32.logi.proto.DeviceDisplayConfigurationChangedEventH\x00\x12n\n-device_connection_configuration_changed_event\x18\x02 \x01(\x0b\x32\x35.logi.proto.DeviceConnectionConfigurationChangedEventH\x00\x12n\n-device_whiteboard_configuration_changed_event\x18\x03 \x01(\x0b\x32\x35.logi.proto.DeviceWhiteboardConfigurationChangedEventH\x00\x12Z\n#device_audio_settings_changed_event\x18\x04 \x01(\x0b\x32+.logi.proto.DeviceAudioSettingsChangedEventH\x00\x42\x07\n\x05\x65ventB%\n#com.logitech.vc.sync.proto.messagesb\x06proto3')
  ,
  dependencies=[device__settings__structures__pb2.DESCRIPTOR,product__state__structures__pb2.DESCRIPTOR,])




_DEVICEDISPLAYCONFIGURATIONCHANGEDEVENT = _descriptor.Descriptor(
  name='DeviceDisplayConfigurationChangedEvent',
  full_name='logi.proto.DeviceDisplayConfigurationChangedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_uuid', full_name='logi.proto.DeviceDisplayConfigurationChangedEvent.device_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.DeviceDisplayConfigurationChangedEvent.product_model', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_configuration', full_name='logi.proto.DeviceDisplayConfigurationChangedEvent.display_configuration', index=2,
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
  serialized_start=111,
  serialized_end=287,
)


_DEVICECONNECTIONCONFIGURATIONCHANGEDEVENT = _descriptor.Descriptor(
  name='DeviceConnectionConfigurationChangedEvent',
  full_name='logi.proto.DeviceConnectionConfigurationChangedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_uuid', full_name='logi.proto.DeviceConnectionConfigurationChangedEvent.device_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.DeviceConnectionConfigurationChangedEvent.product_model', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='connection_configuration', full_name='logi.proto.DeviceConnectionConfigurationChangedEvent.connection_configuration', index=2,
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
  serialized_start=290,
  serialized_end=481,
)


_DEVICEWHITEBOARDCONFIGURATIONCHANGEDEVENT = _descriptor.Descriptor(
  name='DeviceWhiteboardConfigurationChangedEvent',
  full_name='logi.proto.DeviceWhiteboardConfigurationChangedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_uuid', full_name='logi.proto.DeviceWhiteboardConfigurationChangedEvent.device_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.DeviceWhiteboardConfigurationChangedEvent.product_model', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='whiteboard_configuration', full_name='logi.proto.DeviceWhiteboardConfigurationChangedEvent.whiteboard_configuration', index=2,
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
  serialized_start=484,
  serialized_end=669,
)


_DEVICEAUDIOSETTINGSCHANGEDEVENT = _descriptor.Descriptor(
  name='DeviceAudioSettingsChangedEvent',
  full_name='logi.proto.DeviceAudioSettingsChangedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_uuid', full_name='logi.proto.DeviceAudioSettingsChangedEvent.product_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_model', full_name='logi.proto.DeviceAudioSettingsChangedEvent.product_model', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='audio_settings', full_name='logi.proto.DeviceAudioSettingsChangedEvent.audio_settings', index=2,
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
  serialized_start=672,
  serialized_end=828,
)


_DEVICESETTINGSEVENT = _descriptor.Descriptor(
  name='DeviceSettingsEvent',
  full_name='logi.proto.DeviceSettingsEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_display_configuration_changed_event', full_name='logi.proto.DeviceSettingsEvent.device_display_configuration_changed_event', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_connection_configuration_changed_event', full_name='logi.proto.DeviceSettingsEvent.device_connection_configuration_changed_event', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_whiteboard_configuration_changed_event', full_name='logi.proto.DeviceSettingsEvent.device_whiteboard_configuration_changed_event', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_audio_settings_changed_event', full_name='logi.proto.DeviceSettingsEvent.device_audio_settings_changed_event', index=3,
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
      name='event', full_name='logi.proto.DeviceSettingsEvent.event',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=831,
  serialized_end=1283,
)

_DEVICEDISPLAYCONFIGURATIONCHANGEDEVENT.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_DEVICEDISPLAYCONFIGURATIONCHANGEDEVENT.fields_by_name['display_configuration'].message_type = device__settings__structures__pb2._DISPLAYCONFIGURATION
_DEVICECONNECTIONCONFIGURATIONCHANGEDEVENT.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_DEVICECONNECTIONCONFIGURATIONCHANGEDEVENT.fields_by_name['connection_configuration'].message_type = device__settings__structures__pb2._DEVICECONNECTIONCONFIGURATION
_DEVICEWHITEBOARDCONFIGURATIONCHANGEDEVENT.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_DEVICEWHITEBOARDCONFIGURATIONCHANGEDEVENT.fields_by_name['whiteboard_configuration'].message_type = device__settings__structures__pb2._WHITEBOARDCONFIGURATION
_DEVICEAUDIOSETTINGSCHANGEDEVENT.fields_by_name['product_model'].enum_type = product__state__structures__pb2._PRODUCT_MODEL
_DEVICEAUDIOSETTINGSCHANGEDEVENT.fields_by_name['audio_settings'].message_type = device__settings__structures__pb2._AUDIOSETTINGS
_DEVICESETTINGSEVENT.fields_by_name['device_display_configuration_changed_event'].message_type = _DEVICEDISPLAYCONFIGURATIONCHANGEDEVENT
_DEVICESETTINGSEVENT.fields_by_name['device_connection_configuration_changed_event'].message_type = _DEVICECONNECTIONCONFIGURATIONCHANGEDEVENT
_DEVICESETTINGSEVENT.fields_by_name['device_whiteboard_configuration_changed_event'].message_type = _DEVICEWHITEBOARDCONFIGURATIONCHANGEDEVENT
_DEVICESETTINGSEVENT.fields_by_name['device_audio_settings_changed_event'].message_type = _DEVICEAUDIOSETTINGSCHANGEDEVENT
_DEVICESETTINGSEVENT.oneofs_by_name['event'].fields.append(
  _DEVICESETTINGSEVENT.fields_by_name['device_display_configuration_changed_event'])
_DEVICESETTINGSEVENT.fields_by_name['device_display_configuration_changed_event'].containing_oneof = _DEVICESETTINGSEVENT.oneofs_by_name['event']
_DEVICESETTINGSEVENT.oneofs_by_name['event'].fields.append(
  _DEVICESETTINGSEVENT.fields_by_name['device_connection_configuration_changed_event'])
_DEVICESETTINGSEVENT.fields_by_name['device_connection_configuration_changed_event'].containing_oneof = _DEVICESETTINGSEVENT.oneofs_by_name['event']
_DEVICESETTINGSEVENT.oneofs_by_name['event'].fields.append(
  _DEVICESETTINGSEVENT.fields_by_name['device_whiteboard_configuration_changed_event'])
_DEVICESETTINGSEVENT.fields_by_name['device_whiteboard_configuration_changed_event'].containing_oneof = _DEVICESETTINGSEVENT.oneofs_by_name['event']
_DEVICESETTINGSEVENT.oneofs_by_name['event'].fields.append(
  _DEVICESETTINGSEVENT.fields_by_name['device_audio_settings_changed_event'])
_DEVICESETTINGSEVENT.fields_by_name['device_audio_settings_changed_event'].containing_oneof = _DEVICESETTINGSEVENT.oneofs_by_name['event']
DESCRIPTOR.message_types_by_name['DeviceDisplayConfigurationChangedEvent'] = _DEVICEDISPLAYCONFIGURATIONCHANGEDEVENT
DESCRIPTOR.message_types_by_name['DeviceConnectionConfigurationChangedEvent'] = _DEVICECONNECTIONCONFIGURATIONCHANGEDEVENT
DESCRIPTOR.message_types_by_name['DeviceWhiteboardConfigurationChangedEvent'] = _DEVICEWHITEBOARDCONFIGURATIONCHANGEDEVENT
DESCRIPTOR.message_types_by_name['DeviceAudioSettingsChangedEvent'] = _DEVICEAUDIOSETTINGSCHANGEDEVENT
DESCRIPTOR.message_types_by_name['DeviceSettingsEvent'] = _DEVICESETTINGSEVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DeviceDisplayConfigurationChangedEvent = _reflection.GeneratedProtocolMessageType('DeviceDisplayConfigurationChangedEvent', (_message.Message,), dict(
  DESCRIPTOR = _DEVICEDISPLAYCONFIGURATIONCHANGEDEVENT,
  __module__ = 'device_settings_events_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.DeviceDisplayConfigurationChangedEvent)
  ))
_sym_db.RegisterMessage(DeviceDisplayConfigurationChangedEvent)

DeviceConnectionConfigurationChangedEvent = _reflection.GeneratedProtocolMessageType('DeviceConnectionConfigurationChangedEvent', (_message.Message,), dict(
  DESCRIPTOR = _DEVICECONNECTIONCONFIGURATIONCHANGEDEVENT,
  __module__ = 'device_settings_events_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.DeviceConnectionConfigurationChangedEvent)
  ))
_sym_db.RegisterMessage(DeviceConnectionConfigurationChangedEvent)

DeviceWhiteboardConfigurationChangedEvent = _reflection.GeneratedProtocolMessageType('DeviceWhiteboardConfigurationChangedEvent', (_message.Message,), dict(
  DESCRIPTOR = _DEVICEWHITEBOARDCONFIGURATIONCHANGEDEVENT,
  __module__ = 'device_settings_events_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.DeviceWhiteboardConfigurationChangedEvent)
  ))
_sym_db.RegisterMessage(DeviceWhiteboardConfigurationChangedEvent)

DeviceAudioSettingsChangedEvent = _reflection.GeneratedProtocolMessageType('DeviceAudioSettingsChangedEvent', (_message.Message,), dict(
  DESCRIPTOR = _DEVICEAUDIOSETTINGSCHANGEDEVENT,
  __module__ = 'device_settings_events_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.DeviceAudioSettingsChangedEvent)
  ))
_sym_db.RegisterMessage(DeviceAudioSettingsChangedEvent)

DeviceSettingsEvent = _reflection.GeneratedProtocolMessageType('DeviceSettingsEvent', (_message.Message,), dict(
  DESCRIPTOR = _DEVICESETTINGSEVENT,
  __module__ = 'device_settings_events_pb2'
  # @@protoc_insertion_point(class_scope:logi.proto.DeviceSettingsEvent)
  ))
_sym_db.RegisterMessage(DeviceSettingsEvent)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)