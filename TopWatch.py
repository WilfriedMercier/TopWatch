import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import os.path         as     opath

from   PyQt5.QtWidgets import QApplication, QAction, QLabel, QSizePolicy, QMainWindow, QColorDialog, QFontDialog
from   PyQt5.QtGui     import QFont, QColor, QIcon
from   PyQt5.QtCore    import Qt, QPoint, QTimer, QDateTime


class App(QMainWindow):
    def __init__(self, *arg, **kwargs):

        super().__init__()
        self.setWindowTitle('TopWatch')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # set app icon
        scriptDir = opath.dirname(opath.realpath(__file__))
        self.setWindowIcon(QIcon(opath.join(scriptDir, 'icon.png')))

        # Add label
        self.label = QLabel('', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.font       = QFont('fixed', 30, QFont.Bold)
        self.label.setStyleSheet('QLabel { color: #ffdd1c}')
        self.label.setFont(self.font)
        self.showTime()
        
        self.setCentralWidget(self.label)
        
        # Set menu
        menubar        = self.menuBar()
        colorAction    = QAction('&Text color', self)
        colorAction.setShortcut('Ctrl+C')
        colorAction.setStatusTip('Change text color')
        colorAction.triggered.connect(self.changeColor)

        fontAction     = QAction('&Change font', self)
        fontAction.setShortcut('Ctrl+F')
        fontAction.setStatusTip('Change text font')
        fontAction.triggered.connect(self.changeFont)
        
        self.settingmenu = menubar.addMenu('&Settings')
        self.settingmenu.addAction(colorAction)
        self.settingmenu.addAction(fontAction)

        # Start timer
        self.timer     = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.show()

        # Set dimensions relative to label dimensions
        width          = self.label.fontMetrics().width(self.label.text())+5
        height         = self.label.fontMetrics().height()+5
        self.setFixedSize(width, height)


    #############################################
    #               Miscellaneous               #
    #############################################

    def changeColor(self, *args, **kwargs):
        '''Ask for a text color and change it.'''

        color = QColorDialog.getColor()
        if color.isValid():
           self.label.setStyleSheet('QLabel { color: %s }' %color.name())
        return

    def changeFont(self, *args, **kwargs):
        '''Ask for a text style and change it.'''

        font, ok = QFontDialog.getFont()
        if ok:
           self.font = font
           self.updateFont()
        return

    def keyPressEvent(self, e, *args, **kwargs):
        if e.key() == Qt.Key_Down:
           newSize = self.font.pointSize()-1
           if newSize < 1:
               newSize = 1

           self.font.setPointSize(newSize)

        elif e.key() == Qt.Key_Up:
           self.font.setPointSize(self.font.pointSize()+1)
        else:
           return

        self.updateFont()
        return

    def updateFont(self, *args, **kwargs):
        '''Update the label font with the value given in self.font and update the window size accordingly.'''

        self.label.setFont(self.font)
        width  = self.label.fontMetrics().width(self.label.text())+2
        height = self.label.fontMetrics().height()+2
        self.setFixedSize(width, height)
        return

    def showTime(self, *args, **kwargs):
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

