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

Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
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

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

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

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def contains_problematic_chars(v):
    return problemchars.search(v)
    
def shape_address(e, dct):
    if e.attrib["k"].find(":") == e.attrib["k"].rfind(":"): # process single colon address tag only
        discard, addr_subkey = e.attrib["k"].split(":")
        dct[addr_subkey] = e.attrib["v"]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["type"] = element.tag
        created = {}
        
        #print element.attrib
        for k,v in element.attrib.iteritems():
            if k in CREATED:
                created[k] = v
            elif k != "lat" and k != "lon":
                node[k] = v
                
        node["created"] = created
        
        if( "lat" in element.attrib ):
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
        
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
            
        if element.tag == "way":
            node_refs = []
            for e in element.iter("nd"):
                node_refs.append(e.attrib["ref"])
            if node_refs != []:
                node["node_refs"] = node_refs
        
        #pprint.pprint(node)
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    #data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                #data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    #return data
    return

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    process_map(OSMFILE, False)
    #data = process_map(OSMFILE, False)
    #pprint.pprint(data)
    

if __name__ == "__main__":
    test()