// Auto-generated. Do not edit!

// (in-package tada_ros.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class KillConfirmationMsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.motors_killed = null;
      this.sensors_killed = null;
    }
    else {
      if (initObj.hasOwnProperty('motors_killed')) {
        this.motors_killed = initObj.motors_killed
      }
      else {
        this.motors_killed = false;
      }
      if (initObj.hasOwnProperty('sensors_killed')) {
        this.sensors_killed = initObj.sensors_killed
      }
      else {
        this.sensors_killed = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type KillConfirmationMsg
    // Serialize message field [motors_killed]
    bufferOffset = _serializer.bool(obj.motors_killed, buffer, bufferOffset);
    // Serialize message field [sensors_killed]
    bufferOffset = _serializer.bool(obj.sensors_killed, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type KillConfirmationMsg
    let len;
    let data = new KillConfirmationMsg(null);
    // Deserialize message field [motors_killed]
    data.motors_killed = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [sensors_killed]
    data.sensors_killed = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 2;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tada_ros/KillConfirmationMsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8f0c1e581a5a8e60229fdfdefa9033aa';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool motors_killed
    bool sensors_killed
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new KillConfirmationMsg(null);
    if (msg.motors_killed !== undefined) {
      resolved.motors_killed = msg.motors_killed;
    }
    else {
      resolved.motors_killed = false
    }

    if (msg.sensors_killed !== undefined) {
      resolved.sensors_killed = msg.sensors_killed;
    }
    else {
      resolved.sensors_killed = false
    }

    return resolved;
    }
};

module.exports = KillConfirmationMsg;
