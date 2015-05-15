#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Count Tags - Generate a list of tags an dtheir count

Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""

INPUT_FILE = 'new-delhi_india.osm'

import xml.etree.ElementTree as ET
from collections import defaultdict
import pprint

def count_tags(filename):
        # YOUR CODE HERE
        tags_dict = defaultdict(int)
        for event, elem in ET.iterparse(filename):
            tags_dict[elem.tag] += 1
            
        return tags_dict                

def test():

    tags = count_tags(INPUT_FILE)
    pprint.pprint(tags)
        

if __name__ == "__main__":
    test()
