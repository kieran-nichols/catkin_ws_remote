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

class MotorDataMsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.mode = null;
      this.duration = null;
      this.motor1_move = null;
      this.motor2_move = null;
      this.motor1_torque = null;
      this.motor2_torque = null;
    }
    else {
      if (initObj.hasOwnProperty('mode')) {
        this.mode = initObj.mode
      }
      else {
        this.mode = 0;
      }
      if (initObj.hasOwnProperty('duration')) {
        this.duration = initObj.duration
      }
      else {
        this.duration = 0;
      }
      if (initObj.hasOwnProperty('motor1_move')) {
        this.motor1_move = initObj.motor1_move
      }
      else {
        this.motor1_move = 0;
      }
      if (initObj.hasOwnProperty('motor2_move')) {
        this.motor2_move = initObj.motor2_move
      }
      else {
        this.motor2_move = 0;
      }
      if (initObj.hasOwnProperty('motor1_torque')) {
        this.motor1_torque = initObj.motor1_torque
      }
      else {
        this.motor1_torque = 0;
      }
      if (initObj.hasOwnProperty('motor2_torque')) {
        this.motor2_torque = initObj.motor2_torque
      }
      else {
        this.motor2_torque = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MotorDataMsg
    // Serialize message field [mode]
    bufferOffset = _serializer.int32(obj.mode, buffer, bufferOffset);
    // Serialize message field [duration]
    bufferOffset = _serializer.int32(obj.duration, buffer, bufferOffset);
    // Serialize message field [motor1_move]
    bufferOffset = _serializer.int32(obj.motor1_move, buffer, bufferOffset);
    // Serialize message field [motor2_move]
    bufferOffset = _serializer.int32(obj.motor2_move, buffer, bufferOffset);
    // Serialize message field [motor1_torque]
    bufferOffset = _serializer.int32(obj.motor1_torque, buffer, bufferOffset);
    // Serialize message field [motor2_torque]
    bufferOffset = _serializer.int32(obj.motor2_torque, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MotorDataMsg
    let len;
    let data = new MotorDataMsg(null);
    // Deserialize message field [mode]
    data.mode = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [duration]
    data.duration = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [motor1_move]
    data.motor1_move = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [motor2_move]
    data.motor2_move = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [motor1_torque]
    data.motor1_torque = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [motor2_torque]
    data.motor2_torque = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tada_ros/MotorDataMsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '40e9fd659c4732cd7ff0cddac935981b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 mode
    int32 duration
    int32 motor1_move
    int32 motor2_move
    int32 motor1_torque
    int32 motor2_torque
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MotorDataMsg(null);
    if (msg.mode !== undefined) {
      resolved.mode = msg.mode;
    }
    else {
      resolved.mode = 0
    }

    if (msg.duration !== undefined) {
      resolved.duration = msg.duration;
    }
    else {
      resolved.duration = 0
    }

    if (msg.motor1_move !== undefined) {
      resolved.motor1_move = msg.motor1_move;
    }
    else {
      resolved.motor1_move = 0
    }

    if (msg.motor2_move !== undefined) {
      resolved.motor2_move = msg.motor2_move;
    }
    else {
      resolved.motor2_move = 0
    }

    if (msg.motor1_torque !== undefined) {
      resolved.motor1_torque = msg.motor1_torque;
    }
    else {
      resolved.motor1_torque = 0
    }

    if (msg.motor2_torque !== undefined) {
      resolved.motor2_torque = msg.motor2_torque;
    }
    else {
      resolved.motor2_torque = 0
    }

    return resolved;
    }
};

module.exports = MotorDataMsg;
