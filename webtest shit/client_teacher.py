from PySide.QtCore import *
from PySide.QtGui import *
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
from datetime import datetime
import sys

TEACHER = 0
QUESTION = 1
ANSWERS = 2

class MySubscribeCallback(SubscribeCallback):
    def __init__(self):
        pass
    
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        pass
 
    def message(self, pubnub, message):
        if message.message[TEACHER]:
            print(message.message[QUESTION])
            for i, m in enumerate(message.message[ANSWERS]):
                print(i, ":", m)
            response = int(input("0,1,2,3 (index of answer)"))
            pubnub.publish().channel(outputChannel).message([False, response])\
                .should_store(True).use_post(True).async(publish_callback)

def publish_callback(result, status):
    pass

currentChannel = "s_handler"
outputChannel = "t_handler"

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284"
pnconfig.ssl = False
         
pubnub = PubNub(pnconfig)

my_listener = MySubscribeCallback()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels([currentChannel, outputChannel]).execute()

print('connected')

##with open("test.txt", "r") as f:

l = ["what is 2 + 2?", ["1", "2", "3", "4"]]

if __name__ == '__main__':

    #Main Program
    app = QApplication(sys.argv)
    main = QDialog()
    main.show()
    sys.exit(app.exec_())



    
