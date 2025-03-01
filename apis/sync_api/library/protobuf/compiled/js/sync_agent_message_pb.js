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

var transport_pb = require('./transport_pb.js');
var sync_agent_software_update_requests_pb = require('./sync_agent_software_update_requests_pb.js');
var sync_agent_software_update_events_pb = require('./sync_agent_software_update_events_pb.js');
goog.exportSymbol('proto.logi.proto.LSAEvent', null, global);
goog.exportSymbol('proto.logi.proto.LSARequest', null, global);
goog.exportSymbol('proto.logi.proto.LSAResponse', null, global);
goog.exportSymbol('proto.logi.proto.LogiSyncAgentMessage', null, global);

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
proto.logi.proto.LogiSyncAgentMessage = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.logi.proto.LogiSyncAgentMessage.oneofGroups_);
};
goog.inherits(proto.logi.proto.LogiSyncAgentMessage, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.LogiSyncAgentMessage.displayName = 'proto.logi.proto.LogiSyncAgentMessage';
}
/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.logi.proto.LogiSyncAgentMessage.oneofGroups_ = [[3,4]];

/**
 * @enum {number}
 */
proto.logi.proto.LogiSyncAgentMessage.PayloadCase = {
  PAYLOAD_NOT_SET: 0,
  REQUEST: 3,
  EVENT: 4
};

/**
 * @return {proto.logi.proto.LogiSyncAgentMessage.PayloadCase}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.getPayloadCase = function() {
  return /** @type {proto.logi.proto.LogiSyncAgentMessage.PayloadCase} */(jspb.Message.computeOneofCase(this, proto.logi.proto.LogiSyncAgentMessage.oneofGroups_[0]));
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
proto.logi.proto.LogiSyncAgentMessage.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.LogiSyncAgentMessage.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.LogiSyncAgentMessage} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LogiSyncAgentMessage.toObject = function(includeInstance, msg) {
  var f, obj = {
    header: (f = msg.getHeader()) && transport_pb.Header.toObject(includeInstance, f),
    internalApiId: jspb.Message.getFieldWithDefault(msg, 2, 0),
    request: (f = msg.getRequest()) && proto.logi.proto.LSARequest.toObject(includeInstance, f),
    event: (f = msg.getEvent()) && proto.logi.proto.LSAEvent.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.LogiSyncAgentMessage}
 */
proto.logi.proto.LogiSyncAgentMessage.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.LogiSyncAgentMessage;
  return proto.logi.proto.LogiSyncAgentMessage.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.LogiSyncAgentMessage} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.LogiSyncAgentMessage}
 */
proto.logi.proto.LogiSyncAgentMessage.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new transport_pb.Header;
      reader.readMessage(value,transport_pb.Header.deserializeBinaryFromReader);
      msg.setHeader(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setInternalApiId(value);
      break;
    case 3:
      var value = new proto.logi.proto.LSARequest;
      reader.readMessage(value,proto.logi.proto.LSARequest.deserializeBinaryFromReader);
      msg.setRequest(value);
      break;
    case 4:
      var value = new proto.logi.proto.LSAEvent;
      reader.readMessage(value,proto.logi.proto.LSAEvent.deserializeBinaryFromReader);
      msg.setEvent(value);
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
proto.logi.proto.LogiSyncAgentMessage.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.LogiSyncAgentMessage.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.LogiSyncAgentMessage} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LogiSyncAgentMessage.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getHeader();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      transport_pb.Header.serializeBinaryToWriter
    );
  }
  f = message.getInternalApiId();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
  f = message.getRequest();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      proto.logi.proto.LSARequest.serializeBinaryToWriter
    );
  }
  f = message.getEvent();
  if (f != null) {
    writer.writeMessage(
      4,
      f,
      proto.logi.proto.LSAEvent.serializeBinaryToWriter
    );
  }
};


/**
 * optional Header header = 1;
 * @return {?proto.logi.proto.Header}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.getHeader = function() {
  return /** @type{?proto.logi.proto.Header} */ (
    jspb.Message.getWrapperField(this, transport_pb.Header, 1));
};


/** @param {?proto.logi.proto.Header|undefined} value */
proto.logi.proto.LogiSyncAgentMessage.prototype.setHeader = function(value) {
  jspb.Message.setWrapperField(this, 1, value);
};


proto.logi.proto.LogiSyncAgentMessage.prototype.clearHeader = function() {
  this.setHeader(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.hasHeader = function() {
  return jspb.Message.getField(this, 1) != null;
};


/**
 * optional int32 internal_api_id = 2;
 * @return {number}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.getInternalApiId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/** @param {number} value */
proto.logi.proto.LogiSyncAgentMessage.prototype.setInternalApiId = function(value) {
  jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional LSARequest request = 3;
 * @return {?proto.logi.proto.LSARequest}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.getRequest = function() {
  return /** @type{?proto.logi.proto.LSARequest} */ (
    jspb.Message.getWrapperField(this, proto.logi.proto.LSARequest, 3));
};


/** @param {?proto.logi.proto.LSARequest|undefined} value */
proto.logi.proto.LogiSyncAgentMessage.prototype.setRequest = function(value) {
  jspb.Message.setOneofWrapperField(this, 3, proto.logi.proto.LogiSyncAgentMessage.oneofGroups_[0], value);
};


proto.logi.proto.LogiSyncAgentMessage.prototype.clearRequest = function() {
  this.setRequest(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.hasRequest = function() {
  return jspb.Message.getField(this, 3) != null;
};


/**
 * optional LSAEvent event = 4;
 * @return {?proto.logi.proto.LSAEvent}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.getEvent = function() {
  return /** @type{?proto.logi.proto.LSAEvent} */ (
    jspb.Message.getWrapperField(this, proto.logi.proto.LSAEvent, 4));
};


/** @param {?proto.logi.proto.LSAEvent|undefined} value */
proto.logi.proto.LogiSyncAgentMessage.prototype.setEvent = function(value) {
  jspb.Message.setOneofWrapperField(this, 4, proto.logi.proto.LogiSyncAgentMessage.oneofGroups_[0], value);
};


proto.logi.proto.LogiSyncAgentMessage.prototype.clearEvent = function() {
  this.setEvent(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LogiSyncAgentMessage.prototype.hasEvent = function() {
  return jspb.Message.getField(this, 4) != null;
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
proto.logi.proto.LSARequest = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.logi.proto.LSARequest.oneofGroups_);
};
goog.inherits(proto.logi.proto.LSARequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.LSARequest.displayName = 'proto.logi.proto.LSARequest';
}
/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.logi.proto.LSARequest.oneofGroups_ = [[1]];

/**
 * @enum {number}
 */
proto.logi.proto.LSARequest.PayloadCase = {
  PAYLOAD_NOT_SET: 0,
  GET_SOFTWARE_UPDATE_REPORT_REQUEST: 1
};

/**
 * @return {proto.logi.proto.LSARequest.PayloadCase}
 */
proto.logi.proto.LSARequest.prototype.getPayloadCase = function() {
  return /** @type {proto.logi.proto.LSARequest.PayloadCase} */(jspb.Message.computeOneofCase(this, proto.logi.proto.LSARequest.oneofGroups_[0]));
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
proto.logi.proto.LSARequest.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.LSARequest.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.LSARequest} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSARequest.toObject = function(includeInstance, msg) {
  var f, obj = {
    getSoftwareUpdateReportRequest: (f = msg.getGetSoftwareUpdateReportRequest()) && sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportRequest.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.LSARequest}
 */
proto.logi.proto.LSARequest.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.LSARequest;
  return proto.logi.proto.LSARequest.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.LSARequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.LSARequest}
 */
proto.logi.proto.LSARequest.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportRequest;
      reader.readMessage(value,sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportRequest.deserializeBinaryFromReader);
      msg.setGetSoftwareUpdateReportRequest(value);
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
proto.logi.proto.LSARequest.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.LSARequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.LSARequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSARequest.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getGetSoftwareUpdateReportRequest();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportRequest.serializeBinaryToWriter
    );
  }
};


/**
 * optional LSAGetSoftwareUpdateReportRequest get_software_update_report_request = 1;
 * @return {?proto.logi.proto.LSAGetSoftwareUpdateReportRequest}
 */
proto.logi.proto.LSARequest.prototype.getGetSoftwareUpdateReportRequest = function() {
  return /** @type{?proto.logi.proto.LSAGetSoftwareUpdateReportRequest} */ (
    jspb.Message.getWrapperField(this, sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportRequest, 1));
};


/** @param {?proto.logi.proto.LSAGetSoftwareUpdateReportRequest|undefined} value */
proto.logi.proto.LSARequest.prototype.setGetSoftwareUpdateReportRequest = function(value) {
  jspb.Message.setOneofWrapperField(this, 1, proto.logi.proto.LSARequest.oneofGroups_[0], value);
};


proto.logi.proto.LSARequest.prototype.clearGetSoftwareUpdateReportRequest = function() {
  this.setGetSoftwareUpdateReportRequest(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LSARequest.prototype.hasGetSoftwareUpdateReportRequest = function() {
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
proto.logi.proto.LSAResponse = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.logi.proto.LSAResponse.oneofGroups_);
};
goog.inherits(proto.logi.proto.LSAResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.LSAResponse.displayName = 'proto.logi.proto.LSAResponse';
}
/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.logi.proto.LSAResponse.oneofGroups_ = [[1]];

/**
 * @enum {number}
 */
proto.logi.proto.LSAResponse.PayloadCase = {
  PAYLOAD_NOT_SET: 0,
  GET_SOFTWARE_UPDATE_REPORT_RESPONSE: 1
};

/**
 * @return {proto.logi.proto.LSAResponse.PayloadCase}
 */
proto.logi.proto.LSAResponse.prototype.getPayloadCase = function() {
  return /** @type {proto.logi.proto.LSAResponse.PayloadCase} */(jspb.Message.computeOneofCase(this, proto.logi.proto.LSAResponse.oneofGroups_[0]));
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
proto.logi.proto.LSAResponse.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.LSAResponse.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.LSAResponse} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSAResponse.toObject = function(includeInstance, msg) {
  var f, obj = {
    getSoftwareUpdateReportResponse: (f = msg.getGetSoftwareUpdateReportResponse()) && sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportResponse.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.LSAResponse}
 */
proto.logi.proto.LSAResponse.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.LSAResponse;
  return proto.logi.proto.LSAResponse.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.LSAResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.LSAResponse}
 */
proto.logi.proto.LSAResponse.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportResponse;
      reader.readMessage(value,sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportResponse.deserializeBinaryFromReader);
      msg.setGetSoftwareUpdateReportResponse(value);
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
proto.logi.proto.LSAResponse.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.LSAResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.LSAResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSAResponse.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getGetSoftwareUpdateReportResponse();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportResponse.serializeBinaryToWriter
    );
  }
};


/**
 * optional LSAGetSoftwareUpdateReportResponse get_software_update_report_response = 1;
 * @return {?proto.logi.proto.LSAGetSoftwareUpdateReportResponse}
 */
proto.logi.proto.LSAResponse.prototype.getGetSoftwareUpdateReportResponse = function() {
  return /** @type{?proto.logi.proto.LSAGetSoftwareUpdateReportResponse} */ (
    jspb.Message.getWrapperField(this, sync_agent_software_update_requests_pb.LSAGetSoftwareUpdateReportResponse, 1));
};


/** @param {?proto.logi.proto.LSAGetSoftwareUpdateReportResponse|undefined} value */
proto.logi.proto.LSAResponse.prototype.setGetSoftwareUpdateReportResponse = function(value) {
  jspb.Message.setOneofWrapperField(this, 1, proto.logi.proto.LSAResponse.oneofGroups_[0], value);
};


proto.logi.proto.LSAResponse.prototype.clearGetSoftwareUpdateReportResponse = function() {
  this.setGetSoftwareUpdateReportResponse(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LSAResponse.prototype.hasGetSoftwareUpdateReportResponse = function() {
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
proto.logi.proto.LSAEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, proto.logi.proto.LSAEvent.oneofGroups_);
};
goog.inherits(proto.logi.proto.LSAEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.LSAEvent.displayName = 'proto.logi.proto.LSAEvent';
}
/**
 * Oneof group definitions for this message. Each group defines the field
 * numbers belonging to that group. When of these fields' value is set, all
 * other fields in the group are cleared. During deserialization, if multiple
 * fields are encountered for a group, only the last value seen will be kept.
 * @private {!Array<!Array<number>>}
 * @const
 */
proto.logi.proto.LSAEvent.oneofGroups_ = [[1]];

/**
 * @enum {number}
 */
proto.logi.proto.LSAEvent.PayloadCase = {
  PAYLOAD_NOT_SET: 0,
  SOFTWARE_UPDATE_REPORT_EVENT: 1
};

/**
 * @return {proto.logi.proto.LSAEvent.PayloadCase}
 */
proto.logi.proto.LSAEvent.prototype.getPayloadCase = function() {
  return /** @type {proto.logi.proto.LSAEvent.PayloadCase} */(jspb.Message.computeOneofCase(this, proto.logi.proto.LSAEvent.oneofGroups_[0]));
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
proto.logi.proto.LSAEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.LSAEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.LSAEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSAEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    softwareUpdateReportEvent: (f = msg.getSoftwareUpdateReportEvent()) && sync_agent_software_update_events_pb.LSASoftwareUpdateReportEvent.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.LSAEvent}
 */
proto.logi.proto.LSAEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.LSAEvent;
  return proto.logi.proto.LSAEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.LSAEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.LSAEvent}
 */
proto.logi.proto.LSAEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new sync_agent_software_update_events_pb.LSASoftwareUpdateReportEvent;
      reader.readMessage(value,sync_agent_software_update_events_pb.LSASoftwareUpdateReportEvent.deserializeBinaryFromReader);
      msg.setSoftwareUpdateReportEvent(value);
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
proto.logi.proto.LSAEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.LSAEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.LSAEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSAEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSoftwareUpdateReportEvent();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      sync_agent_software_update_events_pb.LSASoftwareUpdateReportEvent.serializeBinaryToWriter
    );
  }
};


/**
 * optional LSASoftwareUpdateReportEvent software_update_report_event = 1;
 * @return {?proto.logi.proto.LSASoftwareUpdateReportEvent}
 */
proto.logi.proto.LSAEvent.prototype.getSoftwareUpdateReportEvent = function() {
  return /** @type{?proto.logi.proto.LSASoftwareUpdateReportEvent} */ (
    jspb.Message.getWrapperField(this, sync_agent_software_update_events_pb.LSASoftwareUpdateReportEvent, 1));
};


/** @param {?proto.logi.proto.LSASoftwareUpdateReportEvent|undefined} value */
proto.logi.proto.LSAEvent.prototype.setSoftwareUpdateReportEvent = function(value) {
  jspb.Message.setOneofWrapperField(this, 1, proto.logi.proto.LSAEvent.oneofGroups_[0], value);
};


proto.logi.proto.LSAEvent.prototype.clearSoftwareUpdateReportEvent = function() {
  this.setSoftwareUpdateReportEvent(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LSAEvent.prototype.hasSoftwareUpdateReportEvent = function() {
  return jspb.Message.getField(this, 1) != null;
};


goog.object.extend(exports, proto.logi.proto);
