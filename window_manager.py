from tkinter import *

class Window:
    def __init__(self, sm, bot):
        print('init window')
        self.sm = sm
        self.bot = bot
        self.window = Tk()
        Canvas(self.window, width=250, height=100, bg='ivory').pack(side=TOP, padx=5, pady=5)
        Button(self.window, text ='Start browser', command=sm.start_browser).pack(side=LEFT, padx=5, pady=5)
        Button(self.window, text ='Introduce', command=bot.introduce).pack(side=RIGHT, padx=5, pady=5)
        Button(self.window, text ='Get URL', command=sm.get_url).pack(side=RIGHT, padx=5, pady=5)
        Button(self.window, text ='Listen', command=sm.start_listening).pack(side=RIGHT, padx=5, pady=5)
        Button(self.window, text ='Stop listen', command=sm.stop_listening).pack(side=RIGHT, padx=5, pady=5)
        Button(self.window, text ='Connect', command=sm.connect_test).pack(side=RIGHT, padx=5, pady=5)
        Button(self.window, text ='Restart listen', command=sm.start_listening).pack(side=RIGHT, padx=5, pady=5)

        Button(self.window, text ='TEST', command=bot.introduce).pack(side=RIGHT, padx=5, pady=5)
        self.window.mainloop()
