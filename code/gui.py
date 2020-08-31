# import module
import tkinter.font as tkFont
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog, dialog
import os
from pandas import ExcelWriter, DataFrame
from crawler import *

window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('mini Bloomberg')
window.geometry('500x500')
window.configure(background='ghost white')
# 設定字體
fontStyle = tkFont.Font(family="MS Sans Serif", size=32, weight="bold")
fontStyle2 = tkFont.Font(family="MS Sans Serif", size=24, weight="bold")

# 標題
header_label = tk.Label(window, text='Mini Bloomberg', font=fontStyle)
header_label.configure(background='ghost white')
header_label.pack()


def crawl():
    global gdp_data
    global foreign_data
    global raw_data
    global bond_data
    global pmi_data
    global rate_data
    global putcall_data
    global contracts_data
    global elec_data
    global indexUSA_data
    global indexTW_data
    bond_lst = BOND()
    info.insert('insert', 'BOND Finish!\n')
    window.update()
    foreign_lst = FOREX()
    info.insert('insert', 'FOREX Finish!\n')
    window.update()
    raw_lst = RAW()
    info.insert('insert', 'RAW Finish!\n')
    window.update()
    gdp_lst, pmi_lst = GDPandPMI()
    info.insert('insert', 'GDP and PMI Finish!\n')
    window.update()
    rate_lst = companyBOND()
    info.insert('insert', 'companyBOND Finish!\n')
    window.update()
    electrionic_lst = TWelectronic()
    info.insert('insert', 'TW ELECTRONIC Finish!\n')
    window.update()
    putcall, contracts_lst = TWFUTURE()
    info.insert('insert', 'TW FUTURE Finish!\n')
    window.update()
    indexUSA_lst, indexTW_lst = VIX()
    info.insert('insert', 'VIX Finish!\n')
    window.update()
    info.insert('insert', 'DONE!')
    window.update()

    # 將資料轉換成表格
    foreign_data = {'標的': [item[0] for item in foreign_lst],
                    '價格': [item[1] for item in foreign_lst],
                    '漲跌': [item[2] for item in foreign_lst]}
    raw_data = {'標的': [item[0] for item in raw_lst],
                '價格': [item[1] for item in raw_lst],
                '漲跌': [item[2] for item in raw_lst]}
    bond_data = {'標的': [item[0] for item in bond_lst],
                 '利率': [item[1] for item in bond_lst]}
    gdp_data = {'國家': [item[0] for item in gdp_lst],
                '季度': [item[1] for item in gdp_lst],
                '數值': [item[2] for item in gdp_lst]}
    pmi_data = {'國家': [item[0] for item in pmi_lst],
                '季度': [item[1] for item in pmi_lst],
                '數值': [item[2] for item in pmi_lst]}
    rate_data = {'標的': [item[0] for item in rate_lst],
                 '時間': [item[1] for item in rate_lst],
                 '利率': [item[2] for item in rate_lst]}
    putcall_data = {'日期': [item[0] for item in putcall],
                    '賣權未平倉量': [item[4] for item in putcall],
                    '買權未平倉量': [item[5] for item in putcall],
                    '買賣權未平倉量比率%': [item[6] for item in putcall]}
    contracts_data = {'未平倉餘額(多方口數)': [item[0] for item in contracts_lst],
                      '未平倉餘額(空方口數)': [item[2] for item in contracts_lst],
                      '未平倉餘額(多空淨額口數)': [item[4] for item in contracts_lst]}
    elec_data = {'本期(上:出口,下:進口)': [item[0] for item in electrionic_lst],
                 '去年同期or上期': [item[1] for item in electrionic_lst],
                 '增減比例': [item[2] for item in electrionic_lst]}
    indexUSA_data = {'標的': [item[0] for item in indexUSA_lst],
                     '價格': [item[1] for item in indexUSA_lst],
                     '漲跌': [item[2] for item in indexUSA_lst]}
    indexTW_data = {'標的': [item[0] for item in indexTW_lst],
                    '價格': [item[1] for item in indexTW_lst]}

    # 轉成dataframe
    foreign_data = DataFrame(foreign_data)
    raw_data = DataFrame(raw_data)
    bond_data = DataFrame(bond_data)
    gdp_data = DataFrame(gdp_data)
    pmi_data = DataFrame(pmi_data)
    rate_data = DataFrame(rate_data)
    putcall_data = DataFrame(putcall_data)
    contracts_data = DataFrame(contracts_data)
    elec_data = DataFrame(elec_data)
    indexUSA_data = DataFrame(indexUSA_data)
    indexTW_data = DataFrame(indexTW_data)
    tkinter.messagebox.showinfo(title='Finish', message='完成！')


file_path = ''


def save_file():
    global file_path

    file_path = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                                        ("All files", "*.*")))

    # 輸出excel檔
    write = ExcelWriter(file_path)
    gdp_data.to_excel(write, index=False)
    pmi_data.to_excel(write, startrow=4, index=False)
    elec_data.to_excel(write, startrow=10, index=False)
    raw_data.to_excel(write, startrow=20, index=False)
    bond_data.to_excel(write, startrow=26, index=False)
    rate_data.to_excel(write, startrow=31, index=False)
    foreign_data.to_excel(write, startrow=35, index=False)
    indexUSA_data.to_excel(write, startrow=40, index=False)
    indexTW_data.to_excel(write, startrow=45, index=False)
    contracts_data.to_excel(write, startrow=50, index=False)
    putcall_data.to_excel(write, startrow=54, index=False)
    write.save()


info = tk.Text(window, font=fontStyle2, fg='red', width=20, height=10)
info.pack()

Button = tk.Button(window, text='執行', width=15, height=2, font=fontStyle,
                   command=lambda: [crawl(), Button.forget(), Button2.pack()])
Button.pack()

Button2 = tk.Button(window, text='儲存檔案', width=15, height=2, font=fontStyle,
                    command=save_file)


# run
window.mainloop()
