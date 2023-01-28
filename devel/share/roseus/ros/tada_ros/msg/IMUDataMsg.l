;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::IMUDataMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'IMUDataMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::IMUDATAMSG")
  (make-package "TADA_ROS::IMUDATAMSG"))

(in-package "ROS")
;;//! \htmlinclude IMUDataMsg.msg.html


(defclass tada_ros::IMUDataMsg
  :super ros::object
  :slots (_accel_x _accel_y _accel_z _gyro_x _gyro_y _gyro_z _state _swing_time ))

(defmethod tada_ros::IMUDataMsg
  (:init
   (&key
    ((:accel_x __accel_x) 0.0)
    ((:accel_y __accel_y) 0.0)
    ((:accel_z __accel_z) 0.0)
    ((:gyro_x __gyro_x) 0.0)
    ((:gyro_y __gyro_y) 0.0)
    ((:gyro_z __gyro_z) 0.0)
    ((:state __state) 0.0)
    ((:swing_time __swing_time) 0.0)
    )
   (send-super :init)
   (setq _accel_x (float __accel_x))
   (setq _accel_y (float __accel_y))
   (setq _accel_z (float __accel_z))
   (setq _gyro_x (float __gyro_x))
   (setq _gyro_y (float __gyro_y))
   (setq _gyro_z (float __gyro_z))
   (setq _state (float __state))
   (setq _swing_time (float __swing_time))
   self)
  (:accel_x
   (&optional __accel_x)
   (if __accel_x (setq _accel_x __accel_x)) _accel_x)
  (:accel_y
   (&optional __accel_y)
   (if __accel_y (setq _accel_y __accel_y)) _accel_y)
  (:accel_z
   (&optional __accel_z)
   (if __accel_z (setq _accel_z __accel_z)) _accel_z)
  (:gyro_x
   (&optional __gyro_x)
   (if __gyro_x (setq _gyro_x __gyro_x)) _gyro_x)
  (:gyro_y
   (&optional __gyro_y)
   (if __gyro_y (setq _gyro_y __gyro_y)) _gyro_y)
  (:gyro_z
   (&optional __gyro_z)
   (if __gyro_z (setq _gyro_z __gyro_z)) _gyro_z)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:swing_time
   (&optional __swing_time)
   (if __swing_time (setq _swing_time __swing_time)) _swing_time)
  (:serialization-length
   ()
   (+
    ;; float64 _accel_x
    8
    ;; float64 _accel_y
    8
    ;; float64 _accel_z
    8
    ;; float64 _gyro_x
    8
    ;; float64 _gyro_y
    8
    ;; float64 _gyro_z
    8
    ;; float64 _state
    8
    ;; float64 _swing_time
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _accel_x
       (sys::poke _accel_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _accel_y
       (sys::poke _accel_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _accel_z
       (sys::poke _accel_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _gyro_x
       (sys::poke _gyro_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _gyro_y
       (sys::poke _gyro_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _gyro_z
       (sys::poke _gyro_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _state
       (sys::poke _state (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _swing_time
       (sys::poke _swing_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _accel_x
     (setq _accel_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _accel_y
     (setq _accel_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _accel_z
     (setq _accel_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _gyro_x
     (setq _gyro_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _gyro_y
     (setq _gyro_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _gyro_z
     (setq _gyro_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _state
     (setq _state (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _swing_time
     (setq _swing_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get tada_ros::IMUDataMsg :md5sum-) "0ebe3b0305f6c75def5f0d35a26d8b2f")
(setf (get tada_ros::IMUDataMsg :datatype-) "tada_ros/IMUDataMsg")
(setf (get tada_ros::IMUDataMsg :definition-)
      "float64 accel_x
float64 accel_y
float64 accel_z
float64 gyro_x
float64 gyro_y
float64 gyro_z
float64 state
float64 swing_time

")



(provide :tada_ros/IMUDataMsg "0ebe3b0305f6c75def5f0d35a26d8b2f")


