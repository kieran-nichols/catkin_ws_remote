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

class ConfigMsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x_loc = null;
      this.y_loc = null;
      this.z_loc = null;
      this.angle_1 = null;
      this.angle_2 = null;
      this.angle_3 = null;
    }
    else {
      if (initObj.hasOwnProperty('x_loc')) {
        this.x_loc = initObj.x_loc
      }
      else {
        this.x_loc = 0.0;
      }
      if (initObj.hasOwnProperty('y_loc')) {
        this.y_loc = initObj.y_loc
      }
      else {
        this.y_loc = 0.0;
      }
      if (initObj.hasOwnProperty('z_loc')) {
        this.z_loc = initObj.z_loc
      }
      else {
        this.z_loc = 0.0;
      }
      if (initObj.hasOwnProperty('angle_1')) {
        this.angle_1 = initObj.angle_1
      }
      else {
        this.angle_1 = 0.0;
      }
      if (initObj.hasOwnProperty('angle_2')) {
        this.angle_2 = initObj.angle_2
      }
      else {
        this.angle_2 = 0.0;
      }
      if (initObj.hasOwnProperty('angle_3')) {
        this.angle_3 = initObj.angle_3
      }
      else {
        this.angle_3 = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ConfigMsg
    // Serialize message field [x_loc]
    bufferOffset = _serializer.float64(obj.x_loc, buffer, bufferOffset);
    // Serialize message field [y_loc]
    bufferOffset = _serializer.float64(obj.y_loc, buffer, bufferOffset);
    // Serialize message field [z_loc]
    bufferOffset = _serializer.float64(obj.z_loc, buffer, bufferOffset);
    // Serialize message field [angle_1]
    bufferOffset = _serializer.float64(obj.angle_1, buffer, bufferOffset);
    // Serialize message field [angle_2]
    bufferOffset = _serializer.float64(obj.angle_2, buffer, bufferOffset);
    // Serialize message field [angle_3]
    bufferOffset = _serializer.float64(obj.angle_3, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ConfigMsg
    let len;
    let data = new ConfigMsg(null);
    // Deserialize message field [x_loc]
    data.x_loc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y_loc]
    data.y_loc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [z_loc]
    data.z_loc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [angle_1]
    data.angle_1 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [angle_2]
    data.angle_2 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [angle_3]
    data.angle_3 = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 48;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tada_ros/ConfigMsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9fbfd22fef180f2f17264d3d24989496';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 x_loc
    float64 y_loc
    float64 z_loc
    float64 angle_1
    float64 angle_2
    float64 angle_3
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ConfigMsg(null);
    if (msg.x_loc !== undefined) {
      resolved.x_loc = msg.x_loc;
    }
    else {
      resolved.x_loc = 0.0
    }

    if (msg.y_loc !== undefined) {
      resolved.y_loc = msg.y_loc;
    }
    else {
      resolved.y_loc = 0.0
    }

    if (msg.z_loc !== undefined) {
      resolved.z_loc = msg.z_loc;
    }
    else {
      resolved.z_loc = 0.0
    }

    if (msg.angle_1 !== undefined) {
      resolved.angle_1 = msg.angle_1;
    }
    else {
      resolved.angle_1 = 0.0
    }

    if (msg.angle_2 !== undefined) {
      resolved.angle_2 = msg.angle_2;
    }
    else {
      resolved.angle_2 = 0.0
    }

    if (msg.angle_3 !== undefined) {
      resolved.angle_3 = msg.angle_3;
    }
    else {
      resolved.angle_3 = 0.0
    }

    return resolved;
    }
};

module.exports = ConfigMsg;
