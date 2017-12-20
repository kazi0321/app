# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.shortcuts import render
#from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_protect
#import geocoder
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

def jtbscraping(hurl):
        start = time.time()
        jtb_price = 0
        r = requests.get('%s'%hurl)
        soup = BeautifulSoup(r.content,"html.parser")
        print(soup)
        #driver = webdriver.PhantomJS()
        #driver.get(hurl)
        #driver.quit()
        #if hurl !=1:
        #        driver = webdriver.PhantomJS()
        #        driver.get(hurl)
        #        soup = BeautifulSoup(driver.page_source,"lxml")
        #        for div in soup.select('div#one-price-area > dl > dd > span'):
        #                jtb_price = div.text
        #        driver.quit()
        #else:
        #        jtb_price = "存在しない"
        end = time.time()
        print("\n" +"jtbscraping"+ str(end-start) + "sec")
        return jtb_price

print(jtbscraping("https://www.jtb.co.jp/kokunai_htl/list/A05/15/1501/150101/3122106/"))
