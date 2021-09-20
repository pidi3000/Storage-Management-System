
import os
from shutil import copyfile

import json
import eel
import tkinter as tk
from tkinter import filedialog


from DB_Handler import *
from Part_Handler import *

from difflib import SequenceMatcher
import distance
import time

# -------------------------------------------------------------
handlerParts = PartsHandler()
handlerTags = TagsHandler()
handlerStorage = StorageHandler()
handlerPartInStorage = PartInStorageHandler()
handlerPartHistory = PartHistoryHandler()
handlerAttachment = AttachmentsHandler()


# -------------------------------------------------------------
# Front end interaction functions

# Search Functions
# -------------------------------------------------------------



@eel.expose
def ask_file():
    # file_flags consists of tuple of tuples, i.e. (("jpeg files", "*.jpg"), ("all files", "*.*))
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    file_path = filedialog.askopenfile(initialdir=os.path.expanduser("~/Desktop"), title="Select File",
                                       filetypes=(("Images", "*.png, *.jpg"), ("all files", "*.*"),))
    print(file_path.name)
    root.destroy()

    if file_path.name:
        # copy file
        file_name = os.path.basename(file_path.name)

        new_Image_Path = "data/attachment/temp/" + file_name
        new_Image_Web_Path = "attachment/temp/" + file_name

        copyfile(file_path.name, new_Image_Path)

        return new_Image_Web_Path

    return None
    # return file_path.name if file_path.name else ""


# Search Stuff
@eel.expose
def searchTag(searchText):
    resultTags = []
    allTags = handlerTags.getAll()

    for tag in allTags:
        # Check if search matches
        searchText = str(searchText).lower()
        tagNameFormated = str(tag[1]).lower()

        similarityRatio = SequenceMatcher(
            None, searchText, tagNameFormated).ratio()

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

        similarityRatio = SequenceMatcher(
            None, searchText, locationNameFormated).ratio()

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

            similarityRatio = SequenceMatcher(
                None, searchText, partNameFormated).ratio()
            similarityRatio1 = distance.nlevenshtein(
                searchText, partNameFormated, method=1)
            similarityRatio2 = distance.nlevenshtein(
                searchText, partNameFormated, method=2)
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
        ps_ID = location[0]
        locationName = handlerStorage.getName(locationID)
        locationQuantity = location[3]

        locations.append({
            "ID": locationID,
            "PS_ID": ps_ID,
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


# Part handling
#############################################################################################
@eel.expose
def addNewPart(json_Part_Data):
    part_Data = json.loads(json_Part_Data)

    return handleNewPart(part_Data)

@eel.expose
def editPart(partID, json_Part_Data):
    part_Data = json.loads(json_Part_Data)

    return handleEditPart(partID, part_Data)

@eel.expose
def deletePart(partID):
    return handleDeletePart(partID)


# -------------------------------------------------------------
if __name__ == '__main__':
    print("start")
    try:
        print("Web start")
        eel.init("data")
        eel.start('test.html', block=False, mode='firefox')

        while True:
            eel.sleep(10)

    except (SystemExit, MemoryError, KeyboardInterrupt):
        # Handle errors and the potential hanging python.exe process
        print("Closing task")
        sys.exit()

        os.system('taskkill /F /IM python.exe /T')
        print("done")

    except Exception as e:
        f = open("crashlog.txt", "w")
        error_msg = str(e)
        print(error_msg)
        f.write("main crashed. Error: \n" + error_msg)
        f.close()

    time.sleep(10)
