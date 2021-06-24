import eel
import json

eel.init('')
eel.start('web/test.html', block=False)


print("test")

testPartData = []

tempPart = {}
tempPart["ID"] = "123456789"
tempPart["Name"] = "Name 1"
tempPart["Total-Quantity"] = "3"
tempPart["Description"] = "This is a template description. This is for testing purpouses only."
tempPart["Image"] = "/data/attachments/default-image-620x600.jpg"
tempPart["Locations"] = [
    {
        "ID": 5,
        "Name": "C9",
        "Quantity": 5
    },
    {
        "ID": 6,
        "Name": "A76",
        "Quantity": 100
    },
    {
        "ID": 7,
        "Name": "R2",
        "Quantity": 13
    },
    {
        "ID": 8,
        "Name": "F6",
        "Quantity": 45
    }
]
tempPart["Tags"] = [
    "Tag100",
    "Sample Tag Name",
    "Tag34",
    "Tag310",
]
tempPart["Attachements"] = [
    "/Screenshot_2021-06-01_07-09-02.png"
]

testPartData.append(tempPart)

tempPart = {}
tempPart["ID"] = "987654321"
tempPart["Name"] = "Name 2"
tempPart["Total-Quantity"] = "500"
tempPart["Description"] = "This is a template description. This is for testing purpouses only.This is a template description. This is for testing purpouses only.This is a template description. This is for testing purpouses only.This is a template description. This is for testing purpouses only.This is a template description. This is for testing purpouses only."
tempPart["Image"] = ""
tempPart["Locations"] = [
    {
        "ID": 1,
        "Name": "C5C5C5C5C5C5 C5C5C5C5C5C5",
        "Quantity": 486
    },
    {
        "ID": 2,
        "Name": "A14",
        "Quantity": 1896
    },
    {
        "ID": 3,
        "Name": "R6",
        "Quantity": 78
    },
    {
        "ID": 4,
        "Name": "F2",
        "Quantity": 16
    }
]
tempPart["Tags"] = [
    "Tag1",
    "Sample Tag Name",
    "Tag4",
    "Tag10",
]
tempPart["Attachements"] = [
    "/temp/a4Doc.jpg",
    "/Screenshot_2021-06-01_07-09-02.png",
    "/temp/a4Doc.jpg",
    "/Screenshot_2021-06-01_07-09-02.png"
]

testPartData.append(tempPart)

eel.my_function("Test", " 12")

# Search Functions
# -------------------------------------------------------------
@eel.expose
def searchTag(searchText):
    tagList = [
        {"ID": 1, "Name": "SMD"},
        {"ID": 2, "Name": "20mm"},
        {"ID": 3, "Name": "LED"},
        {"ID": 4, "Name": "THC"},
    ]

    return json.dumps(tagList)


@eel.expose
def searchLocation(searchText):
    tagList = [
        {"ID": 1, "Name": "C8"},
        {"ID": 2, "Name": "A5"},
        {"ID": 3, "Name": "R42"},
        {"ID": 4, "Name": "B6"},
    ]

    return json.dumps(tagList)


@eel.expose
def searchPart(searchText, searchFilter=None):
    if searchFilter is not None:
        searchFilter = json.loads(searchFilter)

    searchResult = testPartData

    print(searchText, " , ", searchFilter)

    return json.dumps(searchResult)


@eel.expose
def getPartData(partID):
    for part in testPartData:
        if part["ID"] == partID:
            return json.dumps(part)

    return "none"




# -------------------------------------------------------------
while True:
    eel.sleep(10)
