#本实例实现了基本事件处理，包括键盘事件和鼠标事件

import sys
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget,QVBoxLayout, QApplication, QGridLayout, QLabel
from PyQt6.QtWidgets import QLCDNumber, QSlider    #LCD数字显示，滑动条

class Communicate(QObject):
    #外部 Communicate 类的属性 pyqtSignal 创建信号。
    closeApp = pyqtSignal()

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.lcd_slider()

        self.mouse_axis()

        #自定义信号 closeApp 绑定到 QMainWindow 的关闭插槽上
        self.comm = Communicate()
        self.comm.closeApp.connect(self.close)

        #递归开启鼠标追踪，包括所有子部件，不然在一些部件上面没有鼠标移动事件
        self.setMouseTracking(True)
        for w in self.findChildren(QWidget):
            w.setMouseTracking(True)

        screen = QApplication.primaryScreen().geometry()        #窗口移至屏幕中央
        x = (screen.width() - 500) // 2
        y = (screen.height() - 400) // 2
        self.setGeometry(x, y, 500, 400)
        self.setWindowTitle('Nothing')
        self.show()

    #创建一个 LCD 数字显示和一个滑动条
    def lcd_slider(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Orientation.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)

        sld.valueChanged.connect(lcd.display)      #把滑块的 valueChanged 事件和显示器 display 插槽绑定到一起

    #事件处理器的重实现
    def keyPressEvent(self, e):
        #如果用户按下了 ESC 键，就关闭窗口
        if e.key() == Qt.Key.Key_Escape:
            self.close()
    
    #事件对象
    def mouse_axis(self):
        grid = QGridLayout()

        x = 0
        y = 0

        self.text = f'x: {x}, y: {y}'

        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0,Qt.AlignmentFlag.AlignTop)

        self.setMouseTracking(True)         #开启鼠标跟踪，鼠标移动时会触发事件
        self.setLayout(grid)

    #事件对象
    def mouseMoveEvent(self, e):
        x = int(e.position().x())
        y = int(e.position().y())

        self.text = f'x: {x}, y: {y}'
        self.label.setText(self.text)

    #在窗口上点击鼠标按钮的时候，触发 closeApp 信号，程序终止
    def mousePressEvent(self, e):

        self.comm.closeApp.emit()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()