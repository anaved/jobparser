# To change this template, choose Tools | Templates
# and open the template in the editor.


import cookielib
import BeautifulSoup
import lxml.html.clean
import urllib
import urllib2
from urllib2 import URLError

__author__="naved"
__date__ ="$25 Jan, 2011 5:58:40 PM$"


def generateurl(url,query):
        try:
            url = urllib.unquote(url)
        except:
            url= url
        try:
            url %= query
        except:
            pass
        return url

def open_get(url):
          u = urllib2.urlopen(urllib2.Request(url))
          return u

def open_post(params,url):
            for key in params:
                try:
                    params[key] %= self.query
                except:
                    pass
            u = urllib2.urlopen(urllib2.Request(url, urllib.urlencode(params)))
            return u

def open_cookie(cookie_file):
        cj= cookielib.LWPCookieJar()
        cj.load(cookie_file)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        return cj

def gethtml(url,query,is_cookie=True, cookie_file=None,POSTparam={}):
        if is_cookie:
            cj=open_cookie(cookie_file)
        url = generateurl(url,query)
        if POSTparam=={}:
            u=open_get(url)
        else:
            u=open_post(POSTparams,url)
        if is_cookie:
            cj.save(cookie_file)
        return u.read()    


def getsoup(html,clean_html):
        soup= None
        html=unicode(html,errors='ignore')
        if clean_html:
            soup=  BeautifulSoup.BeautifulSoup(lxml.html.clean.clean_html(html))
        else :
          # hack to support reverse compatibility, can remove after validating all parsers
           try:
                soup=  BeautifulSoup.BeautifulSoup(html)
           except:
                soup=  BeautifulSoup.BeautifulSoup(lxml.html.clean.clean_html(html))
        return soup

