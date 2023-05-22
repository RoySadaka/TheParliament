from dataclasses import dataclass

@dataclass
class Persona:
    is_ai:                  bool    # True for LLM, False for human
    name:                   str     # the person's name
    age:                    str     # the person's age
    gender:                 str     # the person's gender
    occupation:             str     # the person's profession or job
    interests:              str     # the person's hobbies or interests
    personality_traits:     str     # the person's personality traits such as introverted, extroverted, responsible, creative, emotional etc.
    education:              str     # the person's level of education
    relationship_status:    str     # the person's current relationship status
    nationality:            str     # the person's nationality or country of origin
    residency:              str     # the person's legal status of residing in a particular country
    income:                 str     # the person's income level or salary
    general_description:    str     # any description

    def to_text(self):
        user_defined_prop_to_value = {k: v for k, v in self.__dict__.items() if not k.startswith('__') and not callable(v)}
        parts = [f'{user_defined_prop}: {value}' for user_defined_prop, value in user_defined_prop_to_value.items() if value is not None]
        return "```\n" + '\n'.join(parts) + "\n```"