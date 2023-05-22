from dataclasses import dataclass
import json

@dataclass
class Response:
    speaker: str
    text: str

    def to_json(self):
        return json.dumps({'speaker':self.speaker, 'text':self.text})
    
    @staticmethod
    def from_json(json_str):
        obj = json.loads(json_str)
        return Response(speaker=obj['speaker'], text=obj['text'])