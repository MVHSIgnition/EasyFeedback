import sys
from PySide.QtCore import QSize, Qt
from PySide.QtGui import *
from PySide.QtWebKit import *
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
from datetime import datetime
import threading
import sys

html = \
"""<html>
<head>
<title>Python Web Plugin Test</title>
</head>

<body>
<h1>Python Web Plugin Test</h1>
<object type="x-pyqt/widget" width="200" height="200"></object>
<p>This is a Web plugin written in Python.</p>
</body>
</html>
"""

class Chat(QDialog):
    def __init__(self):
        #pubnub
        super(Chat, self).__init__()
        self.pnconfig = PNConfiguration()
        self.pnconfig.subscribe_key = "sub-c-d785fd74-f08e-11e6-9283-02ee2ddab7fe"
        self.pnconfig.publish_key = "pub-c-afbd56e9-6341-4a07-b493-cbb3ebf25284"
        self.pnconfig.ssl = False
         
        self.pubnub = PubNub(self.pnconfig)

        my_listener = MySubscribeCallback(self)
        self.pubnub.add_listener(my_listener)

        self.pubnub.subscribe().channels('main_eh').execute()
        print('connected')
        
        
        
        self.setWindowTitle("Chat")
        self.desc = 'Chat Program\n'

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
        self.console_form.addRow(self.usernameLayout)
        self.console_form.addRow(self.prev_text)
        self.console_form.addRow(self.curr_text_layout)
        
        self.setLayout(self.console_form)
        self.show()
    
    def checkForMessage(self, message):
        self.newMessageAll = message[1] + " " + message[0] + ": " + message[2]
        self.text = self.prev_text.toPlainText()
        self.prev_text.append(self.newMessageAll)
        
    def console_enter(self):
        
        self.text = self.curr_text.displayText()
        self.time = str(datetime.now()).split(".")[0]
        self.username = str(self.usernameEdit.text())
        self.message  = str(self.curr_text.text())

        #self.prev_text.setText(self.prev_text.toPlainText() + '\n' + self.message)
        
        self.pubnub.publish().channel('main_eh').message([self.username,self.time,self.message])\
            .should_store(True).use_post(True).async(publish_callback)

        self.curr_text.setText("")


class WebPluginFactory(QWebPluginFactory):

    def __init__(self, parent = None):
        QWebPluginFactory.__init__(self, parent)
    
    def create(self, mimeType, url, names, values):
        if mimeType == "x-pyqt/widget":
            return Chat()
    
    def plugins(self):
        plugin = QWebPluginFactory.Plugin()
        plugin.name = "PyQt Widget"
        plugin.description = "An example Web plugin written with PyQt."
        mimeType = QWebPluginFactory.MimeType()
        mimeType.name = "x-pyqt/widget"
        mimeType.description = "PyQt widget"
        mimeType.fileExtensions = []
        plugin.mimeTypes = [mimeType]
        print("plugins")
        return [plugin]
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
if __name__ == "__main__":

    app = QApplication(sys.argv)
    QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)
    view = QWebView()
    factory = WebPluginFactory()
    view.page().setPluginFactory(factory)
    view.setHtml(html)
    view.show()
    sys.exit(app.exec_())
