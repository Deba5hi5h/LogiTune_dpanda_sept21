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

var sync_agent_software_update_structures_pb = require('./sync_agent_software_update_structures_pb.js');
goog.exportSymbol('proto.logi.proto.LSASoftwareUpdateReportEvent', null, global);

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
proto.logi.proto.LSASoftwareUpdateReportEvent = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.logi.proto.LSASoftwareUpdateReportEvent, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.logi.proto.LSASoftwareUpdateReportEvent.displayName = 'proto.logi.proto.LSASoftwareUpdateReportEvent';
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
proto.logi.proto.LSASoftwareUpdateReportEvent.prototype.toObject = function(opt_includeInstance) {
  return proto.logi.proto.LSASoftwareUpdateReportEvent.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.logi.proto.LSASoftwareUpdateReportEvent} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSASoftwareUpdateReportEvent.toObject = function(includeInstance, msg) {
  var f, obj = {
    report: (f = msg.getReport()) && sync_agent_software_update_structures_pb.LSASoftwareUpdateReport.toObject(includeInstance, f)
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
 * @return {!proto.logi.proto.LSASoftwareUpdateReportEvent}
 */
proto.logi.proto.LSASoftwareUpdateReportEvent.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.logi.proto.LSASoftwareUpdateReportEvent;
  return proto.logi.proto.LSASoftwareUpdateReportEvent.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.logi.proto.LSASoftwareUpdateReportEvent} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.logi.proto.LSASoftwareUpdateReportEvent}
 */
proto.logi.proto.LSASoftwareUpdateReportEvent.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new sync_agent_software_update_structures_pb.LSASoftwareUpdateReport;
      reader.readMessage(value,sync_agent_software_update_structures_pb.LSASoftwareUpdateReport.deserializeBinaryFromReader);
      msg.setReport(value);
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
proto.logi.proto.LSASoftwareUpdateReportEvent.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.logi.proto.LSASoftwareUpdateReportEvent.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.logi.proto.LSASoftwareUpdateReportEvent} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.logi.proto.LSASoftwareUpdateReportEvent.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getReport();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      sync_agent_software_update_structures_pb.LSASoftwareUpdateReport.serializeBinaryToWriter
    );
  }
};


/**
 * optional LSASoftwareUpdateReport report = 1;
 * @return {?proto.logi.proto.LSASoftwareUpdateReport}
 */
proto.logi.proto.LSASoftwareUpdateReportEvent.prototype.getReport = function() {
  return /** @type{?proto.logi.proto.LSASoftwareUpdateReport} */ (
    jspb.Message.getWrapperField(this, sync_agent_software_update_structures_pb.LSASoftwareUpdateReport, 1));
};


/** @param {?proto.logi.proto.LSASoftwareUpdateReport|undefined} value */
proto.logi.proto.LSASoftwareUpdateReportEvent.prototype.setReport = function(value) {
  jspb.Message.setWrapperField(this, 1, value);
};


proto.logi.proto.LSASoftwareUpdateReportEvent.prototype.clearReport = function() {
  this.setReport(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.logi.proto.LSASoftwareUpdateReportEvent.prototype.hasReport = function() {
  return jspb.Message.getField(this, 1) != null;
};


goog.object.extend(exports, proto.logi.proto);