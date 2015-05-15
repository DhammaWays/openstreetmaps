#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
from collections import defaultdict
import operator

"""
Count number of unique users

Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""
INPUT_FILE = 'new-delhi_india.osm'

def get_user(element):
    return


def process_map(filename):
    valid_tags = set(['node', 'way', 'relation'])
    # users = set()
    users = defaultdict(int)
    for _, element in ET.iterparse(filename):
        if element.tag in valid_tags:
            users[element.attrib["uid"] + ":" + element.attrib["user"]] += 1

    return users

def test():

    users = process_map(INPUT_FILE)
    sorted_users = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
    print "Total number of unique users: " + str(len(sorted_users))
    pprint.pprint(sorted_users)
    


if __name__ == "__main__":
    test()
