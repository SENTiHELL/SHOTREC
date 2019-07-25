import sys, datetime, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QAction, qApp, QMenu, QComboBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer
from src import bash, displayInfo, formats, sessions, dialog

process_name = 'SHOTREC'

app = QApplication(sys.argv)
app.setApplicationName(process_name)

for i in sys.argv:
	if i == '--version' or i == '-v':
		print('shotrec v0.1, released 14.04.2019')
		print('author SENTiHELL.com')
		sys.exit()
class Main(QWidget):
    swift = 1
    frameNumber = 0
    timeRec = 0
    defaultdir = 'tmp'

    def __init__(self):
        super(Main, self).__init__()
        self.session = sessions.session()
        load = self.session.load()


        self.setFixedSize(500,200)
        self.dirInput = QLineEdit(self)

        self.dirBtn = QPushButton(self)
        self.dirBtn.setText('...')
        self.dirBtn.clicked.connect(self.dirSel)

        self.fileBox = QHBoxLayout()
        self.fileBox.addWidget(self.dirInput)
        self.fileBox.addWidget(self.dirBtn)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name')
        self.nameInput = QLineEdit(self)
        
        # Infos config
        self.text1 = QLabel(self)
        self.text1.setText('framerate(ms)')
        self.frate = QLineEdit(self)

        self.rangeLabel = QLabel(self)
        self.rangeLabel.setText('range number')
        self.rangeInput = QLineEdit(self)
        self.rangeInput.setFixedWidth(30)

        #Controls

        self.startBtn = QPushButton(self)
        self.startBtn.setIcon(QIcon(self.path() + '/template/icon/play.svg'))
        self.startBtn.setText('start')

        self.stopBtn = QPushButton(self)
        self.stopBtn.setIcon(QIcon(self.path() + '/template/icon/stop.svg'))
        self.stopBtn.setText('stop')
        self.stopBtn.setVisible(False)

        self.pauseBtn = QPushButton(self)
        self.pauseBtn.setIcon(QIcon(self.path() + '/template/icon/pause.svg'))
        self.pauseBtn.setText('pause')
        self.pauseBtn.setVisible(False)

        self.resumeBtn = QPushButton(self)
        self.resumeBtn.setIcon(QIcon(self.path() + '/template/icon/resume.svg'))
        self.resumeBtn.setText('resume')
        self.resumeBtn.setVisible(False)

        ###########
        #EVENT BUTTON
        self.startBtn.clicked.connect(self.play)
        self.stopBtn.clicked.connect(self.stop)
        self.pauseBtn.clicked.connect(self.pause)
        self.resumeBtn.clicked.connect(self.resume)
        ###########

        self.controlBox = QHBoxLayout()
        self.controlBox.addWidget(self.startBtn)
        self.controlBox.addWidget(self.pauseBtn)
        self.controlBox.addWidget(self.resumeBtn)
        self.controlBox.addWidget(self.stopBtn)

        self.setupBox = QHBoxLayout()

        self.setupBox.addWidget(self.nameLabel)
        self.setupBox.addWidget(self.nameInput)
        self.setupBox.addStretch(1)
        self.setupBox.addWidget(self.text1)
        self.setupBox.addWidget(self.frate)

        self.setupBox.addStretch(1)
        self.setupBox.addWidget(self.rangeLabel)

        self.setupBox.addWidget(self.rangeInput)
        self.setupBox.addStretch(1)


        self.info = QLabel(self)

        self.info.setDisabled(True)


        #LIST MONITOR

        self.xList = QComboBox(self)
        self.x = displayInfo.xrandr()
        self.listConnect = self.x.listConnect()

        for item in self.listConnect:
            self.xList.addItem(item['display'])

        self.xListLabel = QLabel(self)
        self.xListLabel.setText('Монитор:')

        self.setupBox2 = QHBoxLayout()
        self.setupBox2.addStretch(1)
        self.setupBox2.addWidget(self.xListLabel)
        self.setupBox2.addWidget(self.xList)

        #LIST FORMAT

        self.fl = formats.formats(self)
        self.flbox = QHBoxLayout()
        self.flbox.addWidget(self.fl)

        self.vbox = QVBoxLayout(self)

        self.vbox.addLayout(self.fileBox)
        self.vbox.addLayout(self.setupBox)
        self.vbox.addLayout(self.setupBox2)
        self.vbox.addLayout(self.flbox)
        self.vbox.addLayout(self.controlBox)
        self.vbox.addWidget(self.info)
        self.vbox.addStretch(1)

        #self.vbox.setContentsMargins(5, 0, 0, 0)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./template/icon/play.svg'))
        self.tray_icon.activated.connect(self.show)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)




        if load:
            self.dirInput.setText(load['dir'])
            self.nameInput.setText(load['name'])
            self.frate.setText(load['rate'])
            self.rangeInput.setText(load['pad'])
            self.fl.selectFormat = load['format']
            self.fl.select(load['format'], int(load['quality']))
        else:
            self.dirInput.setText('/tmp/shotrec')
            self.nameInput.setText('frm')
            self.frate.setText('1000')
            self.rangeInput.setText('6')
 
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
	
    def path(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def inter(self):
        self.timeRec += 1

        if self.swift == 1:
            self.swift = 0
            self.tray_icon.setIcon(QIcon(self.path() + '/template/icon/rec1.svg'))
        else:
            self.swift = 1
            self.tray_icon.setIcon(QIcon(self.path() + '/template/icon/rec2.svg'))
        self.textUpdate()
    def textUpdate(self):
        time = str(datetime.timedelta(seconds=self.timeRec))
        self.info.setText('time record: '+ time + ' frames: '+ str(self.frameNumber).rjust(6, '0'))
      
    def play(self):
        if os.path.isdir(self.dirInput.text()):
            self.dialog = dialog.dialog(self)
            checkdir = self.dialog.warning('Directory not exist, create new folder?')

            if checkdir != True:
                return
            else:
                os.mkdir(str(self.dirInput.text()))

        lenFileInDir = len(os.listdir(self.dirInput.text()))
        if lenFileInDir:
            self.dialog = dialog.dialog(self)
            checkFiles = self.dialog.warning('Directory not empty, clear all files in folder(rm -rf)?')
            if checkFiles == True:
                import shutil
                shutil.rmtree(self.dirInput.text())
                os.mkdir(str(self.dirInput.text()))
            else:
                return
        self.frameNumber = self.timeRec = 0
        self.stopBtn.setVisible(True)
        self.startBtn.setVisible(False)
        self.pauseBtn.setVisible(True)

        self.nameInput.setDisabled(True)
        self.frate.setDisabled(True)
        self.rangeInput.setDisabled(True)
        self.dirInput.setDisabled(True)
        self.dirBtn.setDisabled(True)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.inter)
        self.timer.start()

        self.timelapse = QTimer()
        self.timelapse.setInterval(int(self.frate.text()))
        self.timelapse.timeout.connect(self.tl)
        self.timelapse.start()

        current = self.fl.current()
        self.session.save(str(self.dirInput.text()),
                          str(self.nameInput.text()),
                          str(self.frate.text()),
                          str(self.rangeInput.text()),
                          self.fl.selectFormat,
                          current['value']
                          )

    def tl(self):
        self.frameNumber += 1
        m = self.listConnect[self.xList.currentIndex()]

        bash.bash_apply("ffmpeg -f x11grab -s " + m['w'] + "x" + m['h'] + " -i :0.0+" + m['x'] + "," + m['y'] + " -vframes 1 " + self.fl.getFinal() +" "+ str(self.dirInput.text()) + '/' + str(
            self.nameInput.text()) + '.' + str(self.frameNumber).rjust(int(self.rangeInput.text()), '0') + '.'+self.fl.selectFormat)

    def stop(self):
        self.stopBtn.setVisible(False)
        self.startBtn.setVisible(True)
        self.pauseBtn.setVisible(False)
        self.resumeBtn.setVisible(False)

        self.nameInput.setDisabled(False)
        self.frate.setDisabled(False)
        self.rangeInput.setDisabled(False)
        self.dirInput.setDisabled(False)
        self.dirBtn.setDisabled(False)

        self.timer.stop()
        self.timelapse.stop()

    def pause(self):
        self.pauseBtn.setVisible(False)
        self.resumeBtn.setVisible(True)
        self.timer.stop()
        self.timelapse.stop()

    def resume(self):
        self.pauseBtn.setVisible(True)
        self.resumeBtn.setVisible(False)
        self.timer.start()
        self.timelapse.start()

    def dirSel(self):
        self.dirInput.setText(str(QFileDialog.getExistingDirectory()))

    def closeEvent(self, event):
        self.hide()

mainTabletApp = Main()
mainTabletApp.setWindowTitle(process_name)

path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'template/icon/shotrec.svg')

mainTabletApp.setWindowIcon(QIcon(path))
mainTabletApp.show()
sys.exit(app.exec_())
