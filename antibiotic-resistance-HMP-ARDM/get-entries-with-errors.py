#!/usr/bin/env python

import os

directory_name = "HMP-samples"

files = os.listdir(directory_name)

for file in files:
    path = directory_name + "/" + file

    descriptor = open(path)

    #print("path= " + path)
    first_line = descriptor.readline()
    descriptor.close()

    has_error = first_line.find("ERROR") >= 0

    if has_error:
        print(file)
