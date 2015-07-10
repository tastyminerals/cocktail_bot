#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small chatbot demo using aiml rules"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), r'pyaiml/pyaiml3-master'))
import aiml

class Chatbotty:
    def __init__(self):
        self.chatbot = aiml.Kernel()
    def get_ideas(self, aiml_file):
        self.chatbot.learn(aiml_file)
    def respond(self, user_input):
        print(self.chatbot.respond(user_input))


if __name__ == '__main__':
    bot = Chatbotty()
    bot.get_ideas(sys.argv[1])
    while True:
        i = input('>')
        print(i)
        bot.respond(i)
