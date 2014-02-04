# To change this template, choose Tools | Templates
# and open the template in the editor.
import urllib
import re
import urllib2
import re
import BeautifulSoup
from job.models import *
import json
from datetime import datetime

__author__="naved"
__date__ ="$1 Jan, 2011 5:02:00 PM$"

def create_sd_url(sd):
    url = 'https://%s.taleo.net/careersection/jobsearch.ftl' % sd
    return urllib2.urlopen(url).url

def get_post_data(html):
    bs=BeautifulSoup.BeautifulSoup(html)
    c={}
    for e in bs.findAll(name='input'):
        attrs = dict(e.attrs)
        if 'name' in attrs.keys():
            c[attrs['name']] = attrs['value']
    return c

def get_url(url, postdata):
    data = urllib.urlencode(postdata)
    return urllib2.urlopen(url, data).read()

def get_header(dd):
    pat='^_hlid:\\s*\\[.*?\\],$'
    s=0
    for e in dd:
        if e.strip().startswith('listRequisition:'):
            s=1
        if s and re.match(pat, e.strip()):
            c=e.strip()
            return eval(c[c.index('['):c.rindex(']')+1])
    return []

def get_subdomain(url):    
    name='dummy'
    sd='dummy'
    job_list=[]
    pat = "api.fillList\('requisitionListInterface', 'listRequisition'.*?\[(.*?)\]\);"
    job_url = url.rsplit('/',1)[0] + '/jobdetail.ftl?lang=en&job=%s'
    if not '?' in url:
        url += '?'
    else:
        url+= '&'
    url += "listRequisition.size=100&dropListSize=100"    

    x=urllib2.urlopen(url)
    z=unicode(x.read(), errors='ignore')
    z = get_post_data(z)
    pageno = int(z['rlPager.currentPage'])
    while 1:        
        html = unicode(get_url(url, z), errors='ignore')
        header = get_header(html.split('\n'))
        result = re.search(pat, html)
        if len(header)==0 or not result:
            #print "Unable to parse url : %s" % url
            return
        
        data = eval('['+result.groups()[0]+']')

        index = header.index('reqlistitem.no')
        jobids = data[index::len(header)]

        data = {'subdomain': sd, 'jobid':'', 'url':'', 'timestamp':'', 'name': name}
        for e in jobids:
            data['jobid'], data['url'] = e, job_url % e
            job_list.append(feed(data))            
#            return job_list
        z = get_post_data(html)
        size = int(z['listRequisition.size'])
        pageno = int(z['rlPager.currentPage'])
        total = int(z['listRequisition.nbElements'])

        if size*pageno < total:
            pageno+=1
            z['rlPager.currentPage']=unicode(pageno)
        else:
            break    
    return job_list



COLUMN_HEAD = {'title': 'reqlistitem.title',
               'description': 'reqlistitem.description',
               'qualification':'reqlistitem.qualification',
               'location':'reqlistitem.primarylocation',
               'posting_date': 'reqlistitem.postingdate'}

def get_header_c(dd):
    pat='^_hlid:\\s*\\[.*?\\],$'
    s=0
    for e in dd:
        if e.strip().startswith('descRequisition:'):
            s=1
        if s and re.match(pat, e.strip()):
            c=e.strip()
            return json.loads(c[c.index('['):c.rindex(']')+1].replace("'",'"'))
    return []

def parse(data, name, sd, jid, url):
    pat = "api.fillList\('requisitionDescriptionInterface', 'descRequisition'.*?\[(.*?)\]\);"
    head = get_header_c(data.split('\n'))
    res={'company_name': name, 'company_id': sd, 'source': 'TALEO', 'source_joburl': url, 'company_joburl': url}
    result = re.search(pat, data)
    if len(head)==0 or not result:
        #print "Unable to parse url : %s" % url
        return
    data = '['+result.groups()[0]+']'
    data = json.loads(data.replace("'",'"'))    
    for k,v in COLUMN_HEAD.items():
        try:
            index = head.index(v)
            elem = data[index]
        except ValueError:
            elem = ''
        bs = BeautifulSoup.BeautifulSoup(urllib2.unquote(elem))
        elem = ' '.join(bs.findAll(text=True)).replace('&nbsp;','').replace('!*!','')
        res[k]=elem
    res['posting_date'] = datetime.now()
    res['all_text'] = '\n\n'.join(['Title:', res.get('title',''), 'Location:', res.get('location',''), 'Description:', res.get('description', ''), 'Qualification:', res.get('qualification','')])
    return res

def feed(data):
    name, sd, jid, url = data['name'], data['subdomain'], data['jobid'], data['url']
    u = urllib2.urlopen(url, timeout=60)
    return parse(u.read(), name, sd, jid, url)
    


