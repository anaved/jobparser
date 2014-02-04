#!/usr/bin/env python

import json

from core.Exceptions import GeoException
from job.models import Geo
import urllib2
from urllib2 import URLError

class Geocode:

    def __init__(self, city=None, state=None, zipcode=None, latitude=None, longitude=None):
        self.data = {}
        self.data["city"] = city
        self.data["state"] = state
        self.data["zipcode"] = zipcode
        self.data["latitude"] = latitude
        self.data["longitude"] = longitude

    def address(self):
        parameters = []
        if self.data["city"] is not None:
            parameters.append(self.data["city"])
        if self.data["state"] is not None and self.data["zipcode"] is not None:
            parameters.append(self.data["state"]+' '+self.data["zipcode"])
        elif self.data["state"] is not None:
            parameters.append(self.data["state"])
        elif self.data["zipcode"] is not None:
            parameters.append(self.data["zipcode"])
        return ", ".join(parameters) + ", USA"

    def save(self, results):
        res = []
        for result in results:
            t = {}
            for addcomp in result["address_components"]:
                if "postal_code" in addcomp["types"]:
                    t["zipcode"] = addcomp["long_name"].split('-')[0]
                if "locality" in addcomp["types"]:
                    t["city"] = addcomp["long_name"]
                if "administrative_area_level_1" in addcomp["types"]:
                    t["state"] = addcomp["short_name"]
            t["latitude"] = result["geometry"]["location"]["lat"]
            t["longitude"] = result["geometry"]["location"]["lng"]
            x = Geo.objects.filter(**t)            
            if len(x) == 0:
                g = Geo()
                for key in t:
                    g.__setattr__(key, t[key])
                g.save()
                res.append(g)
            else:
                res += x
        return res

    def geocode(self):
        if self.data["zipcode"] is not None:            
            results = Geo.objects.filter(zipcode=self.data["zipcode"])
        elif self.data["city"] is not None:            
            results = Geo.objects.filter(city=self.data["city"], zipcode=None)
        elif self.data["state"] is not None:
            results = Geo.objects.filter(city=None, state=self.data["state"], zipcode=None)
        else:
            results = Geo.objects.filter(city=None, state=None, zipcode=None)
        if len(results) > 0:
            return results
        url = "http://maps.googleapis.com/maps/api/geocode/json?" + "address=" + self.address() + "&sensor=false"
        url = url.replace(' ', '+')
        try:
            response = urllib2.urlopen(urllib2.Request(url)).read()
        except URLError as e:
            raise(GeoException(self.data,"NO RESPONSE FROM GOOGLE MAP"))
        data = json.loads(response)
        if data["status"] in ["OVER_QUERY_LIMIT","ZERO_RESULTS"]:
            raise(GeoException(self.data,data))
        results = data["results"]
        x=self.save(results)
        print x
        return x