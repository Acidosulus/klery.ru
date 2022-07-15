import base64
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
from klery_driver import *
import colorama
from colorama import Fore, Back, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import request
from urllib.parse import quote
import uuid
import configparser
import requests
from pathlib import Path
import threading
from bs4 import BeautifulSoup
from lxml import html
from click import echo, style
from fake_useragent import UserAgent

def poiskpers(url):
	geourl = '{0}'.format(quote(url))
	return geourl

class Good:
	def __init__(self, ol:WD, pc_link, pc_price:str):
		pc_link = pc_link.replace(r'amp;', '')
		self.pictures = []
		self.sizes = []
		self.prices = []
		self.color = ''
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = ''
		self.brand = ''
		echo(style('Товар: ', fg='bright_yellow') + style(pc_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))
		ol.Get_HTML(pc_link)
		soup = BeautifulSoup(ol.page_source, features='html5lib')

		self.article = soup.find('div', {'class':'h2'}).text.strip()

		images = soup.find_all('a', {'class':'item thumbnail'})
		for image in images:
			append_if_not_exists(image['href'], self.pictures)
		
		self.description =  soup.find('div', {'itemprop':'description'}).text.strip() + \
							soup.find('div', {'id':'tab-specification'}).text.replace('\n','|').replace('\t','').replace('\r','').strip()
		self.description = reduce(self.description)
		self.description = self.description.replace("| ",'|')
		self.description = reduce(self.description,"|")
		
		sizes_prices_json_source = sx(ol.page_source, "ro_params['ro_data'] = [", "];")
		data = json.loads(sizes_prices_json_source)
		ids_list = find_values('relatedoptions_id', file_to_str('sizes_prices_json_source.json'))
		ll = {} # словарь идентификаторов,  цен и наличия
		for id in ids_list:
			#print(data['ro'][id]['ean'],  data['ro'][id]['product_stock_status'],  data['ro'][id]['price'] )
			ll[data['ro'][id]['ean']]=[data['ro'][id]['product_stock_status'],  data['ro'][id]['price']]
		rows = soup.find(name = 'div', attrs={'class':'owq-option'}).find_all(name='tr', attrs={'class':'owq-item'})
		for row in rows:
			lc_id = sx(str(row), '<span calss="ean" style="display:none;">','<')
			lc_size = sx(str(row), 'type="checkbox" value=""/>','<').strip()
			lc_availability = ll[lc_id][0]
			lc_price = str(int(ll[lc_id][1].replace('.0000','')))
			echo(style('Внутренний идентфикатор товара:  ', fg='bright_green') +  style(lc_id, fg='bright_blue') + style('     Размер: '+lc_size, fg='bright_cyan')+\
				style('      ' + lc_availability, fg='bright_white') + style( '       Цена: ', fg='bright_yellow') + style( lc_price, fg='bright_red'))
			if lc_availability == 'В наличии':
				self.sizes.append(lc_size)
				self.prices.append(lc_price)


		return

