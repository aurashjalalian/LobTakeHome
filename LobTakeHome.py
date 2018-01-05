import requests
import json
import sys

class Official:
	""" Class that holds the Address and Name of an Official from the Google Civic Information API"""
	def __init__(self, name, line1, city, state, zip_code, line2, line3):
		self.name = name
		self.line1 = line1
		self.city = city
		self.state = state
		self.line2 = line2
		self.line3 = line3
		self.zip = zip_code
	def get_name(self):
		return self.name
	def get_line1(self):
		return self.line1
	def get_city(self):
		return self.city
	def get_state(self):
		return self.state
	def get_line2(self):
		return self.line2
	def get_line3(self):
		return self.line3
	def get_zip(self):
		return self.zip

def civic_query_url_constructor():
	"""Method that constructs the URL for accessing the Google Civic Information API"""
	host = "https://www.googleapis.com"
	path = "/civicinfo/v2"
	entrypoint = "/representatives"
	url = host + path + entrypoint
	return url

def civic_query_header_constructor(address):
	"""Generates a dictionary named headers which stores a common set of parameters for the get requests on the Google Civic Information API"""
	API_KEY = "AIzaSyDlIXZrd-JfLOc1R_XUEIyXspFO6_OcJlI"
	headers = dict()
	headers["key"] = API_KEY
	headers["address"] = address
	headers["roles"] = "legislatorLowerBody"
	return headers

def civic_api_error_handler(response_str):
	"""Detects errors from the response received from the Google Civic Information API"""
	if response_str.has_key("error"):
		error = response_str["error"]
		code = error["code"]
		error_message = error["message"]
		print("Google Civic Information API Error")
		print(("Error " + str(code) + ": " + str(error_message)))
		return True
	return False

def lob_query_url_constructor(entrypoint):
	"""Method that takes in an entrypoint and uses it to construct the URL for accessing the Lob API"""
	host = " https://api.lob.com"
	path = "/v1"
	entrypoint = entrypoint
	url = host + path + entrypoint
	return url

def lob_query_header_constructor():
	"""Generates a dictionary named headers which stores a common set of parameters for the get requests in search_query, autosuggest_query, and explore_query"""
	API_KEY = "test_512ddbe47f845f2a17063cbad02a1e66e8e"
	headers = dict()
	headers["api_key"] = API_KEY
	return headers

def lob_create_address(name, line1, line2, city, state, zipcode, country, API_KEY):
	""" Given a name, lines one and two of an address, a city, a state, a zipcode, a country, and an API_KEY (all of which in the form of a string), this function creates a Address object using the Lob API."""
	url = lob_query_url_constructor("/addresses")
	address_args = dict()
	address_args["name"] = name
	address_args["address_line1"] = line1
	if line2 is not None:
		address_args["address_line2"] = line2
	address_args["address_city"] = city
	address_args["address_state"] = state
	address_args["address_zip"] = zipcode
	address_args["address_country"] = country
	req = requests.post(url, auth=(API_KEY, ''), data=address_args)
	s = json.loads(req.text)
	return s

def lob_create_letter(to, _from, message, API_KEY, merge_variables):
	""" Given two Address objects (to and _from), a message, an API Key, and merge variables (an object with up to 40 key/value pairs), this function creates a letter object using the Lob API."""
	url = lob_query_url_constructor("/letters")
	letter_args = dict()
	letter_args["to"] = to
	letter_args["from"] = _from
	letter_args["color"] = False
	letter_args["file"] = "<html><head></head><body><div style='text-align: center; vertical-align: center; padding-top: 50%'>{{message}}</div></body></html>"
	merge_variables = json.dumps(merge_variables)
	letter_args["merge_variables"] = merge_variables
	letter_args["description"] = message
	req = requests.post(url, auth=(API_KEY, ''), data=letter_args)
	s = json.loads(req.text)
	return s

def lob_api_error_handler(response_str):
	"""Detects errors from the response received from the Lob API"""
	if response_str.has_key("error"):
		error = response_str["error"]
		code = error["status_code"]
		error_message = error["message"]
		print("Lob API Error")
		print(("Error " + str(code) + ": " + str(error_message)))
		return True
	return False

def main():
	lob_API_KEY = "test_512ddbe47f845f2a17063cbad02a1e66e8e"
	args = sys.argv
	args_name = args[1]
	args_line1 = args[2]
	args_line2 = args[3]
	args_city = args[4]
	args_state = args[5]
	args_country = args[6]
	args_zip = args[7]
	args_message = args[8]
	url = civic_query_url_constructor()
	headers = civic_query_header_constructor(args_line1)
	r = requests.get(url, params=headers)
	s = json.loads(r.text)
	if civic_api_error_handler(s):
		return
	officials_list = s["officials"]
	first_official = officials_list[0]
	mail_to_address = first_official["address"][0]
	line2 = None
	if "line2" in mail_to_address:
		line2 = mail_to_address.get("line2")
	line3 = None
	if "line3" in mail_to_address:
		line3 = mail_to_address.get("line3")
	recip = Official(first_official["name"], mail_to_address["line1"], mail_to_address["city"], mail_to_address["state"], mail_to_address["zip"], line2, line3)
	MT_address_object = lob_create_address(recip.get_name(), recip.get_line1(), recip.get_line2(), recip.get_city(), recip.get_state(), recip.get_zip(), "US", lob_API_KEY)
	if lob_api_error_handler(MT_address_object):
		return
	merge_variables = {
	    'message': args_message
	  }
	MF_address_object = lob_create_address(args_name, args_line1, args_line2, args_city, args_state, args_zip, args_country, lob_API_KEY)
	if lob_api_error_handler(MF_address_object):
		return
	message = args_message
	letter_object = lob_create_letter(MF_address_object["id"], MT_address_object["id"], message, lob_API_KEY, merge_variables)
	if lob_api_error_handler(letter_object):
		return
	pdf = letter_object["url"]
	print(pdf)
	return

if __name__ == "__main__": main()