import urllib2
import html2text as ht
import pprint
from lxml.html.clean import Cleaner
CL = Cleaner(style=True, links=True, add_nofollow=True,page_structure=True, safe_attrs_only=False, meta=True)

import socket
socket.setdefaulttimeout(60)

def totext(baseurl):
    j = urllib2.urlopen(baseurl)
    text = j.read()
    try:
        from feedparser import _getCharacterEncoding as enc
    except ImportError:
        enc = lambda x, y: ('utf-8', 1)

    try:
        encoding = enc(j.headers, text)[0]
        if encoding == 'us-ascii': encoding = 'utf-8'
        data = CL.clean_html(text.decode(encoding, 'replace'))
    except:
        data = CL.clean_html("".join([x for x in text if ord(x) <= 128]))
    m = ht.html2text(data, baseurl)
    return "".join([x for x in m if ord(x) < 128])


def create_chunks(text, size=5):
    res=[]
    tmp = []
    text = text.split('\n')
    for e in text:
        if '[' in e or ']' in e:
            if len(filter(None,tmp)) > size:res.extend(tmp)
            tmp=[]
            continue
        tmp.append(e)
    return res

def get_text(url):
    try:
         return "\n".join(create_chunks(totext(url)))
    except Exception, e:
         return None

def get_desc(soup,url):
        if soup:
            result= ht.html2text_file(str(soup),None)
        else:
            result =unicode(html2content.get_text(url))
        return result