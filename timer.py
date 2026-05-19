import customtkinter
import json
import time

class TimerPage(customtkinter.CTkFrame):
    displayed = 0
    TIMEDATA_PATH = "./.doddledata/timedata.json"
    data = {
        "total_seconds": 0,
        "daily": {}
    }


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 2), weight=1)
        # self.label = customtkinter.CTkLabel(self, text="Timer")
        # self.label.grid(row=0, column=0)

        self.running = False
        self.start_time = 0
        self.elapsed = 0     # 已经过去的秒数

        self.load_timedata()

        self.time_label = customtkinter.CTkLabel(
            self, 
            text="00:00:00",
            font=("Arial", 48, "bold")
        )
        self.time_label.grid(row=0, column=0, sticky="s")

        self.total_label = customtkinter.CTkLabel(
            self, 
            width=200,
            height=20,
            text=f"total: {self.data['total_seconds']/3600: .2f} hours",
            font=("Arial", 16)
        )
        self.total_label.grid(row=1, column=0, sticky="ns")

        self.timer_btn_frame = customtkinter.CTkFrame(
            self,
            width=300,
            height=30,
            # corner_radius=0
        )
        self.timer_btn_frame.grid(row=2, column=0, pady=10, sticky="n")

        self.start_btn = customtkinter.CTkButton(
            self.timer_btn_frame,
            text="start",
            width=90,
            height=30,
            command=self.start_timer
        )
        self.start_btn.grid(row=0, column=0)

        self.pause_btn = customtkinter.CTkButton(
            self.timer_btn_frame,
            text="pause",
            width=90,
            height=30,
            command=self.pause_timer
        )
        self.pause_btn.grid(row=0, column=1, padx=10)

        self.stop_btn = customtkinter.CTkButton(
            self.timer_btn_frame,
            text="stop",
            width=90,
            height=30,
            command=self.stop_timer
        )
        self.stop_btn.grid(row=0, column=2)

        self.update_clock()

    def start_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed
            self.running = True

    def pause_timer(self):
        self.running = False

    def stop_timer(self):
        self.running = False
        if self.elapsed <= 0:
            return

        # 保存数据
        today = time.strftime("%Y-%m-%d")
        self.data["total_seconds"] += int(self.elapsed)
        
        if today not in self.data["daily"]:
            self.data["daily"][today] = 0
        self.data["daily"][today] += int(self.elapsed)

        self.save_data()

        # 重置
        self.elapsed = 0
        self.update_label()
        self.total_label.configure(text=f"total: {self.data['total_seconds']/3600: .2f} hours")
    
    def update_clock(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.update_label()
        self.after(100, self.update_clock)

    def update_label(self):
        sec = int(self.elapsed)
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        self.time_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

    def load_timedata(self):
        try:
            with open(self.TIMEDATA_PATH, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception as e:
            print(e)

    def save_data(self):
        try:
            with open(self.TIMEDATA_PATH, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)
                

    