;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::KillConfirmationMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'KillConfirmationMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::KILLCONFIRMATIONMSG")
  (make-package "TADA_ROS::KILLCONFIRMATIONMSG"))

(in-package "ROS")
;;//! \htmlinclude KillConfirmationMsg.msg.html


(defclass tada_ros::KillConfirmationMsg
  :super ros::object
  :slots (_motors_killed _sensors_killed ))

(defmethod tada_ros::KillConfirmationMsg
  (:init
   (&key
    ((:motors_killed __motors_killed) nil)
    ((:sensors_killed __sensors_killed) nil)
    )
   (send-super :init)
   (setq _motors_killed __motors_killed)
   (setq _sensors_killed __sensors_killed)
   self)
  (:motors_killed
   (&optional (__motors_killed :null))
   (if (not (eq __motors_killed :null)) (setq _motors_killed __motors_killed)) _motors_killed)
  (:sensors_killed
   (&optional (__sensors_killed :null))
   (if (not (eq __sensors_killed :null)) (setq _sensors_killed __sensors_killed)) _sensors_killed)
  (:serialization-length
   ()
   (+
    ;; bool _motors_killed
    1
    ;; bool _sensors_killed
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _motors_killed
       (if _motors_killed (write-byte -1 s) (write-byte 0 s))
     ;; bool _sensors_killed
       (if _sensors_killed (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _motors_killed
     (setq _motors_killed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _sensors_killed
     (setq _sensors_killed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get tada_ros::KillConfirmationMsg :md5sum-) "8f0c1e581a5a8e60229fdfdefa9033aa")
(setf (get tada_ros::KillConfirmationMsg :datatype-) "tada_ros/KillConfirmationMsg")
(setf (get tada_ros::KillConfirmationMsg :definition-)
      "bool motors_killed
bool sensors_killed

")



(provide :tada_ros/KillConfirmationMsg "8f0c1e581a5a8e60229fdfdefa9033aa")


