# -*- coding: utf-8 -*-
"""
嗯，用户希望用PyQt5重写现有的Tkinter交互代码，并且需要详细的注释。
首先，我需要仔细阅读现有的代码，理解各个组件的功能和交互逻辑。
现有的`windows_front.py`使用了Tkinter来构建用户界面，
包括输入框、按钮、下拉菜单、对话显示区域等。
主要的类`Application`负责初始化界面元素，处理用户输入，调用API处理器，并更新显示。

接下来，我需要考虑如何将这些Tkinter组件转换为PyQt5的等效组件。
例如，Tkinter的`Frame`可以对应PyQt5的`QWidget`或布局管理器，
`Entry`对应`QLineEdit`，`Button`对应`QPushButton`，
`Text`对应`QTextEdit`，`Combobox`对应`QComboBox`，等等。
需要注意的是，PyQt5的信号与槽机制与Tkinter的事件绑定有所不同，需要调整事件处理的方式。

另外，现有的代码中使用了多线程来处理API请求，以防止界面冻结。
在PyQt5中，可以使用`QThread`或者`QThreadPool`来实现类似的功能，
确保耗时操作不会阻塞主线程。

还需要注意布局管理。
Tkinter使用`pack()`、`grid()`和`place()`来布局组件，
而PyQt5提供了更灵活的布局管理器，
如`QVBoxLayout`、`QHBoxLayout`和`QGridLayout`，
需要合理使用这些布局来保持界面的整洁和响应式。

在代码结构方面，
可能需要将界面初始化、信号连接、业务逻辑处理分离开来，
以提高代码的可读性和可维护性。
例如，可以创建一个继承自`QMainWindow`的主窗口类，
负责布局界面元素，并定义槽函数来处理用户交互。

还需要处理异常和错误提示。
现有的代码中有一个注释掉的`show_error`方法，
可能需要重新实现，使用PyQt5的`QMessageBox`来显示错误信息。

此外，现有的代码中涉及图像处理和API调用，
这部分逻辑在PyQt5中应保持基本不变，
但需要确保与PyQt5的信号机制兼容，
例如在子线程中更新界面时，需要通过信号来安全地更新UI组件。

最后，需要添加详细的注释，解释每个部分的功能，
特别是PyQt5特有的部分，
如信号与槽的连接、布局管理器的使用、线程处理等，以帮助用户理解代码结构和实现细节。

在转换过程中可能会遇到的一些挑战包括：
不同GUI框架的事件循环机制差异、线程安全的UI更新、
PyQt5组件与Tkinter组件的行为差异等。
需要仔细测试每个功能，
确保转换后的代码在行为上与原始Tkinter应用一致，并且界面布局合理。

总结步骤：

1. 分析现有Tkinter代码的结构和功能。

2. 设计PyQt5的界面布局，选择合适的组件和布局管理器。

3. 将Tkinter组件逐一转换为PyQt5组件，并调整事件处理机制。

4. 实现多线程处理API请求，确保界面流畅。

5. 处理异常和错误提示，使用PyQt5的对话框组件。

6. 添加详细注释，解释关键部分的实现逻辑。

7. 测试转换后的应用，确保功能正常，界面布局合理。
"""


"""
使用PyQt5重构的AI助手界面
"""
import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
                             QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from api_handlers import APIWithoutHistory, APIWithHistory, APIImageWithoutHistory
from image import ImageLoadAndSend

class Communicate(QObject):
    """自定义信号类用于线程间通信"""
    update_signal = pyqtSignal(str, str)  # 参数：角色，内容
    error_signal = pyqtSignal(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化界面
        self.setWindowTitle("AI助手 - PyQt5版")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化变量
        self.api_key = ""
        self.history_mode = 0  # 0-无历史 1-有历史 2-图片模式
        self.model_name = "qwen-max"
        self.image_path = r'.\photos\1012.png'
        
        # 初始化API处理器
        self.api_handler = APIWithoutHistory()
        
        # 创建信号通信对象
        self.comm = Communicate()
        self.comm.update_signal.connect(self.update_display)
        self.comm.error_signal.connect(self.show_error)
        
        # 创建界面组件
        self.init_ui()

    def init_ui(self):
        """初始化界面组件"""
        # 主容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # API密钥输入
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("API密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)  # 密码模式
        key_layout.addWidget(self.key_input)
        main_layout.addLayout(key_layout)

        # 模型选择
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("选择模型:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            'qwen-max', 'qwen-plus', 'qwen-turbo', 
            'qwen-vl-max', 'qwen-vl-plus'  # 示例模型列表
        ])
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        main_layout.addLayout(model_layout)

        # 模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("交互模式:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "开启上下文", 
            "不开启上下文", 
            "图片模式（VL/QVQ模型）"
        ])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        main_layout.addLayout(mode_layout)

        # 图片选择按钮（仅在图片模式显示）
        self.image_btn = QPushButton("选择图片")
        self.image_btn.clicked.connect(self.select_image)
        self.image_btn.hide()  # 默认隐藏
        main_layout.addWidget(self.image_btn)

        # 对话显示区域
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.append("欢迎使用AI助手！请输入您的问题...")
        main_layout.addWidget(self.chat_area)

        # 输入区域
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)  # 回车发送
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("发送")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        main_layout.addLayout(input_layout)

    def on_model_changed(self, text):
        """模型选择变更处理"""
        self.model_name = text

    def on_mode_changed(self, index):
        """模式选择变更处理"""
        self.history_mode = index
        # 更新API处理器
        if index == 0:
            self.api_handler = APIWithHistory()
            self.image_btn.hide()
        elif index == 1:
            self.api_handler = APIWithoutHistory()
            self.image_btn.hide()
        elif index == 2:
            self.api_handler = APIImageWithoutHistory()
            self.image_btn.show()

    def select_image(self):
        """选择图片文件"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.image_path = file_name

    def send_message(self):
        """处理消息发送"""
        question = self.input_field.text().strip()
        if not question:
            QMessageBox.warning(self, "警告", "输入不能为空")
            return
        
        self.input_field.clear()
        self.update_display("用户", question)
        
        # 创建线程处理请求
        thread = threading.Thread(
            target=self.process_request,
            args=(question, self.key_input.text())
        )
        thread.daemon = True
        thread.start()

    def process_request(self, question, api_key):
        """处理API请求（在子线程中执行）"""
        try:
            if self.history_mode == 2:  # 图片模式
                image_loader = ImageLoadAndSend(self.image_path)
                response = self.api_handler.send_request(
                    question,
                    api_key,
                    self.model_name,
                    image=image_loader.load()
                )
            else:  # 文本模式
                response = self.api_handler.send_request(
                    question,
                    api_key,
                    self.model_name
                )
            
            # 通过信号更新UI
            self.comm.update_signal.emit("AI", response)
        
        except Exception as e:
            self.comm.error_signal.emit(str(e))

    def update_display(self, role, content):
        """更新对话显示"""
        self.chat_area.append(f"\n{role}: {content}")
        self.chat_area.ensureCursorVisible()  # 自动滚动到底部

    def show_error(self, error_msg):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", f"请求失败：{error_msg}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


"""
主要改进和注释说明：

信号机制：使用PyQt5的信号槽机制实现线程间通信，确保UI更新安全

布局管理：采用QVBoxLayout和QHBoxLayout进行灵活布局

组件对应：

Tkinter.Entry → QLineEdit

Tkinter.Text → QTextEdit

Tkinter.Combobox → QComboBox

Tkinter.Button → QPushButton

新增功能：

图片选择对话框（QFileDialog）

更完善的错误处理

自动滚动聊天区域

线程处理：使用Python标准线程库，通过信号机制安全更新UI

代码结构：

主窗口继承自QMainWindow

使用单独的Communicate类处理信号

将不同功能拆分为多个方法

注意事项：

PyQt5要求UI操作必须在主线程执行

使用信号机制保证线程安全

组件命名和布局更加规范

建议运行前确保：

已安装PyQt5：pip install pyqt5

保持原有项目结构（image、api_handlers等模块）

图片路径需要根据实际情况调整

这个实现保留了原有功能，
同时利用PyQt5的特性提供了更现代的界面和更好的用户体验。"""