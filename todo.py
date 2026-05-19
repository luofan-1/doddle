import customtkinter
# from datetime import datetime
from dateutil import parser
import csv

TIME_REMIND = "1970-01-01 00:00:00"
TIME_ALWAYS = "2226-05-19 09:35:00"

def visual_width(s):
    return sum(1 if c.isascii() else 2 for c in s)

def align_str(s, total_width):
    pad = total_width - visual_width(s)
    return s + " " * max(pad, 0)

# class Todo:
#     def __init__(self, info):
#         self.info = info
#         self.prev = None
#         self.next = None

# class TodoList:
#     def __init__(self):
#         self.head = None
#         self.tail = None
    
#     def insert(self, todo: Todo):
#         self.todos.append(todo)
#         if not self.head:
#             self.head = todo
#             return
#         it = self.head

class TodoItemBar(customtkinter.CTkFrame):
    pass


class ListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = parent
        
        # print(parent)

        self.item_bars = []

    # 此处是屎，如果每一次都重新创建对象不好，应该将每一个行独立为对象，只更改其属性
    def refresh_list(self):
        if self.item_bars:
            for item in self.item_bars:
                item.grid_forget()
                item.destroy()
            self.item_bars.clear()
        for (i, todo) in enumerate(self.parent.todo_list):
            item_bar = customtkinter.CTkFrame(
                self,
                height=40,
                fg_color="#ECF7DF" if todo["done"] else "#FEE9EC",
                corner_radius=0
            )
            item_bar.columnconfigure(0, weight=1)
            item_bar.rowconfigure(0, weight=1)
            aff = todo["affliation"]
            task = todo["task"]
            ddl = todo["deadline"]
            if ddl==TIME_REMIND:
                ddl = "REMIND"
            elif ddl==TIME_ALWAYS:
                ddl = "ALWAYS"
            info = align_str(aff, 15) + align_str(task, 15) + align_str(ddl, 19)
            # info = f"{todo["affliation"]: <15}{todo["task"]: <15}{todo["deadline"]: <19}"
            # print(info)
            item_info = customtkinter.CTkLabel(
                item_bar,
                text=info,
                font=("Sarasa Mono SC", 14),
                corner_radius=0
            )
            item_info.grid(row=0, column=0, padx=(5, 0), sticky="nsw")
            item_checkbox = customtkinter.CTkCheckBox(
                item_bar,
                text="",
                height=5,
                width=5,
                command=lambda index=i: self.parent.on_item_checked(index) # ???
            )
            if todo["done"]:
                item_checkbox.select() 
            else:
                item_checkbox.deselect()
            item_checkbox.grid(row=0, column=1)
            self.columnconfigure(0, weight=1)
            item_bar.grid(row=i, column=0, padx=4, pady=(4, 0), sticky="we")
            self.item_bars.append(item_bar)            
            
    
class BottomBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        
        self.append_btn = customtkinter.CTkButton(
            self,
            command=master.append_todo,
            fg_color="grey86",
            height=30,
            width=80,
            text="+ 添加事项",
            text_color="#4aa3f7",
            hover_color="#a4ccf1",
            corner_radius=0
        )
        self.append_btn.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsw")

        # self.order_menu_frame = customtkinter.CTkFrame(self)
        # self.order_menu_lable = customtkinter.CTkLabel(
        #     self.order_menu_frame,
        #     text="Order Settings"
        # )
        # self.order_menu_lable.grid(row=0, column=0)
        options = ["ddl", "csv", "affliation"]
        self.selected_order = customtkinter.StringVar(value="ddl")
        self.order_menu = customtkinter.CTkOptionMenu(
            self,
            values=options,
            variable=self.selected_order,
            command=self.master.resort_list,
            corner_radius=0,
        )
        self.order_menu.grid(row=0, column=1, sticky="nse")
        # self.order_menu_frame.grid(row=0, column=1)


class AppendTodoWindow(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        
        # self.title("New Todo")
        self.title("新增事项")
        self.geometry("300x140")
        self.resizable(False, False)
        self.grab_set()
        # self.option_add("*Entry.imeReset", False)

        self.affliation_value = customtkinter.StringVar(value="")
        self.task_value = customtkinter.StringVar(value="")
        self.deadline_value = customtkinter.StringVar(value="")
        self.result = {
            "affliation": self.affliation_value,
            "task": self.task_value,
            "deadline": self.deadline_value
        }
        self.confirmed = 0
        
        self.columnconfigure(0, weight=1)
        
        self.affliation_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="affliation",
            font=("微软雅黑", 14),
            textvariable=self.affliation_value,
            height=30,
            corner_radius=0
        )
        self.affliation_entry.grid(row=0, column=0, padx=(5, 5), pady=(5, 0), sticky="wen")

        self.task_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="task",
            textvariable=self.task_value,
            font=("微软雅黑", 14),
            height=30,
            corner_radius=0
        )
        self.task_entry.grid(row=1, column=0, padx=(5, 5), pady=(5, 0), sticky="we")
        
        self.ddl_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="deadline",
            font=("微软雅黑", 14),
            textvariable=self.deadline_value,
            height=30,
            corner_radius=0
        )
        self.ddl_entry.grid(row=2, column=0, padx=(5, 5), pady=(5, 0), sticky="we")
        self.button_frame = customtkinter.CTkFrame(self, height=30)
        self.button_frame.columnconfigure(0, weight=1)
        self.confirm_btn = customtkinter.CTkButton(
            self.button_frame,
            text="确认",
            command=self.on_confirm
        )
        self.confirm_btn.grid(row=0, column=0, padx=(0, 10), sticky="wens")
        self.cancel_btn = customtkinter.CTkButton(
            self.button_frame,
            text="取消",
            command=self.destroy
        )
        self.cancel_btn.grid(row=0, column=1, padx=(10, 0), sticky="wens")
        self.button_frame.grid(row=3, column=0, padx=(5, 5), pady=(5, 5), sticky="wes")

    def on_confirm(self):
        self.confirmed = 1
        self.destroy()


class TodoPage(customtkinter.CTkFrame):
    displayed = 0
    TODO_LIST_PATH = "./.doddledata/todolist.csv"

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # self.label = customtkinter.CTkLabel(self, text="TODO")
        # self.label.grid(row=0, column=0)
        self.todo_list = []
        self.load_todo_list()

        self.list_frame = ListFrame(
            self,
            parent=self,
            # fg_color="#dfedfc",
            corner_radius=0
        )
        self.list_frame.grid(row=0, column=0, padx=5, pady=(5,0), sticky="nswe")

        self.bottom_bar = BottomBar(
            self,
            # fg_color="#dfedfc",
            corner_radius=0,
            height=30
        )
        self.bottom_bar.grid(row=1, column=0, padx=5, pady=(5,5), sticky="nswe")

        self.resort_list(self.bottom_bar.selected_order.get())


    def load_todo_list(self):
        # affliation,task,deadline,order,done
        try:
            with open(self.TODO_LIST_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.todo_list.append({
                        "affliation": row["affliation"],
                        "task": row["task"],
                        "deadline": row["deadline"],
                        "done": row["done"]=='True',
                        "order": int(row["order"] or 0)
                    })
        except Exception as e:
            print(e)
        # self.todo_list.sort(key=lambda x: x["order"])
        # print(self.todo_list)

    def save_todo_list(self):
        try:
            with open(self.TODO_LIST_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["affliation", "task", "deadline", "done", "order"])
                for todo in self.todo_list:
                    writer.writerow([
                        todo["affliation"],
                        todo["task"],
                        todo["deadline"],
                        todo["done"],
                        todo["order"]
                    ])
        except Exception as e:
            print(e)

    def resort_list(self, choice):
        # 此处是屎，与父对象强耦合
        match choice:
            case 'csv':
                self.todo_list.sort(key=lambda x: (x["done"], x["order"]))
            case 'ddl':
                self.todo_list.sort(
                    key=lambda x: (
                        x["done"],
                        # datetime.strptime(x["deadline"], "%Y-%m-%d %H:%M:%S")
                        parser.parse(x["deadline"])
                    )
                )
            case 'affliation':
                self.todo_list.sort(key=lambda x: (x["done"], x["affliation"]))
        # print(self.todo_list)
        self.list_frame.refresh_list()

    def append_todo(self):
        win = AppendTodoWindow(self)
        self.wait_window(win)
        if not win.confirmed:
            win.destroy()
            return
        # print([val.get() for (_, val) in win.result.items()])
        new_todo = {key: val.get() for key,val in win.result.items()}
        match new_todo["deadline"]:
            case "" | "r" | "remind":
                new_todo["deadline"] = TIME_REMIND
            case "a" | "always":
                new_todo["deadline"] = TIME_ALWAYS
        new_todo["order"] = len(self.todo_list)
        new_todo["done"] = False
        self.todo_list.append(new_todo)
        self.resort_list(self.bottom_bar.selected_order.get())

    def on_item_checked(self, index):
        # print([todo["task"] for todo in self.todo_list])
        self.todo_list[index]["done"] = not self.todo_list[index]["done"]
        # print(f"{index}, {self.todo_list[index]["task"]}")
        self.resort_list(self.bottom_bar.selected_order.get())