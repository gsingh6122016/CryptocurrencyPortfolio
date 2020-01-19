from tkinter import *
from tkinter import messagebox ,Menu
import requests
import json
import sqlite3

pycrypto  = Tk()
pycrypto.title("My Crypto Portfolio")

con = sqlite3.connect('coin.db')
cObj = con.cursor()

cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY , name TEXT ,price REAL ,amount INTEGER ) ")
con.commit()

def reset() :
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_navigation()
    app_header()
    my_portfolio()

def clear_all() :
    cObj.execute("DELETE FROM coin")
    con.commit()

    messagebox.showinfo("Notification" ,"Operation Successfull!")
    reset()

def close() :
    pycrypto.destroy()

def app_navigation() :
    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label = 'Clear Portfolio' ,command = clear_all)
    file_item.add_command(label = 'Close Application' ,command = close)
    menu.add_cascade(label = 'File' ,menu = file_item)
    pycrypto.config(menu = menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=091b6634-7df8-4b74-8da7-4fa40d7c43df")
    api = json.loads(api_request.content)

    cObj.execute("SELECT * FROM coin")
    coins = cObj.fetchall()

    def font_color(val):
        if val >= 0 :
            return "green"
        else :
            return "red"

    def insert_coin() :
        cObj.execute("INSERT INTO coin(name ,price ,amount) VALUES(? ,? ,?)" ,(symbol_txt.get(), price_txt.get(), owned_txt.get()))
        con.commit()

        reset()
        messagebox.showinfo("Notification" ,"Coin Added To Portfolio Successfully!")


    def update() :
        cObj.execute("UPDATE coin SET name=? ,price=? ,amount=? WHERE id=? " ,(update_symbol.get() ,update_price.get() ,update_owned.get() ,update_id.get()))
        con.commit()

        reset()
        messagebox.showinfo("Notification" ,"Coin Updated To Portfolio Successfully!")


    def Delete_coin() :
        cObj.execute("DELETE FROM coin WHERE id=? " ,(delete_id.get(),))
        con.commit()

        reset()
        messagebox.showinfo("Notification" ,"Coin Deleted From Portfolio Successfully!")


    net_profit = 0
    total_current_value = 0
    net_amount_paid = 0
    row_val = 1
    for i in range(0, 300):
      for coin in coins :
        if coin[1] == api["data"][i]["symbol"]:
          total_paid = coin[3] * coin[2]
          current_value =  api["data"][i]["quote"]["USD"]["price"] * coin[3]
          profit_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[2]
          total_profit = profit_per_coin * coin[3]
          net_profit += total_profit
          total_current_value += current_value
          net_amount_paid += total_paid

          portfolio_id = Label(pycrypto ,text = coin[0] ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          portfolio_id.grid(row = row_val ,column = 0,sticky = N+W+E+S)
          name = Label(pycrypto ,text = api["data"][i]["symbol"] ,bg = "grey" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          name.grid(row = row_val ,column = 1,sticky = N+W+E+S)
          price = Label(pycrypto ,text = "${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]) ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          price.grid(row = row_val ,column = 2,sticky = N+W+E+S)
          no_coins = Label(pycrypto ,text = coin[3] ,bg = "grey" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          no_coins.grid(row = row_val ,column = 3,sticky = N+W+E+S)
          amount_paid = Label(pycrypto ,text =  "${0:.2f}".format(total_paid) ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          amount_paid.grid(row = row_val ,column = 4,sticky = N+W+E+S)
          current_val = Label(pycrypto ,text = "${0:.2f}".format(current_value) ,bg = "grey" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          current_val.grid(row = row_val ,column = 5,sticky = N+W+E+S)
          pl_coin = Label(pycrypto ,text = "${0:.2f}".format(profit_per_coin) ,bg = "white" ,fg = font_color(float("{0:.2f}".format(profit_per_coin))) ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          pl_coin.grid(row = row_val ,column = 6,sticky = N+W+E+S)
          total_pl = Label(pycrypto ,text = "${0:.2f}".format(total_profit) ,bg = "grey" ,fg = font_color(float("{0:.2f}".format(total_profit))) ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
          total_pl.grid(row = row_val ,column = 7,sticky = N+W+E+S)

          row_val += 1
#add coin
    symbol_txt = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    symbol_txt.insert(END, 'Enter Symbol')
    symbol_txt.grid(row = row_val + 2 ,column = 4 )
    price_txt = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    price_txt.insert(END, 'Enter Price')
    price_txt.grid(row = row_val + 2 ,column = 5 )
    owned_txt = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    owned_txt.insert(END, 'Enter Coins Owned')
    owned_txt.grid(row = row_val + 2 ,column = 6 )
    add_coin = Button(pycrypto ,text = "Add Coin" , command = insert_coin ,bg = "grey" ,fg = "blue" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    add_coin.grid(row = row_val + 2 ,column = 7,sticky = N+W+E+S)
#update
    update_id = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    update_id.insert(END, 'Enter ID')
    update_id.grid(row = row_val + 3 ,column = 3 )
    update_symbol = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    update_symbol.insert(END, 'Enter Symbol')
    update_symbol.grid(row = row_val + 3 ,column = 4 )
    update_price = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    update_price.insert(END, 'Enter Price')
    update_price.grid(row = row_val + 3 ,column = 5 )
    update_owned = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    update_owned.insert(END, 'Enter Coins Owned')
    update_owned.grid(row = row_val + 3 ,column = 6 )
    update_coin= Button(pycrypto ,text = "Update Coin" , command = update ,bg = "grey" ,fg = "blue" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    update_coin.grid(row = row_val + 3 ,column = 7,sticky = N+W+E+S)

#delete
    delete_id = Entry(pycrypto , borderwidth = 2 ,relief = "groove" )
    delete_id.insert(END, 'Enter ID')
    delete_id.grid(row = row_val + 4 ,column = 6 )
    delete_coin= Button(pycrypto ,text = "Delete Coin" , command = Delete_coin ,bg = "grey" ,fg = "blue" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    delete_coin.grid(row = row_val + 4 ,column = 7,sticky = N+W+E+S)


    total_amount_paid = Label(pycrypto ,text = "${0:.2f}".format(net_amount_paid) ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    total_amount_paid.grid(row = row_val ,column = 4,sticky = N+W+E+S)
    total_current_val = Label(pycrypto ,text = "${0:.2f}".format(total_current_value) ,bg = "grey" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    total_current_val.grid(row = row_val ,column = 5,sticky = N+W+E+S)
    net_pl = Label(pycrypto ,text = "${0:.2f}".format(net_profit) ,bg = "grey" ,fg = font_color(float("{0:.2f}".format(net_profit))) ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    net_pl.grid(row = row_val ,column = 7,sticky = N+W+E+S)

    api = ""

    refresh = Button(pycrypto ,text = "refresh" , command = reset ,bg = "grey" ,fg = "blue" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
    refresh.grid(row = row_val + 1 ,column = 7,sticky = N+W+E+S)


def app_header():
    portfolio_id = Label(pycrypto ,text = "Portfolio ID" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    portfolio_id.grid(row = 0 ,column = 0,sticky = N+W+E+S)
    name = Label(pycrypto ,text = "Coin Name" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    name.grid(row = 0 ,column = 1,sticky = N+W+E+S)
    price = Label(pycrypto ,text = "price" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    price.grid(row = 0 ,column = 2,sticky = N+W+E+S)
    no_coins = Label(pycrypto ,text = "Coin Owened" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    no_coins.grid(row = 0 ,column = 3,sticky = N+W+E+S)
    amount_paid = Label(pycrypto ,text = "Total Amount Paid" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    amount_paid.grid(row = 0 ,column = 4,sticky = N+W+E+S)
    current_val = Label(pycrypto ,text = "Current value" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    current_val.grid(row = 0 ,column = 5,sticky = N+W+E+S)
    pl_coin = Label(pycrypto ,text = "P/L Per Coin" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    pl_coin.grid(row = 0 ,column = 6,sticky = N+W+E+S)
    total_pl = Label(pycrypto ,text = "Total P/L with Coin" ,bg = "#142E54" ,fg = "white" ,font = "Lato 12 bold" ,padx = "5" ,pady = "5" ,borderwidth = 2 ,relief = "groove")
    total_pl.grid(row = 0 ,column = 7,sticky = N+W+E+S)

app_navigation()
app_header()
my_portfolio()

pycrypto.mainloop()
cObj.close()
con.close()
print("program Completed")
