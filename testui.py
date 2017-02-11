from PySide.QtCore import *
from PySide.QtGui import *
import sys

class Chat(QDialog):
    def __init__(self):
        super(Chat, self).__init__()
        
        self.setWindowTitle("Developer Console")
        self.desc = 'Chat Program'

        self.usernameLabel = QLabel('Username')
        self.usernameEdit = QLineEdit()
        self.usernameLayout = QHBoxLayout(self)
        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLayout.addWidget(self.usernameEdit)

        self.prev_text = QTextEdit("<Bald Engineers Developer Console>")
        self.prev_text.setText(self.desc)
        self.prev_text.setReadOnly(True)
        
        self.curr_text = QLineEdit()
        self.curr_text_btn = QPushButton("Enter")
        self.curr_text_btn.clicked.connect(self.enter)
        
        self.curr_text_layout = QHBoxLayout()
        self.curr_text_layout.addWidget(self.curr_text)
        self.curr_text_layout.addWidget(self.curr_text_btn)
        
        self.console_form = QFormLayout()
        self.console_form.addRow(self.usernameLayout)
        self.console_form.addRow(self.prev_text)
        self.console_form.addRow(self.curr_text_layout)
        
        self.setLayout(self.console_form)
        self.show()

    def enter(self):
        pass
        
if __name__ == '__main__':
    #Main Program
    app = QApplication(sys.argv)
    main = Chat()
    main.show()
    sys.exit(app.exec_())
