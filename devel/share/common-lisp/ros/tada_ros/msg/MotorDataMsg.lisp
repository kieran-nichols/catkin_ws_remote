; Auto-generated. Do not edit!


(cl:in-package tada_ros-msg)


;//! \htmlinclude MotorDataMsg.msg.html

(cl:defclass <MotorDataMsg> (roslisp-msg-protocol:ros-message)
  ((mode
    :reader mode
    :initarg :mode
    :type cl:integer
    :initform 0)
   (duration
    :reader duration
    :initarg :duration
    :type cl:integer
    :initform 0)
   (motor1_move
    :reader motor1_move
    :initarg :motor1_move
    :type cl:integer
    :initform 0)
   (motor2_move
    :reader motor2_move
    :initarg :motor2_move
    :type cl:integer
    :initform 0)
   (motor1_torque
    :reader motor1_torque
    :initarg :motor1_torque
    :type cl:integer
    :initform 0)
   (motor2_torque
    :reader motor2_torque
    :initarg :motor2_torque
    :type cl:integer
    :initform 0))
)

(cl:defclass MotorDataMsg (<MotorDataMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MotorDataMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MotorDataMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tada_ros-msg:<MotorDataMsg> is deprecated: use tada_ros-msg:MotorDataMsg instead.")))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <MotorDataMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:mode-val is deprecated.  Use tada_ros-msg:mode instead.")
  (mode m))

(cl:ensure-generic-function 'duration-val :lambda-list '(m))
(cl:defmethod duration-val ((m <MotorDataMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:duration-val is deprecated.  Use tada_ros-msg:duration instead.")
  (duration m))

(cl:ensure-generic-function 'motor1_move-val :lambda-list '(m))
(cl:defmethod motor1_move-val ((m <MotorDataMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:motor1_move-val is deprecated.  Use tada_ros-msg:motor1_move instead.")
  (motor1_move m))

(cl:ensure-generic-function 'motor2_move-val :lambda-list '(m))
(cl:defmethod motor2_move-val ((m <MotorDataMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:motor2_move-val is deprecated.  Use tada_ros-msg:motor2_move instead.")
  (motor2_move m))

(cl:ensure-generic-function 'motor1_torque-val :lambda-list '(m))
(cl:defmethod motor1_torque-val ((m <MotorDataMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:motor1_torque-val is deprecated.  Use tada_ros-msg:motor1_torque instead.")
  (motor1_torque m))

(cl:ensure-generic-function 'motor2_torque-val :lambda-list '(m))
(cl:defmethod motor2_torque-val ((m <MotorDataMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:motor2_torque-val is deprecated.  Use tada_ros-msg:motor2_torque instead.")
  (motor2_torque m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MotorDataMsg>) ostream)
  "Serializes a message object of type '<MotorDataMsg>"
  (cl:let* ((signed (cl:slot-value msg 'mode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'duration)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'motor1_move)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'motor2_move)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'motor1_torque)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'motor2_torque)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MotorDataMsg>) istream)
  "Deserializes a message object of type '<MotorDataMsg>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mode) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'duration) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'motor1_move) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'motor2_move) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'motor1_torque) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'motor2_torque) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MotorDataMsg>)))
  "Returns string type for a message object of type '<MotorDataMsg>"
  "tada_ros/MotorDataMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MotorDataMsg)))
  "Returns string type for a message object of type 'MotorDataMsg"
  "tada_ros/MotorDataMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MotorDataMsg>)))
  "Returns md5sum for a message object of type '<MotorDataMsg>"
  "40e9fd659c4732cd7ff0cddac935981b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MotorDataMsg)))
  "Returns md5sum for a message object of type 'MotorDataMsg"
  "40e9fd659c4732cd7ff0cddac935981b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MotorDataMsg>)))
  "Returns full string definition for message of type '<MotorDataMsg>"
  (cl:format cl:nil "int32 mode~%int32 duration~%int32 motor1_move~%int32 motor2_move~%int32 motor1_torque~%int32 motor2_torque~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MotorDataMsg)))
  "Returns full string definition for message of type 'MotorDataMsg"
  (cl:format cl:nil "int32 mode~%int32 duration~%int32 motor1_move~%int32 motor2_move~%int32 motor1_torque~%int32 motor2_torque~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MotorDataMsg>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MotorDataMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'MotorDataMsg
    (cl:cons ':mode (mode msg))
    (cl:cons ':duration (duration msg))
    (cl:cons ':motor1_move (motor1_move msg))
    (cl:cons ':motor2_move (motor2_move msg))
    (cl:cons ':motor1_torque (motor1_torque msg))
    (cl:cons ':motor2_torque (motor2_torque msg))
))
