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

class MotorListenMsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.curr_pos1 = null;
      this.curr_pos2 = null;
    }
    else {
      if (initObj.hasOwnProperty('curr_pos1')) {
        this.curr_pos1 = initObj.curr_pos1
      }
      else {
        this.curr_pos1 = 0;
      }
      if (initObj.hasOwnProperty('curr_pos2')) {
        this.curr_pos2 = initObj.curr_pos2
      }
      else {
        this.curr_pos2 = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MotorListenMsg
    // Serialize message field [curr_pos1]
    bufferOffset = _serializer.int32(obj.curr_pos1, buffer, bufferOffset);
    // Serialize message field [curr_pos2]
    bufferOffset = _serializer.int32(obj.curr_pos2, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MotorListenMsg
    let len;
    let data = new MotorListenMsg(null);
    // Deserialize message field [curr_pos1]
    data.curr_pos1 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [curr_pos2]
    data.curr_pos2 = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tada_ros/MotorListenMsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b5e8d7932558c0150376d4a17f7d0f96';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 curr_pos1
    int32 curr_pos2
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MotorListenMsg(null);
    if (msg.curr_pos1 !== undefined) {
      resolved.curr_pos1 = msg.curr_pos1;
    }
    else {
      resolved.curr_pos1 = 0
    }

    if (msg.curr_pos2 !== undefined) {
      resolved.curr_pos2 = msg.curr_pos2;
    }
    else {
      resolved.curr_pos2 = 0
    }

    return resolved;
    }
};

module.exports = MotorListenMsg;
