from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from bs4 import BeautifulSoup as BS
from lxml import html
import requests
from click import echo, style
from fake_useragent import UserAgent


class WD:
	def init(self):
		self.site_url = 'https://klery.ru/'
		config = configparser.ConfigParser()
		
	def __init__(self):
		self.init()

	def __del__(self):
		try:
			pass
		except: pass

	def Get_HTML(self, curl):
		r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
		self.page_source = r.text
		if False:
			if os.path.isfile('catalog.html'):
					echo(style('Загружен локальный файл: ', fg='bright_red') + style('catalog.html', fg='red'))
					self.page_source = file_to_str('catalog.html')
			else:
				r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
				self.page_source = r.text
				str_to_file('catalog.html', self.page_source)
		else:
			r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
			self.page_source = r.text
		return self.page_source

	def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link):
		echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white'))
		list_of_pages =  self.Get_List_of_Catalog_Pages(pc_link)
		echo(style(f'{list_of_pages}', fg='green'))
		ll_catalog_items = []
		for link in list_of_pages:
			self.Get_HTML(pc_link)
			soup = BS(self.page_source, features='html5lib')
			items = soup.find_all('div', {'class': 'caption2'})
			for item in items:
				lc_link = sx(str(item),'href="','"')
				echo(style('Товар каталога: ', fg='bright_green') + style(lc_link, fg='green'))
				append_if_not_exists(lc_link, ll_catalog_items)
		return ll_catalog_items

	def Get_List_of_Catalog_Pages(self, pc_link:str) -> list:
		self.Get_HTML(pc_link)
		soup = BS(self.page_source, features='html5lib')
		lc_paginator =str(soup.find_all('ul',{'class':'pagination'}))
		if len(lc_paginator)==0:
			return [pc_link]
		else:
			soup = BS(lc_paginator, features='html5lib')
			link = soup.find(lambda tag:((tag.name=="a") and ("|" in tag.text)))
			page_count = int(sx(str(link),'?page=','"'))
			ll = []
			for i in range(1,page_count+1):
				lc_link_on_page = pc_link + '?page='+str(i)
				ll.append(lc_link_on_page)
			return ll

	def Write_To_File(self, cfilename):
		file = open(cfilename, "w", encoding='utf-8')
		file.write(self.page_source)
		file.close()


def Login():
	return WD()


#colorama.init()

#wd = Login()
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://klery.ru/maski-zashchitnye/'))

#print(wd.Get_List_of_Catalog_Pages('https://klery.ru/maski-zashchitnye/'))