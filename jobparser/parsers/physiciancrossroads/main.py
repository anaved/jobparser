#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.a.nextSibling.next.next.next
        self.fields["company_name"].patterns = [r"Company:\s*(.+)"]
        self.fields["company_name"].process = lambda t: t[0].strip()
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["company_id"].patterns = self.fields["company_name"].patterns
        self.fields["company_id"].process = self.fields["company_name"].process
        self.fields["title"].func = lambda doc: doc.a.string
        self.fields["company_joburl"].func = lambda doc: doc.a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.a["href"]
        self.fields["city"].func = lambda doc: doc.a.nextSibling.next
        self.fields["city"].patterns = [r"Location:\s*([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.a.nextSibling.next
        self.fields["state"].patterns = [r"Location:\s*.*?, (\w\w)\W", r"Location:\s*.*?, (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "physiciancrossroads.com"
        self.fields["posting_date"].func = lambda doc: doc.find("span", {'class': "date"}).string
        self.fields["posting_date"].patterns = [r"(\d+) days? ago", r"()\d+ hours? ago"]
        self.fields["posting_date"].process = common.daysago
        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("td", {'class': "copy"})[4:-2]
        self.url = "http://physiciancrossroads.com/candidate/search.php?new_search=1&search_string=%s&city=&period-s=&limit=50&submit=Search"
    