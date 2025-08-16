from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QAbstractItemView 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import json
import sys

class MyTodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题 (可选)
        self.setWindowTitle("谢斌的待办事项列表")

        # 你的主窗口就是 self
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint) # 初始置顶

        central_widget = QWidget()
        self.setCentralWidget(central_widget) # 使用 self.setCentralWidget

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 确保 greeting_label 被创建了
        self.greeting_label = QLabel("欢迎来到谢斌的待办事项列表！") 
        # 确保 input_list 只创建一次，并使用占位符
        self.input_list = QLineEdit()
        self.input_list.setPlaceholderText('亲爱的谢斌酱~快输入你的待办事项叭<3')

        self.dis_list = QListWidget()
        # 在这里设置选择模式
        self.dis_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.button = QPushButton("添加任务")
        self.toggle_ontop_button = QPushButton("设置/取消置顶")
        self.delete_selected_button = QPushButton("删除当前任务(双击任务也可删除)")

        # === 在这里开始设置字体 ===
        # 1. 设置 greeting_label 的字体
        font_greeting = QFont("Microsoft YaHei", 18) # 使用微软雅黑，你可以选择你喜欢的字体
        font_greeting.setBold(True) # 加粗
        self.greeting_label.setFont(font_greeting)
        # 2. 设置任务列表的字体 (影响列表中的所有项)
        # 注意：这里设置的是 QListWidget 的默认字体。
        # 如果你想让加载的任务也应用这个字体，需要在加载时也设置
        # 如果你希望勾选划线功能不受字体影响，那么 update_task_display 方法需要保持原样
        font_list_item = QFont("Microsoft YaHei", 14)
        self.dis_list.setFont(font_list_item) # 设置 QListWidget 的字体

        # 2. 设置任务列表的字体 (影响列表中的所有项)
        # 注意：这里设置的是 QListWidget 的默认字体。
        # 如果你想让加载的任务也应用这个字体，需要在加载时也设置
        # 如果你希望勾选划线功能不受字体影响，那么 update_task_display 方法需要保持原样
        font_list_item = QFont("Microsoft YaHei", 14)
        self.dis_list.setFont(font_list_item) # 设置 QListWidget 的字体
        # 3. 设置输入框和按钮的字体
        font_controls = QFont("Microsoft YaHei", 12)
        self.input_list.setFont(font_controls)
        self.button.setFont(font_controls)
        self.toggle_ontop_button.setFont(font_controls)
        self.delete_selected_button.setFont(font_controls)
        # === 字体设置结束 ===

        layout.addWidget(self.greeting_label)
        layout.addWidget(self.dis_list)
        layout.addWidget(self.input_list)
        layout.addWidget(self.button)
        layout.addWidget(self.toggle_ontop_button)
        layout.addWidget(self.delete_selected_button)

        # 连接信号和槽 (现在槽函数也是类的方法)
        self.button.clicked.connect(self.add_task)
        self.dis_list.itemChanged.connect(self.update_task_display)
        self.toggle_ontop_button.clicked.connect(self.toggle_ontop)
        self.delete_selected_button.clicked.connect(self.delete_selected_tasks)
        self.dis_list.itemDoubleClicked.connect(self.delete_task_on_double_click)
        self.input_list.returnPressed.connect(self.add_task)
        
        self.load_tasks()

    # 槽函数现在是类的方法
    def add_task(self):
        task_text = self.input_list.text() # 使用 self.input_list
        if task_text:
            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.dis_list.addItem(item) # 使用 self.dis_list
            self.input_list.clear()

    # 槽函数现在是类的方法
    def update_task_display(self, item):
        current_font = item.font()
        if item.checkState() == Qt.CheckState.Checked:
            current_font.setStrikeOut(True)
            item.setFont(current_font)
            print(f"任务 '{item.text()}' 被勾选了！")
        else:
            current_font.setStrikeOut(False)
            item.setFont(current_font)
            print(f"任务 '{item.text()}' 被取消勾选了！")

    # 槽函数现在是类的方法
    def toggle_ontop(self):
        current_flags = self.windowFlags() # 使用 self.windowFlags()
        if current_flags & Qt.WindowType.WindowStaysOnTopHint:
            self.setWindowFlags(current_flags & ~Qt.WindowType.WindowStaysOnTopHint) # 使用 self.setWindowFlags
        else:
            self.setWindowFlags(current_flags | Qt.WindowType.WindowStaysOnTopHint) # 使用 self.setWindowFlags
        self.show() # self.show()

    # 槽函数现在是类的方法
    def delete_selected_tasks(self):
        selected_items = self.dis_list.selectedItems()
    # 从后往前遍历删除
        for item in reversed(selected_items): # reversed() 函数很有用！
            row = self.dis_list.row(item)
            self.dis_list.takeItem(row) # takeItem 会移除并返回项目，然后会自动销毁

    # 槽函数现在是类的方法
    def delete_task_on_double_click(self, item):
        row = self.dis_list.row(item)
        self.dis_list.takeItem(row)

    def closeEvent(self, event):
    # 在这里执行保存任务的逻辑
        self.save_tasks() # 调用一个我们即将定义的保存函数
        event.accept() # 接受关闭事件，允许窗口关闭

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
            
            for task_data in tasks:
                item = QListWidgetItem(task_data["text"])
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                
                # 根据保存的状态设置勾选状态
                if task_data["status"] == 1:
                    item.setCheckState(Qt.CheckState.Checked)
                else:
                    item.setCheckState(Qt.CheckState.Unchecked)
                
                self.dis_list.addItem(item)
            print("任务已加载！")
        except FileNotFoundError:
            print("tasks.json 文件不存在，无需加载任务。")
        except json.JSONDecodeError:
            print("tasks.json 文件格式错误，无法加载。")
        except Exception as e:
            print(f"加载任务失败: {e}")

    def save_tasks(self):
        tasks = []
        for i in range(self.dis_list.count()): # 遍历所有任务
            item = self.dis_list.item(i)
            task_text = item.text()
            # 根据勾选状态决定保存 0 还是 1
            task_status = 1 if item.checkState() == Qt.CheckState.Checked else 0
            tasks.append({"text": task_text, "status": task_status})
        # 将 tasks 列表写入文件
        # 我们使用 JSON 格式会更方便，因为它可以直接保存列表和字典
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=4) # indent=4 让文件更易读
            print("任务已保存！")
        except Exception as e:
            print(f"保存任务失败: {e}") 

    def focusOutEvent(self, event):
        self.hide()
        super().focusOutEvent(event)

    def focusInEvent(self, event):
        self.showNormal()
        super().focusInEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTodoListApp() # 创建你的自定义窗口类的实例
    window.show() # 显示你的窗口实例
    sys.exit(app.exec())
