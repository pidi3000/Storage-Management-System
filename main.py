from DB_Handler import *
import eel
import json

from difflib import SequenceMatcher
import distance
import time

from pathlib import Path

import os
import sys


# -------------------------------------------------------------
handlerParts = PartsHandler()
handlerTags = TagsHandler()
handlerStorage = StorageHandler()
handlerPartInStorage = PartInStorageHandler()
handlerPartHistory = PartHistoryHandler()
handlerAttachment = AttachmentsHandler()

localCache = {}



def loadTestDataToDB():
    # Create parts
    handlerParts.create("LED red", "A normal red LED")
    handlerParts.create("LED blue", "A normal blue SMD LED ")
    handlerParts.create("LED green", "A normal green THC LED")
    handlerParts.create("Arduino Mega",
                        "A Arduino Mega board with the ATmega 256 chip")

    # Create Tags
    handlerTags.create("LED", "Tag for leds")
    handlerTags.create("SMD", "SMD build format")
    handlerTags.create("THC", "Through hole component")
    handlerTags.create("Arduino", "Arduino boards")

    # Create Locations
    handlerStorage.create("C5", "Nothing")
    handlerStorage.create("B9", "Default")
    handlerStorage.create("R34")
    handlerStorage.create("A6")

    # Create Attachments
    handlerAttachment.create("image", "", "a4Doc.jpg")
    handlerAttachment.create(
        "image", " ", "Screenshot_2021-06-01_07-09-02.png")

    ##############################################

    # Connect Parts and Tags
    handlerParts.connectTag(1, 1)
    handlerParts.connectTag(2, 1)
    handlerParts.connectTag(3, 1)

    handlerParts.connectTag(2, 2)
    handlerParts.connectTag(3, 3)
    handlerParts.connectTag(4, 4)

    # Connect Parts and Attachment
    handlerParts.connectAttachment(2, 1)
    handlerParts.connectAttachment(3, 2)

    handlerParts.connectAttachment(4, 1)
    handlerParts.connectAttachment(4, 2)

    # Connect Parts and Location
    handlerPartInStorage.add(1, 1, 30)
    handlerPartInStorage.add(2, 2, 100)

    handlerPartInStorage.add(3, 3, 5214)
    handlerPartInStorage.add(3, 4, 56)

    handlerPartInStorage.add(4, 1, 19)
    handlerPartInStorage.add(4, 4, 5)


def reloadCache():
    global localCache
    localCache = {
        "parts": handlerParts.getAll(),
        "tags": handlerTags.getAll()
    }




# -------------------------------------------------------------
# Front end interaction functions

# Search Functions
# -------------------------------------------------------------


@eel.expose
def searchTag(searchText):
    resultTags = []
    allTags = handlerTags.getAll()
    
    for tag in allTags:
        # Check if search matches
        searchText = str(searchText).lower()
        tagNameFormated = str(tag[1]).lower()

        similarityRatio = SequenceMatcher(None, searchText, tagNameFormated).ratio()

        if searchText in tag[2].lower() or searchText in tagNameFormated or similarityRatio > 0.8:
            resultTags.append(
                {"ID": tag[0],
                 "Name": tag[1],
                 "Description": tag[2],
                 "similarityRatio": similarityRatio
                 })

    resultTags.sort(key=lambda tag: tag["similarityRatio"], reverse=True)
    return json.dumps(resultTags)


@eel.expose
def searchLocation(searchText):
    result = []
    allLocations = handlerStorage.getAll()
    searchText = searchText.lower()

    for location in allLocations:
        # Check if search matches
        searchText = str(searchText).lower()
        locationNameFormated = str(location[1]).lower()

        similarityRatio = SequenceMatcher(None, searchText, locationNameFormated).ratio()

        if searchText in location[2].lower() or searchText in locationNameFormated or similarityRatio > 0.8:
            result.append(
                {"ID": location[0],
                 "Name": location[1],
                 "Description": location[2],
                 "Space-Left": location[3],
                 "similarityRatio": similarityRatio
                 })

    result.sort(key=lambda part: part["similarityRatio"], reverse=True)
    return json.dumps(result)


@eel.expose
def searchPart(searchText, searchFilter=None):
    if searchFilter is not None:
        searchFilter = json.loads(searchFilter)

    result = []
    allParts = handlerParts.getAll()

    for part in allParts:
        partID = part[0]
        partName = part[1]
        partDescription = part[2]
        fitsFilter = True

        # check if filters are set and process them
        if searchFilter is not None:
            # check tag filter, tags are checked with AND rule
            allConnectedTagIDs = handlerParts.getConnectedTags(partID)
            for filterTagID in searchFilter["Tags"]:
                if int(filterTagID) not in allConnectedTagIDs:
                    fitsFilter = False
                    break

            # check location filter, tags are checked with AND rule
            allConnectedLocationIDs = []
            allLocations = handlerPartInStorage.getAllPartLocations(partID)
            for location in allLocations:
                allConnectedLocationIDs.append(location[2])

            for filterLocationID in searchFilter["Locations"]:
                if int(filterLocationID) not in allConnectedLocationIDs:
                    fitsFilter = False
                    break

        if fitsFilter:
            # find similarity to part name

            searchText = str(searchText).lower()
            partNameFormated = str(partName).lower()

            similarityRatio = SequenceMatcher(None, searchText, partNameFormated).ratio()
            similarityRatio1 = distance.nlevenshtein(searchText, partNameFormated, method=1)
            similarityRatio2 = distance.nlevenshtein(searchText, partNameFormated, method=2)
            #similarityRatio2 = distance.hamming(searchText, partName, normalized=True)

            if searchText in partNameFormated or searchText in str(partDescription).lower() or similarityRatio > 0.8:
                allLocations = handlerPartInStorage.getAllPartLocations(partID)
                totalQuantity = 0
                for location in allLocations:
                    totalQuantity += int(location[3])

                result.append(
                    {"ID": partID,
                    "Name": partName,
                    "Description": partDescription,
                    "Image": part[3],
                    "Total-Quantity": totalQuantity,
                    "similarityRatio": similarityRatio
                    })

    result.sort(key=lambda part: part["similarityRatio"], reverse=True)

    return json.dumps(result)


@eel.expose
def getPartData(partID):
    part = handlerParts.getByID(partID)

    # Process attachments
    allAttachements = handlerParts.getConnectedAttachments(partID)
    attachments = []
    for attachmentID in allAttachements:
        attachmentData = handlerAttachment.getByID(attachmentID)
        attachments.append(attachmentData[2] + "/" + attachmentData[3])

    # Process tags
    allTags = handlerParts.getConnectedTags(partID)
    tags = []
    for tagID in allTags:
        tags.append(handlerTags.getName(tagID))

    # Process locations
    allLocations = handlerPartInStorage.getAllPartLocations(partID)
    locations = []
    for location in allLocations:
        locationID = location[2]
        locationName = handlerStorage.getName(locationID)
        locationQuantity = location[3]

        locations.append({
            "ID": locationID,
            "Name": locationName,
            "Quantity": locationQuantity
        })

    # Combine all data
    partData = {
        "Name": part[1],
        "Description": part[2],
        "Image": part[3],
        "Tags": tags,
        "Attachments": attachments,
        "Locations": locations
    }

    return json.dumps(partData)


# -------------------------------------------------------------
if __name__ == '__main__':
    print("start")
    try:
        print("web start")
        eel.init('web')
        eel.start('test.html', block=False, mode='firefox')

        #loadTestDataToDB()
        my_file = Path("web/first-run.txt")
        if not (my_file.is_file()):
            loadTestDataToDB()
            with open('web/first-run.txt', 'w'): pass

        #reloadCache()
        print("test error")
        #raise ValueError("Crashed because I'm a bad exception")

        while True:
            eel.sleep(10)

    except Exception as e:
        f = open("crashlog.txt", "w")
        error_msg = str(e)
        print(error_msg)
        f.write("main crashed. Error: \n" + error_msg)
        f.close() 

    time.sleep(10)
    

          

