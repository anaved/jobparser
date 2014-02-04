#!/usr/bin/env python

import time

from core.JobsiteParser import JobsiteParser
from util import common

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("td")[2].string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.findAll("td")[0].span.a.string
        self.fields["company_joburl"].func = lambda doc: doc.findAll("td")[0].span.a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.findAll("td")[0].span.a["href"]
        self.fields["city"].func = lambda doc: doc.find("div", {'id': "jd"}).findAll("div", recursive=False)[2].findAll("div",recursive=False)[1].div.table.findAll("tr")[2].findAll("td").pop().string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["city"].depth = 2
        self.fields["state"].func = lambda doc: doc.find("div", {'id': "jd"}).findAll("div", recursive=False)[2].findAll("div",recursive=False)[1].div.table.findAll("tr")[2].findAll("td").pop().string
        self.fields["state"].patterns = [r", ([^,/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["state"].depth = 2
        self.fields["source"].func = lambda doc: "adminfinder.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[3].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yy
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.find("table", {'id': "joblist"}).findAll("tr", recursive=False)[1:]
        self.url = "http://adminfinder.com/index.php?order_by=post_date&ord=asc&action=search&5=%s"
        self.dev_mode=True
        def nextpage(doc, page):
            links = doc.find("p", {'class': "nav_page_links"})
            if links is None:
                return None
            link= links.findAll("a")[-1]
            if link.string.strip().startswith('Next'):
                  return link['href']
            return None     



        self.nextlink = nextpage
    