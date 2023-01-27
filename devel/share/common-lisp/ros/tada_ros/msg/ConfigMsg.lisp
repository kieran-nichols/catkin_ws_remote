; Auto-generated. Do not edit!


(cl:in-package tada_ros-msg)


;//! \htmlinclude ConfigMsg.msg.html

(cl:defclass <ConfigMsg> (roslisp-msg-protocol:ros-message)
  ((x_loc
    :reader x_loc
    :initarg :x_loc
    :type cl:float
    :initform 0.0)
   (y_loc
    :reader y_loc
    :initarg :y_loc
    :type cl:float
    :initform 0.0)
   (z_loc
    :reader z_loc
    :initarg :z_loc
    :type cl:float
    :initform 0.0)
   (angle_1
    :reader angle_1
    :initarg :angle_1
    :type cl:float
    :initform 0.0)
   (angle_2
    :reader angle_2
    :initarg :angle_2
    :type cl:float
    :initform 0.0)
   (angle_3
    :reader angle_3
    :initarg :angle_3
    :type cl:float
    :initform 0.0))
)

(cl:defclass ConfigMsg (<ConfigMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ConfigMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ConfigMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tada_ros-msg:<ConfigMsg> is deprecated: use tada_ros-msg:ConfigMsg instead.")))

(cl:ensure-generic-function 'x_loc-val :lambda-list '(m))
(cl:defmethod x_loc-val ((m <ConfigMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:x_loc-val is deprecated.  Use tada_ros-msg:x_loc instead.")
  (x_loc m))

(cl:ensure-generic-function 'y_loc-val :lambda-list '(m))
(cl:defmethod y_loc-val ((m <ConfigMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:y_loc-val is deprecated.  Use tada_ros-msg:y_loc instead.")
  (y_loc m))

(cl:ensure-generic-function 'z_loc-val :lambda-list '(m))
(cl:defmethod z_loc-val ((m <ConfigMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:z_loc-val is deprecated.  Use tada_ros-msg:z_loc instead.")
  (z_loc m))

(cl:ensure-generic-function 'angle_1-val :lambda-list '(m))
(cl:defmethod angle_1-val ((m <ConfigMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:angle_1-val is deprecated.  Use tada_ros-msg:angle_1 instead.")
  (angle_1 m))

(cl:ensure-generic-function 'angle_2-val :lambda-list '(m))
(cl:defmethod angle_2-val ((m <ConfigMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:angle_2-val is deprecated.  Use tada_ros-msg:angle_2 instead.")
  (angle_2 m))

(cl:ensure-generic-function 'angle_3-val :lambda-list '(m))
(cl:defmethod angle_3-val ((m <ConfigMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:angle_3-val is deprecated.  Use tada_ros-msg:angle_3 instead.")
  (angle_3 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ConfigMsg>) ostream)
  "Serializes a message object of type '<ConfigMsg>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'x_loc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'y_loc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'z_loc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'angle_1))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'angle_2))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'angle_3))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ConfigMsg>) istream)
  "Deserializes a message object of type '<ConfigMsg>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x_loc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y_loc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'z_loc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle_1) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle_2) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle_3) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ConfigMsg>)))
  "Returns string type for a message object of type '<ConfigMsg>"
  "tada_ros/ConfigMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ConfigMsg)))
  "Returns string type for a message object of type 'ConfigMsg"
  "tada_ros/ConfigMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ConfigMsg>)))
  "Returns md5sum for a message object of type '<ConfigMsg>"
  "9fbfd22fef180f2f17264d3d24989496")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ConfigMsg)))
  "Returns md5sum for a message object of type 'ConfigMsg"
  "9fbfd22fef180f2f17264d3d24989496")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ConfigMsg>)))
  "Returns full string definition for message of type '<ConfigMsg>"
  (cl:format cl:nil "float64 x_loc~%float64 y_loc~%float64 z_loc~%float64 angle_1~%float64 angle_2~%float64 angle_3~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ConfigMsg)))
  "Returns full string definition for message of type 'ConfigMsg"
  (cl:format cl:nil "float64 x_loc~%float64 y_loc~%float64 z_loc~%float64 angle_1~%float64 angle_2~%float64 angle_3~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ConfigMsg>))
  (cl:+ 0
     8
     8
     8
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ConfigMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'ConfigMsg
    (cl:cons ':x_loc (x_loc msg))
    (cl:cons ':y_loc (y_loc msg))
    (cl:cons ':z_loc (z_loc msg))
    (cl:cons ':angle_1 (angle_1 msg))
    (cl:cons ':angle_2 (angle_2 msg))
    (cl:cons ':angle_3 (angle_3 msg))
))
