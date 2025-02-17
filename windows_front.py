# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import ttk , messagebox
from PIL import Image ,ImageTk
import threading
from image_input import ImageLoader
from api_handlers import APIWithoutHistory, APIWithHistory



class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("哇,是AI,我们有救了")
        self.root.geometry("800x600+100+100")
        self.root.config(bg= "white")

        self.api_key_var = tk.StringVar()
        self.history_mode = tk.IntVar(value=0)
        self.input_text = ""
        self.api_hander = None

        self.create_widgets()
        self.setup_api_hander()

    def create_widgets(self):
        # 输入框和发送按钮
        entry_frame = tk.Frame(self.root)
        self.entry = tk.Entry(entry_frame, bg="white", bd=4)
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.entry.pack(side=tk.LEFT, pady=3)

        tk.Button(
            entry_frame, 
            bg="light blue",
            text="发送",
            command=self.send_message
        ).pack(side=tk.RIGHT, pady=4)
        entry_frame.pack(pady=5)

        # API密钥输入
        key_frame = tk.Frame(self.root)
        tk.Label(key_frame, text="请将'钥匙'/api_key粘贴进灰色框").pack(side=tk.LEFT)
        tk.Entry(key_frame, bg="gray", textvariable=self.api_key_var, show="*").pack(side=tk.RIGHT)
        key_frame.pack()

        # 上下文选择
        #mode_frame = tk.Frame(self.root)
        #tk.Radiobutton(mode_frame, text="需要上下文", variable=self.history_mode, value=1).pack(side=tk.LEFT)
        #tk.Radiobutton(mode_frame, text="不需要上下文", variable=self.history_mode, value=0).pack(side=tk.RIGHT)
        #mode_frame.pack()

        combo_text = ttk.Combobox(
            self.root,
            values=["开启上下文","不开启上下文"],
            state="readonly"  # 设置为只读模式
            )
        combo_text.pack(padx=20, pady=10)
        combo_text.current(0)

        # 绑定选择事件
        def text_select(event):
            if combo_text.get() == "开启上下文":
                self.history_mode.set(1)
            else:
                self.history_mode.set(0)
            self.setup_api_hander()
        combo_text.bind("<<ComboboxSelected>>", text_select)

        # 对话显示区域
        self.text_area = tk.Text(self.root, width=80, height=300)
        self.text_area.pack(pady=10)
        self.text_area.insert("1.0", "用户,您好,这是调用qwen的AI助手,请在上方输入框中提问\n\n")

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.text_area.yview)


    def setup_api_hander(self):
        """根据选择模式初始化API处理器"""
        if self.history_mode.get() == 1:
            self.api_handler = APIWithHistory()
        elif self.history_mode.get() == 0:
            self.api_handler = APIWithoutHistory()

    def send_message(self):
        """处理消息发送"""
        self.input_text = self.entry.get()
        if not self.input_text:
            messagebox.showwarning("警告", "输入不能为空")
            return

        self.entry.delete(0, tk.END)
        self.update_display("用户", self.input_text)
        threading.Thread(target=self.process_request).start()
    def process_request(self):
        """处理API请求"""
        try:
            response = self.api_handler.send_request(
                self.input_text,
                self.api_key_var.get()
            )
            self.root.after(0, self.update_display, "AI", response)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def update_display(self, role, content):
        """更新对话显示"""
        self.text_area.insert(tk.END, f"\n{role}: {content}\n")
        self.text_area.see(tk.END)

    def show_error(self, error_msg):
        """显示错误信息"""
        messagebox.showerror("错误", f"请求失败: {error_msg}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
        