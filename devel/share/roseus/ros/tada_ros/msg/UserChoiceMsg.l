;; Auto-generated. Do not edit!


(when (boundp 'tada_ros::UserChoiceMsg)
  (if (not (find-package "TADA_ROS"))
    (make-package "TADA_ROS"))
  (shadow 'UserChoiceMsg (find-package "TADA_ROS")))
(unless (find-package "TADA_ROS::USERCHOICEMSG")
  (make-package "TADA_ROS::USERCHOICEMSG"))

(in-package "ROS")
;;//! \htmlinclude UserChoiceMsg.msg.html


(defclass tada_ros::UserChoiceMsg
  :super ros::object
  :slots (_choice _angle ))

(defmethod tada_ros::UserChoiceMsg
  (:init
   (&key
    ((:choice __choice) 0)
    ((:angle __angle) 0)
    )
   (send-super :init)
   (setq _choice (round __choice))
   (setq _angle (round __angle))
   self)
  (:choice
   (&optional __choice)
   (if __choice (setq _choice __choice)) _choice)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:serialization-length
   ()
   (+
    ;; uint8 _choice
    1
    ;; int16 _angle
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _choice
       (write-byte _choice s)
     ;; int16 _angle
       (write-word _angle s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _choice
     (setq _choice (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int16 _angle
     (setq _angle (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get tada_ros::UserChoiceMsg :md5sum-) "55503f586513b642e8ca2e4716095bc8")
(setf (get tada_ros::UserChoiceMsg :datatype-) "tada_ros/UserChoiceMsg")
(setf (get tada_ros::UserChoiceMsg :definition-)
      "uint8 choice
int16 angle

")



(provide :tada_ros/UserChoiceMsg "55503f586513b642e8ca2e4716095bc8")


