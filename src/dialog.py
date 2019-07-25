from PyQt5.QtWidgets import QWidget, QMessageBox

class dialog(QWidget):
    def warning(self, text):

        buttonReply = QMessageBox.question(self, 'SHOTREC WARNING', text,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            return True
