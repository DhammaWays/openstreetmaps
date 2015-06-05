#!/usr/bin/env python
# -*- coding: utf-8 -*-

INPUT_FILE = 'new-delhi_india.osm'

import xml.etree.ElementTree as ET
import pprint
import re

"""
Checks for valid/invalid MongoDB keys

Before we process the data and add it into MongoDB, we should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

Using 3 regular expressions to check for certain patterns
in the tags. Later on befor epopulating MongoDB, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
"""


# Regular expression for key patterns
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

problem_keys = []

# Classify given element into set of key patterns
def key_type(element, keys):
    # Only interested in tag elements
    # Match and map against the key patterns we are inetrested in
    if element.tag == "tag":
        
        v = element.attrib['k']
        m = lower.search(v) 
        if m:
            keys["lower"] += 1
        else:
            m = lower_colon.search(v)
            if m:
                keys["lower_colon"] += 1
            else:
                m = problemchars.search(v)
                if m:
                    keys["problemchars"] += 1
                    problem_keys.append(element.attrib)
                else:
                    keys["other"] += 1
        
    return keys

# Parse the gven file, listing down key patterns we may want to explore before
# putting data in MongoDB
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


# Main entry point to parse and list down categorized key 
def test():
    keys = process_map(INPUT_FILE)
    pprint.pprint(keys)
    pprint.pprint(problem_keys)
    

if __name__ == "__main__":
    test()