import customtkinter
from timer import TimerPage
from todo import TodoPage


class SideBar(customtkinter.CTkFrame):
    def __init__(self, master, mainframe, **kwargs):
        super().__init__(master, **kwargs)
        self.mainframe = mainframe

        self.columnconfigure(0, weight=1)

        self.timer_page_btn = customtkinter.CTkButton(
            self,
            text="Timer ⏰",
            # font=("Arial", 13),
            border_color="#4aa3f7",
            text_color="#4aa3f7",
            fg_color="#f0faf2",
            #hover_color="blue",
            corner_radius=0,
            command=self.mainframe.show_timer_page
        )
        self.timer_page_btn.grid(row=0, column=0, sticky="we")

        self.todo_page_btn = customtkinter.CTkButton(
            self,
            text="TODO 📋",
            # font=("Arial", 13),
            border_color="#4aa3f7",
            text_color="#4aa3f7",
            fg_color="#f0faf2",
            #hover_color="#62bcf5",
            corner_radius=0,
            command=self.mainframe.show_todo_page
        )
        self.todo_page_btn.grid(row=1, column=0, sticky="we")

class MainFrame(customtkinter.CTkFrame):
    # pages = []
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.timer_page = TimerPage(self, fg_color="#faf4e3", corner_radius=0)
        self.todo_page = TodoPage(self, fg_color="#faf4e3", corner_radius=0)

        self.show_timer_page()
    
    def show_timer_page(self):
        if self.todo_page.displayed:
            self.todo_page.grid_forget()
            self.todo_page.displayed = 0
        self.timer_page.displayed = 1
        self.timer_page.grid(row=0, column=0, sticky="nswe")
    
    def show_todo_page(self):
        if self.timer_page.displayed:
            self.timer_page.grid_forget()
            self.todo_page.displayed = 0
        self.todo_page.displayed = 1
        self.todo_page.grid(row=0, column=0, sticky="nswe")

    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        self.title("Doddle ✏️")
        self.minsize(600, 370)
        self.geometry("600x370")
        self.protocol("WM_DELETE_WINDOW", self.on_main_window_close)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.mainframe = MainFrame(self, fg_color="#faf4e3", corner_radius=0)
        self.mainframe.grid(row=0, column=1, sticky="nswe")

        self.sidebar = SideBar(
            self,
            self.mainframe,
            width=80,
            fg_color="#f0faf2",
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, padx=0, pady=0, sticky="ns")

    def on_main_window_close(self):
        self.mainframe.timer_page.stop_timer()
        self.mainframe.todo_page.save_todo_list()
        self.destroy()
    
doddle = App()
doddle.mainloop()