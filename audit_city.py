"""
Auditing city names and fixing them:

Goal here is to cleanup city names in our dataset. Ideally "city" field should
only have proper city name but we find that in our dataset we have several
instances where instead of a just a proper city name, either street address
or area name along with city name has entered. For example:
-'Pocket 6, Sector 9, Rohini, New Delhi'
-'Pratap Colony, Siraspur, Delhi'
-'Noida , Uttar Pradesh'

Our job is to first list down possible problematic patterns with auditing, for example:
'New Delhi': set(['Chanakyapuri, New Delhi',
                   'Pandav Nagar, New Delhi',
                   'Paschim Vihar, New Delhi',
                   'Pitam Pura, New Delhi',
                   'Pocket 6, Sector 9, Rohini, New Delhi',
                   'West Karawal Nagar, New Delhi'])
                
Then we try to fix it by mapping it to only the known city name, for example:
Pocket 6, Sector 9, Rohini, New Delhi => New Delhi
Pratap Colony, Siraspur, Delhi => Delhi
Noida , Uttar Pradesh => Noida

"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "new-delhi_india.osm"

expected = ["New Delhi", "Delhi", "Noida", "Greater Noida", "Gurgaon", "Ghaziabad", "Faridabad"]

# Categorize city names by city types
def audit_city_type(city_types, city_name):    
    city_l = city_name.rsplit(',', 1) 
    
    # We are only interested in city names which are kind of street adress
    # If possible city names figures by itself (i.e. no commas found in name), we will leave it alone
    if len(city_l) > 1:
        city_type = city_l[len(city_l)-1].lstrip() # pick up last element and remove any whitespaces
        city_types[city_type].add(city_name) # add it to our set

# Does this element contgain city name
def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

# Find if a known city name figues in given "name" 
def find_known_city_name(name, expected):
    city_found = None
    for city in expected:
        if city.lower() in name.lower(): # ignore case
            city_found = city
            break
        
    return city_found
            
# Audit the given file for possible city types to allow us to fix the bad ones
def audit(osmfile):
    osm_file = open(osmfile, "r")
    city_types = defaultdict(set)
    
    # As given file can be big, only iteratively parse it
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        # We are only interested in elements which have city names
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    audit_city_type(city_types, tag.attrib['v'])

    return city_types


# Fix up the city names with our known city names
def update_name(name, expected, city_type): 

    # Straightforward fixing if given city type is already in known list,   
    if city_type in expected:
        name = city_type
    else:
        # Return a known city name if we can find it anywhere in original name
        city_found = find_known_city_name(name, expected)
        if( city_found ):
            name = city_found

    return name


# Audit and fix the city names
def audit_fix():
    city_types = audit(OSMFILE)
    pprint.pprint(dict(city_types))
    
    # For each possible problematic city original name fix it if we can
    for city_type, address_set in city_types.iteritems():
        for name in address_set:
            better_name = update_name(name, expected, city_type)
            if name != better_name:
                print name, "=>", better_name
    

if __name__ == '__main__':
    audit_fix()
