#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("div", {'class': "block"}).findAll("div")[2].p.a.string
        self.fields["company_name"].depth = 2
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["company_id"].depth = self.fields["company_name"].depth
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "block"}).findAll("div")[1].p.string
        self.fields["title"].depth = 2
        self.fields["company_joburl"].func = lambda doc: doc.findAll("td")[2].a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.findAll("td")[2].a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td")[3].string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td")[3].string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "hirefinders.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[0].string
        self.fields["posting_date"].patterns = [r"(\d\d?)-(\d\d?)-(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
#        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("span", text=re.compile("Job Locations:")).parent.parent.findAll(text=True))
#        self.filterfields["zipcode"].patterns = [r"\D(\d{5})\D", r"\D(\d{5})$"]
#        self.filterfields["zipcode"].process = lambda t: t[0].strip()
#        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            curl= doc.find("ul", {'class': "pagenavigator"}).findAll('span')[-1]
            links = doc.find("ul", {'class': "pagenavigator"}).findAll("li")
            if int(curl.string) >= page+1:
                    return links[page].a["href"]
            return None
        
        self.datafunc = lambda doc: doc.findAll("tr", {'class': re.compile("tr")})
        self.url = "http://www.hirefinders.com/browsejobs?ddlSearchType=browsejobs&tbSearchKeywords=%s&tbSearchLocation=&ddlDistance=20&tbSearchExcludeKeywords=&ddlJobType=&ddlSearchDateAdded=&ddlSearchDateJoined=&ddlSearchIndustry=&ddlSearchIn=&amsSearchJobFunctions=&jfValues=&hdSearchMode=&hdAdvSearch=&lng_val=&lat_val="
        self.nextlink = nextpage
    
    