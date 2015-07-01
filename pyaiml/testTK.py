import sys
sys.path.append('./aiml')

import aiml
k = aiml.Kernel()
k.learn('test.aiml')
while True: 
    response = k.respond(input("aiml> "))
    print(response)
