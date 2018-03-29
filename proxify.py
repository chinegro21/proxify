# Created by Somdev Sangwan
# Taken from https://github.com/UltimateHackers/proxify/blob/master/proxify.py
# with slight modifications by Marcus Agard
# His installation instructions don't work



import requests
import re
import random

def make_request(): # Function to extract proxy data. Returns list.
	response = requests.get('https://free-proxy-list.net/').text # makes request to the site and retrieves source code
	# Regex to extract "valuable stuff" from the source code.
	return re.findall(r"<tr><td>[^<]*</td><td>[^<]*</td><td>[^<]*</td><td class='hm'>[^<]*</td><td>[^<]*</td><td class='hm'>[^<]*</td><td class='hx'>[^<]*</td><td class='hm'>[^<]*</td></tr>", response)

def one(): # function to fetch one proxy. Returns string.
	match = random.choice(make_request()) # selects random item from "valuable stuff" list
	result = match.split('</td>') # makes list of match by spliting it from '</td>'
	ip_address = result[0].strip('<tr><td>') # fetches first item of result list and removes '<tr><td>' from it
	port = result[1].strip('</td>') # fetches 2nd item of result list and removes '</td>' from it
	if result[6].strip('<td class=\'hx\'>') == 'yes': # fetches fifth item of result list and removes ''<td class='hx'>'' from it and checks if its equal to 'yes'
		typ = 'https'
	else:
		typ = 'http'
	return typ + '://' + ip_address + ':' + port # returns http(s)://ip_address:port

def many(): # function to fetch many proxies. Returns list.
	proxies = [] # list to store proxies, obvious lmao
	for match in make_request(): # iterating over the "valueable stuff" list
		result = match.split('</td>') # makes list of match by spliting it from '</td>'
		ip_address = result[0].strip('<tr><td>') # fetches first item of result list and removes '<tr><td>' from it
		port = result[1].strip('</td>') # fetches 2nd item of result list and removes '</td>' from it
		if result[6].strip('<td class=\'hx\'>') == 'yes': # fetches fifth item of result list and removes ''<td class='hx'>'' from it and checks if its equal to 'yes'
			typ = 'https'
		else:
			typ = 'http'
		proxies.append(typ + '://' + ip_address + ':' + port)
	return proxies

def get(number): # function to fetch specific number of proxies. Returns list.
	proxies = [] # list to store proxies, obvious lmao
	if number > 300: # Maximum number of proxies we can fetch in one is 300
		print("Maximum number of returnable proxies is 300. Fetching 300 proxies")
		number = 300
	matches = make_request()[:number] # fetching n items from the "valueable stuff" list
	for match in matches: # iterating over the n items
		result = match.split('</td>') # makes list of match by spliting it from '</td>'
		ip_address = result[0].strip('<tr><td>') # fetches first item of result list and removes '<tr><td>' from it
		port = result[1].strip('</td>') # fetches 2nd item of result list and removes '</td>' from it
		if result[6].strip('<td class=\'hx\'>') == 'yes': # fetches fifth item of result list and removes ''<td class='hx'>'' from it and checks if its equal to 'yes'
			typ = 'https'
		else:
			typ = 'http'
		proxies.append(typ + '://' + ip_address + ':' + port)
	return proxies

def verify(proxy):
	test_url = 'http://www.icanhazip.com'
	test_proxy = {proxy.split(':')[0]: proxy}
	try:
		resp = requests.get(test_url, proxies=test_proxy, timeout=60)
		resp.raise_for_status()
	except:
		return False
	else:
		return True

def format(proxy):
	"""
	Return the proxy in a format useable by requests
	"""
	return {proxy.split(':')[0]: proxy}
