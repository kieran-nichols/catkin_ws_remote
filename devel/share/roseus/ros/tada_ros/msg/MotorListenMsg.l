;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::MotorListenMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'MotorListenMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::MOTORLISTENMSG")
  (make-package "TADA_ROS::MOTORLISTENMSG"))

(in-package "ROS")
;;//! \htmlinclude MotorListenMsg.msg.html


(defclass tada_ros::MotorListenMsg
  :super ros::object
  :slots (_curr_pos1 _curr_pos2 ))

(defmethod tada_ros::MotorListenMsg
  (:init
   (&key
    ((:curr_pos1 __curr_pos1) 0)
    ((:curr_pos2 __curr_pos2) 0)
    )
   (send-super :init)
   (setq _curr_pos1 (round __curr_pos1))
   (setq _curr_pos2 (round __curr_pos2))
   self)
  (:curr_pos1
   (&optional __curr_pos1)
   (if __curr_pos1 (setq _curr_pos1 __curr_pos1)) _curr_pos1)
  (:curr_pos2
   (&optional __curr_pos2)
   (if __curr_pos2 (setq _curr_pos2 __curr_pos2)) _curr_pos2)
  (:serialization-length
   ()
   (+
    ;; int32 _curr_pos1
    4
    ;; int32 _curr_pos2
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _curr_pos1
       (write-long _curr_pos1 s)
     ;; int32 _curr_pos2
       (write-long _curr_pos2 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _curr_pos1
     (setq _curr_pos1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _curr_pos2
     (setq _curr_pos2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tada_ros::MotorListenMsg :md5sum-) "b5e8d7932558c0150376d4a17f7d0f96")
(setf (get tada_ros::MotorListenMsg :datatype-) "tada_ros/MotorListenMsg")
(setf (get tada_ros::MotorListenMsg :definition-)
      "int32 curr_pos1
int32 curr_pos2
")



(provide :tada_ros/MotorListenMsg "b5e8d7932558c0150376d4a17f7d0f96")


