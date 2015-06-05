#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pprint
import re
from collections import defaultdict
import operator

"""
Count number of unique users

Our task is to find out how many unique users
have contributed to the map in this particular area!

The function process_map would return a set of unique user IDs ("uid").
For example:
('56597:Oberaffe', 269365)

"""
INPUT_FILE = 'new-delhi_india.osm'

def get_user(element):
    return element.attrib["user"]

# Generate a list of unqiue users who have contributed to given map file
def process_map(filename):
    valid_tags = set(['node', 'way', 'relation'])
    users = defaultdict(int)
    
    # Iteratively pasre the file as it can be huge
    for _, element in ET.iterparse(filename):
        # We are only interesetd in "node", "way" and "relation" 
        if element.tag in valid_tags:
            # Create key as uid:user_name to uniquely/easily identify the user
            users[element.attrib["uid"] + ":" + element.attrib["user"]] += 1

    return users

# Main entry point to process given map file and list down list of unique users
# sorted from largest contributors down 
def test():
    users = process_map(INPUT_FILE)
    sorted_users = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
    print "Total number of unique users: " + str(len(sorted_users))
    pprint.pprint(sorted_users)
    

if __name__ == "__main__":
    test()
