
import zipfile
import json

data = []
zf = zipfile.ZipFile('new-delhi_india.osm.zip', 'r')
f = zf.open('new-delhi_india.osm.json', 'r')
#for line in f:
 #   print line
#    data.append( json.loads(line) )
try:
    data = json.loads(f.read())
except ValueError:
    pass
print len(data)
f.close()
zf.close()