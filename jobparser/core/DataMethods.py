# To change this template, choose Tools | Templates
# and open the template in the editor.


import datetime
from geo.google import Geocode
from job.models import Job


__author__="naved"
__date__ ="$25 Jan, 2011 6:56:58 PM$"

def dooutput(fields, entry,csv=False,csvfile=None):
        if csv:
            write_csv(csvfile,fields,entry)
        else:
            write_db(fields,entry)

def write_csv(csvfile,fields,entry):
        f = open(csvfile, "a")
        s = []
        for key in fields:
            if entry[key] is None:
                s.append('""')
            else:
                s.append('"' + str(entry[key]).replace('"', '""') + '"')
        f.write(",".join(s)+"\n")
        f.close()

def write_db(fields,entry):
     j = Job()
     for key in fields:
                if entry[key] is not None and entry[key] != "":
                    j.__setattr__(key, entry[key])
     j.save()

def writeheader(csvfile,header):
            f = open(csvfile, "w")
            f.write(",".join([key for key in header])+"\n")
            f.close()


def getstring(doc, field):
#        try:
            x = field.func(doc)
            if not field.mandatory:
                x = x or ""
            if x.__class__.__name__=='str':
                #strip all the fields and replace '\xa0'
                return x.replace(u'\xa0', ' ').strip()
            return x
#        except Exception as e:
#            if field.mandatory:
#                print field
#                return None
#            else:
#                return False

def repeat(entry):
        x = Job.objects.filter(source_joburl = entry["source_joburl"], source=entry["source"])
        for y in x:
            y.timestamp=datetime.datetime.now()
            y.save()
        return len(x) > 0

def parse(data, field):
        try:
            return field.process(data)
        except Exception as e:            
            if field.mandatory:
                return None
            else:
                return False

def geo(x):
#        f= lambda x : x if  x!='' else None
#        g = Geocode.Geocode(city=f(x.get("city", None)), state=f(x.get("state", None)), zipcode=f(x.get("zipcode", None)))
#        res = g.geocode()
#        for field in ["state", "latitude", "longitude"]:
#             x[field] = res[0].__getattribute__(field)
#
#        #special handling for city, as it can be empty
#        x['city'] = res[0].__getattribute__('city') or " "
        return x