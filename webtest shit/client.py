from PySide.QtCore import *
from PySide.QtGui import *
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
import sys

QUESTIONS = 4
USERS = 1
cur_question = ""
cur_answers = 0
a = 0
b = 0
c = 0
d = 0

def publish_callback(result, status):
    pass

class MySubscribeCallback(SubscribeCallback):
    
    def __init__(self):
        pass
    
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        pass
 
    def message(self, pubnub, message):
        global a,b,c,d, cur_answers, cur_question
        if message.message[0] == False:
            if message.message[1] == 0:
                a += 1
            elif message.message[1] == 1:
                b+=1
            elif message.message[1] == 2:
                c+=1
            elif message.message[1] == 3:
                d+=1
            print(cur_question+"\na: "+str(a)+"\nb: "+str(b)+"\nc: "+str(c)+"\nd: "+str(d))
            cur_answers+=1

##def newquestion():
##    a,b,c,d = 0,0,0,0
##    cur_answers=0
##
##



        

currentChannel = "t_handler"
outputChannel = "s_handler"
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284"
pnconfig.ssl = False

pubnub = PubNub(pnconfig)

my_listener = MySubscribeCallback()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels([currentChannel,outputChannel]).execute()

#for i in range(QUESTIONS):
##    with open("question"+str(i+1)+".txt", "r") as f:
##        print("question"+str(i+1)+".txt")
##        newquestion()
##        question = f.readlines()[0].replace("[","").replace("]","")
##        cur_question = question
##        print(f.readlines())
##        answers = f.readlines()[1].replace("[","").replace("]","").split(",")

question = "how many moons are in asshole!>?"
cur_question = question
answers = ["1","2","3","hey pei pei"]
pubnub.publish().channel(outputChannel).message([True,question,answers])\
    .should_store(True).use_post(True).async(publish_callback)

            
if __name__ == '__main__':

    #Main Program
    app = QApplication(sys.argv)
    main = QDialog()
    main.show()
    sys.exit(app.exec_())



