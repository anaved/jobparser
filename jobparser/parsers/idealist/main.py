#!/usr/bin/env python

from util import common
from core.JobsiteParser import JobsiteParser
import re
import urllib

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("div", {'class': "assetOwner"}).a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: "".join(doc.li.h2.a.findAll(text=True))
        self.fields["company_joburl"].func = lambda doc: "http://www.idealist.org" + doc.li.h2.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.idealist.org" + doc.li.h2.a["href"]
        self.fields["city"].func = lambda doc: doc.find("div", {'class': "assetLocation"}).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("div", {'class': "assetLocation"}).string
        self.fields["state"].patterns = [r", (.*?)\s+United States"]
        self.fields["state"].process = common.shorten
        self.fields["state"].mandatory = True
        self.fields["source"].func = lambda doc: "idealist.org"
        self.fields["posting_date"].func = lambda doc: "".join(doc.find("div", {'class': "assetDates"}).findAll(text=True))
        self.fields["posting_date"].patterns = [r"(\w\w\w)\w* (\d\d?), (\d\d\d\d)"]
        self.fields["posting_date"].process = common.mmm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("span", text=re.compile("Location:")).parent.parent.findAll(text=True))
        self.filterfields["zipcode"].patterns = [r"\D(\d{5})\D", r"\D(\d{5})$"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.find('ul',{'class':'itemsList'}).findAll('li') if doc else None
        self.url = 'http://www.idealist.org/search?search_keywords=%s&search_type=job'#"http://www.idealist.org/if/idealist/en/SiteIndex/AssetSearch/search?assetTags=JOB_TYPE&assetTypes=Job&fetchLimit=50&keywords=%s&keywordsAsString=%s&languageDesignations=en&onlyFetchAssetProperties=1&siteClassifierName=idealist&sortOrderings=modificationDate&validStatusTypes=APPROVED&validStatusTypes=UNAPPROVED&validStatusTypes=DEFERRED"

    def generateurl(self):
        url = urllib.unquote(self.url)
        try:
            url %= (self.query, self.query)
        except:
            pass
        return url
    