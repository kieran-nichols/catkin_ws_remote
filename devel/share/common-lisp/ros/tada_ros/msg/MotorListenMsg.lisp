; Auto-generated. Do not edit!


(cl:in-package tada_ros-msg)


;//! \htmlinclude MotorListenMsg.msg.html

(cl:defclass <MotorListenMsg> (roslisp-msg-protocol:ros-message)
  ((curr_pos1
    :reader curr_pos1
    :initarg :curr_pos1
    :type cl:integer
    :initform 0)
   (curr_pos2
    :reader curr_pos2
    :initarg :curr_pos2
    :type cl:integer
    :initform 0))
)

(cl:defclass MotorListenMsg (<MotorListenMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MotorListenMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MotorListenMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tada_ros-msg:<MotorListenMsg> is deprecated: use tada_ros-msg:MotorListenMsg instead.")))

(cl:ensure-generic-function 'curr_pos1-val :lambda-list '(m))
(cl:defmethod curr_pos1-val ((m <MotorListenMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:curr_pos1-val is deprecated.  Use tada_ros-msg:curr_pos1 instead.")
  (curr_pos1 m))

(cl:ensure-generic-function 'curr_pos2-val :lambda-list '(m))
(cl:defmethod curr_pos2-val ((m <MotorListenMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:curr_pos2-val is deprecated.  Use tada_ros-msg:curr_pos2 instead.")
  (curr_pos2 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MotorListenMsg>) ostream)
  "Serializes a message object of type '<MotorListenMsg>"
  (cl:let* ((signed (cl:slot-value msg 'curr_pos1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'curr_pos2)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MotorListenMsg>) istream)
  "Deserializes a message object of type '<MotorListenMsg>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'curr_pos1) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'curr_pos2) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MotorListenMsg>)))
  "Returns string type for a message object of type '<MotorListenMsg>"
  "tada_ros/MotorListenMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MotorListenMsg)))
  "Returns string type for a message object of type 'MotorListenMsg"
  "tada_ros/MotorListenMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MotorListenMsg>)))
  "Returns md5sum for a message object of type '<MotorListenMsg>"
  "b5e8d7932558c0150376d4a17f7d0f96")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MotorListenMsg)))
  "Returns md5sum for a message object of type 'MotorListenMsg"
  "b5e8d7932558c0150376d4a17f7d0f96")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MotorListenMsg>)))
  "Returns full string definition for message of type '<MotorListenMsg>"
  (cl:format cl:nil "int32 curr_pos1~%int32 curr_pos2~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MotorListenMsg)))
  "Returns full string definition for message of type 'MotorListenMsg"
  (cl:format cl:nil "int32 curr_pos1~%int32 curr_pos2~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MotorListenMsg>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MotorListenMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'MotorListenMsg
    (cl:cons ':curr_pos1 (curr_pos1 msg))
    (cl:cons ':curr_pos2 (curr_pos2 msg))
))
