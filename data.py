#!/usr/bin/env python
# -*- coding: utf-8 -*-

OSMFILE = "new-delhi_india.osm"

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
Generate the datamodel (JSON) for MongoDB analysis

Task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output would be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

A process map function parses the map file, and then calls the 'shape_element' function with the element
as an argument. This returns a dictionary, containing the shaped data for that element.

Finally save the data in a file, so that one could use mongoimport later on to import the
shaped data into MongoDB. 

In particular the following things are done:
- process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" are turned into regular key/value pairs, except:
    - attributes in the CREATED array is  added under a key "created"
    - attributes for latitude and longitude is  added to a "pos" array,
      for use in geospacial indexing. Also makes the values inside "pos" array as floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it is ignored
- if second level tag "k" value starts with "addr:", it is  added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag is ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  is turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

is  turned into
"node_refs": ["305896090", "1719825889"]
"""

# Regular expression for key patterns

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Compound "created" field type
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# Does the given string have problematic characters
def contains_problematic_chars(v):
    return problemchars.search(v)

# Restructure address as a compund field    
def shape_address(e, dct):
    if e.attrib["k"].find(":") == e.attrib["k"].rfind(":"): # process single colon address tag only
        discard, addr_subkey = e.attrib["k"].split(":") # only interested in subtag
        dct[addr_subkey] = e.attrib["v"]

# Shape given element
# Following info is re-shaped to craete a more strcutured element:
# - Created
# - Address
# - Pos, containing lat and long
# - Ways for node references
#
def shape_element(element):
    node = {}
    
    # Only interested in "node" and "way" kinf of elements
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["type"] = element.tag
        created = {}
        
        # Regroup creation related info under "created" 
        for k,v in element.attrib.iteritems():
            if k in CREATED:
                created[k] = v
            elif k != "lat" and k != "lon":
                node[k] = v
                
        node["created"] = created
        
        # Regroup position info under "pos"
        if( "lat" in element.attrib ):
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
        
        # Regroup "address" related info under "address"
        address = {}
        for e in element.iter("tag"):
            if contains_problematic_chars(e.attrib["k"]):
                continue
                
            if e.attrib["k"].startswith("addr:"):
                shape_address(e, address)
            else:
                node[e.attrib["k"]] = e.attrib["v"]
        
        if address != {}:
            node["address"] = address 
         
        # Regroup all node references for a way under "noder_refs"
        if element.tag == "way":
            node_refs = []
            for e in element.iter("nd"):
                node_refs.append(e.attrib["ref"])
            if node_refs != []:
                node["node_refs"] = node_refs
        
        #pprint.pprint(node)
        
        return node
    else:
        # Not interested in this element
        return None


# Parse the given map file and dump the strcutured JSON to output file
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    
    # Iteratively parse input file, re-shaping and writing each element into a structured
    # JSON element
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
                    
    return

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    process_map(OSMFILE, False)
    

if __name__ == "__main__":
    test()
