# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/env python

import sys
from xml.dom import minidom
import lxml.html as etree


filename = "DevonHealthKit_20200928.xml"
username = "Devon"
userid = "3"


def main():
    # filename = sys.argv[1]

    newfilename = str(filename).replace(".xml", "_sqllite3.txt")

    print(filename)
    print(newfilename)

    # read_file = open(filename, 'r')
    healthxml = minidom.parse(filename)
    # <Record type="HKQuantityTypeIdentifierStepCount" sourceName="iphone" sourceVersion="11.4.1"
    # device="&lt;&lt;HKDevice: 0x2817c70c0&gt;, name:iPhone, manufacturer:Apple, model:iPhone,
    # hardware:iPhone9,1, software:11.4.1&gt;"
    # unit="count" creationDate="2019-03-01 19:31:14 -0700" startDate="2019-03-01 19:00:01 -0700"
    # endDate="2019-03-01 19:06:19 -0700" value="12"/>
    records = healthxml.getElementsByTagName('Record')
    new_file_content = ""
    model = 'Iphone'
    step = 'HKQuantityTypeIdentifierStepCount'
    distance = 'HKQuantityTypeIdentifierDistanceWalkingRunning'
    idx = 0
    hk_totalvalue = 0
    for elem in records:
        # print(elem.attributes['type'].value)
        # print(elem.attributes['value'].value)
        # print(elem.attributes['device'].value)
        # deviceinfo = elem.attributes['device'].firstChild.value
        # print(elem.attributes['unit'].value)
        # print(elem.attributes['creationDate'].value[0:10])
        # print(elem.attributes['startDate'].value[0:19])
        # print(elem.attributes['endDate'].value)

        if step.__str__().lower() in elem.attributes['type'].value.__str__().lower():
            hk_type = elem.attributes['type'].value
            hk_unit = elem.attributes['unit'].value
            hk_creationdate = elem.attributes['creationDate'].value[0:11]
            hk_start = elem.attributes['startDate'].value[0:19]
            hk_end = elem.attributes['endDate'].value[0:19]
            hk_value = int(elem.attributes['value'].value)
            hk_totalvalue += hk_value

            if records[idx + 1] and records[idx + 1].attributes['creationDate'].value[0:11] != hk_creationdate:
                sSQL = "INSERT INTO getoutapp_health (type, sourcename, unit, creationdate, startdate, enddate, " \
                       "value, login_id) SELECT '" + hk_type + "','" + model \
                       + "','" + hk_unit + "','" + hk_creationdate + "','" \
                       + hk_start + "','" + hk_end \
                       + "'," + str(hk_totalvalue) + "," + userid \
                       + " WHERE NOT EXISTS (SELECT * FROM getoutapp_health WHERE login_id = " + userid \
                       + " AND unit = '" + hk_unit + "' AND creationdate = '" \
                       + hk_creationdate + "' LIMIT 1);"
                # print(sSQL)
                new_file_content += sSQL + "\n"
                hk_totalvalue = 0
        idx += 1

    write_file = open(newfilename, "w")
    write_file.write(new_file_content)

    new_file_content = ""
    idx = 0
    for elem in records:
        if distance.__str__().lower() in elem.attributes['type'].value.__str__().lower():
            hk_type = elem.attributes['type'].value
            hk_unit = elem.attributes['unit'].value
            hk_creationdate = elem.attributes['creationDate'].value[0:11]
            hk_start = elem.attributes['startDate'].value[0:19]
            hk_end = elem.attributes['endDate'].value[0:19]
            hk_value = float(elem.attributes['value'].value)
            hk_totalvalue += hk_value

            if records[idx + 1] and records[idx + 1].attributes['creationDate'].value[0:11] != hk_creationdate:
                sSQL = "INSERT INTO getoutapp_health (type, sourcename, unit, creationdate, startdate, enddate, " \
                       "value, login_id) SELECT '" + hk_type + "','" + model \
                       + "','" + hk_unit + "','" + hk_creationdate + "','" \
                       + hk_start + "','" + hk_end \
                       + "'," + str(hk_totalvalue) + "," + userid \
                       + " WHERE NOT EXISTS (SELECT * FROM getoutapp_health WHERE login_id = " + userid \
                       + " AND unit = '" + hk_unit + "' AND creationdate = '" \
                       + hk_creationdate + "' LIMIT 1);"
                # print(sSQL)
                new_file_content += sSQL + "\n"
                hk_totalvalue = 0
        idx += 1

    write_file.write(new_file_content)
    write_file.close()
    print('**** DONE PROCESSING ****')


def main2():
    root = etree.parse(filename)
    # for n in root.findall(".//record[@type]"):
    #     print(n.get("type"))
    # https://stackoverflow.com/questions/36656241/python-find-unique-xml-attributes
    # tuple () a collection which is ordered and unchangeable/immutable. Allows duplicate members.
    print(sorted({n.get("type") for n in root.findall(".//record[@type]")}))
    # list [] a collection which is ordered and changeable. Allows duplicate members. 0 based, xxx[included:excluded]
    # ['HKQuantityTypeIdentifierDistanceWalkingRunning', 'HKQuantityTypeIdentifierFlightsClimbed',
    #  'HKQuantityTypeIdentifierHeadphoneAudioExposure', 'HKQuantityTypeIdentifierStepCount']

    # print({n.get("type") for n in root.findall(".//record[@type]")})
    # dictionary {} a collection which is unordered, changeable and indexed. No duplicate members.
    # {'HKQuantityTypeIdentifierHeadphoneAudioExposure', 'HKQuantityTypeIdentifierStepCount',
    #  'HKQuantityTypeIdentifierDistanceWalkingRunning', 'HKQuantityTypeIdentifierFlightsClimbed'}


def main3():
    filename = sys.argv[1]
    newfilename = str(filename).replace(".txt", "_sqllite3.txt")

    print(filename)
    print(newfilename)

    read_file = open(filename, 'r')
    healthxml = minidom.parse(filename)
    records = healthxml.getElementsByTagName('Record')
    for elem in records:
        print(elem.attributes['type'].value)

    # -- INTO-health -> INTO getoutapp_health,
    # FROM-health -> FROM getoutapp_health,
    # FROM-DUAL - empty,
    # login-id -> login_id

    # -- INTO-locations -> INTO getoutapp_locations,
    # FROM-locations -> FROM getoutapp_locations,
    # FROM-DUAL - empty,
    # login-id -> login_id,
    # locations-id -> id,
    # INTO-location -> INTO
    new_file_content = ""
    if 'mysql_route' in read_file.__str__().lower():
        for line in read_file:
            stripped_line = line.strip()
            new_line = stripped_line.replace("INTO locations", "INTO getoutapp_locations")
            new_line = new_line.replace("FROM locations", "FROM getoutapp_locations")
            new_line = new_line.replace("from locations", "FROM getoutapp_locations")
            # wvs todo case insensitive replace i.e. regular expressions
            new_line = new_line.replace("FROM DUAL", "")
            new_line = new_line.replace("loginid", "login_id")
            new_line = new_line.replace("locationsid", "id")
            new_line = new_line.replace("INTO location", "INTO getoutapp_location")
            new_file_content += new_line + "\n"
    elif 'mysql_health' in read_file.__str__().lower():
        for line in read_file:
            stripped_line = line.strip()
            new_line = stripped_line.replace("INTO health", "INTO getoutapp_health")
            new_line = new_line.replace("FROM health", "FROM getoutapp_health")
            new_line = new_line.replace("FROM DUAL", "")
            new_line = new_line.replace("loginid", "login_id")
            new_file_content += new_line + "\n"
    else:
        print('not processing ' + read_file.__str__())
    read_file.close()

    # write_file = open(filename, "w")
    write_file = open(newfilename, "w")

    write_file.write(new_file_content)
    write_file.close()


if __name__ == '__main__':
    main()



