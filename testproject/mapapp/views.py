# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from .forms import MyForm
from django.views.decorators.csrf import csrf_protect
import geocoder
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET
import requests
import lxml.html
import time
import signal
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import concurrent.futures as confu

ghotel = 0
gcount = 0
gimage = 0
JTB_url = ""
RAKUTEN_url = ""
JALAN_url= ""
jtb_price=[""]*6
rakuten_price=""
jalan_price=[""]*6
ENCODING = 'utf-8'
@csrf_protect
def form_test(request):
	lat=35.689488
	lng=139.691706	  
	form = MyForm()
	return render(request, 'mapapp/index2.html',{
        'form': form,
        'lat': lat,
        'lng': lng,

    })

@csrf_protect
def submain(request):
	hotel = ghotel
	x = gcount  
	jtb = JTB_url
	rakuten = RAKUTEN_url
	jalan = JALAN_url
	pjalan = jalan_price
	pjtb = jtb_price
	prakuten = rakuten_price
	for i,jalan2 in enumerate(pjalan):
		if i==0:
			continue
		elif i > x:
			break
		pjalan[i][0] = str(pjalan[i][0]) + "円"
		pjalan[i][1] = str(pjalan[i][1]) + "円"
		
	for i,jtb2 in enumerate(pjtb):
		if i == 0:
			continue
		elif i > x:
			break
		pjtb[i] = str(jtb2).split("～")
	
	for i,rakuten2 in enumerate(prakuten):
                if i==0:
                        continue
                elif i > x:
                        break
                prakuten[i][0] = str(prakuten[i][0]) + "円"
                prakuten[i][1] = str(prakuten[i][1]) + "円"	

	#print(pjalan)
	print(pjtb)
	#print(prakuten)
	if x == 3:
		return render(request, 'mapapp/index5.html', {
			'a1': [hotel[1],hotel[2],hotel[3]],
			'a2': [jalan[1],jalan[2],jalan[3]],
			'a3': [jtb[1],jtb[2],jtb[3]],
			'a4': [rakuten[1],rakuten[2],rakuten[3]],
			'a5': [pjalan[1][0],pjalan[1][1],pjalan[2][0],pjalan[2][1],pjalan[3][0],pjalan[3][1]],
			'a6': [pjtb[1],pjtb[1],pjtb[2],pjtb[2],pjtb[3],pjtb[3]],	
			'a7': [prakuten[1][0],prakuten[1][1],prakuten[2][0],prakuten[2][1],prakuten[3][0],prakuten[3][1]]
				
		})
	else:
		return render(request, 'mapapp/index4.html', {
			'a1': [hotel[1],hotel[2],hotel[3],hotel[4],hotel[5]],
			'a2': [jalan[1],jalan[2],jalan[3],jalan[4],jalan[5]],
			'a3': [jtb[1],jtb[2],jtb[3],jtb[4],jtb[5]],
			'a4': [rakuten[1],rakuten[2],rakuten[3],rakuten[4],rakuten[5]],
			'a5': [pjalan[1][0],pjalan[1][1],pjalan[2][0],pjalan[2][1],pjalan[3][0],pjalan[3][1],pjalan[4][0],pjalan[4][1],pjalan[5][0],pjalan[5][1]],
			'a6': [pjtb[1],pjtb[1],pjtb[2],pjtb[2],pjtb[3],pjtb[3],pjtb[4],pjtb[4],pjtb[5],pjtb[5]],	
			'a7': [prakuten[1][0],prakuten[1][1],prakuten[2][0],prakuten[2][1],prakuten[3][0],prakuten[3][1],prakuten[4][0],prakuten[4][1],prakuten[5][0],prakuten[5][1]]
		})

@csrf_protect
def test(request):
	start = time.time()
	index = "index.html"
	html = 0
	x = 0
	lat = 35.689488
	lng = 139.691706
	hotel = [" "] * 7
	hurl = [" "] * 7
	image = [" "] * 7
	price = [1]*7
	purl = [" "]*10
	lat2 = [1] * 10
	lng2 = [1] * 10
	global ghotel
	global gcount
	global JTB_url
	global RAKUTEN_url
	global JALAN_url
	global jalan_price
	global jtb_price
	global rakuten_price	

	if request.method == "POST":
		form = MyForm(data=request.POST)

		if form.is_valid():
			w = request.POST['search']
			a = geocode(w)
			dom = xml.dom.minidom.parseString(a)
			location = dom.getElementsByTagName('location')
			if location.length > 0:
				lat = location[0].getElementsByTagName('lat')[0].firstChild.data
				lng = location[0].getElementsByTagName('lng')[0].firstChild.data
				html = jalan(lat, lng)
				hotel = result(html, 1)
				ghotel = hotel
				x = count(html, 1)
				hurl = result(html, 6)
				price = hprice(html)
				image = result(html, 9)
				hlocation = result(html, 3)
				htype = result(html,5)
				if x == 2:
					pric = [hurl,hotel,hotel]
					kansuu = [scraping,js_jtb,rakuten]
					process = parapara(kansuu,x,parallel,pric)
					purl,price2,price3 = process[0],process[1],process[2]
					JTB_url = price2
					RAKUTEN_url = price3
					JALAN_url = purl
					pric = [price2,hotel,hotel]
					kansuu = [jtbscraping,jalanscraping,rscraping]
					process = parapara(kansuu,x,parallel,pric)
					jtb_price = process[0]
					jalan_price = process[1]
					rakuten_price = process[2]
				elif x>=5:
					x = 5
					#purl = parallel(hurl,5,scraping)
					#price2 = parallel(hotel,5,js_jtb)
					#price3 = parallel(hotel,5,rakuten)
					pric = [hurl,hotel,hotel]
					kansuu = [scraping,js_jtb,rakuten]
					process = parapara(kansuu,x,parallel,pric)
					purl,price2,price3 = process[0],process[1],process[2]
					JTB_url = price2
					RAKUTEN_url = price3
					JALAN_url = purl
					#print(JALAN_url)
					#jtbinfo = [""]*6
					#for a in range(6):
					#	jtbinfo[a] = [hotel[a],price2[a]]
					#print(jtbinfo) 
					pric = [price2,hotel,hotel]
					kansuu = [jtbscraping,jalanscraping,rscraping]
					process = parapara(kansuu,x,parallel,pric)
					jtb_price = process[0]
					jalan_price = process[1]
					rakuten_price = process[2]
					#jtb_price = parallel(price2,5,jtbscraping)
					#jalan_price = parallel(purl,5,jalanscraping)
					#rakuten_price = parallel(price3,5,rscraping)
				for i in range(x):
					r = re.compile("([^,]*)(/)(.*)")
					try:
						m = r.match("%s"%price2[i])
						ss=m.group(1)+m.group(2)
						price2[i]=ss
					except AttributeError:
						pass
				gcount = x
				#print(price2)
				#print(price3)
#				for i,jalan2 in enumerate(pjalan):
#					if i==0:
#						continue
#					elif i > x:
#						break
#					pjalan[i][0] = str(pjalan[i][0]) + "円"
#					pjalan[i][1] = str(pjalan[i][1]) + "円"
#
#				for i,jtb2 in enumerate(pjtb):
#					if i == 0:
#						continue
#					elif i > x:
#						break
#				jtb_price[i] = str(jtb2).split("～")
#
#				for i,rakuten2 in enumerate(prakuten):
#					if i==0:
#						continue
#					elif i > x:
#						break
#					prakuten[i][0] = str(prakuten[i][0]) + "円"
#					prakuten[i][1] = str(prakuten[i][1]) + "円"

				for i in range(x):
					geo = geocode(hlocation[i + 1])
					dom = xml.dom.minidom.parseString(geo)
					location = dom.getElementsByTagName('location')
					if location.length > 0:
						lat2[i] = location[0].getElementsByTagName('lat')[0].firstChild.data
						lng2[i] = location[0].getElementsByTagName('lng')[0].firstChild.data
				if x == 2:
					index = "index3.html"
				else:
					index = "index.html"

		end = time.time()
		print("\n" +"main"+ str(end-start) + "sec")
	else:
		form = MyForm()
	if x == 2:
		return render(request, 'mapapp/%s' % index, {
			'form': form,
			'html': html,
			'lat': lat,
			'lng': lng,
			'a1': [hotel[1],hotel[2]],
			'a2': [hurl[1],hurl[2],
			'b1': [image[1],image[2]],
			'c1': [lat2[0], lat2[1]],
			'c2': [lng2[0], lng2[1], lng2[2]],
			'd1': [price[1],price[2],price[3]],
			'e1': [hlocation[1],hlocation[2],hlocation[3]],
			'f1': [htype[1],htype[2],htype[3]],
			'purl': [purl[1],purl[2],purl[3]]

		})
	else:
		return render(request, 'mapapp/%s' % index, {
			'form': form,
			'html': html,
			'lat': lat,
			'lng': lng,
			'a1': [hotel[1],hotel[2],hotel[3],hotel[4],hotel[5]],
			'a2': [hurl[1],hurl[2],hurl[3],hurl[4],hurl[5]],
			'b1': [image[1],image[2],image[3],image[4],image[5]],
			'c1': [lat2[0], lat2[1], lat2[2], lat2[3], lat2[4]],
			'c2': [lng2[0], lng2[1], lng2[2], lng2[3], lng2[4]],
			'd1': [price[1],price[2],price[3],price[4],price[5]],
			'e1': [hlocation[1],hlocation[2],hlocation[3],hlocation[4],hlocation[5]],
                        'f1': [htype[1],htype[2],htype[3],htype[4],htype[5]],
			'purl': [purl[1],purl[2],purl[3],purl[4],purl[5]]
		

		})

def geocode(name):
	start = time.time()
	ENCODING = 'utf-8'
	url = u"http://maps.google.com/maps/api/geocode/xml?&language=ja&sensor=false&region=ja&address="

	url = url + urllib.parse.quote(name.encode(ENCODING))
	
	buffer = urllib.request.urlopen(url).read()
	end = time.time()
	print("\n" +"geocode "+ str(end-start) + "sec")
	return buffer

def jalan(lat,lng):
	start = time.time()
	lat = float(lat) * 1.000106961 - float(lat) * 0.000017467 - 0.004602017
	lng = float(lng) * 1.000083049 + float(lng) * 0.000046047 - 0.010041046
	lat = lat * 3600 * 1000
	lng = lng * 3600 * 1000
	lat = int(lat)
	lng = int(lng)
	url = "http://jws.jalan.net/APIAdvance/HotelSearch/V1/"
	api_key = "and15e316b9f30"
	range = 10
	url = url +  "?order=4&xml_ptn=1&pict_size=0&key=" + api_key + "&x=" + str(lng) +"&y=" + str(lat) + "&range=" + str(range)
	html = urllib.request.urlopen(url).read()
	end = time.time()
	print("\n" +"jalan "+ str(end-start) + "sec")
	return html


def result(html,x):
	start = time.time()
	root=ET.fromstring(html)
	i=4
	hotel = ["A"]
	for a in root:
		tag=a.tag
		if tag=="{jws}Hotel":
			hotel.append(root[i][x].text)
			i+=1
	end = time.time()
	print("\n" +"result "+ str(end-start) + "sec")
	return hotel



def count(html,x):
	start = time.time()
	root=ET.fromstring(html)
	i=4
	hotel = ["A"]
	x=0
	for a in root:
		tag=a.tag
		if tag=="{jws}Hotel":
			hotel.append(root[i][x].text)
			i+=1
			x+=1
	end = time.time()
	print("\n" +"count "+ str(end-start) + "sec")
	return x

def hprice(html):
	start = time.time()
	root=ET.fromstring(html)
	i=4
	price = [" "]
	x=0
	for a in root:
		tag=a.tag
		tag2=a.tag
		x=0
		if tag=="{jws}Hotel":
			while tag2 != "{jws}SampleRateFrom":
				x+=1
				tag2 = root[i][x].tag
			price.append(root[i][x].text)
			i+=1
	end = time.time()
	print("\n" +"hprice "+ str(end-start) + "sec")
	return price

def scraping(hurl):
	start = time.time()
	r = requests.get('%s'%hurl)
	content_type_encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
	soup = BeautifulSoup(r.content, 'html.parser', from_encoding=content_type_encoding)
	for link in soup.find_all("link", rel="canonical"):
		purl=link['href']
	url = purl + "plan/"
	#r = requests.get(url)
	#content_type_encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
	#soup = BeautifulSoup(r.content, 'html.parser', from_encoding=content_type_encoding)
	end = time.time()
	print("\n" +"scraping2 "+ str(end-start) + "sec")
	return url

def parallel(hotel,x,js):
	start = time.time()
	pool = ThreadPoolExecutor(x)
	url=[""]*9
	h=[""]*9
	for i,hotelname in enumerate(hotel):
		if i == 0:
			continue
		elif i > x:
			break
		h[i-1] = pool.submit(js,hotelname)
	for i in range(x):
		url[i+1] = h[i].result()
	end = time.time()
	print("\n" +"parallel "+ str(end-start) + "sec")
	return url	

def parapara(kansuu,x,parallel,hotel):
	start = time.time()
	c = [""]*10
	d = [""]*10
	pool = ThreadPoolExecutor(3)
	for i,k in enumerate(kansuu):
		c[i] = pool.submit(parallel,hotel[i],x,k)
	for i in range(3):
		d[i] = c[i].result()
	end = time.time()
	print("\n" +"parapara "+ str(end-start) + "sec")
	#print(d)
	return d

def js_jtb(hotel):
	start = time.time()
	driver = webdriver.PhantomJS()
	driver.get('http://www.jtb.co.jp/search/?q=' + urllib.parse.quote_plus(hotel, encoding='utf-8'))
	soup = BeautifulSoup(driver.page_source,"lxml")
	a = soup.find("a", class_="gs-title")
	try:
		href = a['href']
	except KeyError:
		pass
	except TypeError:
		pass
	if 'purl' in locals():
		url = 1
	else:
		url = href
	driver.service.process.send_signal(signal.SIGTERM)
	driver.quit()
	end = time.time()
	print("\n" +"js_jtb "+ str(end-start) + "sec")
	return url

def rakuten(hotel):
	start = time.time()
	num=0
	hurl = "https://kw.travel.rakuten.co.jp/keyword/Search.do?charset=utf-8&f_max=30&lid=topC_search_keyword&f_query=" + urllib.parse.quote_plus(hotel, encoding='utf-8')
	r = requests.get('%s'%hurl)
	soup = BeautifulSoup(r.content,"html.parser")
	for div in soup.select('div > h2 > a'):	
		try:
			purl=div['href']
			purl="https:" + purl
		except KeyError:
			pass
		except TypeError:
			pass
		if 'purl' in locals():
			break
	try:
		r2 = requests.get('%s'%purl) 
		soup2 = BeautifulSoup(r2.content,"lxml")
		for a in soup2.find_all("a",class_="rtconds"):
			try:
				href = a['href']
			except KeyError:
				pass
			except TypeError:
				pass
			if num == 1:
				break
			num+=1
		url = href
	except UnboundLocalError:
		url = 1
	end = time.time()
	print("\n" +"rakuten "+ str(end-start) + "sec")
	return url

def jtbscraping(jtbinfo):
	print(jtbinfo)
	cnt = 0
	start = time.time()
	r = requests.get('%s'%jtbinfo)
	soup = BeautifulSoup(r.content,"html.parser")
	name = soup.select("div#htl_titleTop > h1")
	name = name[0].text
	regex=r'（.*）'
	name = re.sub(regex,"",name)
	jtb_price = 0
	jtbinfo = list(jtbinfo)
	jtbinfo.pop()
	for a in range(len(jtbinfo)):
		b = jtbinfo.pop()
		if b == "/":
			if jtbinfo.count("/") == 8:
				break				
	jtbinfo = ''.join(jtbinfo)
	r = requests.get('%s'%jtbinfo)
	soup = BeautifulSoup(r.content,"html.parser")
	for a in soup.select("#shisetsu_list > div > div.htl_title > div > h2 > a > span"):
		if name == a.text:
			print(a.text)
			price = soup.select("#shisetsu_list > div > div.htl_listInner > div.htl_body > div > dl.htl_price1 > dd > span")
			jtb_price = price[cnt].text
		cnt+=1
	end = time.time()
	print("\n" +"jtbscraping"+ str(end-start) + "sec")
	return jtb_price

def jalanscraping(hurl):
	start = time.time()
	url = "https://www.jalan.net/uw/uwp2011/uww2011init.do?keyword=" +  urllib.parse.quote_plus(hurl,encoding='shift_jis')
	jaran_price = [0,1000000000000]
	r = requests.get('%s'%url)
	soup = BeautifulSoup(r.content,"html.parser")
	div = soup.select('div#fw > div.result > div.detail.clearfix > div.detail-r > div.price.clearfix > span.bold')
	print("\n" +"jaranscraping"+ str(end-start) + "sec")
	return jaran_price

def rscraping(url):
	start = time.time()
	hello = [10000000,0]
	url = "https://kw.travel.rakuten.co.jp/keyword/Search.do?charset=utf-8&f_max=30&lid=topC_search_keyword&f_query=" + url 
	try:
		#url = "https:" + url
		r = requests.get('%s'%url)
		soup = BeautifulSoup(r.content,"html.parser")
		b = soup.select('div#result > div.hotelBox > dl.price > dd > em')
		hello[0] = b[0].text
	except:
		pass
	end = time.time()
	print("\n" +"rscraping "+ str(end-start) + "sec")
	return hello


