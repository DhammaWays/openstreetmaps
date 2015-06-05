"""
Audit street address and fix it
Two major steps:

1) Audit the OSMFILE to find the addresses needing to fix, for example:

 'Rd': set(['Arya Samaj Rd']),

2) Update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
  Example fixed output:
  
  Arya Samaj Rd => Arya Samaj Road
  
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "new-delhi_india.osm"

# Regular expression to find abbreviated street names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Common street names we may find
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# Mapping table provinding mapping from abbreviated street name to full name
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "St": "Street",
            "St.": "Street"
            }


# Bucket our street adresses by street names
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        # We will like to only examine the streets which are unusual/abbreviated
        if street_type not in expected:
            street_types[street_type].add(street_name)

# Does this element contain street data
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Audit given file, returning a possible street types set which may need to examine/fix
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    # As the given file can be quite large, we process it iteratively
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        # Audit only street data
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


# Fix the street name if we can
def update_name(name, mapping, st_type): 

    # Looking into our mapping table to find possible fixed name
    if st_type in mapping:
        name = street_type_re.sub(mapping[st_type], name)

    return name

# Audit and fix the street names
def audit_fix():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    # For each possible problematic street name fix it if we can
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping, st_type)
            if name != better_name:
                print name, "=>", better_name


if __name__ == '__main__':
    audit_fix()
