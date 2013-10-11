#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 andres <andres@andres.fedoracore>, Joseph Turian
#
# Distributed under terms of the MIT license.

#!/usr/bin/python

import sys, struct
import zipfile
from cStringIO import StringIO

CLASS_ID = 218217067
VERSION_ID = 1
FILE_TESTING = "/home/andres/test80legs.80"

"""
method from https://github.com/turian/py80legsformat/blob/master/eightyformat.py
"""
def read(file):
    """
    Return a generator that yields (url, data) tuples.
    """
    # Make sure "h" fmt returns 32-bits (hopefully an integer)
    assert(struct.calcsize("i")) == 4

    l = file.read(2*4)
    (classID, versionID) = struct.unpack("ii", l)
    assert (classID, versionID) == (CLASS_ID, VERSION_ID)

    l = "not EOF"
    data = []
    l = file.read(1*4)
    while l != "":
        (URLSIZE,) = struct.unpack("i", l)
        url = file.read(URLSIZE).decode("utf-8")
        l = file.read(1*4)
        (DATASIZE,) = struct.unpack("i", l)
        data = str(file.read(DATASIZE))
        yield (url, data)
        l = file.read(1*4)

"""
method from https://github.com/turian/py80legsformat/blob/master/eightyformat.py
"""
def readzip(zfilename):
    """
    Read a zipfile and process all .80 files therein.
    """
    zfile = zipfile.ZipFile(zfilename, "r")
    for info in zfile.infolist():
        fname = info.filename
        if fname.endswith(".80"):
            data = zfile.read(fname)
            for r in read(StringIO(data)):
                yield r

def write(data, file_name):
    """
	Create a .80 file (file_name = complete path) with the specific data
	data = List[tuples]
    """
    file_temp = open(file_name, "w")
    file_temp.write(struct.pack("ii", CLASS_ID, VERSION_ID))
    for info in data:
        url = info[0]
        file_temp.write(struct.pack("i", len(url)))
        file_temp.write(url.encode())
        content = info[1]
        file_temp.write(struct.pack("i", len(content)))
        file_temp.write(content)

    file_temp.close()
 
"""
 test write and read a file
"""
if __name__ == "__main__":
    data = list()
    info = ()
    for i in range(6):
        info = ("http://www.google"+str(i)+".com", "<html>TEST DATA Q CARAMELITO"+str(i)+"</html>")
        data.append(info)

    write(data, FILE_TESTING)
	
    file_read = open(FILE_TESTING)
    results = read(file_read)
    for result in results:
        print result[0] +" - "+ result[1]

    print "Test finished ok!"
