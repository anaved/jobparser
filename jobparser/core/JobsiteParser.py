#!/usr/bin/env python

import time

import ParserField
from conf.app_settings import COOKIEFILE
from conf.app_settings import KEYWORD_SLEEP_TIME
from conf.app_settings import LISTING_SLEEP_TIME
from conf.app_settings import TOTAL_FETCH_LIMIT
from conf.app_settings import URL_SLEEP_TIME
from core.DataMethods import dooutput
from core.DataMethods import geo
from core.DataMethods import getstring
from core.DataMethods import parse
from core.DataMethods import repeat
from core.DataMethods import writeheader
from core.Exceptions import GeoException
from job.models import ZCTA
import re
import traceback
from util import html2content
from util.netutil import gethtml
from util.netutil import getsoup
class JobsiteParser:

    def __init__(self,logger):
        self.logger = logger
        self.query=""
        self.keyword =[""]
        self.fields = {
                       "company_name": ParserField.ParserField(False),\
                       "company_id": ParserField.ParserField(False),\
                       "source": ParserField.ParserField(False),\
                       "title": ParserField.ParserField(True),\
                       "description": ParserField.ParserField(False),\
                       "qualification": ParserField.ParserField(False),\
                       "all_text": ParserField.ParserField(True),\
                       "location": ParserField.ParserField(True),\
                       "state": ParserField.ParserField(False),\
                       "city": ParserField.ParserField(False),\
                       "latitude": ParserField.ParserField(False),\
                       "longitude": ParserField.ParserField(False),\
                       "posting_date": ParserField.ParserField(True),\
                       "source_joburl": ParserField.ParserField(True),\
                       #made company_joburl mandatory
                       "company_joburl": ParserField.ParserField(True),\
                       "timestamp": ParserField.ParserField(False)
                       }
        self.fields["all_text"].func = lambda doc: unicode(html2content.get_text(self.url))
        self.fields["all_text"].patterns = [r"(.*)"]
        self.fields["all_text"].process = lambda t: t[0] if t[0].strip()!='' else None# markdown.markdown(t[0])
        self.fields["all_text"].depth = 2
        self.fields["latitude"].func = lambda x: None#lat_lng(x).latitude if lat_lng(x) else None
        self.fields["latitude"].patterns = [r"(.*)"]
        self.fields["latitude"].process = lambda t: 0.0#float(t[0].strip()) if t[0].strip() else 0.0
        self.fields["latitude"].depth = 3
        self.fields["longitude"].func = lambda x: None#lat_lng(x).longitude if lat_lng(x) else None
        self.fields["longitude"].patterns = [r"(.*)"]
        self.fields["longitude"].process = lambda t: 0.0#float(t[0].strip()) if t[0].strip() else 0.0
        self.fields["longitude"].depth = 3
        def lat_lng(x):
            zcta= ZCTA.objects.filter(postal_code = x["zipcode"])
            return zcta[0] if len(zcta) else None
        
        def loc(x):
            if x["state"]:
                return x["city"] + "-" + x["state"] + "-US"
            else:
                return None
        self.fields["location"].func = loc
        self.fields["location"].depth = 4
        self.filterfields = {"experience": ParserField.ParserField(False), "zipcode": ParserField.ParserField(False)}
        self.output = False
        self.printtitle = True
        self.csv = False
        self.db = True
        self.csvfile = "database.csv"
        self.datafunc = lambda doc: doc
        self.url = ""
        self.baseurl=""
        self.POSTparam = {}
        self.total = TOTAL_FETCH_LIMIT
        self.nextlink = lambda doc, page: None
        self.sleeptime = LISTING_SLEEP_TIME
        self.query_sleeptime=KEYWORD_SLEEP_TIME
        self.url_sleeptime=URL_SLEEP_TIME
        self.cookie = True
        self.dev_mode=False
        self.clean_html=False
            
    
    def collate(self, entry, depth):
        data={}
        fields = self.filterfields.copy()
        fields.update(self.fields)        
        for (key,value) in fields.items():
            if value.depth != depth:
                continue
            try:
                data[key] = getstring(entry, value)
            except Exception as e:
                self.log_except("Error finding : %s , %s"%(key,str(e)))
                if value.mandatory:
                    data[key]= None
                else:
                    data[key]= False
            if data[key] is None:
                self.log_debug("Mandatory Missing : "+key+" In URL: "+self.url)
                return  None
            elif data[key] is False:
                data[key] = None
                continue            
            matchfound = True
            for pattern in value.patterns:
                matchfound = False
                m = re.search(pattern, data[key], flags=re.DOTALL)                
                if m is not None:
                    matchfound = True
                    data[key] = parse(m.groups(), value)
                    if data[key] is None:
                        return None
                    elif data[key] is False:
                        data[key] = None                    
                    break
            if not matchfound:
                if value.mandatory:
                    return None
                data[key] = None
        return data
    
    def get_soup(self):
            cookie_file=COOKIEFILE+'.'+self.__module__+'.txt'            
            try:
                self.log_debug("Obtaining HTML")
                htm=gethtml(self.url,self.query,self.cookie,cookie_file,self.POSTparam)
                self.log_debug("Creating soup")
                soup = getsoup(htm,self.clean_html)
            except Exception as e:
                soup=None
                self.log_except(e)
            return soup

    def process_entry(self, entry):
        x = self.collate(entry, 1)
        if x is not None and not repeat(x):
            self.url = x["company_joburl"]
            self.POSTparam = {}  
            soup=self.get_soup()
            y = self.collate(soup, 2)
            if y is not None:
                x.update(y)
                z = self.collate(x, 3)
                if z is not None:
                    x.update(z)
                    x = geo(x)
                    f = self.collate(x, 4)
                    if f is not None:
                        x.update(f)
                        self.logger.info('Saving : '+self.mod_key+x["title"]+" | "+x["company_joburl"])
                        try:
                            dooutput(self.fields,x,self.csv,self.csvfile)
                        except :
                            self.logger.debug(self.mod_key+traceback.format_exc())


    def process_result_list(self,data,entries_parsed=0):
         for entry in data:
                if self.sleeptime is not None:
                    self.logger.info("Sleeping for listing sleep : "+str(self.sleeptime))
                    time.sleep(self.sleeptime)
                try:
                    self.log_debug("Sending entry %d to process "%(entries_parsed,))
                    self.process_entry(entry)
                except GeoException as e:
                    self.log_except(e)
                    continue
                except Exception as e:
                    self.log_except(e, True)                    
                entries_parsed += 1
                if entries_parsed >= self.total:
                    break
         return entries_parsed
     
    def execute(self):
        self.set_logger()
        entries = 0
        page = 1
        while True:
            try:                
                soup = self.get_soup()
                self.log_debug("Calling datafunction on soup")
                data = self.datafunc(soup)
                if data:
                    self.log_debug(" Sending %d entries to process"%(len(data) if data else 0,))
                    entries= self.process_result_list(data,entries)
                    if entries < self.total and self.nextlink(soup, page) is not None:
                        self.baseurl=self.url = self.nextlink(soup, page)
                        page += 1
                    else:
                        self.logger.info(self.mod_key+ str(entries)  + " entries processed")
                        break
                else:
                    self.log_debug(" No data found to process, Exiting.")
                    break
            except Exception as e:                
                self.log_except(e, True)
                break

    def run(self):
        for e in self.keyword:
            self.query=e
            if self.url.__class__.__name__=='list':               
               url_list=self.url
               for u in url_list:
                   self.url=self.baseurl=u
                   self.logger.info(" Executing for : "+str(self.url))
                   self.execute()
                   if self.url_sleeptime:
                            self.logger.info("Sleeping for url sleep : "+str(self.url_sleeptime))
                            time.sleep(self.url_sleeptime)
            else:
                self.logger.info(" Executing for : "+str(self.url))
                self.execute()
            if self.query_sleeptime:
                self.logger.info("Sleeping for keyword sleep : "+str(self.query_sleeptime))
                time.sleep(self.query_sleeptime)



    def test(self):
        self.db = False
        self.csv = True
        writeheader()
        self.run()

    def set_logger(self):
        self.mod_key=' MODULE : %s, KEYWORD  :  %s '%(self.__module__,self.query)

    def log_debug(self,message):
        self.logger.debug(self.mod_key+message)
        
    def log_except(self,exception,log_error=False):        
        if self.dev_mode or log_error:
            self.logger.error(self.mod_key+' |'+self.url+' | '+str(exception)+traceback.format_exc())
        else:
            self.logger.warn(self.mod_key+' |'+self.url+' | ' + str(exception))