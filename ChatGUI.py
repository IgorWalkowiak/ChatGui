import tkinter as tk
import tkinter.ttk as ttk
from time import localtime, strftime

mainWindow = tk.Tk()


class ChatNotebookTab(tk.Frame):
    NUMBER_OF_LINE_IN_CHAT = 35
    def __init__(self, name, outputFun, localUser, *args, **kwargs):
        ttk.Notebook.__init__(self, *args, **kwargs)
        labels = []
        self.tabUser = name
        self.localUser = localUser

        for row_index in range(ChatNotebookTab.NUMBER_OF_LINE_IN_CHAT):
            tk.Grid.rowconfigure(self, row_index, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            labels.append(tk.Label(self))
            labels[-1].grid(row=row_index, column=0, sticky="w", padx=3, pady=0)
        self.outputHandler = outputFun
        self.input = tk.StringVar()
        self.textInput = tk.Entry(self, width=15, textvariable=self.input)
        self.textInput.grid(row=ChatNotebookTab.NUMBER_OF_LINE_IN_CHAT+1, column=0, sticky="sew")
        self.textInput.bind("<Return>", self.__onReturnKey)

    def __onReturnKey(self, event):
        print("ENTER")
        inputText = self.input.get()
        if(inputText == ""):
            return
        self.outputHandler(inputText)
        self.addText("right", inputText)
        self.textInput.delete(0, "end")

    def __moveMessagesUp(self):
        for _ in range(2):
            for i in range(len(self.grid_slaves())-1, 1, -1):
                labelDown = self.grid_slaves()[i-1]
                labelUp = self.grid_slaves()[i]
                labelUp["text"] = labelDown["text"]
                labelUp["font"] = labelDown["font"]
                labelUp.grid(sticky=(labelDown.grid_info()['sticky']))

    def addText(self, side, text):
        self.__moveMessagesUp()

        if side == "left":
            self.grid_slaves()[2]["text"] = self.tabUser + strftime(" %H:%M:%S :", localtime())
            self.grid_slaves()[2].grid(sticky="w")
            self.grid_slaves()[1].grid(sticky="w")
        elif side == "right":
            self.grid_slaves()[2]["text"] = self.localUser + strftime(" %H:%M:%S :", localtime())
            self.grid_slaves()[2].grid(sticky="e")
            self.grid_slaves()[1].grid(sticky="e")

        self.grid_slaves()[2]["font"] = ("System", 7)
        self.grid_slaves()[1]["text"] = text
        self.grid_slaves()[1]["font"] = ("Times", 12)

class ChatNotebook(ttk.Notebook):
    def __init__(self, outputFun, localUser, *args, **kwargs):
        self.__init_custom_style()
        self.localUser = localUser
        self.chatUsers = {}
        self.outputFun = outputFun
        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def __inputHandler(self, text):
        toNick = self.tab(self.select(), "text")
        self.outputFun(toNick, text)

    def addTab(self, name, **kwargs):
        if name not in self.chatUsers.keys():
            bookmark = ChatNotebookTab(name, self.__inputHandler, self.localUser)
            self.chatUsers[name] = bookmark
            self.add(bookmark, text=name)
        if kwargs["autoActiv"] == True:
            self.select(self.chatUsers[name]) #activate new added tab

    def newMessageFrom(self, message, user):
        if user not in self.chatUsers.keys():
            self.addTab(user, autoActiv=False)
        self.chatUsers[user].addText("left", message)

    def on_close_release(self, event):
        element = self.identify(event.x, event.y)
        index = self.index("@{},{}".format(event.x, event.y))
        tab = self.tab("@{},{}".format(event.x, event.y))
        print(tab["text"])
        if "closeButton" in element:
            del self.chatUsers[tab["text"]]
            self.forget(index)


    def __init_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
            iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/
            9hAAAABHNCSVQICAgIfAhkiAAAAAFzUkdCAK7OHOkA
            AAAEZ0FNQQAAsY8L/GEFAAAACXBIWXMAAA7EAAAOxA
            GVKw4bAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2Nh
            cGUub3Jnm+48GgAAAodJREFUOE+dk09IVFEUxn/vzZ
            gzbxyZcSJbBFmWClIQUVRCpkhEC8EWERTUqkwhoVa1
            axO0KBGSElqYFIQLKQNpJCwXEv1DKAS1LGvVRKOj45
            t5Ns68zn3zJ41WHbjcy33v+853znePljJT9tjuERKfT
            HS3BpqsXBSndYY3RSjOuHI3YNs2mbRNaEspbeEWtBc1
            YducjOPyuLARcEZDc9nOz38TZNQ3TX2zSSVX2FAdRHc
            y58C/LC/oGZaTHsnkYJxQ56WYoU6y+2TXKPK6iX5ZRN
            eU7By4KdzHkfgNDtx9TNLyO0BFPB8JcPZ6H1ffXuJyX
            2eBRHfJ0lTNIs3jMzEav8J0iPVHZ6i/108iVcrc9wAd
            3XfYXv8BZssJ7Z/CH1wSclWOEAiVyLaxTB/RB7UQsGD
            eS1nTLHu6Bmm/1svWuklYlKylCWYG9zoKsr0QHU+9j5
            yTkqtkH7r/kGDDN4h5QFrCwjikpH5/gtlX1XS2nidYH
            iuYlVUgoS68njjPT50gMlAFnhWw3LBcJHakmBjexc1z
            a8EqCgT/GwWCfAkNUkL5selsdqVCsisVtYfHudhz23F
            ktcUOgbpQNh7s7f9TvzTzx5NK3o/udJpH3KBi3xQXbv
            VgLhgFkqyCnI2hkxNZcDDJ3LMK3nQ0033lDJ/HaoTEF
            CcMKptfUxIwhSDbCF297byNiZHNUBXl51Alo6ePYxQt
            UrYxRld7Kx9Hd0BFhOjLauLzJY6NCqsNuQfs1a9xnSe
            R2y08mewsrEu7HNmGlGIu+BwF6o2qodKNbT4yVlrgto
            CSUo5OsddaY5U6lwSkD/JXHqyGSU2kXveuEV+Nn8yKe
            vWycpP4r9Cl1HxmNYlt4RZ+A2lxGPUXcvbXAAAAAElF
            TkSuQmCC
            '''))
        style.element_create("closeButton", "image", "img_close",
                            ("active", "img_close"), border=16, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "children": [
                    ("CustomNotebook.padding", {
                        "children": [
                            ("CustomNotebook.focus", {
                                "children": [
                                    ("CustomNotebook.label", {"side": "left"}),
                                    ("CustomNotebook.closeButton", {"side": "left"}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

class UserBrowser():
    def __init__(self, *args, **kwargs):
        self.scroll = tk.Scrollbar(mainWindow, jump=1, width=20)
        self.scroll.pack(side="left", fill="y")
        self.availableUsers = []
        self.te = tk.Label(mainWindow, text='Users: ')
        self.te.pack()

        self.listbox = tk.Listbox(mainWindow, font=("Times", 18, "bold"),
            width=21, height=10, bd=5, fg="black", yscrollcommand=self.scroll.set)
        self.listbox.pack(side="left", fill="y")
        self.listbox.bind("<Double-Button-1>", self.handleDoubleClick)


    def doubleTabClickHandlerSubscribe(self, handler):
        self.doubleClickHandler = handler

    def addAvailableUser(self, name):
        if name not in self.availableUsers:
            self.availableUsers.append(name)
            self.listbox.insert("end", name)

    def handleDoubleClick(self, event):
        selectedBox = self.listbox.get("active")
        if len(selectedBox) == 0:
            return
        print(selectedBox)
        self.doubleClickHandler(selectedBox, autoActiv=True)

class ChatGUI:
    def __init__(self, width, height, localUser, userOutputHandler):
        self.notebook = ChatNotebook(userOutputHandler, localUser, width=width, height=height)
        self.notebook.pack(side="right", fill="both", expand=1)

        self.userBrowse = UserBrowser()
        self.userBrowse.doubleTabClickHandlerSubscribe(self.notebook.addTab)

    def updateAvailableUsers(self, users):
        for user in users:
            self.userBrowse.addAvailableUser(user)

    def newMessageFrom(self, message, user):
        self.userBrowse.addAvailableUser(user)
        self.notebook.newMessageFrom(message, user)
