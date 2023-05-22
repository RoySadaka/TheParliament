from enum import IntEnum, auto

class AppPage(IntEnum):
    THE_TOPIC           = auto()
    TOPIC_RAISER        = auto()
    HUMAN_ASK_TALK      = auto()
    HUMAN_TALK          = auto()
    AI_TALK             = auto()
    SUMMARY             = auto()
    STOP                = auto()
