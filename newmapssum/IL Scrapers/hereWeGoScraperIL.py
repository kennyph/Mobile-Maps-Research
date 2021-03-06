import csv
import time
from selenium import webdriver
import pymysql

db = pymysql.connect(host="ec2-18-216-116-132.us-east-2.compute.amazonaws.com",
                     user="Kean",
                     passwd="MobileMapsResearch0718!",
                     db="MapData_IL",)

cursor = db.cursor()

url = 'https://wego.here.com/directions/drive/Kennedy-Expy-E,-Chicago,-IL-60656,-United-States:41.98233,-87.80144/Dan-Ryan-Expy-E,-Chicago,-IL-60609,-USA:loc-dmVyc2lvbj0xO3RpdGxlPURhbitSeWFuK0V4cHkrRTtsYXQ9NDEuODEzNzQ3O2xvbj0tODcuNjMwNjgzO3N0cmVldD1EYW4rUnlhbitFeHB5K0U7Y2l0eT1DaGljYWdvO3Bvc3RhbENvZGU9NjA2MDk7Y291bnRyeT1VU0E7ZGlzdHJpY3Q9RnVsbGVyK1Bhcms7c3RhdGVDb2RlPUlMO2NvdW50eT1Db29rO2NhdGVnb3J5SWQ9c3RyZWV0LXNxdWFyZTtzb3VyY2VTeXN0ZW09aW50ZXJuYWw?map=41.89812,-87.71607,12,normal'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

browser = webdriver.Chrome(executable_path='..\chromedriver',chrome_options=chrome_options)

def grabAndSave():
    browser.get(url)
    time.sleep(5)
    
    # Selects route 1 (unique) and retrieves route info        
    nav = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[1]/div/div[2]/div[3]/span[3]")
    data = (nav.text).splitlines()

    #Retrieves time data from Route 1
    time1 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[1]/div/div[2]/div[1]/span/span[1]")
    timedata1 = (time1.text).splitlines()

    #Retrieves distance data from Route 1
    distance1 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[1]/div/div[2]/div[3]/span[1]")
    distancedata1 = (distance1.text).splitlines()
    
    #Prints out Route 1 results
    print("Route: " + data[0] +" | Time: " + timedata1[0] + " | Distance: " + distancedata1[0])
    
    # Prepare clicker for route 2
    check1 = False;
    try:
        check1 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[2]/div/div[2]/div[3]/span[3]")
    except:
        print("There is no route 2 this time!")

    if (check1):
        # Gets route info from route 2
        nav1 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[2]/div/div[2]/div[3]/span[3]")
        data1 = (nav1.text).splitlines()

        #Retrieves time data from Route 2
        time2 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[2]/div/div[2]/div[1]/span/span[1]")
        timedata2 = (time2.text).splitlines()

        #Retrieves distance data from Route 2
        distance2 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[2]/div/div[2]/div[3]/span[1]")
        distancedata2 = (distance2.text).splitlines()

        #Prints out Route 2 results
        print("Route: " + data1[0] +" | Time: " + timedata2[0] + " | Distance: " + distancedata2[0])

    # Prepare Clicker for Route 3
    check2 = False;
    try:
        check2 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[3]/div/div[2]/div[3]/span[3]")
    except:
        print("There is no route 3 this time!")
    # Check if there is a route 3 available
    if (check2):
        # Get route info from Route 3
        nav2 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[3]/div/div[2]/div[3]/span[3]")
        data2 = (nav1.text).splitlines()
        #Retrieves time data from Route 1
        time3 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[3]/div/div[2]/div[1]/span")
        timedata3 = (time3.text).splitlines()
        #Retrieves distance data from Route 1
        distance3 = browser.find_element_by_xpath("//*[@id='routes_list']/div[2]/ul/li[3]/div/div[2]/div[3]/span[1]")
        distancedata3 = (distance3.text).splitlines()
        #Prints out Route 1 results
        print("Route: " + data2[0] +" | Time: " + timedata3[0] + " | Distance: " + distancedata3[0])

    print(readable)
    writer.writerow({'Route Number': 1, 'ETA': timedata1[0] + " min", 'Distance': distancedata1[0], 'Route': data[0], 'Time': readable})
    if (check1):
        writer.writerow({'Route Number': 2,'ETA': timedata2[0] + " min", 'Distance': distancedata2[0], 'Route': data1[0], 'Time': readable})
    if (check2):
        writer.writerow({'Route Number': 3,'ETA': timedata3[0] + " min", 'Distance': distancedata3[0], 'Route': data2[0], 'Time': readable})
    print ("Cycle completed\n\n")

    # upload to db
    sql = "INSERT INTO `HereWeGo` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"

    routenum1 = 1
    eta1 = timedata1[0] + " min"
    routedistance1 = distancedata1[0]
    routeinfo1 = data[0]
    currtime = readable

    if (check1):
        routenum2 = 2
        eta2 = timedata2[0] + " min"
        routedistance2 = distancedata2[0]
        routeinfo2 = data1[0]

    if (check2):
        routenum3 = 3
        eta3 = timedata3[0] + " min"
        routedistance3 = distancedata3[0]
        routeinfo3 = data2[0]

    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (routenum1, eta1, routedistance1, routeinfo1, currtime))
            db.commit()

            print("Route 1 data uploaded to database")
            if (check1):
                cursor.execute(sql, (routenum2, eta2, routedistance2, routeinfo2, currtime))
                db.commit()
                print("Route 2 data uploaded to database")

            if (check2):
                cursor.execute(sql, (routenum3, eta3, routedistance3, routeinfo3, currtime))
                db.commit()
                print("Route 3 data uploaded to database")

            print("All data uploaded to database")
    except Exception:
        print("Exception, there was an error uploading to the database")

with open('hereMapsDataCA.csv', 'w', newline='') as csvfile:
    fieldnames = ['Route Number', 'ETA', 'Distance', 'Route', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            ts = time.time()
            readable = time.ctime(ts)
            grabAndSave()
            time.sleep(1) # 298 second day, gives 2 seconds for the program to run
    except KeyboardInterrupt:
        print("\n\nStopped by KEYBOARD INTERRUMPTION\n\n")
        pass

browser.close()