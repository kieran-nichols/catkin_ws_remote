;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::ReconDataMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'ReconDataMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::RECONDATAMSG")
  (make-package "TADA_ROS::RECONDATAMSG"))

(in-package "ROS")
;;//! \htmlinclude ReconDataMsg.msg.html


(defclass tada_ros::ReconDataMsg
  :super ros::object
  :slots (_timestamp _pos_x _pos_y _pos_z _vel_x _vel_y _vel_z _accel_x _accel_y _accel_z ))

(defmethod tada_ros::ReconDataMsg
  (:init
   (&key
    ((:timestamp __timestamp) 0.0)
    ((:pos_x __pos_x) 0.0)
    ((:pos_y __pos_y) 0.0)
    ((:pos_z __pos_z) 0.0)
    ((:vel_x __vel_x) 0.0)
    ((:vel_y __vel_y) 0.0)
    ((:vel_z __vel_z) 0.0)
    ((:accel_x __accel_x) 0.0)
    ((:accel_y __accel_y) 0.0)
    ((:accel_z __accel_z) 0.0)
    )
   (send-super :init)
   (setq _timestamp (float __timestamp))
   (setq _pos_x (float __pos_x))
   (setq _pos_y (float __pos_y))
   (setq _pos_z (float __pos_z))
   (setq _vel_x (float __vel_x))
   (setq _vel_y (float __vel_y))
   (setq _vel_z (float __vel_z))
   (setq _accel_x (float __accel_x))
   (setq _accel_y (float __accel_y))
   (setq _accel_z (float __accel_z))
   self)
  (:timestamp
   (&optional __timestamp)
   (if __timestamp (setq _timestamp __timestamp)) _timestamp)
  (:pos_x
   (&optional __pos_x)
   (if __pos_x (setq _pos_x __pos_x)) _pos_x)
  (:pos_y
   (&optional __pos_y)
   (if __pos_y (setq _pos_y __pos_y)) _pos_y)
  (:pos_z
   (&optional __pos_z)
   (if __pos_z (setq _pos_z __pos_z)) _pos_z)
  (:vel_x
   (&optional __vel_x)
   (if __vel_x (setq _vel_x __vel_x)) _vel_x)
  (:vel_y
   (&optional __vel_y)
   (if __vel_y (setq _vel_y __vel_y)) _vel_y)
  (:vel_z
   (&optional __vel_z)
   (if __vel_z (setq _vel_z __vel_z)) _vel_z)
  (:accel_x
   (&optional __accel_x)
   (if __accel_x (setq _accel_x __accel_x)) _accel_x)
  (:accel_y
   (&optional __accel_y)
   (if __accel_y (setq _accel_y __accel_y)) _accel_y)
  (:accel_z
   (&optional __accel_z)
   (if __accel_z (setq _accel_z __accel_z)) _accel_z)
  (:serialization-length
   ()
   (+
    ;; float64 _timestamp
    8
    ;; float64 _pos_x
    8
    ;; float64 _pos_y
    8
    ;; float64 _pos_z
    8
    ;; float64 _vel_x
    8
    ;; float64 _vel_y
    8
    ;; float64 _vel_z
    8
    ;; float64 _accel_x
    8
    ;; float64 _accel_y
    8
    ;; float64 _accel_z
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _timestamp
       (sys::poke _timestamp (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pos_x
       (sys::poke _pos_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pos_y
       (sys::poke _pos_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pos_z
       (sys::poke _pos_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vel_x
       (sys::poke _vel_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vel_y
       (sys::poke _vel_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vel_z
       (sys::poke _vel_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _accel_x
       (sys::poke _accel_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _accel_y
       (sys::poke _accel_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _accel_z
       (sys::poke _accel_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _timestamp
     (setq _timestamp (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pos_x
     (setq _pos_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pos_y
     (setq _pos_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pos_z
     (setq _pos_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vel_x
     (setq _vel_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vel_y
     (setq _vel_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vel_z
     (setq _vel_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _accel_x
     (setq _accel_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _accel_y
     (setq _accel_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _accel_z
     (setq _accel_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get tada_ros::ReconDataMsg :md5sum-) "6efa2547ee2ac33067aa70230a2d9b97")
(setf (get tada_ros::ReconDataMsg :datatype-) "tada_ros/ReconDataMsg")
(setf (get tada_ros::ReconDataMsg :definition-)
      "float64 timestamp
float64 pos_x
float64 pos_y
float64 pos_z
float64 vel_x
float64 vel_y
float64 vel_z
float64 accel_x
float64 accel_y
float64 accel_z

")



(provide :tada_ros/ReconDataMsg "6efa2547ee2ac33067aa70230a2d9b97")


