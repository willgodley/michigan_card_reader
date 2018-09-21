import datetime
import time
import json
import csv

###############################################################################
###############################################################################
##########################        FUNCTIONS        ############################
###############################################################################
###############################################################################

def greeting():

    print()
    print("-"*50)
    print("Welcome to the Michigan IFC Card Swiper")
    print("-"*50)
    print()
    print("-"*50)
    print("What would you like to do?")
    print("1. Make guest list.")
    print("2. Search a past guest list.")

    while True:

        try:
            choice = int(input("> "))
            assert(choice == 1 or choice == 2)
            print("-"*50)
            print()
            break

        except:
            print("-"*50)
            print()
            print("-"*50)
            print("Invalid input!")
            print("-"*50)
            print()
            print("-"*50)
            print("1. Make guest list.")
            print("2. Search a past guest list.")

    return choice

def getCurrentDate():

    print("-"*50)
    print("Enter current date as MM DD YYYY: ")
    currentDate = input("> ")
    print("-"*50)
    print()

    while True:

        try:
            dates = currentDate.split()
            assert(len(dates[0]) == 2)
            assert(len(dates[1]) == 2)
            assert(len(dates[2]) == 4)
            month = int(dates[0])
            day = int(dates[1])
            year = int(dates[2])
            break

        except:
            print("-"*50)
            print("Wrong format")
            print("Enter current date as MM DD YYYY: ")
            currentDate = input("> ")
            print("-"*50)
            print()

    currentDate = str(month) + "_" + str(day) + "_" + str(year)

    return currentDate

def openSwipeJsonCache(currentDate):

    jsonCacheName = "Guest_List_" + currentDate + ".json"

    try:
        jsonCardCache = open(jsonCacheName, 'r')
        cardContents = jsonCardCache.read()
        jsonCardCache.close()
        jsonCardDict = json.loads(cardContents)
    except:
        jsonCardDict = {}

    return (jsonCardDict, jsonCacheName, currentDate)

def swipe():

    date = getCurrentDate()
    jsonCacheInfo = openSwipeJsonCache(date)
    jsonCacheDiction = jsonCacheInfo[0]
    jsonCacheName = jsonCacheInfo[1]

    print("-"*50)
    print("Swipe card")
    print("If not an Mcard, press 1")
    print("If they don't have a college ID, press 2")
    print("Type QUIT to exit")
    print("-"*50)
    print()

    cardData = input("> ")

    roundNum = 0

    if cardData == "quit":
        cardData = "QUIT"

    while cardData != "QUIT":

        if roundNum != 0:
            jsonCacheInfo = openSwipeJsonCache(date)
            jsonCacheDiction = jsonCacheInfo[0]
            jsonCacheName = jsonCacheInfo[1]

        if cardData == "1":
            personalData = []
            print()
            print("-"*50)
            print()
            print("Please type last name,first initial. Ex. SMITH,R.")
            name = input("> ")

            if name in jsonCacheDiction:
                jsonCacheDiction[name].append(getTime())

            else:
                print()
                print("Now swipe card")
                cardData = input("> ")
                print()
                print("-"*50)
                personalData.append("Non UM Student")
                personalData.append(cardData)
                personalData.append(getTime())
                jsonCacheDiction[name] = personalData

        elif cardData == "2":
            personalData = []

            print()
            print("-"*50)
            print("Please type last name,first initial. Ex. SMITH,R.")
            name = input("> ")

            if name in jsonCacheDiction:
                jsonCacheDiction[name].append(getTime())

            else:
                print()
                print("Is this person a UM student? (Y/N)")
                status = input("> ")

                while True:
                    if status == "Y" or status == "N":
                        if status == "Y":
                            personalData.append("UM Student")
                            personalData.append("Didn't have a card")
                            print()
                            print("Enter UMID")
                            UMID = input("> ")
                            while len(UMID) != 8:
                                print("Bad input. Please try again.")
                                UMID = input("> ")
                            personalData.append(UMID)
                        else:
                            personalData.append("Non UM Student")
                            personalData.append("Didn't have a card")
                        personalData.append(getTime())
                        jsonCacheDiction[name] = personalData
                        break
                    else:
                        while True:
                            print()
                            print("Bad Input. Try Again.")
                            print("Is this person a UM student? (Y/N)")
                            status = input("> ")

                            if status == "Y" or status == "N":
                                break

            print("-"*50)

        else:
            try:
                personalData = []
                UMID = cardData[8:16]
                cardDataSplit = cardData.split("^")
                name = cardDataSplit[1][:-2] + "," + cardDataSplit[1][-1]

                if name in jsonCacheDiction:
                    jsonCacheDiction[name].append(getTime())
                else:
                    personalData.append("UM Student")
                    personalData.append(cardData)
                    personalData.append(UMID)
                    personalData.append(getTime())
                    jsonCacheDiction[name] = personalData
            except:
                print()
                print("-"*50)
                print()
                print("-"*50)
                print("Input error. Please swipe/type again.")
                print("-"*50)

        closeSwipeCache(jsonCacheName, jsonCacheDiction)
        print()
        print("-"*50)
        print()
        cardData = input("> ")
        if cardData == 'quit':
            cardDate = 'QUIT'
        roundNum += 1

    return (jsonCacheDiction, date)

def closeSwipeCache(jsonCacheName, jsonCardDict):

    jsonCardCache = open(jsonCacheName, 'w')
    jsonCardCache.write(json.dumps(jsonCardDict))
    jsonCardCache.close()

def saveToCSV(cardDict, eventDate):

    csvFilename = "Guest_List_" + eventDate + ".csv"

    csvFile = open(csvFilename, "w")
    header = "Name     , UMID   , Time Entered  , Time Exited   \n"
    csvFile.write(header)

    for person in cardDict.keys():

        name = person
        nameInQuotes = "\"" + name + "\""

        if cardDict[person][0] == "UM Student":
            UMID = cardDict[person][2]
            timeIn = cardDict[person][3]
            try:
                timeOut = cardDict[person][4]
            except:
                timeOut = "N/A"

        else:
            UMID = "N/A"
            timeIn = cardDict[person][2]
            try:
                timeOut = cardDict[person][3]
            except:
                timeOut = "N/A"

        fullInfo = nameInQuotes + ',' + UMID + ',' + timeIn + ',' + timeOut + '\n'
        csvFile.write(fullInfo)

def openPastCache():

    while True:

        print("-"*50)
        print("Enter event date as MM DD YYYY: ")
        currentDate = input("> ")
        print("-"*50)
        print()

        while True:

            try:
                dates = currentDate.split()
                assert(len(dates[0]) == 2)
                assert(len(dates[1]) == 2)
                assert(len(dates[2]) == 4)
                month = int(dates[0])
                day = int(dates[1])
                year = int(dates[2])
                break

            except:
                print("-"*50)
                print("Wrong format")
                print("Enter event date as MM DD YYYY: ")
                currentDate = input("> ")
                print("-"*50)
                print()

        searchDate = str(month) + "_" + str(day) + "_" + str(year)

        jsonCacheName = "Guest_List_" + searchDate + ".json"

        try:
            jsonCardCache = open(jsonCacheName, 'r')
            cardContents = jsonCardCache.read()
            jsonCardCache.close()
            jsonCardDict = json.loads(cardContents)
            break
        except:
            print("-"*50)
            print("There was no event on this date.")
            print("-"*50)
            print()

    return(jsonCardDict, searchDate)

def printGuestList(jsonCardDict, date):

    print("-"*50)
    print("Guest info for event on " + date)
    print("-"*50)

    for a in jsonCardDict:
        if jsonCardDict[a][0] == "UM Student":
            if len(jsonCardDict[a]) == 5:
                data = jsonCardDict[a]
                print()
                print("Name: " + a)
                print("UMID: " + str(data[2]))
                print("Time in: " + str(data[3]))
                print("Time out: " + str(data[4]))
            else:
                data = jsonCardDict[a]
                print()
                print("Name: " + a)
                print("UMID: " + str(data[2]))
                print("Time in: " + str(data[3]))

        elif jsonCardDict[a][0] == "Non UM Student":
            if len(jsonCardDict[a]) == 3:
                data = jsonCardDict[a]
                print()
                print("Name: " + a)
                print("Time in: " + str(data[2]))
            else:
                data = jsonCardDict[a]
                print()
                print("Name: " + a)
                print("Time in: " + str(data[2]))
                print("Time out: " + str(data[3]))

    print()

def printSearchGreeting():

    print("-"*50)
    print("What would you like to do?")
    print("1. Print entire guest list")
    print("2. Search for a specific person")
    goal = input("> ")
    print("-"*50)
    print()

    while True:
        if goal == "1" or goal == "2":
            break
        print()
        print("Invalid selection. Try again.")
        goal = input("> ")

    return goal

def printSpecificNames(jsonCardDict):

    print("-"*50)
    print("Enter a name as last name,first initial. Ex. SMITH,R.")
    name = input("> ")
    print("-"*50)
    print()

    if name not in jsonCardDict:
        print("-"*50)
        print("This person did not attend")
        print("-"*50)
        print()
    else:
        data = jsonCardDict[name]
        if data[0] == "Non UM Student":
            if len(data) == 3:
                swipeInfo = str(data[1])
                timeIn = str(data[2])

                print("-"*50)
                print(name + " entered at " + timeIn + ".")
                print("-"*50)
                print()

            else:
                swipeInfo = str(data[1])
                timeIn = str(data[2])
                timeOut = str(data[3])

                print("-"*50)
                print(name + " entered at " + timeIn + ", left at " + timeOut + ".")
                print("-"*50)
                print()

            print("-"*50)
            print("Do you want the full swipe info? (Y/N)")
            decision = input("> ")
            print("-"*50)
            print()
            if decision == "Y":
                print("-"*50)
                print("Full info received from swipe:")
                print(swipeInfo)
                print("-"*50)
                print()

        elif data[0] == "UM Student":
            if len(data) == 4:
                swipeInfo = str(data[1])
                UMID = str(data[2])
                timeIn = str(data[3])

                print("-"*50)
                print(name + " entered at " + timeIn + ", their UMID is " + UMID + ".")
                print("-"*50)
                print()

            elif len(data) == 5:
                swipeInfo = str(data[1])
                UMID = str(data[2])
                timeIn = str(data[3])
                timeOut = str(data[4])

                print("-"*50)
                print(name + " entered at " + timeIn + ", left at " + timeOut + ", their UMID is " + UMID + ".")
                print("-"*50)
                print()

            print("-"*50)
            print("Do you want the full swipe info? (Y/N)")
            decision = input("> ")
            print("-"*50)
            print()
            if decision == "Y":
                print("-"*50)
                print("Full info received from swipe:")
                print(swipeInfo)
                print("-"*50)
                print()

def printSearchEnding():

    print("-"*50)
    print("What do you want to do now?")
    print("1. Get info for same event")
    print("2. Pick new event")
    print("3. Quit")
    decision = input("> ")
    print("-"*50)
    print()

    return decision

def getTime():
    badTime = str(datetime.datetime.now().time())
    hour1 = badTime[:2]
    hour = int(badTime[:2])
    if hour > 12:
        hour -= 12
        timeFixed = str(hour) + badTime[2:8] + " PM"
    else:
        timeFixed = badTime[:8] + " AM"

    return timeFixed

###############################################################################
###############################################################################
#############################       MAIN       ################################
###############################################################################
###############################################################################

def main():
    choice = greeting()

    if choice == 1:

        info = swipe()

        cardDict = info[0]
        date = info[1]

        saveToCSV(cardDict, date)

    elif choice == 2:

        skipNewCache = False

        while True:

            if skipNewCache == True:
                junk = 1
            else:
                jsonCacheData = openPastCache()
                jsonCacheDict = jsonCacheData[0]
                searchDate = jsonCacheData[1]

            goal = printSearchGreeting()

            if goal == "1":

                printGuestList(jsonCacheDict, searchDate)

            elif goal == "2":

                printSpecificNames(jsonCacheDict)

            decision = printSearchEnding()

            if decision == "1":
                skipNewCache = True
                continue
            elif decision == "2":
                skipNewCache = False
                continue
            else:
                break

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

main()
