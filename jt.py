import json
from my_library import *



with open("sizes_prices_json_source.json", "r") as read_file:
	data = json.load(read_file)

ids_list = find_values('relatedoptions_id', file_to_str('sizes_prices_json_source.json'))
ll = {}
for id in ids_list:
	#print(data['ro'][id]['ean'],  data['ro'][id]['product_stock_status'],  data['ro'][id]['price'] )
	ll[data['ro'][id]['ean']]=[data['ro'][id]['product_stock_status'],  data['ro'][id]['price']]

print(ll)
#print(data['relatedoptions_id'])
