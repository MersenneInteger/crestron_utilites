#!/usr/bin/python
import os, sys, csv
from xml.dom import minidom

if len(sys.argv) != 3:
    sys.exit('invalid number of args: 2 required and only {} given'.format(len(sys.argv)))

if '.xml' in sys.argv[1] and '.csv' in sys.argv[2]:
    fileName = sys.argv[1]
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, fileName)
    print(path)
    pos, nvxType, name, dev, ip, mac, mAddr, rows = ([] for i in range(8))

    doc = minidom.parse(fileName)
    devs = doc.getElementsByTagName('device')
    for i, nvx in enumerate(devs):
        pos.append(nvx.attributes['position'].value)
        nvxType.append(nvx.attributes['type'].value)
        name.append(nvx.attributes['Name'].value)
        dev.append(nvx.attributes['Device'].value)
        ip.append(nvx.attributes['IP'].value)
        mac.append(nvx.attributes['MAC'].value)
        mAddr.append(nvx.attributes['MAddr'].value)
        rows.append([pos[i], nvxType[i], name[i], dev[i], ip[i], mac[i], mAddr[i]])

    fieldNames = ['position', 'type', 'Name', 'Device', 'IP', 'MAC', 'MAddr']
    with open(sys.argv[2], 'w') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldNames, delimiter=',')
        writer.writeheader()
        writer = csv.writer(fh, delimiter=',')
        for row in rows:
            writer.writerow(row)
elif '.csv' in sys.argv[1] and '.xml' in sys.argv[2]:
    pass
else:
    sys.exit('invalid file extensions given')

