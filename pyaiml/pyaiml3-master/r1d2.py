import aiml
import time
#import commands
 
k = aiml.Kernel()
 
# load the aiml file
k.learn("r1d1.aiml")
#k.learn("std-startup.xml")
 
# set a constant
k.setBotPredicate("name", "R1D1")
k.setBotPredicate("city", "Singapore")

# open the log file
logfile = open("log.txt", 'a')
#datetime = time.localtime()
logfile.write(time.strftime("%a, %d %b %Y %H:%M:%S\n"))
logfile.flush()

#k.respond("load aiml b")
#k.respond("load r1d1")

#Enter the main input/output loop.
print("exit to quit")
user = input("> ")
while(user != "exit" ):
	logfile.write("U: " +  str(user) +  "\r")
	agent = k.respond(user)
	print(agent)
	user = input("> ")
	logfile.write("B: " + str(agent) + "\r")
	logfile.flush()

logfile.write("-----------------------------------" + "\r")
logfile.close()
