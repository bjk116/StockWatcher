import tkinter as tk
from tkinter import Label, Button, StringVar
from tkinter.messagebox import showinfo
import requests


class App(tk.Tk):
    components = []
    def __init__(self):
        super().__init__()
        # Runs on startrup our change to initalize the winodw\app
        self.title("Stock Watcher")
        self.geometry('800x800')
        background_color = '#001f3f'
        self.configure(bg=background_color)
        self.title = Label(self, text="Stock Watcher 1.0",
                bg=background_color,
                fg="#ffffff",
                font='android 20 bold')
        self.title.pack()
        self.button = Button(self, text='Click me!')
        self.button['command'] = self.refreshStockPrices
        self.button.pack()
        self.stock_1_text = StringVar()
        self.stock_1_text.set("")
        self.stock_1 = Label(self, textvariable=self.stock_1_text)
        self.stock_2_text = StringVar()
        self.stock_2_text.set("")
        self.stock_2 = Label(self, textvariable=self.stock_2_text)
        self.stock_3_text = StringVar()
        self.stock_3_text.set("")
        self.stock_3 = Label(self, textvariable=self.stock_3_text)
        self.stock_4_text = StringVar()
        self.stock_4_text.set("")
        self.stock_4 = Label(self, textvariable=self.stock_4_text)
        self.stock_1.pack()
        self.stock_2.pack()
        self.stock_3.pack()
        self.stock_4.pack()
        self.refreshStockPrices()

    def refreshStockPrices(self):
        tellAPIToUpdate = requests.post('http://127.0.0.1:8000/scrape')
        latest_prices_attempt = requests.get('http://127.0.0.1:8000/latest')
        latest_prices_data = latest_prices_attempt.json()['data']
        for i, row in enumerate(latest_prices_data,1):
            currentComponent = getattr(self, f'stock_{i}_text')
            textToWrite = f"{row['symbol']:} ${row['price']} @ {row['t_stamp']}"
            currentComponent.set(textToWrite)

    def button_clicked(self):
        self.refreshStockPrices()

if __name__ == "__main__":
    app = App()
    app.mainloop()