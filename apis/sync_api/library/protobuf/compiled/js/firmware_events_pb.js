/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

var jspb = require('google-protobuf');
var goog = jspb;
var global = Function('return this')();

var common_pb = require('./common_pb.js');
var firmware_structures_pb = require('./firmware_structures_pb.js');
goog.exportSymbol('proto.logi.proto.FirmwareEvent', null, global);
goog.exportSymbol('proto.logi.proto.FirmwareUpdateCompletedEvent', null, global);
goog.exportSymbol('proto.logi.proto.FirmwareUpdateErrorEvent', null, global);
goog.exportSymbol('proto.logi.proto.FirmwareUpdateProgressEvent', null, global);
goog.exportSymbol('proto.logi.proto.FirmwareUpdateStartedEvent', null, global);

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
proto.logi.proto.FirmwareUpdateProgressEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.logi.proto.FirmwareUpdateProgressEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.FirmwareUpdateProgressEvent.displayName = 'proto.logi.proto.FirmwareUpdateProgressEvent';
}


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
proto.logi.proto.FirmwareUpdateProgressEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.FirmwareUpdateProgressEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.FirmwareUpdateProgressEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateProgressEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    progress: (f = msg.getProgress()) && firmware_structures_pb.FirmwareUpdateProgress.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.FirmwareUpdateProgressEvent}
 */
proto.logi.proto.FirmwareUpdateProgressEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.FirmwareUpdateProgressEvent;
  return proto.logi.proto.FirmwareUpdateProgressEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.FirmwareUpdateProgressEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.FirmwareUpdateProgressEvent}
 */
proto.logi.proto.FirmwareUpdateProgressEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new firmware_structures_pb.FirmwareUpdateProgress;
      reader.readMessage(value,firmware_structures_pb.FirmwareUpdateProgress.deserializeBinaryFromReader);
      msg.setProgress(value);
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
proto.logi.proto.FirmwareUpdateProgressEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.FirmwareUpdateProgressEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.FirmwareUpdateProgressEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateProgressEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getProgress();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      firmware_structures_pb.FirmwareUpdateProgress.serializeBinaryToWriter
    );
  }
};


/**
 * optional FirmwareUpdateProgress progress = 1;
 * @return {?proto.logi.proto.FirmwareUpdateProgress}
 */
proto.logi.proto.FirmwareUpdateProgressEvent.prototype.getProgress = function() {
  return /** @type{?proto.logi.proto.FirmwareUpdateProgress} */ (
    jspb.Message.getWrapperField(this, firmware_structures_pb.FirmwareUpdateProgress, 1));
};


/** @param {?proto.logi.proto.FirmwareUpdateProgress|undefined} value */
proto.logi.proto.FirmwareUpdateProgressEvent.prototype.setProgress = function(value) {
  jspb.Message.setWrapperField(this, 1, value);
};


proto.logi.proto.FirmwareUpdateProgressEvent.prototype.clearProgress = function() {
  this.setProgress(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.FirmwareUpdateProgressEvent.prototype.hasProgress = function() {
  return jspb.Message.getField(this, 1) != null;
};



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
proto.logi.proto.FirmwareUpdateStartedEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.logi.proto.FirmwareUpdateStartedEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.FirmwareUpdateStartedEvent.displayName = 'proto.logi.proto.FirmwareUpdateStartedEvent';
}


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
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.FirmwareUpdateStartedEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.FirmwareUpdateStartedEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateStartedEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    productUuid: jspb.Message.getFieldWithDefault(msg, 1, ""),
    currentFirmwarePackageVersion: jspb.Message.getFieldWithDefault(msg, 2, ""),
    newFirmwarePackageVersion: jspb.Message.getFieldWithDefault(msg, 3, "")
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
 * @return {!proto.logi.proto.FirmwareUpdateStartedEvent}
 */
proto.logi.proto.FirmwareUpdateStartedEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.FirmwareUpdateStartedEvent;
  return proto.logi.proto.FirmwareUpdateStartedEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.FirmwareUpdateStartedEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.FirmwareUpdateStartedEvent}
 */
proto.logi.proto.FirmwareUpdateStartedEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setProductUuid(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setCurrentFirmwarePackageVersion(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setNewFirmwarePackageVersion(value);
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
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.FirmwareUpdateStartedEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.FirmwareUpdateStartedEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateStartedEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getProductUuid();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getCurrentFirmwarePackageVersion();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getNewFirmwarePackageVersion();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
};


/**
 * optional string product_uuid = 1;
 * @return {string}
 */
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.getProductUuid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.setProductUuid = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string current_firmware_package_version = 2;
 * @return {string}
 */
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.getCurrentFirmwarePackageVersion = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/** @param {string} value */
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.setCurrentFirmwarePackageVersion = function(value) {
  jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string new_firmware_package_version = 3;
 * @return {string}
 */
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.getNewFirmwarePackageVersion = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/** @param {string} value */
proto.logi.proto.FirmwareUpdateStartedEvent.prototype.setNewFirmwarePackageVersion = function(value) {
  jspb.Message.setProto3StringField(this, 3, value);
};



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
proto.logi.proto.FirmwareUpdateCompletedEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.logi.proto.FirmwareUpdateCompletedEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.FirmwareUpdateCompletedEvent.displayName = 'proto.logi.proto.FirmwareUpdateCompletedEvent';
}


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
proto.logi.proto.FirmwareUpdateCompletedEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.FirmwareUpdateCompletedEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.FirmwareUpdateCompletedEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateCompletedEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    productUuid: jspb.Message.getFieldWithDefault(msg, 1, ""),
    newFirmwarePackageVersion: jspb.Message.getFieldWithDefault(msg, 2, "")
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
 * @return {!proto.logi.proto.FirmwareUpdateCompletedEvent}
 */
proto.logi.proto.FirmwareUpdateCompletedEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.FirmwareUpdateCompletedEvent;
  return proto.logi.proto.FirmwareUpdateCompletedEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.FirmwareUpdateCompletedEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.FirmwareUpdateCompletedEvent}
 */
proto.logi.proto.FirmwareUpdateCompletedEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setProductUuid(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setNewFirmwarePackageVersion(value);
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
proto.logi.proto.FirmwareUpdateCompletedEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.FirmwareUpdateCompletedEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.FirmwareUpdateCompletedEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateCompletedEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getProductUuid();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getNewFirmwarePackageVersion();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string product_uuid = 1;
 * @return {string}
 */
proto.logi.proto.FirmwareUpdateCompletedEvent.prototype.getProductUuid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.logi.proto.FirmwareUpdateCompletedEvent.prototype.setProductUuid = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string new_firmware_package_version = 2;
 * @return {string}
 */
proto.logi.proto.FirmwareUpdateCompletedEvent.prototype.getNewFirmwarePackageVersion = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/** @param {string} value */
proto.logi.proto.FirmwareUpdateCompletedEvent.prototype.setNewFirmwarePackageVersion = function(value) {
  jspb.Message.setProto3StringField(this, 2, value);
};



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
proto.logi.proto.FirmwareUpdateErrorEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.logi.proto.FirmwareUpdateErrorEvent.repeatedFields_, null);
};
goog.inherits(proto.logi.proto.FirmwareUpdateErrorEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.FirmwareUpdateErrorEvent.displayName = 'proto.logi.proto.FirmwareUpdateErrorEvent';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.logi.proto.FirmwareUpdateErrorEvent.repeatedFields_ = [2];



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
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.FirmwareUpdateErrorEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.FirmwareUpdateErrorEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateErrorEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    productUuid: jspb.Message.getFieldWithDefault(msg, 1, ""),
    errorsList: jspb.Message.toObjectList(msg.getErrorsList(),
    common_pb.Error.toObject, includeInstance)
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
 * @return {!proto.logi.proto.FirmwareUpdateErrorEvent}
 */
proto.logi.proto.FirmwareUpdateErrorEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.FirmwareUpdateErrorEvent;
  return proto.logi.proto.FirmwareUpdateErrorEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.FirmwareUpdateErrorEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.FirmwareUpdateErrorEvent}
 */
proto.logi.proto.FirmwareUpdateErrorEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setProductUuid(value);
      break;
    case 2:
      var value = new common_pb.Error;
      reader.readMessage(value,common_pb.Error.deserializeBinaryFromReader);
      msg.addErrors(value);
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
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.FirmwareUpdateErrorEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.FirmwareUpdateErrorEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareUpdateErrorEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getProductUuid();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getErrorsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      2,
      f,
      common_pb.Error.serializeBinaryToWriter
    );
  }
};


/**
 * optional string product_uuid = 1;
 * @return {string}
 */
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.getProductUuid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.setProductUuid = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * repeated Error errors = 2;
 * @return {!Array<!proto.logi.proto.Error>}
 */
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.getErrorsList = function() {
  return /** @type{!Array<!proto.logi.proto.Error>} */ (
    jspb.Message.getRepeatedWrapperField(this, common_pb.Error, 2));
};


/** @param {!Array<!proto.logi.proto.Error>} value */
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.setErrorsList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 2, value);
};


/**
 * @param {!proto.logi.proto.Error=} opt_value
 * @param {number=} opt_index
 * @return {!proto.logi.proto.Error}
 */
proto.logi.proto.FirmwareUpdateErrorEvent.prototype.addErrors = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 2, opt_value, proto.logi.proto.Error, opt_index);
};


proto.logi.proto.FirmwareUpdateErrorEvent.prototype.clearErrorsList = function() {
  this.setErrorsList([]);
};



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
proto.logi.proto.FirmwareEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.logi.proto.FirmwareEvent.oneofGroups_);
};
goog.inherits(proto.logi.proto.FirmwareEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.FirmwareEvent.displayName = 'proto.logi.proto.FirmwareEvent';
}
/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.logi.proto.FirmwareEvent.oneofGroups_ = [[1,2,3,4]];

/**
 * @enum {number}
 */
proto.logi.proto.FirmwareEvent.EventCase = {
  EVENT_NOT_SET: 0,
  FIRMWARE_UPDATE_PROGRESS_EVENT: 1,
  FIRMWARE_UPDATE_STARTED_EVENT: 2,
  FIRMWARE_UPDATE_ERROR_EVENT: 3,
  FIRMWARE_UPDATE_COMPLETED_EVENT: 4
};

/**
 * @return {proto.logi.proto.FirmwareEvent.EventCase}
 */
proto.logi.proto.FirmwareEvent.prototype.getEventCase = function() {
  return /** @type {proto.logi.proto.FirmwareEvent.EventCase} */(jspb.Message.computeOneofCase(this, proto.logi.proto.FirmwareEvent.oneofGroups_[0]));
};



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
proto.logi.proto.FirmwareEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.FirmwareEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.FirmwareEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    firmwareUpdateProgressEvent: (f = msg.getFirmwareUpdateProgressEvent()) && proto.logi.proto.FirmwareUpdateProgressEvent.toObject(includeInstance, f),
    firmwareUpdateStartedEvent: (f = msg.getFirmwareUpdateStartedEvent()) && proto.logi.proto.FirmwareUpdateStartedEvent.toObject(includeInstance, f),
    firmwareUpdateErrorEvent: (f = msg.getFirmwareUpdateErrorEvent()) && proto.logi.proto.FirmwareUpdateErrorEvent.toObject(includeInstance, f),
    firmwareUpdateCompletedEvent: (f = msg.getFirmwareUpdateCompletedEvent()) && proto.logi.proto.FirmwareUpdateCompletedEvent.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.FirmwareEvent}
 */
proto.logi.proto.FirmwareEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.FirmwareEvent;
  return proto.logi.proto.FirmwareEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.FirmwareEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.FirmwareEvent}
 */
proto.logi.proto.FirmwareEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.logi.proto.FirmwareUpdateProgressEvent;
      reader.readMessage(value,proto.logi.proto.FirmwareUpdateProgressEvent.deserializeBinaryFromReader);
      msg.setFirmwareUpdateProgressEvent(value);
      break;
    case 2:
      var value = new proto.logi.proto.FirmwareUpdateStartedEvent;
      reader.readMessage(value,proto.logi.proto.FirmwareUpdateStartedEvent.deserializeBinaryFromReader);
      msg.setFirmwareUpdateStartedEvent(value);
      break;
    case 3:
      var value = new proto.logi.proto.FirmwareUpdateErrorEvent;
      reader.readMessage(value,proto.logi.proto.FirmwareUpdateErrorEvent.deserializeBinaryFromReader);
      msg.setFirmwareUpdateErrorEvent(value);
      break;
    case 4:
      var value = new proto.logi.proto.FirmwareUpdateCompletedEvent;
      reader.readMessage(value,proto.logi.proto.FirmwareUpdateCompletedEvent.deserializeBinaryFromReader);
      msg.setFirmwareUpdateCompletedEvent(value);
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
proto.logi.proto.FirmwareEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.FirmwareEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.FirmwareEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.FirmwareEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getFirmwareUpdateProgressEvent();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      proto.logi.proto.FirmwareUpdateProgressEvent.serializeBinaryToWriter
    );
  }
  f = message.getFirmwareUpdateStartedEvent();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      proto.logi.proto.FirmwareUpdateStartedEvent.serializeBinaryToWriter
    );
  }
  f = message.getFirmwareUpdateErrorEvent();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      proto.logi.proto.FirmwareUpdateErrorEvent.serializeBinaryToWriter
    );
  }
  f = message.getFirmwareUpdateCompletedEvent();
  if (f != null) {
    writer.writeMessage(
      4,
      f,
      proto.logi.proto.FirmwareUpdateCompletedEvent.serializeBinaryToWriter
    );
  }
};


/**
 * optional FirmwareUpdateProgressEvent firmware_update_progress_event = 1;
 * @return {?proto.logi.proto.FirmwareUpdateProgressEvent}
 */
proto.logi.proto.FirmwareEvent.prototype.getFirmwareUpdateProgressEvent = function() {
  return /** @type{?proto.logi.proto.FirmwareUpdateProgressEvent} */ (
    jspb.Message.getWrapperField(this, proto.logi.proto.FirmwareUpdateProgressEvent, 1));
};


/** @param {?proto.logi.proto.FirmwareUpdateProgressEvent|undefined} value */
proto.logi.proto.FirmwareEvent.prototype.setFirmwareUpdateProgressEvent = function(value) {
  jspb.Message.setOneofWrapperField(this, 1, proto.logi.proto.FirmwareEvent.oneofGroups_[0], value);
};


proto.logi.proto.FirmwareEvent.prototype.clearFirmwareUpdateProgressEvent = function() {
  this.setFirmwareUpdateProgressEvent(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.FirmwareEvent.prototype.hasFirmwareUpdateProgressEvent = function() {
  return jspb.Message.getField(this, 1) != null;
};


/**
 * optional FirmwareUpdateStartedEvent firmware_update_started_event = 2;
 * @return {?proto.logi.proto.FirmwareUpdateStartedEvent}
 */
proto.logi.proto.FirmwareEvent.prototype.getFirmwareUpdateStartedEvent = function() {
  return /** @type{?proto.logi.proto.FirmwareUpdateStartedEvent} */ (
    jspb.Message.getWrapperField(this, proto.logi.proto.FirmwareUpdateStartedEvent, 2));
};


/** @param {?proto.logi.proto.FirmwareUpdateStartedEvent|undefined} value */
proto.logi.proto.FirmwareEvent.prototype.setFirmwareUpdateStartedEvent = function(value) {
  jspb.Message.setOneofWrapperField(this, 2, proto.logi.proto.FirmwareEvent.oneofGroups_[0], value);
};


proto.logi.proto.FirmwareEvent.prototype.clearFirmwareUpdateStartedEvent = function() {
  this.setFirmwareUpdateStartedEvent(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.FirmwareEvent.prototype.hasFirmwareUpdateStartedEvent = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional FirmwareUpdateErrorEvent firmware_update_error_event = 3;
 * @return {?proto.logi.proto.FirmwareUpdateErrorEvent}
 */
proto.logi.proto.FirmwareEvent.prototype.getFirmwareUpdateErrorEvent = function() {
  return /** @type{?proto.logi.proto.FirmwareUpdateErrorEvent} */ (
    jspb.Message.getWrapperField(this, proto.logi.proto.FirmwareUpdateErrorEvent, 3));
};


/** @param {?proto.logi.proto.FirmwareUpdateErrorEvent|undefined} value */
proto.logi.proto.FirmwareEvent.prototype.setFirmwareUpdateErrorEvent = function(value) {
  jspb.Message.setOneofWrapperField(this, 3, proto.logi.proto.FirmwareEvent.oneofGroups_[0], value);
};


proto.logi.proto.FirmwareEvent.prototype.clearFirmwareUpdateErrorEvent = function() {
  this.setFirmwareUpdateErrorEvent(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.FirmwareEvent.prototype.hasFirmwareUpdateErrorEvent = function() {
  return jspb.Message.getField(this, 3) != null;
};


/**
 * optional FirmwareUpdateCompletedEvent firmware_update_completed_event = 4;
 * @return {?proto.logi.proto.FirmwareUpdateCompletedEvent}
 */
proto.logi.proto.FirmwareEvent.prototype.getFirmwareUpdateCompletedEvent = function() {
  return /** @type{?proto.logi.proto.FirmwareUpdateCompletedEvent} */ (
    jspb.Message.getWrapperField(this, proto.logi.proto.FirmwareUpdateCompletedEvent, 4));
};


/** @param {?proto.logi.proto.FirmwareUpdateCompletedEvent|undefined} value */
proto.logi.proto.FirmwareEvent.prototype.setFirmwareUpdateCompletedEvent = function(value) {
  jspb.Message.setOneofWrapperField(this, 4, proto.logi.proto.FirmwareEvent.oneofGroups_[0], value);
};


proto.logi.proto.FirmwareEvent.prototype.clearFirmwareUpdateCompletedEvent = function() {
  this.setFirmwareUpdateCompletedEvent(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.FirmwareEvent.prototype.hasFirmwareUpdateCompletedEvent = function() {
  return jspb.Message.getField(this, 4) != null;
};


goog.object.extend(exports, proto.logi.proto);
