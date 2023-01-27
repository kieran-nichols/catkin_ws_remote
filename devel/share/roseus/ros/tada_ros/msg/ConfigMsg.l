;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::ConfigMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'ConfigMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::CONFIGMSG")
  (make-package "TADA_ROS::CONFIGMSG"))

(in-package "ROS")
;;//! \htmlinclude ConfigMsg.msg.html


(defclass tada_ros::ConfigMsg
  :super ros::object
  :slots (_x_loc _y_loc _z_loc _angle_1 _angle_2 _angle_3 ))

(defmethod tada_ros::ConfigMsg
  (:init
   (&key
    ((:x_loc __x_loc) 0.0)
    ((:y_loc __y_loc) 0.0)
    ((:z_loc __z_loc) 0.0)
    ((:angle_1 __angle_1) 0.0)
    ((:angle_2 __angle_2) 0.0)
    ((:angle_3 __angle_3) 0.0)
    )
   (send-super :init)
   (setq _x_loc (float __x_loc))
   (setq _y_loc (float __y_loc))
   (setq _z_loc (float __z_loc))
   (setq _angle_1 (float __angle_1))
   (setq _angle_2 (float __angle_2))
   (setq _angle_3 (float __angle_3))
   self)
  (:x_loc
   (&optional __x_loc)
   (if __x_loc (setq _x_loc __x_loc)) _x_loc)
  (:y_loc
   (&optional __y_loc)
   (if __y_loc (setq _y_loc __y_loc)) _y_loc)
  (:z_loc
   (&optional __z_loc)
   (if __z_loc (setq _z_loc __z_loc)) _z_loc)
  (:angle_1
   (&optional __angle_1)
   (if __angle_1 (setq _angle_1 __angle_1)) _angle_1)
  (:angle_2
   (&optional __angle_2)
   (if __angle_2 (setq _angle_2 __angle_2)) _angle_2)
  (:angle_3
   (&optional __angle_3)
   (if __angle_3 (setq _angle_3 __angle_3)) _angle_3)
  (:serialization-length
   ()
   (+
    ;; float64 _x_loc
    8
    ;; float64 _y_loc
    8
    ;; float64 _z_loc
    8
    ;; float64 _angle_1
    8
    ;; float64 _angle_2
    8
    ;; float64 _angle_3
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x_loc
       (sys::poke _x_loc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y_loc
       (sys::poke _y_loc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z_loc
       (sys::poke _z_loc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _angle_1
       (sys::poke _angle_1 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _angle_2
       (sys::poke _angle_2 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _angle_3
       (sys::poke _angle_3 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x_loc
     (setq _x_loc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y_loc
     (setq _y_loc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z_loc
     (setq _z_loc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _angle_1
     (setq _angle_1 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _angle_2
     (setq _angle_2 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _angle_3
     (setq _angle_3 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get tada_ros::ConfigMsg :md5sum-) "9fbfd22fef180f2f17264d3d24989496")
(setf (get tada_ros::ConfigMsg :datatype-) "tada_ros/ConfigMsg")
(setf (get tada_ros::ConfigMsg :definition-)
      "float64 x_loc
float64 y_loc
float64 z_loc
float64 angle_1
float64 angle_2
float64 angle_3

")



(provide :tada_ros/ConfigMsg "9fbfd22fef180f2f17264d3d24989496")


