import sys
import signal
import time
signal.signal(signal.SIGINT, signal.SIG_DFL)

import os
import os.path         as     opath

from   PyQt5.QtWidgets import QApplication, QAction, QLabel, QSizePolicy, QMainWindow, QColorDialog, QFontDialog, QPushButton, QGridLayout, QWidget, QTimeEdit, QDesktopWidget, QGraphicsOpacityEffect, QDoubleSpinBox
from   PyQt5.QtGui     import QFont, QColor, QIcon
from   PyQt5.QtCore    import Qt, QPoint, QTimer, QDateTime, QTime

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

        # Hidden opacity used as a temporary slot when opacity is changed for blinking
        self._opacity     = 1

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

        self.opacity      = configuration['opacity']

        self.blinkActive  = False
        self.blinkPeriod  = configuration['blinkPeriod']
        self.blinkNb      = configuration['blinkNb']
        self.blinkFreq    = configuration['blinkFreq']

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
        blinkAction.triggered.connect(self.blinkWindow)

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

        # Blink timer
        self.blinktimer  = QTimer()
        self.blinktimer.timeout.connect(self.run_blink)

        # Small timer used to make the text flicker rapidly
        self.smalltimer = QTimer()
        self.smalltimer.timeout.connect(self.blink_text)

        self.op = QGraphicsOpacityEffect(self)
        self.op.setOpacity(self.opacity)
        self.label.setGraphicsEffect(self.op)
        self.setAutoFillBackground(True)

        self.show()

        # Set dimensions relative to label dimensions
        width             = self.label.fontMetrics().width(self.label.text())+5
        height            = self.label.fontMetrics().height()+5
        self.setFixedSize(width, height)


    #####################################
    #        Blink windows setup        #
    #####################################

    def blinkWindow(self, *args, **kwargs):
        '''
        Creates a window to setup blinking.
        If blinking is activated, calling this function deactivates it.
        '''

        if self.blinkActive:
            # Reset to default values and show back the clock
            self.blinkActive = False

            # Stop timers
            self.smalltimer.stop()
            self.blinktimer.stop()

            # Resume previous opacity
            self.opacity     = self._opacity
            self.setLabelOpacity(self.opacity)
        else:
            blinkDialog      = BlinkWindow(self)
            blinkDialog.show()

        return

    def blink_text(self, *args, **kwargs):
        '''Function used to make the text blink a given number of times.'''

        self.cnt += 1
        self.setLabelOpacity(1-self.opacity)

        # Blink 9 times for now and then stop small timer
        if self.cnt == self.blinkNb:
            self.setLabelOpacity(0)
            self.smalltimer.stop()

        return

    def run_blink(self, *args, **kwargs):
        '''Function called ever time the text must be blinked.'''

        # Counter used to know when to stop the flickering
        self.cnt         = 0
        self.smalltimer.start(100)
        return

    def start_blink(self, blinkfreq, period, nb, *args, **kwargs):
        '''
        Starts blinking of the clock.

        :param float blinkfreq: number of ms between blinks
        :param QTimeEdit period: time between two blink phases
        :param int nb: number of blinks per blink phase
        '''

        if not isinstance(blinkfreq, (int, float)):
            raise TypeError('Blinking frequency must be an int but is given as a %s' %type(blinkfreq))
        else:
            blinkfreq    = int(blinkfreq)

        if blinkfreq <= 0:
            raise ValueError('Blinking frequency must be positive only (current value is %f)' %blinkfreq)

        if not isinstance(nb, (int, float)):
            raise TypeError('Number of blinks must be int but is given as a %s' %type(nb))
        else:
            nb           = int(nb)

        if nb <= 0:
            raise ValueError('Number of blinks must be positive only (current value is %d)' %nb)

        # Store values if the user save the current configuration later on
        self.blinkActive = True
        self.blinkNb     = nb
        self.blinkFreq   = blinkfreq # in ms
        self.blinkPeriod = period

        # Period between blinking phases in ms
        period_ms        = sum([int(i)*60**pos for pos, i in enumerate(self.blinkPeriod.toString().split(':')[::-1])]) * 1000

        # Save opacity for when we go back to normal
        self._opacity    = self.opacity
        self.setLabelOpacity(0)

        self.blinktimer.start(period_ms)
        return


    #############################################
    #               Miscellaneous               #
    #############################################
    
    def setLabelOpacity(self, value, *args, **kwargs):
        '''Set the opacity of the label.'''
        
        if value > 1:
            value = 1
        elif value < 0:
            value = 0
            
        self.opacity = value
        self.op.setOpacity(self.opacity)
        return

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
        ''''Actions taken when a key is pressed.'''
        
        # Deal with shift key being pressed first
        if e.modifiers() & Qt.ShiftModifier:
            if e.key() == Qt.Key_Up:
                self.setLabelOpacity(self.opacity+0.05)
            elif e.key() == Qt.Key_Down:
                self.setLabelOpacity(self.opacity-0.05)
        else:
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

        # Try to save color with its name if it exists, otherwise use color code
        try:
            color     = self.color.name()
        except AttributeError:
            color     = self.color

        # Convert blinking period from Qt Qtimer to string
        period_str    = self.blinkPeriod.toString()

        configuration = {'font'        : self.font.toString(),
                         'color'       : color,
                         'x'           : self.x(),
                         'y'           : self.y(),
                         'opacity'     : round(self.opacity, 2),
                         'blinkPeriod' : period_str,
                         'blinkFreq'   : int(self.blinkFreq),
                         'blinkNb'     : int(self.blinkNb)
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
        self.parent    = parent

        self.setWindowTitle('TopWatch - Setup blinking')
        self.setWindowFlags(Qt.Dialog)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.setGeometry(sizeObject.width()//2, sizeObject.height()//2, self.geometry().width(), self.geometry().height())

        # Time edit label
        self.teditTxt = QLabel()
        self.teditTxt.setText('Period (hh:mm:ss)')

        # Time edit widget
        self.tedit    = QTimeEdit(self)
        self.tedit.setDisplayFormat('hh:mm:ss')
        self.tedit.setTime(self.parent.blinkPeriod)

        # Duration edit label
        self.lenTxt   = QLabel()
        self.lenTxt.setText('Duration (ms)')

        # Duration edit widget
        self.lenedit  = QDoubleSpinBox(self)
        self.lenedit.setDecimals(0)
        self.lenedit.setMaximum(10000)
        self.lenedit.setMinimum(50)
        self.lenedit.setValue(self.parent.blinkFreq)

        # Blink number edit label
        self.blnbTxt  = QLabel()
        self.blnbTxt.setText('Blink number')

        # Blink number edit widget
        self.blnbedit = QDoubleSpinBox(self)
        self.blnbedit.setValue(self.parent.blinkNb)
        self.blnbedit.setDecimals(0)
        self.blnbedit.setMinimum(1)

        # Ok button setup
        self.okButton = QPushButton(self)
        self.okButton.setText('Ok')
        self.okButton.clicked.connect(self.ok)
        self.okButton.setToolTip("Activate blinking")

        # Cancel button setup
        self.cancelButton = QPushButton(self)
        self.cancelButton.setText('Cancel')
        self.cancelButton.clicked.connect(self.cancel)
        self.cancelButton.setToolTip("Cancel blinking setup")

        # Layout
        self.layout      = QGridLayout()

        self.layout.addWidget(self.teditTxt,     0, 0)
        self.layout.addWidget(self.tedit,        1, 0)

        self.layout.addWidget(self.lenTxt,       2, 0)
        self.layout.addWidget(self.lenedit,      3, 0)

        self.layout.addWidget(self.blnbTxt,      2, 1)
        self.layout.addWidget(self.blnbedit,     3, 1)

        self.layout.addWidget(self.okButton,     4, 0)
        self.layout.addWidget(self.cancelButton, 4, 1)

        self.mainWidget   = QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)


    ###############################
    #           Methods           #
    ###############################

    def cancel(self, *args, **kwargs):
        '''When cancel is pressed blinking parameters are updated it the user wants to save later on.'''

        self.parent.blinkNb     = self.blnbedit.value()
        self.parent.blinkPeriod = self.tedit.time()
        self.parent.blinkFreq   = self.lenedit.value()
        self.close()
        return

    def keyPressEvent(self, e, *args, **kwargs):
        '''Actions taken when a key is pressed.'''

        if e.key() == Qt.Key_Escape:
           self.cancel(*args, **kwargs)
        elif e.key() == Qt.Key_Return:
            self.ok(*args, **kwargs)
        return

    def ok(self, *args, **kwargs):
        '''Start blinking when ok is pressed.'''

        self.parent.start_blink(self.lenedit.value(), self.tedit.time(), self.blnbedit.value())
        self.close()
        return



if __name__ == '__main__':
    root   = QApplication(sys.argv)
    app    = App()
    sys.exit(root.exec_())

