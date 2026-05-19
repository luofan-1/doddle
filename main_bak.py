import customtkinter as ctk
import time
import json
import os
from webdav.client import Client

WEBDAV_URL = "https://dav.jianguoyun.com/dav"
WEBDAV_USER = "1340397059@qq.com"
WEBDAV_PWD = "abbuv7pizj2fv273"

CLOUD_DODDLEFILE_DIR = "/.doddledata"
CLOUD_TIMEDATA_FILE = "data.json"
CLOUD_TIMEDATA_PATH = "/".join([CLOUD_DODDLEFILE_DIR, CLOUD_TIMEDATA_FILE])

LOCAL_DODDLEFILE_DIR = "./.doddledata"
LOCAL_TIMEDATA_FILE = "data.json"
LOCAL_TIMEDATA_PATH = "/".join([LOCAL_DODDLEFILE_DIR, LOCAL_TIMEDATA_FILE])

webdav_options = {
    'webdav_hostname' : WEBDAV_URL,
    'webdav_login' : WEBDAV_USER,
    'webdav_password' : WEBDAV_PWD
}

cl = Client(webdav_options)

default_data = {
    "total_seconds" : 0,
    "daily" : {},
}

def download_data():
    ret = 1
    if not cl.check(CLOUD_TIMEDATA_PATH):
        cloud_dirs = cl.list("/")
        for cloud_dir in cloud_dirs:
            if cloud_dir==".doddledata/":
                print("未在云端查找到时间数据文件，自动创建空时间文件")
                cl.mkdir(CLOUD_TIMEDATA_PATH)
                break
        else:
            print("未在云端创建 .doddledata 文件夹")
            exit(0)
        ret = 1
    # ！这里如果本地有文件而云端没有的话可能会覆盖掉本地文件
    cl.download_sync(CLOUD_TIMEDATA_PATH, LOCAL_TIMEDATA_PATH)
    return ret # 返回值表示文件原来是否存在
    

def load_data():
    if not os.path.exists(LOCAL_TIMEDATA_PATH):
        file_exists = download_data()
        if not file_exists:
            return default_data
    with open(LOCAL_TIMEDATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open(LOCAL_TIMEDATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class DoddleApp(ctk.CTk):
    def __init__(self):
        super.__init__()
        self.title("Doddle")
        
class TimerPage(ctk.CTkFrame):
    pass

class TodoPage(ctk.CTkFrame):
    pass

class TimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 窗口设置
        self.title("Doddle ✏️")
        self.geometry("450x300")
        ctk.set_appearance_mode("light")  # 浅色模式
        ctk.set_default_color_theme("blue")

        # 计时状态
        self.running = False
        self.start_time = 0
        self.elapsed = 0     # 已经过去的秒数

        # 加载数据
        self.data = load_data()

        # ====================== UI ======================
        # 时间显示
        self.time_label = ctk.CTkLabel(
            self, text="00:00:00",
            font=("Arial", 48, "bold")
        )
        self.time_label.pack(pady=20)

        # 总时长显示
        # self.total_label = ctk.CTkLabel(
        #     self, text=f"总学习时长：{self.data['total_seconds'] // 3600} 小时",
        #     font=("Arial", 16)
        # )
        # self.total_label.pack(pady=5)

        # 按钮
        frame = ctk.CTkFrame(self)
        frame.pack(pady=15)

        self.start_btn = ctk.CTkButton(frame, text="start", command=self.start_timer, width=100)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.pause_btn = ctk.CTkButton(frame, text="pause", command=self.pause_timer, width=100)
        self.pause_btn.grid(row=0, column=1, padx=10)

        self.stop_btn = ctk.CTkButton(frame, text="stop", command=self.stop_save, width=100)
        self.stop_btn.grid(row=0, column=2, padx=10)

        # 定时器刷新
        self.update_clock()

    # ====================== 计时逻辑 ======================
    def start_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed
            self.running = True

    def pause_timer(self):
        self.running = False

    def stop_save(self):
        self.running = False
        if self.elapsed <= 0:
            return

        # 保存数据
        today = time.strftime("%Y-%m-%d")
        self.data["total_seconds"] += int(self.elapsed)
        
        if today not in self.data["daily"]:
            self.data["daily"][today] = 0
        self.data["daily"][today] += int(self.elapsed)

        save_data(self.data)

        # 重置
        self.elapsed = 0
        self.update_label()
        # self.total_label.configure(text=f"总学习时长：{self.data['total_seconds'] // 3600} 小时")

    def append_missed():
        pass

    # ====================== 界面更新 ======================
    def update_label(self):
        sec = int(self.elapsed)
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        self.time_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

    def update_clock(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.update_label()

        self.after(100, self.update_clock)  # 每100ms刷新一次

# ====================== 运行 ======================
if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()