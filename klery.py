from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sqlite3
from os import system
from my_library import *
import sys
from klery_driver import *
from klery_good import *
import colorama
from colorama import Fore, Back, Style
from click import echo, style

def unload_one_good(dw:WD, lc_link_on_good: str, pc_price:str):
    lo_good = Good(dw, lc_link_on_good, pc_price)
    print(Fore.YELLOW + "Название:" + Fore.LIGHTGREEN_EX, lo_good.name, Fore.RESET)
    print(Fore.YELLOW + "Артикул:" + Fore.LIGHTGREEN_EX, lo_good.article, Fore.RESET)
    print(Fore.YELLOW + "Цены:" + Fore.LIGHTGREEN_EX, lo_good.prices, Fore.RESET)
    print(Fore.YELLOW + "Описание:" + Fore.LIGHTGREEN_EX, lo_good.description, Fore.RESET)
    print(Fore.YELLOW + "Картинки:" + Fore.LIGHTGREEN_EX, lo_good.pictures, Fore.RESET)
    print(Fore.YELLOW + "Размеры:" + Fore.LIGHTGREEN_EX, lo_good.sizes, Fore.RESET)
    return lo_good




########################################################################################################################
########################################################################################################################
colorama.init()

########################################################################################################################




if sys.argv[1] == 'good':
    wd = Login()
    print(sys.argv[1])
    print(sys.argv[2])
    good = unload_one_good(wd, sys.argv[2], sys.argv[3])


if sys.argv[1] == 'catalog':
    wd = Login()
    links_list = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
    ln_total = len(links_list)
    ln_counter = 0
    price = Price(sys.argv[3])
    for link in links_list:
        ln_counter = ln_counter + 1
        print('Товар: ', link, Fore.LIGHTWHITE_EX, ln_counter, '/', ln_total, Fore.RESET)
        if is_price_have_link(sys.argv[3], link):
            print('Товар уже имеется в прайсе')
            continue
        #try:
        lo_good = unload_one_good(wd, link, sys.argv[3])
        #except: 
        #    print(Fore.RED,'ОШИБКА ПРИ ЗАГРУЗКЕ ТОВАРА',Fore.RESET)
        #    continue
        if int(lo_good.price)>0:
            price.add_good('',
                                prepare_str(lo_good.name + ' ' + lo_good.article),
                                prepare_str(lo_good.description),
                                prepare_str(str(round(float(lo_good.price) * float(sys.argv[4]),2))),
                                '15',
                                prepare_str(link),
                                prepare_for_csv_non_list(lo_good.pictures),
                                prepare_for_csv_list(lo_good.sizes)
                                )
            price.write_to_csv(sys.argv[3])

if sys.argv[1] == 'reverse':
    reverse_csv_price(sys.argv[2])

if sys.argv[1] == 'ansi':
    convert_file_to_ansi(sys.argv[2] + '_reversed.csv')

