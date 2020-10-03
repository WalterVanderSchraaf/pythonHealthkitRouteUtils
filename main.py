# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/env python
from datetime import datetime
import sys
import os
from xml.dom import minidom
import lxml.html as etree
import json
from pandas import json_normalize

filename = "DevonHealthKit_20200928.xml"
username = "Devon"
userid = "3"
file_locations = "tblLocations.json"
file_location = "tblLocation.json"
download_folder = os.path.expanduser("~")+"/Downloads/"

django_prefix = 'getoutapp_'
tblLocations = django_prefix + 'locations'
tblLocation = django_prefix + 'location'


def mainHealthKitToSqlite():
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


def mainMySQLToSqlite():
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


def convertlocationsSqliteJSONToSqlite():

    # [ locations.json
    #     {
    #         "Checked": "0",
    #         "DateTime": "2020-03-23 12:34:46",
    #         "HeartDuration": "",
    #         "HeartIntensity": "",
    #         "LocationsId": "4",
    #         "LoginId": "0",
    #         "MoveMinutes": "",
    #         "Orderby": "",
    #         "PathName": "Dog Walk",
    #         "TotalDistance": "1.050377368927",
    #         "TotalSteps": "565",
    #         "Totaltime": "00:55:35",
    #         "ZoomLevel": "16.4416980743408",
    #         "ZoomToLatitude": "37.760930159238",
    #         "ZoomToLongitude": "-122.4063430354"
    #     }

    # [ location.json
    #     {
    #         "Accuracy": "",
    #         "ActivityId": "",
    #         "Altitude": "-6.7",
    #         "ColorPath": "-16777216",
    #         "DateTime": "2020-03-23 12:34:52",
    #         "Latitude": "37.760385",
    #         "LocationId": "54",
    #         "LocationsId": "4",
    #         "Longitude": "-122.4084233",
    #         "TransitionId": ""
    #     }
    with open(download_folder + file_locations) as f:
        locations_json = json.load(f)  # list object [{'Checked': '0', 'DateTime': '2020-03-23 12:34:46',   }]
    f.close()
    # for itm in locations_json:
    #     print(itm)

    with open(download_folder + file_location) as f:
        location_json = json.load(f)
    f.close()

    # for rw in datajson:
    #     print(rw['LocationsId'] + ' : ' + rw['DateTime'])
    df_locations = json_normalize(locations_json)
    df_location = json_normalize(location_json)
    # df = df.sort_values(['LocationsId', "DateTime"], ascending=True)  # convert string id to int val then sort
    # https://stackoverflow.com/questions/37693600/how-to-sort-dataframe-based-on-particular-stringcolumns-using-python-pandas
    # df['sort'] = df['LocationsId'].str.extract(r'(\d)', expand=False).astype(int)
    df_locations['sort'] = df_locations['LocationsId'].astype(int)
    df_locations = df_locations.sort_values(['sort'], ascending=True)
    df_location['sort'] = df_location['LocationId'].astype(int)
    df_location = df_location.sort_values(['sort'], ascending=True)

    # df = df.sort_values(['LocationsId'], ascending=True)
    # df = df.sort_values(['date'], ascending=[1])
    # print(df)
    # for r1 in df:
    #     print(r1)
    now = datetime.now()
    filedatepart = now.strftime("%Y%m%d%H%M")
    write_file = open(download_folder + "jsonSqlite_locations" + filedatepart + ".txt", "w")
    tmpCnt = 0
    for index, row in df_locations.iterrows():
        print(row['sort'], row['LocationsId'] + ' ' + row['DateTime'])
#       insert locations row
        ilogin_id = row['LoginId'] if row['LoginId'].__str__() != '0' else '1'
        spathname = row['PathName']
        sdatetime = row['DateTime']
        izoomlevel = row['ZoomLevel'] if row['ZoomLevel'].__len__() != 0 else 'NULL'
        izoomtolatitude = row['ZoomToLatitude'] if row['ZoomToLatitude'].__len__() != 0 else 'NULL'
        izoomtolongitude = row['ZoomToLongitude'] if row['ZoomToLongitude'].__len__() != 0 else 'NULL'
        stotaltime = row['Totaltime']
        itotaldistance = row['TotalDistance']
        itotalsteps = row['TotalSteps']if row['TotalSteps'].__len__() != 0 else '0'
        iheartminutes = row['HeartDuration'] if row['HeartDuration'].__len__() != 0 else 'NULL'
        iheartpts = row['HeartIntensity'] if row['HeartIntensity'].__len__() != 0 else 'NULL'
        imoveminutes = row['MoveMinutes'] if row['MoveMinutes'].__len__() != 0 else 'NULL'
#       insert relevant location rows
        df_location1 = df_location.loc[(df_location['LocationsId'] == row['LocationsId'])]
        sSQLdjango = 'INSERT INTO ' + tblLocations + \
        ' (id,login_id,pathname,datetime,zoomlevel,zoomtolatitude,zoomtolongitude,totaltime,totaldistance,totalsteps,' \
        'heartminutes,heartpoints,moveminutes) SELECT (SELECT id FROM (SELECT MAX(id)+1 AS id FROM ' + \
                     tblLocations + ') AS locsid),' + ilogin_id + ",'" + spathname + "','" + \
                     sdatetime + "'," + izoomlevel + "," + izoomtolatitude + "," + \
                     izoomtolongitude + ",'" + stotaltime + "'," + itotaldistance + "," + \
                     itotalsteps + "," + iheartminutes + "," + iheartpts + "," + imoveminutes + \
                     ' WHERE NOT EXISTS (SELECT * FROM ' + tblLocations + ' WHERE login_id = ' + \
                     ilogin_id + " AND pathname = '" + spathname + "' AND datetime = '" + sdatetime + \
                     "' LIMIT 1); \n"
        # print(sSQLdjango)
        write_file.write(sSQLdjango)
        tmpCnt += 1
        for idx, rw in df_location1.iterrows():
            ilatitude = rw['Latitude']
            ilongitude = rw['Longitude']
            ialtitude = rw['Altitude']
            iactivityid = rw['ActivityId'] if rw['ActivityId'].__len__() != 0 else '-1'
            itransitionid = rw['TransitionId'] if rw['TransitionId'].__len__() != 0 else '-1'
            icolorpath = rw['ColorPath']
            iaccuracy = rw['Accuracy'] if rw['Accuracy'].__len__() != 0 else 'NULL'
            sdatetime = rw['DateTime']
            sSQLdjango2 = ""
            sSQLdjango2 = 'INSERT INTO ' + tblLocation + ' VALUES (NULL,' + ilatitude + ',' + \
                          ilongitude + ',' + ialtitude + ',' + iactivityid + ',' + itransitionid + ',' + icolorpath
            sSQLdjango2 = sSQLdjango2 + ',' + iaccuracy + ',\''
            sSQLdjango2 = sSQLdjango2 + sdatetime + "',"
            sSQLdjango2 = sSQLdjango2 + '(SELECT id FROM (SELECT MAX(id) AS id FROM ' + tblLocations + ") AS locs1)); \n"
            # print(sSQLdjango2)
            write_file.write(sSQLdjango2)
        if tmpCnt > 1:
            break

    write_file.close()

if __name__ == '__main__':
    # main()
    convertlocationsSqliteJSONToSqlite()



