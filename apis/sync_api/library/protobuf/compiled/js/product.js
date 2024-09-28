/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

goog.provide('proto.logi.proto.Product');
goog.provide('proto.logi.proto.Product.Model');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.logi.proto.Device');
goog.require('proto.logi.proto.DeviceEdge');

goog.forwardDeclare('proto.logi.proto.SyncUpdateState');

/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.logi.proto.Product = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.logi.proto.Product.repeatedFields_, null);
};
goog.inherits(proto.logi.proto.Product, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.Product.displayName = 'proto.logi.proto.Product';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.logi.proto.Product.repeatedFields_ = [6,7];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.logi.proto.Product.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.Product.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.Product} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.Product.toObject = function(includeInstance, msg) {
  var f, obj = {
    uuid: jspb.Message.getFieldWithDefault(msg, 1, ""),
    model: jspb.Message.getFieldWithDefault(msg, 2, 0),
    name: jspb.Message.getFieldWithDefault(msg, 3, ""),
    firmwarePackageVersion: jspb.Message.getFieldWithDefault(msg, 4, ""),
    lastFirmwareUpdateTime: jspb.Message.getFieldWithDefault(msg, 5, 0),
    devicesList: jspb.Message.toObjectList(msg.getDevicesList(),
    proto.logi.proto.Device.toObject, includeInstance),
    deviceConnectionsList: jspb.Message.toObjectList(msg.getDeviceConnectionsList(),
    proto.logi.proto.DeviceEdge.toObject, includeInstance),
    serialNumber: jspb.Message.getFieldWithDefault(msg, 8, ""),
    currentUpdateState: jspb.Message.getFieldWithDefault(msg, 9, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.logi.proto.Product}
 */
proto.logi.proto.Product.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.Product;
  return proto.logi.proto.Product.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.Product} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.Product}
 */
proto.logi.proto.Product.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setUuid(value);
      break;
    case 2:
      var value = /** @type {!proto.logi.proto.Product.Model} */ (reader.readEnum());
      msg.setModel(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setFirmwarePackageVersion(value);
      break;
    case 5:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setLastFirmwareUpdateTime(value);
      break;
    case 6:
      var value = new proto.logi.proto.Device;
      reader.readMessage(value,proto.logi.proto.Device.deserializeBinaryFromReader);
      msg.addDevices(value);
      break;
    case 7:
      var value = new proto.logi.proto.DeviceEdge;
      reader.readMessage(value,proto.logi.proto.DeviceEdge.deserializeBinaryFromReader);
      msg.addDeviceConnections(value);
      break;
    case 8:
      var value = /** @type {string} */ (reader.readString());
      msg.setSerialNumber(value);
      break;
    case 9:
      var value = /** @type {!proto.logi.proto.SyncUpdateState} */ (reader.readEnum());
      msg.setCurrentUpdateState(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.logi.proto.Product.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.Product.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.Product} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.Product.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getUuid();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getModel();
  if (f !== 0.0) {
    writer.writeEnum(
      2,
      f
    );
  }
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getFirmwarePackageVersion();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getLastFirmwareUpdateTime();
  if (f !== 0) {
    writer.writeUint32(
      5,
      f
    );
  }
  f = message.getDevicesList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      6,
      f,
      proto.logi.proto.Device.serializeBinaryToWriter
    );
  }
  f = message.getDeviceConnectionsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      7,
      f,
      proto.logi.proto.DeviceEdge.serializeBinaryToWriter
    );
  }
  f = message.getSerialNumber();
  if (f.length > 0) {
    writer.writeString(
      8,
      f
    );
  }
  f = message.getCurrentUpdateState();
  if (f !== 0.0) {
    writer.writeEnum(
      9,
      f
    );
  }
};


/**
 * @enum {number}
 */
proto.logi.proto.Product.Model = {
  UNKNOWN: 0,
  MEETUP: 1,
  RALLY: 20,
  RALLY_CAMERA: 21
};

/**
 * optional string uuid = 1;
 * @return {string}
 */
proto.logi.proto.Product.prototype.getUuid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.logi.proto.Product.prototype.setUuid = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional Model model = 2;
 * @return {!proto.logi.proto.Product.Model}
 */
proto.logi.proto.Product.prototype.getModel = function() {
  return /** @type {!proto.logi.proto.Product.Model} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/** @param {!proto.logi.proto.Product.Model} value */
proto.logi.proto.Product.prototype.setModel = function(value) {
  jspb.Message.setProto3EnumField(this, 2, value);
};


/**
 * optional string name = 3;
 * @return {string}
 */
proto.logi.proto.Product.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/** @param {string} value */
proto.logi.proto.Product.prototype.setName = function(value) {
  jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string firmware_package_version = 4;
 * @return {string}
 */
proto.logi.proto.Product.prototype.getFirmwarePackageVersion = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/** @param {string} value */
proto.logi.proto.Product.prototype.setFirmwarePackageVersion = function(value) {
  jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * optional uint32 last_firmware_update_time = 5;
 * @return {number}
 */
proto.logi.proto.Product.prototype.getLastFirmwareUpdateTime = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 5, 0));
};


/** @param {number} value */
proto.logi.proto.Product.prototype.setLastFirmwareUpdateTime = function(value) {
  jspb.Message.setProto3IntField(this, 5, value);
};


/**
 * repeated Device devices = 6;
 * @return {!Array<!proto.logi.proto.Device>}
 */
proto.logi.proto.Product.prototype.getDevicesList = function() {
  return /** @type{!Array<!proto.logi.proto.Device>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.logi.proto.Device, 6));
};


/** @param {!Array<!proto.logi.proto.Device>} value */
proto.logi.proto.Product.prototype.setDevicesList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 6, value);
};


/**
 * @param {!proto.logi.proto.Device=} opt_value
 * @param {number=} opt_index
 * @return {!proto.logi.proto.Device}
 */
proto.logi.proto.Product.prototype.addDevices = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 6, opt_value, proto.logi.proto.Device, opt_index);
};


proto.logi.proto.Product.prototype.clearDevicesList = function() {
  this.setDevicesList([]);
};


/**
 * repeated DeviceEdge device_connections = 7;
 * @return {!Array<!proto.logi.proto.DeviceEdge>}
 */
proto.logi.proto.Product.prototype.getDeviceConnectionsList = function() {
  return /** @type{!Array<!proto.logi.proto.DeviceEdge>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.logi.proto.DeviceEdge, 7));
};


/** @param {!Array<!proto.logi.proto.DeviceEdge>} value */
proto.logi.proto.Product.prototype.setDeviceConnectionsList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 7, value);
};


/**
 * @param {!proto.logi.proto.DeviceEdge=} opt_value
 * @param {number=} opt_index
 * @return {!proto.logi.proto.DeviceEdge}
 */
proto.logi.proto.Product.prototype.addDeviceConnections = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 7, opt_value, proto.logi.proto.DeviceEdge, opt_index);
};


proto.logi.proto.Product.prototype.clearDeviceConnectionsList = function() {
  this.setDeviceConnectionsList([]);
};


/**
 * optional string serial_number = 8;
 * @return {string}
 */
proto.logi.proto.Product.prototype.getSerialNumber = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 8, ""));
};


/** @param {string} value */
proto.logi.proto.Product.prototype.setSerialNumber = function(value) {
  jspb.Message.setProto3StringField(this, 8, value);
};


/**
 * optional SyncUpdateState current_update_state = 9;
 * @return {!proto.logi.proto.SyncUpdateState}
 */
proto.logi.proto.Product.prototype.getCurrentUpdateState = function() {
  return /** @type {!proto.logi.proto.SyncUpdateState} */ (jspb.Message.getFieldWithDefault(this, 9, 0));
};


/** @param {!proto.logi.proto.SyncUpdateState} value */
proto.logi.proto.Product.prototype.setCurrentUpdateState = function(value) {
  jspb.Message.setProto3EnumField(this, 9, value);
};

