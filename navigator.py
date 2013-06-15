'''
Created on 14/giu/2013

@author: ben
'''

from PyQt4 import QtGui

import sys
import os

import converter

class Navigator(QtGui.QWidget):

    def __init__(self):
        super(Navigator, self).__init__()

        self._init_gui()

    def _init_gui(self):
        self.resize(400, 70)
        self.center()
        self.setWindowTitle("Media Converter")
        self.setFixedHeight(70)

        # Setting up the layout
        self.pedit = QtGui.QLineEdit(os.getcwd())

        obutt = QtGui.QPushButton("Path")
        obutt.clicked.connect(self.openPathDialog)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.pedit)
        hbox1.addWidget(obutt)

        cbutt = QtGui.QPushButton("Convert")
        cbutt.clicked.connect(self.convertFiles)

        self.fcomb = QtGui.QComboBox(self)
        self.fcomb.addItem(".mp3")
        self.fcomb.addItem(".aac")

        self.bcomb = QtGui.QComboBox(self)
        self.bcomb.addItem("192k")
        self.bcomb.addItem("160k")

        self.scomb = QtGui.QComboBox(self)
        self.scomb.addItem("44100")
        self.scomb.addItem("48000")

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(cbutt)
        hbox2.addWidget(self.fcomb)
        hbox2.addWidget(self.bcomb)
        hbox2.addWidget(self.scomb)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        self.show()

    def openPathDialog(self):
        if os.path.isdir(self.pedit.text()):
            directory = self.pedit.text()
        else:
            directory = os.path.dirname(self.pedit.text())
        file_path = QtGui.QFileDialog.getOpenFileName(parent = self, caption = "Bene", \
                                                      directory = directory, \
                                                      filter = "Video (*.flv *.mp4)")
        self.pedit.setText(file_path)

    def convertFiles(self):
        conv = converter.Converter(default_sampling = str(self.scomb.currentText()), \
                                   default_bitrate = str(self.bcomb.currentText()), \
                                   default_format = str(self.fcomb.currentText()) )
        conv.convert(file_name = str(self.pedit.text()))

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    nav = Navigator()
    sys.exit(app.exec_())

