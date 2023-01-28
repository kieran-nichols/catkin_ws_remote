; Auto-generated. Do not edit!


(cl:in-package tada_ros-msg)


;//! \htmlinclude KillConfirmationMsg.msg.html

(cl:defclass <KillConfirmationMsg> (roslisp-msg-protocol:ros-message)
  ((motors_killed
    :reader motors_killed
    :initarg :motors_killed
    :type cl:boolean
    :initform cl:nil)
   (sensors_killed
    :reader sensors_killed
    :initarg :sensors_killed
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass KillConfirmationMsg (<KillConfirmationMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <KillConfirmationMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'KillConfirmationMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tada_ros-msg:<KillConfirmationMsg> is deprecated: use tada_ros-msg:KillConfirmationMsg instead.")))

(cl:ensure-generic-function 'motors_killed-val :lambda-list '(m))
(cl:defmethod motors_killed-val ((m <KillConfirmationMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:motors_killed-val is deprecated.  Use tada_ros-msg:motors_killed instead.")
  (motors_killed m))

(cl:ensure-generic-function 'sensors_killed-val :lambda-list '(m))
(cl:defmethod sensors_killed-val ((m <KillConfirmationMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tada_ros-msg:sensors_killed-val is deprecated.  Use tada_ros-msg:sensors_killed instead.")
  (sensors_killed m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <KillConfirmationMsg>) ostream)
  "Serializes a message object of type '<KillConfirmationMsg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'motors_killed) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'sensors_killed) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <KillConfirmationMsg>) istream)
  "Deserializes a message object of type '<KillConfirmationMsg>"
    (cl:setf (cl:slot-value msg 'motors_killed) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'sensors_killed) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<KillConfirmationMsg>)))
  "Returns string type for a message object of type '<KillConfirmationMsg>"
  "tada_ros/KillConfirmationMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'KillConfirmationMsg)))
  "Returns string type for a message object of type 'KillConfirmationMsg"
  "tada_ros/KillConfirmationMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<KillConfirmationMsg>)))
  "Returns md5sum for a message object of type '<KillConfirmationMsg>"
  "8f0c1e581a5a8e60229fdfdefa9033aa")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'KillConfirmationMsg)))
  "Returns md5sum for a message object of type 'KillConfirmationMsg"
  "8f0c1e581a5a8e60229fdfdefa9033aa")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<KillConfirmationMsg>)))
  "Returns full string definition for message of type '<KillConfirmationMsg>"
  (cl:format cl:nil "bool motors_killed~%bool sensors_killed~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'KillConfirmationMsg)))
  "Returns full string definition for message of type 'KillConfirmationMsg"
  (cl:format cl:nil "bool motors_killed~%bool sensors_killed~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <KillConfirmationMsg>))
  (cl:+ 0
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <KillConfirmationMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'KillConfirmationMsg
    (cl:cons ':motors_killed (motors_killed msg))
    (cl:cons ':sensors_killed (sensors_killed msg))
))
