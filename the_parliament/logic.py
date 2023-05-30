import uuid
import openai
from the_parliament.app import app
from the_parliament.config import Config
from the_parliament.response import Response
from typing import Optional


def query_chat_gpt(messages):
    result = openai.ChatCompletion.create(model=Config.CHAT_GPT_MODEL_NAME, messages=messages, temperature=Config.CHAT_GPT_TEMPERATURE)
    result = result['choices'][0]['message']['content'].strip()
    return result

def get_conversation_as_text():
    return '```\n' + '\n```\n'.join([m.to_json() for m in app.metadata.conversation]) + '\n```'

def query_with_retry() -> Optional[Response]:
    ai_speakers = {persona.name for persona in app.metadata.scene.personas if persona.is_ai}
    admin_guide = get_admin_guide()

    messages = [{"role": "system", "content": app.metadata.system_role}]
    messages.append({"role": "user", "content": get_conversation_as_text() + admin_guide})


    for i in range(Config.MAX_PARSE_RETRY):
        raw_response = None
        try:
            raw_response = query_chat_gpt(messages)
            parsed_response = parse_raw_response(raw_response)
            assert parsed_response.speaker in ai_speakers
            app.metadata.conversation.append(parsed_response)
            return
        except:
            if i == Config.MAX_PARSE_RETRY-1:
                raise '[panic error ⛔] - existing'

def get_system_role() -> str:
    personas_str = '\n---\n'.join([persona.to_text() for persona in app.metadata.scene.personas])

    system_role = f"""Your task is to simulate human conversation.

---
    
Scenery:
{app.metadata.scene.scenery}

---

The personality descriptions:
{personas_str}

---

Expected articulation style:
{app.metadata.scene.articulation_style}

---

At each step, you will choose who speaks next and what they say.
A Response may address specific participants in the conversation.
A Response don't always have to ask questions, it may express opinions and ideas.
A Response may contradict the opinions of others and offer counterclaims.
A Response should be brief and appropriate for a casual human like conversation.
A Response should reflect the unique perspective, characteristics, and style of the chosen persona.
The conversation should be realistic in both content and delivery.
The topic should be explored from every angle and detail, even after conclusions have been made.

---

At each step of the conversation, you will need to output your response in a specific JSON format:
{{
    "speaker": <string, representing the name of the next speaker>
    "text": <string, represents the response, can also be null if you have nothing to say>
}}

The objective is to generate a smooth and captivating dialogue that closely mimics a human conversation, taking into account the personas participating and their unique perspectives.
Therefore, it is crucial to articulate the dialogue in a manner consistent with how humans naturally speak.

You may occasionally receive Admin Response as guidance, but it is not part of the conversation.
"""
    return system_role

def parse_raw_response(text: str) -> Response:
    start_index = text.find('{')
    end_index = text.find('}') + 1
    extracted_json = text[start_index:end_index]
    response = Response.from_json(extracted_json)
    return response

def conclude() -> str:
    system_role = f"""Your objective is to condense the final outcome of a discussion among humans. 
Focus on the most important information and disregard any irrelevant details.
"""

    conversation_description = f"""The following is a discussion among humans.
Their names:
{', '.join([name for name in app.metadata.names[:-1]]) + ' and ' + app.metadata.names[-1]}
The scenery description:
{app.metadata.scene.scenery}
"""
    conversation_text = get_conversation_as_text()
    messages = [{"role": "system", "content": system_role},
                         {"role": "user", "content": conversation_description + conversation_text}]
    conclusion = query_chat_gpt(messages).replace('. ', '.\n')
    return f'<h1>Summary</h1><h2>{conclusion}</h2>'

def log():
    system_role = """Your task is to recommend a brief file name for the provided text.
Use underscores instead of spaces and add ".txt" at the end."""

    messages = [{"role": "system", "content": system_role},
                {"role": "user", "content": app.metadata.summary}]
    
    conversation_text = get_conversation_as_text()
    identifier = str(uuid.uuid4())
    if app.metadata.summary is not None:
        file_name = query_chat_gpt(messages).replace('.txt', f'__{identifier}.txt')
    else:
        file_name = f'{identifier}.txt'
    text_file = open(f"{Config.LOG_DIR}{file_name}", "w")
    summary = f'\n\n[SUMMARY]\n\n{app.metadata.summary}'
    text_file.write(f'[SYSTEM]\n\n{app.metadata.system_role}\n\n[CONVERSATION]\n\n{conversation_text}{summary}')
    text_file.close()

def get_admin_guide() -> str:
    names_limitation = f"Your next speaker will be: {app.metadata.ai_names[0]}." if len(app.metadata.ai_names) == 1 \
                        else f"Please select the most suitable speaker from the limited options of [{', '.join(app.metadata.ai_names)}] to continue speaking."
    
    admin_template = f"""Continue to engage in conversation and provide a response in the form of a single JSON that represents your simulated human reply.
{names_limitation}
"""
    admin_guide = Response(speaker='Admin', text=admin_template)
    admin_guide = f'\n\n---\n\n```\n{admin_guide.to_json()}\n```'
    return admin_guide
    
def get_gr_chatbot_history() -> list:
    messages = []
    is_pair = True
    for msg in app.metadata.conversation:
        text = f'{app.metadata.name_to_color[msg.speaker]} {msg.speaker}:\n{msg.text}'
        if is_pair:
            messages.append([text])
        else:
            messages[-1].append(text)
        is_pair = not is_pair
    
    if not is_pair:
        messages[-1].append("")

    return messages

def get_header() -> str:
    names = ', '.join([name for name in app.metadata.names[:-1]]) + ' and ' + app.metadata.names[-1]

    header = f"""<h1><center>☕️ THE PARLIAMENT ☕️</center></h1>
<h3><center>{names} {app.metadata.scene.scenery}<br/>Rest assured we're all certified experts here 😉</center></h3>

---
"""
    return header
