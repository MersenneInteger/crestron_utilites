#!/usr/bin/python
import os, sys, csv, itertools
from xml.dom import minidom
import xml.etree.ElementTree as ElemTree
    
pos, nvxType, name, dev, ip, mac, mAddr, rows = ([] for i in range(8))

if len(sys.argv) < 3:
    sys.exit('invalid number of args: 2 required and only {} given'.format(len(sys.argv)))

if '.xml' in sys.argv[1] and '.csv' in sys.argv[2]:
    
    csvFileName, xmlFileName = sys.argv[2], sys.argv[1]
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, xmlFileName)
    print(path)

    doc = minidom.parse(xmlFileName)
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
    try:
        with open(csvFileName, 'w') as fileHandle:
            writer = csv.DictWriter(fileHandle, fieldnames=fieldNames, delimiter=',')
            writer.writeheader()
            writer = csv.writer(fileHandle, delimiter=',')
            for row in rows:
                writer.writerow(row)
    except IOError as e:
        print('Error writing to file: {}'.format(e.args))
    except Exception as e:
        print('Error occured: {}'.format(e.args))

elif '.csv' in sys.argv[1] and '.xml' in sys.argv[2]:
    
    subElems = [pos, nvxType, name, dev, ip, mac, mAddr]
    csvFileName, xmlFileName, xioDirIP = sys.argv[1], sys.argv[2], sys.argv[3]
    domainName = sys.argv[4]
    with open(csvFileName, 'r') as fileHandle:
        reader = csv.reader(fileHandle, delimiter=',')
        for row in reader:
            rows.append(row)
            for i in range(len(row)):
                subElems[i].append(row[i])

    for i in range(len(subElems)):
        del subElems[i][0]
    attributes = rows[0]
    del rows[0]

    deviceRoot = ElemTree.Element('xio')
    switchInfo = ElemTree.SubElement(deviceRoot, 'switch')
    switchInfo.set('snmpCommunity', 'public')
    switchInfo.set('snmpVersion', 'v2c')
    switchInfo.set('address', xioDirIP)
    domainInfo = ElemTree.SubElement(deviceRoot, 'domain')
    domainInfo.set('name', domainName)

    devices = ElemTree.SubElement(deviceRoot, 'devices')
    numOfDevs = len(subElems[0])
    node = [[] for i in range(numOfDevs)]

    for i in range(numOfDevs):
        node[i] = ElemTree.SubElement(devices, 'device')    
    for i in range(len(rows)):
        node[i].set(attributes[0], rows[i][0])
        node[i].set(attributes[1], rows[i][1])
        node[i].set(attributes[2], rows[i][2])
        node[i].set(attributes[3], rows[i][3])
        node[i].set(attributes[4], rows[i][4])
        node[i].set(attributes[5], rows[i][5])
        node[i].set(attributes[6], rows[i][6])

    with open(xmlFileName, 'w') as xmlFileHandle:
        dataToWrite = ElemTree.tostring(deviceRoot, encoding='utf8', method='xml')
        dataToWrite = dataToWrite.decode()
        xmlFileHandle.write(dataToWrite)
else:
    sys.exit('invalid file extensions given')

