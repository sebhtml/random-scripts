#!/usr/bin/env python

import os
import sys

class OutputWriter:
    def __init__(self):
        self.columns = {}
        self.index = 0

    def add_example(self, example):
        self.columns[example] = self.index
        self.index += 1

class Head:
    def __init__(self, path):
        self.path = path

        self.file = open(self.path)
        self.next()

    def get_current_line(self):
        return self.current_line

    def has_next(self):
        return self.file.tell() < os.fstat(self.file.fileno()).st_size

    def next(self):
        if self.has_next():
            self.current_line = self.file.readline()

    def close(self):
        self.file.close()

class Merger:
    def __init__(self):
        self.files = []
        self.output = "default"
        self.maximum_file_count = 8
        self.heads = []

    def add_file(self, file):

        if len(self.files) == self.maximum_file_count:
            return

        self.files.append(file)

    def get_minimum_head(self):
        # here, there are N heads
        lowest_key = None

        i = 0
        for head in self.heads:
            key = head.get_current_line().strip().split()[0]
            #print("head # " + str(i) + " is " + key)

            if lowest_key == None or key < lowest_key:
                lowest_key = key
            i += 1

        # print("lowest_key is " + lowest_key)


        # here, there are N heads
        lowest_key = None

        i = 0
        for head in self.heads:
            key = head.get_current_line().strip().split()[0]
            # print("head # " + str(i) + " is " + key)

            if lowest_key == None or key < lowest_key:
                lowest_key = key
            i += 1

        # print("lowest_key is " + lowest_key)

        return lowest_key

    def not_done(self):
        for head in self.heads:
            if head.has_next():
                return True

        return False

    def merge(self):
        # print("Merging " + str(len(self.files)) + " examples")

        # open files
        self.heads = []
        for file in self.files:
            descriptor = Head(file)
            self.heads.append(descriptor)

        while self.not_done():
            #print("getting selection")
            selection = self.get_minimum_head()

            self.consume(selection)

        # close files
        for file in self.heads:
            file.close()
        self.heads = []

    def consume(self, selected_key):
        index = 0

        self.emit_event({"eventName": "OpenKey"})
        for head in self.heads:
            example = self.files[index]
            key = head.get_current_line().strip().split()[0]
            if key == selected_key:
                self.emit_event({
                                "eventName": "AddExampleCount",
                                "exampleName": example,
                                "key": head.get_current_line().strip().split()[0],
                                "value": head.get_current_line().strip().split()[1]
                            })

                head.next()
            index += 1
        self.emit_event({"eventName": "CloseKey"})

    def emit_event(self, options = {}):
        eventName = options['eventName']

        if eventName != "AddExampleCount":
            print(eventName)
            return

        exampleName = options["exampleName"]
        key = options["key"]
        value = options["value"]

        print(eventName + " " + exampleName + " " + key + " " + value)

    def set_output(self, output):
        self.output = output

if __name__ == '__main__':
    merger = Merger()

    directory = sys.argv[1]
    for file in os.listdir(directory):
        merger.add_file(os.path.join(directory, file))

    merger.set_output('output')
    merger.merge()
