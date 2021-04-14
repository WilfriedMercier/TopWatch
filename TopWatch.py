import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import os
import os.path         as     opath

from   PyQt5.QtWidgets import QApplication, QAction, QLabel, QSizePolicy, QMainWindow, QColorDialog, QFontDialog, QPushButton, QGridLayout, QWidget, QDateTimeEdit, QDesktopWidget
from   PyQt5.QtGui     import QFont, QColor, QIcon
from   PyQt5.QtCore    import Qt, QPoint, QTimer, QDateTime

# Own imports
import setup

class App(QMainWindow):
    def __init__(self, *arg, **kwargs):
        '''
        Initialize the Application.
        '''

        super().__init__()
        self.setWindowTitle('TopWatch')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # Attribute used to know whether bliking is active or not
        self.blinkActive  = False

        # set app icon
        self.scriptDir    = opath.dirname(opath.realpath(__file__))
        self.setWindowIcon(QIcon(opath.join(self.scriptDir, 'icon.png')))

        # Setup initial color, font and window position
        configuration, ok = setup.init(self.scriptDir)
        self.color        = configuration['color']
        self.font         = QFont()
        self.font.fromString(configuration['font'])

        self.xpos         = configuration['x']
        self.ypos         = configuration['y']
        self.setGeometry(self.xpos, self.ypos, self.geometry().width(), self.geometry().height())

        # Add label
        self.label        = QLabel('', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('QLabel { color: %s}' %self.color)
        self.label.setFont(self.font)
        self.showTime()

        self.setCentralWidget(self.label)

        # Set menu
        menubar           = self.menuBar()
        colorAction       = QAction('&Text color', self)
        colorAction.setShortcut('Ctrl+C')
        colorAction.setStatusTip('Change text color')
        colorAction.triggered.connect(self.changeColor)

        fontAction        = QAction('&Change font', self)
        fontAction.setShortcut('Ctrl+F')
        fontAction.setStatusTip('Change text font')
        fontAction.triggered.connect(self.changeFont)

        resetAction       = QAction('&Reset', self)
        resetAction.setShortcut('Ctrl+Alt+R')
        resetAction.setStatusTip('Reset configuration')
        resetAction.triggered.connect(self.reset)

        saveAction        = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current configuration')
        saveAction.triggered.connect(self.save)
        
        blinkAction       = QAction('&Blink', self)
        blinkAction.setShortcut('Ctrl+b')
        blinkAction.setStatusTip('Blink configuration')
        blinkAction.triggered.connect(self.blink)

        self.filemenu     = menubar.addMenu('&File')
        self.filemenu.addAction(saveAction)
        
        self.editmenu     = menubar.addMenu('&Edit')
        self.editmenu.addAction(blinkAction)

        self.settingmenu  = menubar.addMenu('&Settings')
        self.settingmenu.addAction(colorAction)
        self.settingmenu.addAction(fontAction)
        self.settingmenu.addAction(resetAction)

        # Start timer
        self.timer        = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.show()

        # Set dimensions relative to label dimensions
        width             = self.label.fontMetrics().width(self.label.text())+5
        height            = self.label.fontMetrics().height()+5
        self.setFixedSize(width, height)


    #####################################
    #        Blink windows setup        #
    #####################################

    def blink(self, *args, **kwargs):
        '''
        Creates a window to setup blinking.
        If blinking is activated, calling this function deactivates it.
        '''
        
        if self.blinkActive:
            self.blinkActive = False
            pass
        else:
            blinkDialog = BlinkWindow(self)
            blinkDialog.show()
            self.blinkActive = True
            pass
        return
        

    #############################################
    #               Miscellaneous               #
    #############################################

    def changeColor(self, *args, **kwargs):
        '''Ask for a text color and change it.'''

        color         = QColorDialog.getColor()
        if color.isValid():
           self.color = color
           self.label.setStyleSheet('QLabel { color: %s }' %self.color.name())
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

    def reset(self, *args, **kwargs):
       '''Reset the configuration.'''

       # Reset interface
       self.color = '#ffdd1c'
       self.font.fromString('fixed,30,-1,5,75,0,0,0,0,0')
       self.label.setStyleSheet('QLabel { color: %s }' %self.color)
       self.updateFont()

       # Reset configuration file
       setup.default('settings.yaml')
       return

    def updateFont(self, *args, **kwargs):
        '''Update the label font with the value given in self.font and update the window size accordingly.'''

        self.label.setFont(self.font)
        width  = self.label.fontMetrics().width(self.label.text())+2
        height = self.label.fontMetrics().height()+2
        self.setFixedSize(width, height)
        return

    def save(self, *args, **kwargs):
        '''Save the current configuration.'''

        try:
            color = self.color.name()
        except AttributeError:
            color = self.color

        configuration = {'font' : self.font.toString(),
                         'color': color,
                         'x'    : self.x(),
                         'y'    : self.y()
                        }
        setup.writeConfiguration(opath.join(self.scriptDir, 'settings.yaml'), configuration)
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
    
    
class BlinkWindow(QMainWindow):
    def __init__(self, parent, *arg, **kwargs):
        '''
        Initialize the Window.
        '''

        super().__init__(parent)
        self.setWindowTitle('TopWatch - Setup blinking')
        self.setWindowFlags(Qt.Dialog)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.setGeometry(sizeObject.width()//2, sizeObject.height()//2, self.geometry().width(), self.geometry().height())
        
        # Time edit label
        self.teditTxt = QLabel()
        self.teditTxt.setText('Blinking frequency (hh:mm:ss)')
        
        # Time edit widget
        self.tedit    = QDateTimeEdit(self)
        self.tedit.setDisplayFormat('hh:mm:ss')
        
        # Start time edit label
        self.startTxt = QLabel()
        self.startTxt.setText('Start in (hh:mm:ss)')
        
        # Start time edit widget
        self.startedi = QDateTimeEdit(self)
        self.startedi.setDisplayFormat('hh:mm:ss')
        
        # Ok button setup
        self.okButton = QPushButton(self)
        self.okButton.setText('Ok')
        self.okButton.setToolTip("Activate blinking")
        
        # Cancel button setup
        self.cancelButton = QPushButton(self)
        self.cancelButton.setText('Cancel')
        self.cancelButton.clicked.connect(self.close)
        self.cancelButton.setToolTip("Cancel blinking setup")
        
        # Layout
        self.layout      = QGridLayout()
        
        self.layout.addWidget(self.okButton,     2, 0)
        self.layout.addWidget(self.cancelButton, 2, 1)
        
        self.layout.addWidget(self.teditTxt,     0, 0)
        self.layout.addWidget(self.tedit,        1, 0)
        
        self.layout.addWidget(self.startTxt,     0, 1)
        self.layout.addWidget(self.startedi,     1, 1)
        
        self.mainWidget   = QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)



if __name__ == '__main__':
    root   = QApplication(sys.argv)
    app    = App()
    sys.exit(root.exec_())

