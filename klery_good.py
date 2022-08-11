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
	def __init__(self, ol:WD, pc_good_link, pc_price:str):
		pc_good_link = pc_good_link.replace(r'amp;', '')
		self.pictures = []
		self.sizes = []
		self.prices = []
		self.color = ''
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = ''
		self.brand = ''
		echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))
		ol.Get_HTML(pc_good_link)
		#print(f'GOO  {pc_good_link}')
		#ol.driver.get(pc_good_link)
		ol.page_source = ol.driver.page_source
		soup = BeautifulSoup(ol.page_source, features='html5lib')
		self.article = soup.find('div', {'class':'h2'}).text.strip()
		images = soup.find_all('a', {'class':'item thumbnail'})
		for image in images:
			append_if_not_exists(image['href'], self.pictures)
		
		try:
			self.description =  self.description + soup.find('div', {'itemprop':'description'}).text.strip()
		except: pass
		try:
			self.description =  self.description + soup.find('div', {'id':'tab-specification'}).text.replace('\n','|').replace('\t','').replace('\r','').strip()
		except: pass
		self.description = reduce(self.description)
		self.description = self.description.replace("| ",'|')
		self.description = reduce(self.description,"|")
		
		try:
			elements = ol.driver.find_element(by=By.CLASS_NAME, value='owq-option').find_elements(by=By.CLASS_NAME, value='owq-item')
			ii = 0
			for element in elements:
				st = element.get_attribute('innerHTML')
				ii += 1
				#str_to_file(f'table_{ii}.html',st)
				lc_size = sx(st, 'style="display: inline-block;">','<').strip()
				lc_availability_source = sx(st, 'data-quantity="','"')
				lc_price = sx(st, '<td class="price hidden-xs">', '<').strip().replace(' ','').replace('р.','')
				if len(lc_price)==0:
					lc_price = sx(st, '<td class="price hidden-xs"><span class="special">', '<').strip().replace(' ','').replace('р.','')
				if int(lc_availability_source) == 0:
					lc_availability = 'Нет в наличии'
				if 8 >= int(lc_availability_source) > 0:
					lc_availability = f'Осталось {lc_availability_source} шт.'
					self.sizes.append(lc_size + ' ' + lc_availability)
					self.prices.append(lc_price)
				if int(lc_availability_source) >= 9:
					lc_availability = 'В наличии'
					self.sizes.append(lc_size)
					self.prices.append(lc_price)
				echo(style('     Размер: '+lc_size, fg='bright_cyan')+\
					style(f'      {lc_availability}  ({lc_availability_source})', fg='bright_white') + \
					style( '       Цена: ', fg='bright_yellow') + style( lc_price, fg='bright_red'))
		except:
			pass


		return
		sizes_prices_json_source = sx(ol.page_source, "ro_params['ro_data'] = [", "];")
		str_to_file('j.json',sizes_prices_json_source)
		data = json.loads(sizes_prices_json_source)
		ids_list = find_values('relatedoptions_id', sizes_prices_json_source)
		ll = {} # словарь идентификаторов,  цен и наличия
		for id in ids_list:
			#print(data['ro'][id]['ean'],  data['ro'][id]['product_stock_status'],  data['ro'][id]['price'] )
			ll[data['ro'][id]['ean']]=[data['ro'][id]['product_stock_status'],  data['ro'][id]['price']]
		rows = soup.find(name = 'div', attrs={'class':'owq-option'}).find_all(name='tr', attrs={'class':'owq-item'})
		#ii = 0
		for row in rows: 
			#ii += 1
			#str_to_file(f'table_{ii}.html',str(row))
			lc_id = sx(str(row), '<span calss="ean" style="display:none;">','<')
			lc_size = sx(str(row), 'type="checkbox" value=""/>','<').strip()
			lc_availability = ll[lc_id][0]
			lc_availability_h = sx(str(row), '<td data-quantity="1" style="color:green;font-family:Arial;">','<').strip()
			lc_price = str(int(ll[lc_id][1].replace('.0000','')))
			echo(style('Внутренний идентфикатор товара:  ', fg='bright_green') +  style(lc_id, fg='bright_blue') + style('     Размер: '+lc_size, fg='bright_cyan')+\
				style('      ' + lc_availability_h, fg='bright_white') + style( '       Цена: ', fg='bright_yellow') + style( lc_price, fg='bright_red'))
			if lc_availability == 'В наличии':
				self.sizes.append(lc_size)
				self.prices.append(lc_price)


		return

