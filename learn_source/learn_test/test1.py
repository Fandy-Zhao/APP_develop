# from PyQt6.QtCore import QDate, QTime, QDateTime, Qt

# now = QDate.currentDate()

# print(now.toString(Qt.DateFormat.ISODate))
# print(now.toString(Qt.DateFormat.RFC2822Date))

# datetime = QDateTime.currentDateTime()

# print(datetime.toString())

# time = QTime.currentTime()
# print(time.toString(Qt.DateFormat.ISODate))

import sys
from PyQt6.QtWidgets import QWidget, QToolTip,QPushButton, QApplication
from PyQt6.QtGui import QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif',10))                 #字体设置，10pt 的 SansSerif 字体

        self.setToolTip('This is a <b>QWidget</b> widget')      #设置提示信息，可以使用富文本内容

        btn = QPushButton('Button',self)                        #创建一个按钮
        btn.setToolTip('This is a <b>QPushButton</b> widget')   #
        btn.resize(btn.sizeHint())                              #设置按钮大小为推荐大小
        btn.move((250 - btn.width()) // 2,(200 - btn.height()) // 2)         #移动按钮位置

        qbtn = QPushButton('Quit', self)                        #创建一个取消按钮
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(20, 20)

        screen = QApplication.primaryScreen().geometry()        #窗口移至屏幕中央
        x = (screen.width() - 250) // 2
        y = (screen.height() - 200) // 2
        self.setGeometry(x, y, 250, 200)
        self.setWindowTitle('Tooltips')
        self.show()


def main():

    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
