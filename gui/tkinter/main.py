from tkinter import *

def button_clicked():
    print("You clicked me!")

class Table:
    def __init_(self, root, data):
        for i in range(len(data)):
            for j in range(len(data[0])):
                self.e = Entra(root, width(20, fg='blue', font=('Arial', 16, 'bold')))
                self.e.grid(row=i,column=j)
                self.e.insert(END,data[i][j])

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
    my_button = Button(root, text="Click me", command=button_clicked)
    title.pack()
    my_button.pack()
    root.mainloop()

if __name__ == "__main__":
    run()