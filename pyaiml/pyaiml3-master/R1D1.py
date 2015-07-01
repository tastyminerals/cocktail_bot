import aiml
#import commands
 
k = aiml.Kernel()
 
# load the aiml file
k.learn("r1d1.aiml")
#k.learn("std-startup.xml")
 
# set a constant
k.setBotPredicate("name", "R1D1")
k.setBotPredicate("city", "Singapore")

#k.respond("load aiml b")
#k.respond("load r1d1")

# Enter the main input/output loop.
print("\nINTERACTIVE MODE (ctrl-c to exit)")
while(True):
	print(k.respond(input("> ")))
