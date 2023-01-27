#!/usr/bin/env python

# Constants
grav = 9.81;
dt = 0.01;

# Thresholds
gyro_threshold_velocity = 0.8;
gyro_threshold_orientation = 0.55;
accel_threshold = 0.8;
low_motion_count_threshold = 10;
nonlow_motion_count_threshold = 5;
