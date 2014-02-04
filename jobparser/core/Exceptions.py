# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "naved"
__date__ = "$9 Nov, 2010 4:43:51 PM$"

class GeoException(Exception):
    def __init__(self, *args):
        self.value = args
    def __str__(self):
        return repr(self.value)

