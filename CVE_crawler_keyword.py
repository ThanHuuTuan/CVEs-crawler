import requests
import sys
import numpy
from bs4 import BeautifulSoup
import csv
import xlsxwriter
import os.path

web_base = "cvedetail"

def get_vendor_id(keyword, web_base="cvedetail"):
	url_search_vendor = "https://www.google.com/search?q=%s" % (keyword + web_base)
	res = requests.get(url_search_vendor)
	html = BeautifulSoup(res.text, "lxml")
	for link in html.findAll('a'):
		url = link.get('href')
		if "/vulnerability-list/vendor_id" in url:
			for part in url.split("/"):
				if "product_id" in part:
					print "product_id for %s: %s " % (keyword, part)
					return part
			for part in url.split("/"):
				if "vendor_id" in part:
					print "vendor_id for %s: %s " % (keyword, part)
					return part
	sys.exit("Can not get product_id or vendor_id. The program may need more specific keyword.\nEx: Oracle => Oracle+SQL, RoundCube => RoundCube+mail")

def get_result_pages(product_id):
	url_search_cves = "https://www.cvedetails.com/vulnerability-list/%s/" % (product_id)
	res = requests.get(url_search_cves)
	html = BeautifulSoup(res.text, "lxml")
	pages = html.find("div", {"class":"paging", "id":"pagingb"})
	links = pages.find_all("a", href=True)
	urls = []
	for link in links:
		urls.append("https://www.cvedetails.com" + link['href'])
	return urls

def get_result_cves(url_search_cves, file_exist, year_filter):
	res = requests.get(url_search_cves)
	html = BeautifulSoup(res.text, "lxml")
	table = html.find("table", { "class" : "searchresults sortable", "id": "vulnslisttable" })
	rows = table.findAll("tr")
	results = []
	if file_exist == False:
		for row in rows:
			data_row = []
			cols = row.find_all('th')
			for col in cols:
				data_row.append(col.text.encode('utf-8').strip())
			data_row.append("Description")
			results.append(data_row)
			break

	data_row = []
	for row in rows:
		cols = row.find_all('td')
		for col in cols:
			if (col.get('class') != None):
				class_attr = col.get('class')[0]
			else:
				class_attr = "#ignore"
			if col.text.strip() != "":
				data_row.append(col.text.encode('utf-8').strip())
			else:
				data_row.append("None")
			if class_attr == "cvesummarylong":
				year = int(data_row[1].split("-")[1])
				if year < int(year_filter):
					return results
				results.append(data_row)
				print data_row
				if len(data_row) != 16:
					sys.exit("Invalid number of fields (!= 16)")
				data_row = []
				print "-------------------------------"
	return results

def export_csv(data, name):
	myFile = open(name, 'a')
	with myFile:
	   writer = csv.writer(myFile)
	   writer.writerows(data)
	print "Export completed"

if __name__ == "__main__":
	if len(sys.argv) == 3:
		keyword = sys.argv[1]
		year_filter = sys.argv[2]
	else:
		print "-----> python CVE_crawler_keyword.py <key_word> <year_filter> <-----\n\r"
		print "Ex: python CVE_crawler_keyword.py Joomla 2012"
		sys.exit(1)
	product_id = get_vendor_id(keyword)
	pages = get_result_pages(product_id)
	file_name = "CVEs_%s.csv" % keyword
	file_exist = False
	for c, page in enumerate(pages):
		print "page %d " % (c)
		if os.path.exists(file_name):
			file_exist = True
		data = get_result_cves(page, file_exist, year_filter)
		export_csv(data, name=file_name)

