# PyQt6 桌面应用开发：从零开始完整学习框架

## 🎯 总体学习路线图

遵循 **"基础准备 → 核心掌握 → 项目实战 → 高级进阶"** 的循序渐进路径。

## 📚 阶段 1：基础准备（1-2周）

### 1.1 Python 基础巩固

**目标**：掌握 PyQt6 开发必需的 Python 知识。

- [ ] **变量、数据类型、运算符
- [ ] **流程控制**（if-else, for, while）
- [ ] **函数定义和使用**
- [ ] **面向对象编程（重点！）**  
  - 类和对象  
  - 继承和多态 
  - 方法和属性

### 1.2 开发环境搭建

**必备工具**：

- **Python 3.8+**：从官网安装

- **VS Code**：轻量级代码编辑器  - 安装 Python 和 Pylance 扩展
- **PyQt6 安装**：  

```bash
pip install pyqt6  
pip install pyqt6-tools
```

### 1.3 第一个 PyQt6 程序

创建 `first_app.py`：

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget

# 创建应用实例
app = QApplication(sys.argv)

# 创建窗口
window = QWidget()
window.setWindowTitle("我的第一个 PyQt6 程序")
window.resize(400, 300)
window.show()

# 进入事件循环
sys.exit(app.exec())
```

运行命令：
```bash
python first_app.py
```

## 🏗️ 阶段 2：核心组件掌握（3-4周）

### 2.1 基础窗口组件

**学习顺序**：
1. **QMainWindow**：主窗口类（包含菜单栏、状态栏等）
2. **QDialog**：对话框类
3. **布局管理器**：
   - `QVBoxLayout`：垂直布局
   - `QHBoxLayout`：水平布局  
   - `QGridLayout`：网格布局

### 2.2 常用控件学习

按此顺序学习控件：

```python
# 基础输入控件
QPushButton, QLabel, QLineEdit, QTextEdit
QCheckBox, QRadioButton, QComboBox

# 高级控件
QListWidget, QTableWidget, QTreeWidget
QProgressBar, QSlider, QSpinBox
```

### 2.3 信号与槽机制（核心！）

**重点掌握**：

```python
# 内置信号连接
from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import pyqtSignal

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        button = QPushButton("点击我", self)
        # 连接信号与槽
        button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        print("按钮被点击了！")

# 自定义信号
class MyWidget(QWidget):
    # 定义自定义信号
    custom_signal = pyqtSignal(str)
    
    def send_message(self):
        self.custom_signal.emit("Hello!")
```

### 阶段 2 实战项目：**个人信息收集器**

**功能要求**：
- 包含姓名、年龄、性别、爱好等输入项
- 使用多种布局组合
- 实现数据验证和提交功能
- 点击提交后在控制台显示收集的信息

## 🎨 阶段 3：界面美化与数据持久化（2-3周）

### 3.1 界面美化 - QSS

**学习 Qt Style Sheets**（类似 CSS）：

```python
# 设置样式
window.setStyleSheet("""
    QMainWindow {
        background-color: #f0f0f0;
    }
    QPushButton {
        background-color: #007acc;
        color: white;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #005a9e;
    }
    QPushButton:pressed {
        background-color: #003d6b;
    }
    QLineEdit {
        border: 2px solid #cccccc;
        border-radius: 4px;
        padding: 5px;
        font-size: 14px;
    }
    QLineEdit:focus {
        border-color: #007acc;
    }
""")
```

### 3.2 数据持久化 - SQLite

```python
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='myapp.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_user(self, name, email, age):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, email, age)
                VALUES (?, ?, ?)
            ''', (name, email, age))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()
```

### 3.3 文件操作

```python
from PyQt6.QtWidgets import QFileDialog, QMessageBox

class FileManager:
    def __init__(self, parent_window):
        self.parent = parent_window
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 
            "选择文件", 
            "", 
            "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                return content
            except Exception as e:
                QMessageBox.warning(self.parent, "错误", f"无法打开文件: {str(e)}")
        return None
    
    def save_file_dialog(self, content):
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "保存文件",
            "",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                QMessageBox.information(self.parent, "成功", "文件保存成功！")
                return True
            except Exception as e:
                QMessageBox.warning(self.parent, "错误", f"无法保存文件: {str(e)}")
        return False
```

### 阶段 3 实战项目：**简易笔记本**

**功能要求**：
- 富文本编辑功能（QTextEdit）
- 笔记列表展示（QListWidget）
- 数据保存到 SQLite 数据库
- 自定义美观的界面样式
- 支持笔记的创建、编辑、删除和搜索

## 🚀 阶段 4：高级特性与项目实战（3-4周）

### 4.1 多线程编程

**防止界面卡顿**：

```python
from PyQt6.QtCore import QThread, pyqtSignal
import time

class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, task_data):
        super().__init__()
        self.task_data = task_data
        self.is_running = True
    
    def run(self):
        try:
            for i in range(101):
                if not self.is_running:
                    break
                # 模拟耗时操作
                time.sleep(0.1)
                self.progress_updated.emit(i)
            
            if self.is_running:
                self.finished.emit("任务完成！")
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def stop(self):
        self.is_running = False

# 在主窗口中使用
class MainWindow(QMainWindow):
    def start_long_task(self):
        self.worker = WorkerThread("一些数据")
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)
        self.worker.error_occurred.connect(self.task_error)
        self.worker.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
```

### 4.2 自定义控件

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

class CustomButton(QPushButton):
    """自定义按钮控件"""
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        self.setup_ui(icon_path)
    
    def setup_ui(self, icon_path):
        self.setMinimumSize(120, 40)
        self.setStyleSheet("""
            CustomButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            CustomButton:hover {
                background-color: #45a049;
            }
            CustomButton:pressed {
                background-color: #3d8b40;
            }
        """)

class TaskWidget(QWidget):
    """任务项自定义控件"""
    task_deleted = pyqtSignal(int)
    task_completed = pyqtSignal(int, bool)
    
    def __init__(self, task_id, title, description):
        super().__init__()
        self.task_id = task_id
        self.setup_ui(title, description)
    
    def setup_ui(self, title, description):
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #666; font-size: 12px;")
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            TaskWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
            }
            TaskWidget:hover {
                border-color: #007acc;
            }
        """)
```

### 4.3 打包分发

使用 PyInstaller 打包应用：

```bash
# 基础打包
pyinstaller --onefile --windowed your_app.py

# 带图标的打包
pyinstaller --onefile --windowed --icon=app.ico your_app.py

# 添加额外文件的打包
pyinstaller --onefile --windowed --add-data "data;data" your_app.py

# 隐藏命令行窗口（仅 Windows）
pyinstaller --onefile --noconsole your_app.py
```

创建打包配置文件 `build.spec`：

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['your_app.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images'), ('data', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)
```

### 阶段 4 终极项目：**个人任务管理系统**

**完整功能要求**：

1. **核心功能**：
   - 任务的增删改查
   - 任务分类和优先级设置
   - 截止日期提醒

2. **高级功能**：
   - 数据统计图表（使用 QChart）
   - 定时提醒功能（系统通知）
   - 数据导入导出（JSON、CSV）
   - 多主题切换

3. **技术特性**：
   - 使用 SQLite 数据库
   - 多线程处理耗时操作
   - 自定义控件和样式
   - 可打包为独立执行文件

## 🛠️ 学习资源推荐

### 官方文档
- **PyQt6 官方文档**：https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Qt 官方文档**：https://doc.qt.io/qt-6/index.html

### 推荐书籍
- 《PyQt6 快速开发与实战》
- 《Rapid GUI Programming with Python and Qt》

### 实践建议

1. **每日编码**：保持连续学习，哪怕每天30分钟
2. **项目驱动**：每个阶段都要完成对应的实战项目
3. **循序渐进**：不要跳跃学习，打好基础很重要
4. **善用搜索**：遇到问题先搜索，大部分问题都有解决方案

## 📅 学习时间规划表

| 阶段      | 持续时间 | 每周计划     | 目标产出                 |
| --------- | -------- | ------------ | ------------------------ |
| **阶段1** | 1-2周    | 10-15小时/周 | 能创建基础窗口和应用     |
| **阶段2** | 3-4周    | 12-18小时/周 | 能制作完整的表单应用     |
| **阶段3** | 2-3周    | 10-15小时/周 | 能制作有数据库的美观应用 |
| **阶段4** | 3-4周    | 15-20小时/周 | 能制作复杂应用并打包分发 |

## 🔧 故障排除指南

### 常见问题及解决方案

1. **导入错误**：
   ```python
   # 错误：ModuleNotFoundError: No module named 'PyQt6'
   # 解决：重新安装 PyQt6
   pip uninstall pyqt6
   pip install pyqt6
   ```

2. **界面卡顿**：
   - 使用多线程处理耗时操作
   - 避免在主线程中进行大量计算

3. **打包问题**：
   - 确保所有资源文件路径正确
   - 使用 `os.path.join` 处理路径

## 🎯 下一步行动

1. **立即开始**：安装 Python 和 PyQt6
2. **创建第一个程序**：运行阶段1的示例代码
3. **制定计划**：根据自身情况调整学习时间表
4. **加入社区**：关注相关技术论坛和社群

**记住：最好的学习方式是动手实践！从现在开始编写代码吧！**
## 一些可能的日历 UI 参考

## 复旦大学 elearning

### 控制面板视图

![image-20251019143334034](C:\Users\16244\AppData\Roaming\Typora\typora-user-images\image-20251019143334034.png)

### 日历视图（月）

![image-20251019143455940](C:\Users\16244\AppData\Roaming\Typora\typora-user-images\image-20251019143455940.png)

### 日历视图（事项）

![image-20251019143526180](C:\Users\16244\AppData\Roaming\Typora\typora-user-images\image-20251019143526180.png)

### 日历视图（周）

![image-20251019143641169](C:\Users\16244\AppData\Roaming\Typora\typora-user-images\image-20251019143641169.png)

## 复旦大学 OJ

### 日历视图

![image-20251019143843548](C:\Users\16244\AppData\Roaming\Typora\typora-user-images\image-20251019143843548.png)
