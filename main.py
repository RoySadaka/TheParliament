import the_parliament.landing_page as landing_page
import openai
from the_parliament.scenes.casual_friends import scene
# from the_parliament.scenes.deep_learning_colleagues import scene
# from the_parliament.scenes.casual_friends_joe_rogan_crypto import scene

if __name__ == '__main__':
    openai.api_key = '#####'
    landing_page.parliament(scene)