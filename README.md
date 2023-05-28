# 🎙️ The Parliament 🎙️
### Rest assured we're all certified experts here 😉
<img src="https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/the_parliament/the_parliament.jpeg"  width="400" height="400">

Engage in AI-powered group conversations on various subjects, assuming different personas and locations.

``The Parliament`` name inspired by the Israeli series (הפרלמנט).

![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/roysadaka.svg?style=social&label=roysadaka)](https://twitter.com/roysadaka)


# The Parliament - AI Conversational Project

The Parliament is a Gradio-powered AI conversational project based on OpenAI's ChatGPT. It simulates a casual conversation between AI and human participants, with AI-driven chatbots taking on different personas in a conversation.

The conversation takes place in a set scene, and users can interact with the AI chatbot through text inputs. The AI chatbot then responds based on the personas, scenery, and subject presented.

## Dependencies

To run the project, first make sure you have installed:

- Python 3.6 or newer
- OpenAI Python library `openai`
- Gradio `gradio`
- If you are on a Mac, the following additional dependencies are required:
  - Rust: `brew install rust`
  - Xcode: `xcode-select --install`

## Usage - run main.py

```python
import the_parliament.landing_page as landing_page
import openai
from the_parliament.scenes.casual_friends import scene
# from the_parliament.scenes.deep_learning_colleagues import scene
# from the_parliament.scenes.casual_friends_joe_rogan_crypto import scene

if __name__ == '__main__':
    openai.api_key = 'your_openai_api_key'
    landing_page.parliament(scene)
```

Please substitute `your_openai_api_key` with your own OpenAI API key. You have the option to comment or uncomment various scene imports in order to switch between scenes, or even create a new scene instance that best suits your requirements.


To begin, execute the command python main.py to initiate the Gradio web application with the specified scene.  
This action will generate URLs resembling the following examples:
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://50c0be910a804096fe.gradio.live
```
To launch the parliament app, open the local URL in your web browser,  
You may also use the public URL for devices outside your network.

## Example Scenes

### Casual Friends

```python
from the_parliament.persona import Persona
from the_parliament.scene import Scene

scene = Scene(
    scenery = 'At a local coffee shop.',
    articulation_style = 'The group is made up of close friends, so formalities are not necessary.',
    topic_hint='Is pineapple an acceptable pizza topping, or a crime against humanity?',
    personas = [
        # Add your Personas here
        ]
)
```

### Deep Learning Colleagues

```python
from the_parliament.persona import Persona
from the_parliament.scene import Scene

scene = Scene(
    scenery = 'At a conference on deep learning.',
    articulation_style = 'The group is made up of colleagues, so a mix of casual and formal speech is appropriate.',
    topic_hint='Discuss the benefits and drawbacks of using deep learning in various industries.',
    personas = [
        # Add your Personas here
        ]
)
```

### Joe Rogan podcast

```python
from the_parliament.persona import Persona
from the_parliament.scene import Scene

scene = Scene(
    scenery = 'At Joe Rogan podcast.',
    articulation_style = 'The Joe Rogan podcast has a conversational and engaging articulation style, featuring open and unfiltered discussions on various topics with active listening and probing questions',
    topic_hint='Satoshi might be alive, what if he sells?',
    personas = [
        # Add your Personas here
        ]
)
```