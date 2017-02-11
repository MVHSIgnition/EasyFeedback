from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from datetime import datetime
from PySide.QtCore import *
from PySide.QtGui import *
import sys

if __name__ == "__main__":
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = "sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe"
    pnconfig.publish_key = "pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284"
    pnconfig.ssl = False
     
    pubnub = PubNub(pnconfig)

    my_listener = SubscribeListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels('main_eh').execute()

def publish_callback(result, status):
    pass

pubnub.publish().channel('main_eh').message(["Hello","there"])\
        .should_store(True).use_post(True).async(publish_callback)


def console_enter(self):
    self.text = self.curr_text.displayText()
    self.time = str(datetime.now()).split(".")[0]
    self.username = str(self.usernameEdit.text())
    self.message  = str(self.curr_text.text())
    
    pubnub.publish().channel('main_eh').message([self.username,self.time,self.message])\
        .should_store(True).use_post(True).async(publish_callback)

    self.curr_text.setText("")
    
