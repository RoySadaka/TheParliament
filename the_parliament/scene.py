from the_parliament.persona import Persona
from dataclasses import dataclass
from typing import List

@dataclass
class Scene:
    scenery:            str
    articulation_style: str
    topic_hint:         str
    personas:           List[Persona]