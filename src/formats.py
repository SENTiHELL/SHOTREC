from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QSizePolicy
from PyQt5.QtCore import Qt
import math

class formats(QWidget):

    conf = {
        'png': {
            'min': 1,
            'max': 100,
            'default': 5,
            'good': 'max',
            'var': '-qscale:v',
            'value': 100
        },
        'jpg': {
            'min': 2,
            'max': 31,
            'default': 5,
            'good': 'min',
            'var': '-qscale:v',
            'value': 2
        }
    }

    selectFormat = 'png'

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)
        self.parent = parent

        self.initUI()

    def initUI(self):

        self.mbox = QHBoxLayout(self)
        i = 0
        self.row = []

        self.mbox.setContentsMargins(0,0,0,0)

        for item in self.conf:
            #Set default

            self.conf[item]['value'] = self.conf[item]['default']


            frame = QWidget(self)
            vbox = QVBoxLayout(frame)
            hbox = QHBoxLayout()

            comb = QComboBox(self)

            for form_text in self.conf:
                comb.addItem(form_text)

            sld = QSlider(Qt.Horizontal, self)

            text = QLabel(self)

            text.setFixedSize(45, 28)

            text.setText(item)


            hbox.addWidget(comb)
            hbox.addWidget(sld)
            hbox.addWidget(text)

            vbox.addLayout(hbox)
            vbox.setContentsMargins(0,0,0,0)
            comb.raise_()
            frame.hide()

            self.row.append([item, frame])
            comb.activated.connect(self.ComboEvent)
            sld.valueChanged.connect(self.changeSld)
            self.change(sld)


            i = i + 1

        self.selectFormat = self.row[0][0]
        self.row[0][1].show()

        for it in self.row:
            if it[0] == self.selectFormat:
                it[1].children()[1].setValue(self.conf[self.selectFormat]['value'])
            self.mbox.addWidget(it[1])

    def ComboEvent(self):
        for item in self.row:
            item[1].hide()
            if item[0] == self.sender().currentText():
                item[1].show()
                item[1].children()[3].setCurrentText(item[0])
                self.selectFormat = item[0]

    def changeSld(self):
        self.change(self.sender())

    def change(self, obj):
        text = obj.parent().children()[2]
        val = obj.value()

        text.setText(str(val))

        conf = self.conf[self.selectFormat]

        cmax = conf['max'] - conf['min']

        def perc(val):
            return math.ceil(cmax / 100 * val) + conf['min']



        if conf['good'] == 'max':
            max = conf['max']
            min = conf['min']
        elif conf['good'] == 'min':
            max = conf['min']
            min = conf['max']

        def color(v, t=0):
            v = v
            red = [33,100,5]
            green = [133,90,30]

            if t == 1:
                red, green = green, red

            min = [math.ceil((red[0] - green[0]) / 100 * v),
                   math.ceil((red[1] - green[1]) / 100 * v),
                   math.ceil((red[2] - green[2]) / 100 * v)]
            res = [red[0] - min[0],
                   red[1] - min[1],
                   red[2] - min[2]]
            return str(res[0])+', '+str(res[1])+', '+str(res[2])

        if min < max:
            text.setStyleSheet("""
                color: rgb(""" + color(val, 1) + """)
            """)

            if val > 50:
                text.setText(str(perc(val)) + ' HQ')
            else:
                text.setText(str(perc(val)) + ' LQ')
        elif min > max:
            text.setStyleSheet("""
                color: rgb(""" + color(val, 0) + """)
            """)

            if val < 50:
                text.setText(str(perc(val)) + ' HQ')
            else:
                text.setText(str(perc(val)) + ' LQ')
        self.conf[self.selectFormat]['value'] = perc(val)

    def current(self):
        return self.conf[self.selectFormat]
    def select(self, format, value):
        for item in self.row:
            item[1].hide()
            if item[0] == format:
                item[1].show()
                item[1].children()[3].setCurrentText(item[0])

                conf = self.conf[format]
                cmax = conf['max'] - conf['min']
                koef = 100/cmax
                item[1].children()[1].setValue((koef*value) - (koef*conf['min']))
                self.selectFormat = item[0]

    def getFinal(self):
        conf = self.conf[self.selectFormat]
        cmax = conf['max'] - conf['min']

        def perc(val):
            return math.ceil(cmax / 100 * val) + conf['min']

        for it in self.row:
            if it[0] == self.selectFormat:
                return conf['var'] +' '+ str(perc(it[1].children()[1].value()))
