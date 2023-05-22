from typing import Dict, List
from the_parliament.response import Response
from the_parliament.scene import Scene


class Metadata:
    scene:Scene                     = None
    system_role:str                 = None
    topic: str                      = None
    topic_raiser: str               = None
    name_to_color: Dict[str,str]    = None
    conversation: List[Response]    = list()
    summary: str                    = None
    names: List[str]                = list()
    ai_names: List[str]             = list()