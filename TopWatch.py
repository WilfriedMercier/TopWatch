import os
import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import os.path         as     opath

from   PyQt5.QtWidgets import QApplication, QAction, QLabel, QSizePolicy, QMainWindow, QColorDialog
from   PyQt5.QtGui     import QFont, QColor, QIcon
from   PyQt5.QtCore    import Qt, QPoint, QTimer, QDateTime


class App(QMainWindow):
    def __init__(self, *arg, **kwargs):

        super().__init__()
        self.setWindowTitle('TopWatch')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # set app icon
        scriptDir = opath.dirname(opath.realpath(__file__))
        self.setWindowIcon(QIcon(opath.join(scriptDir, 'icon.png')))

        # Add label
        self.label = QLabel('', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.color      = QColor()
        self.label.setStyleSheet('QLabel { color: #ffdd1c}')
        self.label.setFont(QFont('fixed', 30, QFont.Bold))
        self.showTime()
        
        self.setCentralWidget(self.label)
        
        # Set menu
        menubar        = self.menuBar()
        colorAction    = QAction('&Text color', self)        
        colorAction.setShortcut('Ctrl+C')
        colorAction.setStatusTip('Change text color')
        colorAction.triggered.connect(self.changeColor)
        
        self.statusBar()
        
        self.colormenu = menubar.addMenu('&Settings')
        self.colormenu.addAction(colorAction)
        
        self.timer    = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.show()
        self.setFixedSize(self.size())
        
    def changeColor(self, *args, **kwargs):
        '''Ask for a text color and change it.'''
        
        color = QColorDialog.getColor()
        self.label.setStyleSheet('QLabel { color: %s }' %color.name())
        return

    def showTime(self):
        '''Update the time label when value has changed.'''
        
        time       = QDateTime.currentDateTime()
        timeStr    = time.toString('hh:mm')
        
        if timeStr != self.label.text():
            self.label.setText(timeStr)
        return

    ############################################
    #               Mouse events               #
    ############################################

    def mousePressEvent(self, event):
        
        button = event.button()
        
        if   button == 1:
            self.oldPos = event.globalPos()
        elif button == 2:
            self.close()
        return

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        return


if __name__ == '__main__':
    root = QApplication(sys.argv)
    app  = App()
    sys.exit(root.exec_())

