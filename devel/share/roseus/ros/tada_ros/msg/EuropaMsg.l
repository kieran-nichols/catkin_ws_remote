;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::EuropaMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'EuropaMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::EUROPAMSG")
  (make-package "TADA_ROS::EUROPAMSG"))

(in-package "ROS")
;;//! \htmlinclude EuropaMsg.msg.html


(defclass tada_ros::EuropaMsg
  :super ros::object
  :slots (_mx _my _fz _t ))

(defmethod tada_ros::EuropaMsg
  (:init
   (&key
    ((:mx __mx) 0.0)
    ((:my __my) 0.0)
    ((:fz __fz) 0.0)
    ((:t __t) 0.0)
    )
   (send-super :init)
   (setq _mx (float __mx))
   (setq _my (float __my))
   (setq _fz (float __fz))
   (setq _t (float __t))
   self)
  (:mx
   (&optional __mx)
   (if __mx (setq _mx __mx)) _mx)
  (:my
   (&optional __my)
   (if __my (setq _my __my)) _my)
  (:fz
   (&optional __fz)
   (if __fz (setq _fz __fz)) _fz)
  (:t
   (&optional __t)
   (if __t (setq _t __t)) _t)
  (:serialization-length
   ()
   (+
    ;; float64 _mx
    8
    ;; float64 _my
    8
    ;; float64 _fz
    8
    ;; float64 _t
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _mx
       (sys::poke _mx (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _my
       (sys::poke _my (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _fz
       (sys::poke _fz (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _t
       (sys::poke _t (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _mx
     (setq _mx (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _my
     (setq _my (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _fz
     (setq _fz (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _t
     (setq _t (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get tada_ros::EuropaMsg :md5sum-) "5c9da1dd517ee166f38f63eacb3ba095")
(setf (get tada_ros::EuropaMsg :datatype-) "tada_ros/EuropaMsg")
(setf (get tada_ros::EuropaMsg :definition-)
      "float64 mx
float64 my
float64 fz
float64 t

")



(provide :tada_ros/EuropaMsg "5c9da1dd517ee166f38f63eacb3ba095")


