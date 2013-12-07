import colourer
import sys
from PySide import QtGui

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
	self.col = colourer.Colourer('_')
        self.setWindowTitle("Word Filter")
	self.setGeometry(300, 300, 350, 250)

	self.label = QtGui.QLabel(self)
        self.label.move(60, 40)

        self.field = QtGui.QLineEdit(self)
        self.field.move(60, 100)
        self.field.textChanged[str].connect(self.onChanged)

	self.show()

    def onChanged(self, text):
        self.label.setText(self.col.wordFilter(text))
        self.label.adjustSize()


def main():
    app = QtGui.QApplication(sys.argv)
    col = colourer.Colourer()
    main_win = MainWindow()
    sys.exit(app.exec_())

main()
