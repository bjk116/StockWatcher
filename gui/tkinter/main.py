from tkinter import *

def button_clicked():
    print("You clicked me!")

def run():
    root = Tk()
    root.title("Stock Watcher")
    root.geometry('800x800')
    background_color = '#001f3f'
    root.configure(bg=background_color)
    title = Label(root, text="Stock Watcher 1.0",
                bg=background_color,
                fg="#ffffff",
                font='android 20 bold')
    my_button = Button(root, text="Click me")
    title.pack()
    my_button.pack()
    root.mainloop()

if __name__ == "__main__":
    run()