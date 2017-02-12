from PySide.QtCore import *
from PySide.QtGui import *
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
from datetime import datetime
import threading
import sys

#from pntest import console_enter

class Chat(QDialog):
    def __init__(self):
        #pubnub
        super(Chat, self).__init__()
        self.currentChannel = "handler_1"
        self.pnconfig = PNConfiguration()
        self.pnconfig.subscribe_key = "sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe"
        self.pnconfig.publish_key = "pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284"
        self.pnconfig.ssl = False
         
        self.pubnub = PubNub(self.pnconfig)

        my_listener = MySubscribeCallback(self)
        self.pubnub.add_listener(my_listener)

        self.pubnub.subscribe().channels(self.currentChannel).execute()
        print('connected')
        
        
        
        self.setWindowTitle("Chat")
        self.desc = 'Chat Program\n'

    
        self.channelLabel = QLabel("Change Channel")
        self.channelText = QLineEdit("main_eh")
        self.channelButton = QPushButton("Go")
        self.channelButton.clicked.connect(self.changeChannel)
        self.channelLayout = QHBoxLayout()
        self.channelLayout.addWidget(self.channelLabel)
        self.channelLayout.addWidget(self.channelText)
        self.channelLayout.addWidget(self.channelButton)

        self.usernameLabel = QLabel('Username')
        self.usernameEdit = QLineEdit()
        self.usernameLayout = QHBoxLayout()
        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLayout.addWidget(self.usernameEdit)

        self.prev_text = QTextEdit()
        self.prev_text.setText(self.desc)
        self.prev_text.setReadOnly(True)
        
        self.curr_text = QLineEdit()
        self.curr_text_btn = QPushButton("Enter")
        self.curr_text_btn.clicked.connect(self.console_enter)
        
        self.curr_text_layout = QHBoxLayout()
        self.curr_text_layout.addWidget(self.curr_text)
        self.curr_text_layout.addWidget(self.curr_text_btn)
        
        self.console_form = QFormLayout()
        self.console_form.addRow(self.channelLayout)
        self.console_form.addRow(self.usernameLayout)
        self.console_form.addRow(self.prev_text)
        self.console_form.addRow(self.curr_text_layout)
    
        
        self.setLayout(self.console_form)
        self.show()
    def changeChannel(self):
        self.newChannel = str(self.channelText.text())
        self.pubnub.publish().channel(self.currentChannel).message([1,self.username,self.newChannel,self.currentChannel]).should_store(True).use_post(True).async(publish_callback)
        self.pubnub.unsubscribe().channels(self.currentChannel).execute()
        self.pubnub.subscribe().channels(self.newChannel).execute()
        self.pubnub.publish().channel(self.newChannel).message([1,self.username,self.newChannel,self.currentChannel]).should_store(True).use_post(True).async(publish_callback)
        
        self.currentChannel = self.newChannel
    
    def checkForMessage(self, message):
        if message[0] == 0:
            self.newMessageAll = message[2] + " " + message[1] + ": " + message[3]
            self.text = self.prev_text.toPlainText()
            self.prev_text.append(self.newMessageAll)
        elif message[0] == 1:
            self.prev_text.append(message[1] + " has moved from " + message[3] + " to " +message[2]+".")
        
    def console_enter(self):
        
        self.text = self.curr_text.displayText()
        self.time = str(datetime.now()).split(".")[0]
        self.username = str(self.usernameEdit.text())
        self.message  = str(self.curr_text.text())

        #self.prev_text.setText(self.prev_text.toPlainText() + '\n' + self.message)
        
        self.pubnub.publish().channel(self.currentChannel).message([0,self.username,self.time,self.message])\
            .should_store(True).use_post(True).async(publish_callback)

        self.curr_text.setText("")

##        
##        self.hear_message(result.message)

##    def hear_message(self, message):



def publish_callback(result, status):
    pass

class MySubscribeCallback(SubscribeCallback):
    def __init__(self, parent):
        self.parent = parent
    
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        pass
 
    def message(self, pubnub, message):
        self.parent.checkForMessage(message.message)
        
        
if __name__ == '__main__':



    #Main Program
    app = QApplication(sys.argv)
    main = Chat()
    main.show()
    sys.exit(app.exec_())
