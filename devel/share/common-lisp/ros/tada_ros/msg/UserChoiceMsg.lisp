; Auto-generated. Do not edit!


(cl:in-package tada_ros-msg)


;//! \htmlinclude UserChoiceMsg.msg.html

(cl:defclass <UserChoiceMsg> (roslisp-msg-protocol:ros-message)
  ((choice
    :reader choice
    :initarg :choice
    :type cl:fixnum
    :initform 0)
   (angle
    :reader angle
    :initarg :angle
    :type cl:fixnum
    :initform 0))
)

(cl:defclass UserChoiceMsg (<UserChoiceMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <UserChoiceMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'UserChoiceMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tada_ros-msg:<UserChoiceMsg> is deprecated: use tada_ros-msg:UserChoiceMsg instead.")))

(cl:ensure-generic-function 'choice-val :lambda-list '(m))
(cl:defmethod choice-val ((m <UserChoiceMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:choice-val is deprecated.  Use tada_ros-msg:choice instead.")
  (choice m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <UserChoiceMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:angle-val is deprecated.  Use tada_ros-msg:angle instead.")
  (angle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <UserChoiceMsg>) ostream)
  "Serializes a message object of type '<UserChoiceMsg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'choice)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'angle)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <UserChoiceMsg>) istream)
  "Deserializes a message object of type '<UserChoiceMsg>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'choice)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'angle) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<UserChoiceMsg>)))
  "Returns string type for a message object of type '<UserChoiceMsg>"
  "tada_ros/UserChoiceMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'UserChoiceMsg)))
  "Returns string type for a message object of type 'UserChoiceMsg"
  "tada_ros/UserChoiceMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<UserChoiceMsg>)))
  "Returns md5sum for a message object of type '<UserChoiceMsg>"
  "55503f586513b642e8ca2e4716095bc8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'UserChoiceMsg)))
  "Returns md5sum for a message object of type 'UserChoiceMsg"
  "55503f586513b642e8ca2e4716095bc8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<UserChoiceMsg>)))
  "Returns full string definition for message of type '<UserChoiceMsg>"
  (cl:format cl:nil "uint8 choice~%int16 angle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'UserChoiceMsg)))
  "Returns full string definition for message of type 'UserChoiceMsg"
  (cl:format cl:nil "uint8 choice~%int16 angle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <UserChoiceMsg>))
  (cl:+ 0
     1
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <UserChoiceMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'UserChoiceMsg
    (cl:cons ':choice (choice msg))
    (cl:cons ':angle (angle msg))
))
