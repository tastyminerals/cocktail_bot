#!/usr/bin/env python3
"""
Small chatbot demo using aiml rules
"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), r'pyaiml/pyaiml3-master'))
import aiml
import json

class Chatbotty_helper:
    def __init__(self, path):
        self.path_to_brains = path
        self._prepare_brains()
    def _prepare_brains(self):
        with open(self.path_to_brains, 'r') as jfile:
            brains = json.load(jfile)
        print(brains)

class Chatbotty:
    def __init__(self):
        self.chatbot = aiml.Kernel()
    def include(self, aiml_file):
        self.chatbot.learn(aiml_file)
    def entertain(self, user_input):
        print(self.chatbot.respond(user_input))


def wake_the_bot():
    """
    This function is a bot chat session initializer.
    """
    bot = Chatbotty()
    bot.include('cocktail_brains.aiml')
    help_bot = Chatbotty_helper('small_brains.json')
    
    while True:
        master = input('>')
        print(master)        
        bot.entertain(master)
    

if __name__ == '__main__':
    wake_the_bot()
