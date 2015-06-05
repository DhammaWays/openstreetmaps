#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Count Tags - Generate a list of tags and their count

Using the iterative parsing process the map file and find out not only
what tags are there, but also how many, to get the feeling on how much
of which data we can expect to have in the map.

The output is a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.
For example:
'node': 502661
'way': 87420

"""

INPUT_FILE = 'new-delhi_india.osm'

import xml.etree.ElementTree as ET
from collections import defaultdict
import pprint

# Return a list of top level tags and their counts
def count_tags(filename):
        tags_dict = defaultdict(int)
        
        # Iteratively parse the file as it can be huge
        for event, elem in ET.iterparse(filename):
            tags_dict[elem.tag] += 1
            
        return tags_dict                

def test():

    tags = count_tags(INPUT_FILE)
    pprint.pprint(tags)
        

if __name__ == "__main__":
    test()
