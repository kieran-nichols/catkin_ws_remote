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

class UserChoiceMsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.choice = null;
      this.angle = null;
    }
    else {
      if (initObj.hasOwnProperty('choice')) {
        this.choice = initObj.choice
      }
      else {
        this.choice = 0;
      }
      if (initObj.hasOwnProperty('angle')) {
        this.angle = initObj.angle
      }
      else {
        this.angle = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type UserChoiceMsg
    // Serialize message field [choice]
    bufferOffset = _serializer.uint8(obj.choice, buffer, bufferOffset);
    // Serialize message field [angle]
    bufferOffset = _serializer.int16(obj.angle, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type UserChoiceMsg
    let len;
    let data = new UserChoiceMsg(null);
    // Deserialize message field [choice]
    data.choice = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [angle]
    data.angle = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 3;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tada_ros/UserChoiceMsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '55503f586513b642e8ca2e4716095bc8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 choice
    int16 angle
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new UserChoiceMsg(null);
    if (msg.choice !== undefined) {
      resolved.choice = msg.choice;
    }
    else {
      resolved.choice = 0
    }

    if (msg.angle !== undefined) {
      resolved.angle = msg.angle;
    }
    else {
      resolved.angle = 0
    }

    return resolved;
    }
};

module.exports = UserChoiceMsg;
