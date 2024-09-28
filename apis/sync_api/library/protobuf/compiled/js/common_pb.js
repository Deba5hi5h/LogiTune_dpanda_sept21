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

goog.exportSymbol('proto.logi.proto.Error', null, global);
goog.exportSymbol('proto.logi.proto.SyncConnectionState', null, global);
goog.exportSymbol('proto.logi.proto.SyncUpdateState', null, global);

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
proto.logi.proto.Error = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.logi.proto.Error, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.Error.displayName = 'proto.logi.proto.Error';
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
proto.logi.proto.Error.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.Error.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.Error} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.Error.toObject = function(includeInstance, msg) {
  var f, obj = {
    errorCode: jspb.Message.getFieldWithDefault(msg, 1, 0),
    errorMessage: jspb.Message.getFieldWithDefault(msg, 2, ""),
    errorLogUri: jspb.Message.getFieldWithDefault(msg, 3, ""),
    jsonMetadata: jspb.Message.getFieldWithDefault(msg, 4, "")
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
 * @return {!proto.logi.proto.Error}
 */
proto.logi.proto.Error.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.Error;
  return proto.logi.proto.Error.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.Error} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.Error}
 */
proto.logi.proto.Error.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setErrorCode(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setErrorMessage(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setErrorLogUri(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setJsonMetadata(value);
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
proto.logi.proto.Error.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.Error.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.Error} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.Error.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getErrorCode();
  if (f !== 0) {
    writer.writeUint32(
      1,
      f
    );
  }
  f = message.getErrorMessage();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getErrorLogUri();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getJsonMetadata();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional uint32 error_code = 1;
 * @return {number}
 */
proto.logi.proto.Error.prototype.getErrorCode = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/** @param {number} value */
proto.logi.proto.Error.prototype.setErrorCode = function(value) {
  jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional string error_message = 2;
 * @return {string}
 */
proto.logi.proto.Error.prototype.getErrorMessage = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/** @param {string} value */
proto.logi.proto.Error.prototype.setErrorMessage = function(value) {
  jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string error_log_uri = 3;
 * @return {string}
 */
proto.logi.proto.Error.prototype.getErrorLogUri = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/** @param {string} value */
proto.logi.proto.Error.prototype.setErrorLogUri = function(value) {
  jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string json_metadata = 4;
 * @return {string}
 */
proto.logi.proto.Error.prototype.getJsonMetadata = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/** @param {string} value */
proto.logi.proto.Error.prototype.setJsonMetadata = function(value) {
  jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * @enum {number}
 */
proto.logi.proto.SyncConnectionState = {
  SYNC_CONNECTION_STATE_UNKNOWN: 0,
  SYNC_CONNECTION_STATE_OFFLINE: 10,
  SYNC_CONNECTION_STATE_ONLINE: 11,
  SYNC_CONNECTION_STATE_ENUMERATING: 20
};

/**
 * @enum {number}
 */
proto.logi.proto.SyncUpdateState = {
  SYNC_UPDATE_STATE_UNKNOWN: 0,
  SYNC_UPDATE_STATE_CURRENT: 10,
  SYNC_UPDATE_STATE_AVAILABLE: 11,
  SYNC_UPDATE_STATE_STARTING: 13,
  SYNC_UPDATE_STATE_DOWNLOADING: 14,
  SYNC_UPDATE_STATE_READY: 15,
  SYNC_UPDATE_STATE_UPDATING: 16,
  SYNC_UPDATE_STATE_SCHEDULED: 17,
  SYNC_UPDATE_STATE_ERROR: 18
};

goog.object.extend(exports, proto.logi.proto);
