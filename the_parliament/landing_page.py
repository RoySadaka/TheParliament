import gradio as gr
from the_parliament.app import app
from the_parliament.app_page import AppPage
from the_parliament.config import Config
import the_parliament.logic as lo
from the_parliament.response import Response
from the_parliament.scene import Scene


def get_next_step_ui_elements(next_step: AppPage):
    next_step_ui_elements = {e: gr.update(visible=False) for e in app.gr_elements}

    if next_step == AppPage.THE_TOPIC:
        next_step_ui_elements[app.gr_textbox_topic]    = gr.update(visible=True)
        next_step_ui_elements[app.gr_btn_topic_submit] = gr.update(visible=True)

    elif next_step == AppPage.TOPIC_RAISER:
        next_step_ui_elements[app.gr_markdown_who_raised_topic]    = gr.update(visible=True)
        next_step_ui_elements[app.gr_row_topic_raiser]             = gr.update(visible=True)

    elif next_step == AppPage.HUMAN_ASK_TALK:
        next_step_ui_elements[app.gr_chatbot]                          = gr.update(value=lo.get_gr_chatbot_history(), visible=True)
        next_step_ui_elements[app.gr_markdown_would_you_like_to_talk]  = gr.update(visible=True)
        next_step_ui_elements[app.gr_row_would_you_like_to_talk]       = gr.update(visible=True)
    
    elif next_step == AppPage.HUMAN_TALK:
        next_step_ui_elements[app.gr_chatbot]              = gr.update(value=lo.get_gr_chatbot_history(), visible=True)
        next_step_ui_elements[app.gr_textbox_human_input]  = gr.update(visible=True, interactive=True, value="")
        next_step_ui_elements[app.gr_btn_human_input_send] = gr.update(visible=True)
    
    elif next_step == AppPage.AI_TALK:
        next_step_ui_elements[app.gr_chatbot]                  = gr.update(value=lo.get_gr_chatbot_history(), visible=True)
        next_step_ui_elements[app.gr_markdown_should_continue] = gr.update(visible=True)
        next_step_ui_elements[app.gr_row_should_continue]      = gr.update(visible=True)
    
    elif next_step == AppPage.SUMMARY:
        next_step_ui_elements[app.gr_chatbot]                  = gr.update(value=lo.get_gr_chatbot_history(), visible=True)
        next_step_ui_elements[app.gr_markdown_summary]         = gr.update(value=app.metadata.summary, visible=True)

    elif next_step == AppPage.STOP:
        next_step_ui_elements[app.gr_chatbot]                  = gr.update(value=lo.get_gr_chatbot_history(), visible=True)

    return next_step_ui_elements

def continue_chat():
    available_human_speakers = [persona.name for persona in app.metadata.scene.personas if not persona.is_ai and persona.name != app.metadata.conversation[-1].speaker]
    if len(available_human_speakers) == 0:
        lo.query_with_retry()
        return get_next_step_ui_elements(AppPage.AI_TALK)
    else:
        return get_next_step_ui_elements(AppPage.HUMAN_ASK_TALK)

def topic_raiser_handler(name):
    if app.metadata.topic_raiser is None:
        app.metadata.topic_raiser = name
        app.metadata.conversation.append(Response(speaker=app.metadata.topic_raiser, text=app.metadata.topic))
    return continue_chat()

def raw_topic_handler(raw_topic):
    if len(raw_topic) == 0:
        return get_next_step_ui_elements(AppPage.THE_TOPIC)
    app.metadata.topic = app.gr_textbox_topic.label + raw_topic
    return get_next_step_ui_elements(AppPage.TOPIC_RAISER)

def should_human_talk_handler(label):
    if label == 'Yes':
        return get_next_step_ui_elements(AppPage.HUMAN_TALK)
    elif label == "No":
        lo.query_with_retry()
        return get_next_step_ui_elements(AppPage.AI_TALK)

def should_continue_handler(label):
    if label == "Continue":
        return continue_chat()
    elif label == "Summary":
        app.metadata.summary = lo.conclude()
        lo.log()
        return get_next_step_ui_elements(AppPage.SUMMARY)
    elif label == "Stop":
        lo.log()
        return get_next_step_ui_elements(AppPage.STOP)

def human_input_handler(input_text):
    human_speaker = [persona.name for persona in app.metadata.scene.personas if not persona.is_ai][0]
    app.metadata.conversation.append(Response(speaker=human_speaker, text=input_text))
    return get_next_step_ui_elements(AppPage.AI_TALK)

def initialize(scene:Scene):
    app.metadata.scene = scene
    app.metadata.names = [persona.name for persona in app.metadata.scene.personas]
    app.metadata.ai_names = [persona.name for persona in app.metadata.scene.personas if persona.is_ai]
    assert len(app.metadata.names) <= Config.MAX_PARTICIPANTS, f'Parliament works best with 2-{Config.MAX_PARTICIPANTS} participants, got {len(app.metadata.names)}'
    assert sum([1 for persona in app.metadata.scene.personas if not persona.is_ai]) <= 1, 'Only 1 human speaker supported'
    app.metadata.name_to_color = {name:Config.CHAT_COLORS[idx] for idx, name in enumerate(app.metadata.names)} 
    app.topic_prompt = "Let's discuss the following topic: "
    app.metadata.system_role = lo.get_system_role()
    app.gr_elements = []

# for mac, to install gradio, i had to:
# brew install rust
# xcode-select --install
# pip install gradio

def parliament(scene:Scene):
    initialize(scene)

    # HEADER
    header = gr.Markdown(lo.get_header())

    # CHAT
    app.gr_chatbot = gr.Chatbot(visible=False)
    app.gr_elements.append(app.gr_chatbot)

    # HUMAN INPUT
    app.gr_textbox_human_input = gr.Textbox(label="Your input", placeholder='Say something',lines=2, visible=False)
    app.gr_elements.append(app.gr_textbox_human_input)
    app.gr_btn_human_input_send = gr.Button(value="Send", visible=False)
    app.gr_elements.append(app.gr_btn_human_input_send)

    # WOULD YOU LIKE TO TALK
    app.gr_markdown_would_you_like_to_talk = gr.Markdown("""<h3>Would you like to talk?</h3>""", visible=False)
    app.gr_elements.append(app.gr_markdown_would_you_like_to_talk)
    app.gr_row_would_you_like_to_talk = gr.Row(visible=False)
    app.gr_elements.append(app.gr_row_would_you_like_to_talk)

    # TOPIC RAISER
    app.gr_markdown_who_raised_topic = gr.Markdown("""<h3>Who raises the topic?</h3>""", visible=False)
    app.gr_elements.append(app.gr_markdown_who_raised_topic)
    app.gr_row_topic_raiser = gr.Row(visible=False)
    app.gr_elements.append(app.gr_row_topic_raiser)

    # SHOULD CONTINUE
    app.gr_markdown_should_continue = gr.Markdown("""<h3>Continue?</h3>""", visible=False)
    app.gr_elements.append(app.gr_markdown_should_continue)
    app.gr_row_should_continue = gr.Row(visible=False)
    app.gr_elements.append(app.gr_row_should_continue)

    # TOPIC
    app.gr_textbox_topic = gr.Textbox(label=app.topic_prompt, placeholder=app.metadata.scene.topic_hint,lines=2) # 2 for multiline
    app.gr_elements.append(app.gr_textbox_topic)
    app.gr_btn_topic_submit = gr.Button(value="Wing it!")
    app.gr_elements.append(app.gr_btn_topic_submit)

    # SUMMARY
    app.gr_markdown_summary = gr.Markdown(value='', visible=False)
    app.gr_elements.append(app.gr_markdown_summary)


    with gr.Blocks() as demo:
        header.render()
        app.gr_chatbot.render()
        app.gr_textbox_human_input.render()
        app.gr_btn_human_input_send.render()
        app.gr_btn_human_input_send.click(human_input_handler, inputs=app.gr_textbox_human_input, outputs=app.gr_elements)

        app.gr_markdown_would_you_like_to_talk.render() 
        app.gr_row_would_you_like_to_talk.render()
        with app.gr_row_would_you_like_to_talk:
            for label in ["Yes", "No"]:
                btn = gr.Button(value=label)
                btn.click(should_human_talk_handler, inputs=btn, outputs=app.gr_elements)
        

        app.gr_markdown_who_raised_topic.render()
        app.gr_row_topic_raiser.render()
        with app.gr_row_topic_raiser:
            for name in app.metadata.names:
                btn_name = gr.Button(value=name)
                btn_name.click(topic_raiser_handler, inputs=btn_name, outputs=app.gr_elements)


        app.gr_textbox_topic.render() 
        app.gr_btn_topic_submit.render() 
        app.gr_btn_topic_submit.click(raw_topic_handler, inputs=app.gr_textbox_topic, outputs=app.gr_elements)


        app.gr_markdown_should_continue.render()
        app.gr_row_should_continue.render()
        with app.gr_row_should_continue:
            for label in ["Continue", "Summary", "Stop"]:
                btn = gr.Button(value=label)
                btn.click(should_continue_handler, inputs=btn, outputs=app.gr_elements)   

        app.gr_markdown_summary.render()

    demo.launch(share=True, show_api=False)
