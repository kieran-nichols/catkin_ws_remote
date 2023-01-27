#!/usr/bin/env python
from enum import Enum

class UserChoiceEnum(Enum):
    PLANTARFLEXION = 1
    DORSIFLEXION = 2
    INVERSION = 3
    EVERSION = 4
    CHOOSE_ANGLE = 5
    AUTOHOME = 6
    KILL = 7
    SWEEP = 8
    TEST_GYRO = 9
    CURRENT_CONFIG = 10
    DEBUG = 11
