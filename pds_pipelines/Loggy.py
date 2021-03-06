#!/usr/bin/env python

import json
from collections import OrderedDict

from SubLoggy import *


class Loggy(object):
    """
    Writes to the logs file.
    
    Attributes
    ---------
    Lfile : dict
    loggyDict : dict
    """
    def __init__(self, Lfile):
        """
        Parameters
        ----------
        Lfile : dict
        """
        self.Lfile = Lfile
        self.loggyDict = {}
        self.loggyDict[self.Lfile] = OrderedDict()

    def setFileStatus(self, item):
        """
        Parameters
        ----------
        item
        """
        pass

    def AddProcess(self, PD):
        """
        Parameters
        ----------
        PD : dict
        """
        self.loggyDict[self.Lfile].update(PD)

    def Loggy2json(self):
        """
        Returns
        ----------
        str
            Ljson
        """
        Ljson = json.dumps(self.loggyDict)
        return Ljson
