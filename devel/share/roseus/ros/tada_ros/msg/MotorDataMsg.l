;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::MotorDataMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'MotorDataMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::MOTORDATAMSG")
  (make-package "TADA_ROS::MOTORDATAMSG"))

(in-package "ROS")
;;//! \htmlinclude MotorDataMsg.msg.html


(defclass tada_ros::MotorDataMsg
  :super ros::object
  :slots (_mode _duration _motor1_move _motor2_move _motor1_torque _motor2_torque ))

(defmethod tada_ros::MotorDataMsg
  (:init
   (&key
    ((:mode __mode) 0)
    ((:duration __duration) 0)
    ((:motor1_move __motor1_move) 0)
    ((:motor2_move __motor2_move) 0)
    ((:motor1_torque __motor1_torque) 0)
    ((:motor2_torque __motor2_torque) 0)
    )
   (send-super :init)
   (setq _mode (round __mode))
   (setq _duration (round __duration))
   (setq _motor1_move (round __motor1_move))
   (setq _motor2_move (round __motor2_move))
   (setq _motor1_torque (round __motor1_torque))
   (setq _motor2_torque (round __motor2_torque))
   self)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:duration
   (&optional __duration)
   (if __duration (setq _duration __duration)) _duration)
  (:motor1_move
   (&optional __motor1_move)
   (if __motor1_move (setq _motor1_move __motor1_move)) _motor1_move)
  (:motor2_move
   (&optional __motor2_move)
   (if __motor2_move (setq _motor2_move __motor2_move)) _motor2_move)
  (:motor1_torque
   (&optional __motor1_torque)
   (if __motor1_torque (setq _motor1_torque __motor1_torque)) _motor1_torque)
  (:motor2_torque
   (&optional __motor2_torque)
   (if __motor2_torque (setq _motor2_torque __motor2_torque)) _motor2_torque)
  (:serialization-length
   ()
   (+
    ;; int32 _mode
    4
    ;; int32 _duration
    4
    ;; int32 _motor1_move
    4
    ;; int32 _motor2_move
    4
    ;; int32 _motor1_torque
    4
    ;; int32 _motor2_torque
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _mode
       (write-long _mode s)
     ;; int32 _duration
       (write-long _duration s)
     ;; int32 _motor1_move
       (write-long _motor1_move s)
     ;; int32 _motor2_move
       (write-long _motor2_move s)
     ;; int32 _motor1_torque
       (write-long _motor1_torque s)
     ;; int32 _motor2_torque
       (write-long _motor2_torque s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _mode
     (setq _mode (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _duration
     (setq _duration (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _motor1_move
     (setq _motor1_move (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _motor2_move
     (setq _motor2_move (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _motor1_torque
     (setq _motor1_torque (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _motor2_torque
     (setq _motor2_torque (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tada_ros::MotorDataMsg :md5sum-) "40e9fd659c4732cd7ff0cddac935981b")
(setf (get tada_ros::MotorDataMsg :datatype-) "tada_ros/MotorDataMsg")
(setf (get tada_ros::MotorDataMsg :definition-)
      "int32 mode
int32 duration
int32 motor1_move
int32 motor2_move
int32 motor1_torque
int32 motor2_torque

")



(provide :tada_ros/MotorDataMsg "40e9fd659c4732cd7ff0cddac935981b")


