#!/usr/bin/env python3
"""
Cocktail adviser chatbot.
"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), r'pyaiml/pyaiml3-master'))
import aiml
import json


class Chatbotty_helper:
    def __init__(self, path):
        self.path_to_brains = path
        self.small_brains = {}
        self._prepare_brains()
    def _prepare_brains(self):
         with open(self.path_to_brains, 'r') as jfile:
             self.small_brains = json.load(jfile)
    def sayhi(self):
        print(self.small_brains.get('sayhi'))
    def say(self, key):
        print(self.small_brains.get(key))


class Chatbotty:
    def __init__(self):
        self.chatbot = aiml.Kernel()
    def include(self, aiml_file):
        self.chatbot.learn(aiml_file)
    def entertain(self, user_input):
        print('\033[32m', self.chatbot.respond(user_input), '\033[00m')


def wake_the_bot():
    """
    This function is a bot chat session initializer.
    """
    os.chdir('brains')
    bot = Chatbotty()
    bot.include('cocktail_brains.aiml')
    helpy = Chatbotty_helper('small_brains.json')
    helpy.sayhi()
    while True:
        master = input('> ')
        bot.entertain(master)


if __name__ == '__main__':
    wake_the_bot()
