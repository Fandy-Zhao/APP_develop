#本代码事例，包含菜单，工具栏，布局管理的实现

import sys
from PyQt6.QtWidgets import QWidget, QToolTip,QPushButton, QMessageBox, QMenu, QApplication
from PyQt6.QtWidgets import QMainWindow #状态栏
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout#布局管理
from PyQt6.QtGui import QFont, QIcon, QAction


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif',10))                 #字体设置，10pt 的 SansSerif 字体

        self.setToolTip('This is a <b>QWidget</b> widget')      #设置提示信息，可以使用富文本内容

        self.buffer_create()                                    #按钮创建

        self.q_buf_create()                                     #退出按键创建                                   

        self.statusBar().showMessage('Ready')                   #状态栏

        self.menu_create()                                      #菜单创建

        #self.layout()                                           #布局管理
        self.grid_layout()                                      #网格布局管理 


        screen = QApplication.primaryScreen().geometry()        #窗口移至屏幕中央
        x = (screen.width() - 500) // 2
        y = (screen.height() - 400) // 2
        self.setGeometry(x, y, 500, 400)
        self.setWindowTitle('Tooltips')
        self.show()

    #创建一个按钮
    def buffer_create(self):
        btn = QPushButton('Button',self)                        #创建一个按钮
        btn.setToolTip('This is a <b>QPushButton</b> widget')   #
        btn.resize(btn.sizeHint())                              #设置按钮大小为推荐大小
        btn.move((250 - btn.width()) // 2,(200 - btn.height()) // 2)         #移动按钮位置

    #退出按键创建
    def q_buf_create(self):
        qbtn = QPushButton('Quit', self)                        #创建一个取消按钮
        qbtn.clicked.connect(QApplication.instance().quit)      #连接按钮的点击信号到应用程序的退出槽
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(20, 20)

    #创建了有一个菜单的菜单栏(包含菜单，子菜单，勾选菜单)
    #有一个问题，在碰到菜单时，状态栏的内容就会消失
    def menu_create(self):
        menubar = self.menuBar()                                #menuBar 方法创建了一个菜单栏
        fileMenu = menubar.addMenu('&File')                     #addMenu 创建一个文件菜单

        #创建了一个带有特定图标和 ‘Exit’ 标签的行为
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')                #创建一个状态提示，将鼠标指针悬停在菜单项上时，状态栏中就会显示这个提示。
        exitAct.triggered.connect(QApplication.instance().quit)

        fileMenu.addAction(exitAct)                             #将退出行为添加到文件菜单中

        #子菜单
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        fileMenu.addMenu(impMenu)

        #勾选菜单
        viewStatAct = QAction('View statusbar', self, checkable=True)  #这个行为用来展现或者隐藏状态栏，如果状态栏可见，菜单是勾选的状态。
        viewStatAct.setChecked(True)                                   #设置初始状态为选中
        viewStatAct.setCheckable(True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.triggered.connect(self.toggleMenu)

        fileMenu.addAction(viewStatAct)

    #弹窗确认退出，关闭 QWidget 操作会产生 QCloseEvent 事件。重新实现 closeEvent 事件处理，替换部件的默认行为。
    def closeEvent(self, event):

        #创建了一个带有两个按钮的消息框：是和否。第一个参数是标题栏，第二个参数是对话框显示的消息文本，第三个参数是对话框中的按钮组合，最后一个参数是默认选中的按钮。返回值存储在变量 reply 中。
        reply = QMessageBox.question(self, 'Message',
                    "Are you sure to quit?", QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:

            event.accept()
        else:

            event.ignore()

    #勾选菜单
    def toggleMenu(self, state):

        if state:
            self.statusBar().setVisible(True)
        else:
            self.statusBar().setVisible(False)

    #布局管理,右下角添加两个会随窗口大小变化位置的按钮
    #在 QMainWindow 中，如果你想使用自定义布局（比如 QVBoxLayout），要把它放在一个普通的 QWidget 中，然后再把这个 QWidget 设置为中央部件
    def layout(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)

        self.setCentralWidget(central_widget)

    #创建管理多行多列的布局
    def grid_layout(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        names = ['','','','',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i,j) for i in range(4) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        central_widget = QWidget()
        central_widget.setLayout(grid)

        self.setCentralWidget(central_widget)

def main():

    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
