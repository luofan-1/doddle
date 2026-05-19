import time
import json
import os
from datetime import datetime
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
# WebDAV 坚果云同步
from webdav.client import Client

# ===================== 坚果云 WebDAV 配置 =====================
WEBDAV_URL = "https://dav.jianguoyun.com/dav/"
WEBDAV_USER = "1340397059@qq.com"
WEBDAV_PWD  = "abbuv7pizj2fv273"

CLOUD_DODDLEFILE_DIR = "/.doddledata"
CLOUD_TIMEDATA_FILE = "data.json"
CLOUD_TIMEDATA_PATH = "/".join([CLOUD_DODDLEFILE_DIR, CLOUD_TIMEDATA_FILE])

LOCAL_DODDLEFILE_DIR = "./.doddledata"
LOCAL_TIMEDATA_FILE = "data.json"
LOCAL_TIMEDATA_PATH = "/".join([LOCAL_DODDLEFILE_DIR, LOCAL_TIMEDATA_FILE])
# ========================================================================

DEFAULT_DATA = {
    "total_seconds": 0,
    "daily": {}
}

# 初始化 WebDAV 客户端
def init_dav_client():
    webdav_options = {
        'webdav_hostname': WEBDAV_URL,
        'webdav_login':    WEBDAV_USER,
        'webdav_password': WEBDAV_PWD
    }
    return Client(webdav_options)

dav_client = init_dav_client()

# 从坚果云下载 data.json 到本地
def download_from_cloud():
    try:
        dav_client.download_sync(CLOUD_TIMEDATA_FILE, LOCAL_TIMEDATA_FILE)
        print("✅ 从坚果云拉取成功")
    except Exception as e:
        print("⚠️ 云端无文件，使用默认数据", e)

# 上传本地 data.json 到坚果云
def upload_to_cloud():
    try:
        dav_client.upload_file(LOCAL_TIMEDATA_FILE, CLOUD_TIMEDATA_FILE)
        print("✅ 已同步到坚果云")
    except Exception as e:
        print("⚠️ 同步失败", e)

# 本地读写
def load_data():
    if not os.path.exists(LOCAL_TIMEDATA_FILE):
        return DEFAULT_DATA.copy()
    try:
        with open(LOCAL_TIMEDATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return DEFAULT_DATA.copy()

def save_data(data):
    with open(LOCAL_TIMEDATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 秒转时分秒
def format_sec(sec):
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

class TimerUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (360, 600)

        self.running = False
        self.start_ts = 0
        self.elapsed = 0

        # 启动先从云端拉最新数据
        download_from_cloud()
        self.data = load_data()

        layout = MDBoxLayout(orientation="vertical", padding=30, spacing=20)

        self.time_label = MDLabel(text="00:00:00", font_style="H3", halign="center")
        self.total_label = MDLabel(
            text=f"总学习时长：{self.data['total_seconds'] // 3600} 小时",
            halign="center"
        )

        btn_layout = MDBoxLayout(spacing=15)
        self.btn_start = MDRaisedButton(text="开始", on_press=self.start_timer)
        self.btn_pause = MDRaisedButton(text="暂停", on_press=self.pause_timer)
        self.btn_stop = MDRaisedButton(text="结束保存", on_press=self.stop_timer)

        btn_layout.add_widget(self.btn_start)
        btn_layout.add_widget(self.btn_pause)
        btn_layout.add_widget(self.btn_stop)

        layout.add_widget(self.time_label)
        layout.add_widget(self.total_label)
        layout.add_widget(btn_layout)
        self.add_widget(layout)

        Clock.schedule_interval(self.update_timer, 0.1)

    def start_timer(self, _):
        if not self.running:
            self.start_ts = time.time() - self.elapsed
            self.running = True

    def pause_timer(self, _):
        self.running = False

    def stop_timer(self, _):
        self.running = False
        if self.elapsed < 1:
            return

        today = datetime.now().strftime("%Y-%m-%d")
        self.data["total_seconds"] += int(self.elapsed)
        if today not in self.data["daily"]:
            self.data["daily"][today] = 0
        self.data["daily"][today] += int(self.elapsed)

        # 保存本地 + 自动上传坚果云
        save_data(self.data)
        upload_to_cloud()

        self.total_label.text = f"总学习时长：{self.data['total_seconds'] // 3600} 小时"
        self.elapsed = 0

    def update_timer(self, dt):
        if self.running:
            self.elapsed = time.time() - self.start_ts
        self.time_label.text = format_sec(int(self.elapsed))

class TimerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return TimerUI()

if __name__ == "__main__":
    TimerApp().run()