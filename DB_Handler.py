from datetime import datetime 
import sqlite3
import json


#datetime.now()



def openConnection():
    dbName = "test.db"
    connection = sqlite3.connect(dbName)

    return connection

def checkDBSetup():
    connection = openConnection()
    cursor = connection.cursor()
    with open('DB_Structure.json') as f:
        dbTables = json.load(f)

    for tableName in dbTables:
        tableStructure = dbTables[tableName]

        sqlCreateTable = "CREATE TABLE IF NOT EXISTS " + tableName + " ( "

        primaryKeys = ""
        for columnName in tableStructure:
            columnData = tableStructure[columnName]

            sqlCreateTable += columnName + " "
            sqlCreateTable += columnData["Type"] + " "

            if "NOT NULL" in columnData:
                if columnData["NOT NULL"]:
                    sqlCreateTable += "NOT NULL "

            if "PRIMARY KEY" in columnData:
                if columnData["PRIMARY KEY"]:
                    primaryKeys += columnName + ", "

            if "AUTO_INCREMENT" in columnData:
                if columnData["AUTO_INCREMENT"]:
                    pass  # sqlCreateTable += "AUTOINCREMENT "

            sqlCreateTable += ", "

        if primaryKeys != "":
            sqlCreateTable += "PRIMARY KEY (" + primaryKeys[:-2] + ")"

        if sqlCreateTable[-2:] == ", ":
            sqlCreateTable = sqlCreateTable[:-3]

        sqlCreateTable += ") "

        # print(sqlCreateTable)
        cursor.execute(sqlCreateTable)

    connection.close()

def runQuery(sqlQuery, dataList):
    connection = openConnection()
    cursor = connection.cursor()

    if dataList == None:
        result = cursor.execute(sqlQuery)
    else:
        result = cursor.execute(sqlQuery, dataList)
    rows = result.fetchall()

    connection.commit()
    connection.close()
    return rows

##################################################################################

class PartsHandler:
    # SQL Querys
    sqlTableName = "Parts"
    sqlPrefix = "Part"

    sqlCreate = f"INSERT INTO {sqlTableName} ({sqlPrefix}_Name, {sqlPrefix}_Description, {sqlPrefix}_Image) VALUES(?,?,?)"
    sqlDelete = f"DELETE FROM {sqlTableName} WHERE {sqlPrefix}_ID = ?"

    sqlGetAll = f"SELECT * FROM {sqlTableName} ORDER BY Part_Name"
    sqlGetByID = f"SELECT * FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"

    sqlUpdateName = f"UPDATE {sqlTableName} SET {sqlPrefix}_Name = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateDescription = f"UPDATE {sqlTableName} SET {sqlPrefix}_Description = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateImage = f"UPDATE {sqlTableName} SET {sqlPrefix}_Image = ? WHERE {sqlPrefix}_ID = ?"

    ##############################

    sqlConnectTag = "INSERT INTO Parts_Tagging (Part_ID, Tag_ID) VALUES(?,?)"
    sqlDisconnectTag = "DELETE FROM Parts_Tagging WHERE Part_ID = ? AND Tag_ID = ?"
    sqlGetConnectedTags = "SELECT Tag_ID FROM Parts_Tagging WHERE Part_ID = ?"

    ##############################

    sqlConnectAttachment = "INSERT INTO Parts_Attachment (Part_ID, Attachment_ID, Note) VALUES(?,?,?)"
    sqlDisconnectAttachment = "DELETE FROM Parts_Attachment WHERE Part_ID = ? AND Attachment_ID = ?"
    sqlGetConnectedAttachments = "SELECT Attachment_ID FROM Parts_Attachment WHERE Part_ID = ?"
    sqlGetAttachmentNote = "SELECT Note FROM Parts_Attachment WHERE Part_ID = ? AND Attachment_ID = ?"

    ########################################################################

    def __init__(self):
        pass #print("class start")
        
    def create(self, name, description = "", image = ""):
        if image == "":
            image = "/data/attachments/default-image-620x600.jpg"
        return runQuery(self.sqlCreate, (name, description, image))

    def delete(self, partID):
        return runQuery(self.sqlDelete, (partID, ))

    def getByID(self, partID):
        return runQuery(self.sqlGetByID, (partID, ))[0]

    def getAll(self):
        return runQuery(self.sqlGetAll, None)

    def updateName(self, partID, name):
        return runQuery(self.sqlUpdateName, (name, partID, ))

    def updateDescription(self, partID, description):
        return runQuery(self.sqlUpdateDescription, (description, partID, ))

    def updateImage(self, partID, image):
        return runQuery(self.sqlUpdateImage, (image, partID, ))
    #########################################
    #              Tag Handler              #
    #########################################

    def connectTag(self, partID, tagID):
        return runQuery(self.sqlConnectTag, (partID, tagID, ))

    def disconnectTag(self, partID, tagID):
        return runQuery(self.sqlDisconnectTag, (partID, tagID, ))

    def getConnectedTags(self, partID):
        tagList = []
        for tag in runQuery(self.sqlGetConnectedTags, (partID, )):
            tagList.append(tag[0])

        return tagList

    #########################################
    #           Attachment Handler          #
    #########################################

    def connectAttachment(self, partID, attachmentID, note=""):
        return runQuery(self.sqlConnectAttachment, (partID, attachmentID, note, ))

    def disconnectAttachment(self, partID, attachmentID):
        return runQuery(self.sqlDisconnectAttachment, (partID, attachmentID, ))

    def getConnectedAttachments(self, partID):
        attachmentList = []
        for attachment in runQuery(self.sqlGetConnectedAttachments, (partID, )):
            attachmentList.append(attachment[0])

        return attachmentList

    def getAttachmentNote(self, partID, attachmentID):
        return runQuery(self.sqlGetAttachmentNote, (partID, attachmentID, ))
#########################################################################################

class TagsHandler:
    # SQL Querys
    sqlTableName = "Tags"
    sqlPrefix = "Tag"

    sqlCreate = f"INSERT INTO {sqlTableName} ({sqlPrefix}_Name, {sqlPrefix}_Description) VALUES(?,?)"
    sqlDelete = f"DELETE FROM {sqlTableName} WHERE {sqlPrefix}_ID = ?"

    sqlGetAll = f"SELECT * FROM {sqlTableName} ORDER BY {sqlPrefix}_Name"
    sqlGetByID = f"SELECT * FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"
    sqlGetName = f"SELECT {sqlPrefix}_Name FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"

    sqlUpdateName = f"UPDATE {sqlTableName} SET {sqlPrefix}_Name = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateDescription = f"UPDATE {sqlTableName} SET {sqlPrefix}_Description = ? WHERE {sqlPrefix}_ID = ?"

    ########################################################################

    def __init__(self):
        pass #print("class start")
        
    def create(self, name, description = ""):
        return runQuery(self.sqlCreate, (name, description))

    def delete(self, tagID):
        return runQuery(self.sqlDelete, (tagID, ))

    def getByID(self, tagID):
        return runQuery(self.sqlGetByID, (tagID, ))

    def getAll(self):
        return runQuery(self.sqlGetAll, None)

    def getName(self, tagID):
        return runQuery(self.sqlGetName, (tagID, ))[0][0]

    def updateName(self, tagID, name):
        return runQuery(self.sqlUpdateName, (name, tagID, ))

    def updateDescription(self, tagID, description):
        return runQuery(self.sqlUpdateDescription, (description, tagID, ))
#########################################################################################

class StorageHandler:
    # SQL Querys
    sqlTableName = "Storage_Location"
    sqlPrefix = "Location"

    sqlCreate = f"INSERT INTO {sqlTableName} ({sqlPrefix}_Name, {sqlPrefix}_Description, Space_Left) VALUES(?,?,?)"
    sqlDelete = f"DELETE FROM {sqlTableName} WHERE {sqlPrefix}_ID = ?"

    sqlGetAll = f"SELECT * FROM {sqlTableName} ORDER BY {sqlPrefix}_Name"
    sqlGetByID = f"SELECT * FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"
    sqlGetName = f"SELECT {sqlPrefix}_Name FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"

    sqlUpdateName = f"UPDATE {sqlTableName} SET {sqlPrefix}_Name = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateDescription = f"UPDATE {sqlTableName} SET {sqlPrefix}_Description = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateSpaceLeft = f"UPDATE {sqlTableName} SET Space_Left = ? WHERE {sqlPrefix}_ID = ?"

    ##############################

    sqlConnectAttachment = "INSERT INTO Parts_Attachment (Part_ID, Attachment_ID) VALUES(?,?)"
    sqlDisconnectAttachment = "DELETE FROM Parts_Attachment WHERE Part_ID = ? AND Attachment_ID = ?"
    sqlGetConnectedAttachments = "SELECT Attachment_ID FROM Parts_Attachment WHERE Part_ID = ?"

    ########################################################################

    def __init__(self):
        pass #print("class start")
        
    def create(self, name, description = "", spaceLeft = "a lot"):
        return runQuery(self.sqlCreate, (name, description, spaceLeft))

    def delete(self, locationID):
        return runQuery(self.sqlDelete, (locationID, ))

    def getByID(self, locationID):
        return runQuery(self.sqlGetByID, (locationID, ))

    def getAll(self):
        return runQuery(self.sqlGetAll, None)

    def getName(self, locationID):
        return runQuery(self.sqlGetName, (locationID, ))[0][0]

    def updateName(self, locationID, name):
        return runQuery(self.sqlUpdateName, (name, locationID, ))

    def updateDescription(self, locationID, description):
        return runQuery(self.sqlUpdateDescription, (description, locationID, ))

    def updateSpaceLeft(self, locationID, spaceLeft):
        return runQuery(self.sqlUpdateSpaceLeft, (spaceLeft, locationID, ))

    #########################################
    #           Attachment Handler          #
    #########################################

    def connectAttachment(self, partID, attachmentID):
        return runQuery(self.sqlConnectTag, (partID, attachmentID, ))

    def disconnectAttachment(self, partID, attachmentID):
        return runQuery(self.sqlDisconnectTag, (partID, attachmentID, ))

    def getConnectedAttachments(self, partID):
        return runQuery(self.sqlGetConnectedTags, (partID, ))
#########################################################################################

class PartInStorageHandler:
    # SQL Querys
    sqlTableName = "Parts_In_Storage"
    sqlPrefix = "PS"

    sqlAdd = f"INSERT INTO {sqlTableName} (Part_ID, Location_ID, Quantity) VALUES(?,?,?)"
    sqlRemove = f"DELETE FROM {sqlTableName} WHERE {sqlPrefix}_ID = ?"

    sqlGetAll = f"SELECT * FROM {sqlTableName}"
    sqlGetByID = f"SELECT * FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"
    sqlGetAllPartLocations = f"SELECT * FROM {sqlTableName} WHERE Part_ID = ?"

    sqlUpdateLocation = f"UPDATE {sqlTableName} SET Location_ID = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateQuantity = f"UPDATE {sqlTableName} SET Quantity = ? WHERE {sqlPrefix}_ID = ?"

    ##############################

    sqlConnectAttachment = "INSERT INTO Parts_Attachment (Part_ID, Attachment_ID) VALUES(?,?)"
    sqlDisconnectAttachment = "DELETE FROM Parts_Attachment WHERE Part_ID = ? AND Attachment_ID = ?"
    sqlGetConnectedAttachments = "SELECT Attachment_ID FROM Parts_Attachment WHERE Part_ID = ?"

    ########################################################################

    def __init__(self):
        pass #print("class start")
        
    def add(self, Part_ID, Location_ID, Quantity):
        return runQuery(self.sqlAdd, (Part_ID, Location_ID, Quantity))

    def remove(self, psID):
        return runQuery(self.sqlRemove, (psID, ))

    def getByID(self, psID):
        return runQuery(self.sqlGetByID, (psID, ))

    def getAllPartLocations(self, partID):
        return runQuery(self.sqlGetAllPartLocations, (partID, ))

    def getAll(self):
        return runQuery(self.sqlGetAll, None)

    def updateLocation(self, psID, location_ID):
        return runQuery(self.sqlUpdateLocation, (location_ID, psID, ))

    def updateQuantity(self, psID, quantity):
        return runQuery(self.sqlUpdateQuantity, (quantity, psID, ))

    #########################################
    #           Attachment Handler          #
    #########################################

    def connectAttachment(self, partID, attachmentID):
        return runQuery(self.sqlConnectTag, (partID, attachmentID, ))

    def disconnectAttachment(self, partID, attachmentID):
        return runQuery(self.sqlDisconnectTag, (partID, attachmentID, ))

    def getConnectedAttachments(self, partID):
        return runQuery(self.sqlGetConnectedTags, (partID, ))
#########################################################################################

class PartHistoryHandler:
    # SQL Querys
    sqlTableName = "Part_History"
    sqlPrefix = "Event"

    sqlCreate = f"INSERT INTO {sqlTableName} (PS_ID, Date, Quantity, Note) VALUES(?,?,?,?)"
    sqlDelete = f"DELETE FROM {sqlTableName} WHERE {sqlPrefix}_ID = ?"

    sqlGetAll = f"SELECT * FROM {sqlTableName}"
    sqlGetByID = f"SELECT * FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"
    sqlGetPartHistory = f"SELECT * FROM {sqlTableName} WHERE PS_ID = ?"

    sqlUpdateQuantity = f"UPDATE {sqlTableName} SET Quantity = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateNote = f"UPDATE {sqlTableName} SET Note = ? WHERE {sqlPrefix}_ID = ?"

    ########################################################################

    def __init__(self):
        pass #print("class start")
        
    def create(self, PS_ID, Quantity, Note = ""):
        return runQuery(self.sqlCreate, (PS_ID, datetime.now(), Quantity, Note))

    def delete(self, eventID):
        return runQuery(self.sqlDelete, (eventID, ))

    def getByID(self, eventID):
        return runQuery(self.sqlGetByID, (eventID, ))

    def getPartHistory(self, psID):
        return runQuery(self.sqlGetPartHistory, (psID, ))

    def getAll(self):
        return runQuery(self.sqlGetAll, None)

    def updateQuantity(self, eventID, quantity):
        return runQuery(self.sqlUpdateQuantity, (quantity, eventID, ))

    def updateNote(self, eventID, Note):
        return runQuery(self.sqlUpdateNote, (Note, eventID, ))
#########################################################################################

class AttachmentsHandler:
    # SQL Querys
    sqlTableName = "Attachments"
    sqlPrefix = "Attachment"

    sqlCreate = f"INSERT INTO {sqlTableName} (File_Type, File_Directory, File_Name) VALUES(?,?,?)"
    sqlDelete = f"DELETE FROM {sqlTableName} WHERE {sqlPrefix}_ID = ?"

    sqlGetAll = f"SELECT * FROM {sqlTableName}"
    sqlGetByID = f"SELECT * FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"
    sqlGetDirectory = f"SELECT File_Directory FROM {sqlTableName} WHERE {sqlPrefix}_ID = ? LIMIT 1"

    sqlUpdateType = f"UPDATE {sqlTableName} SET File_Type = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateDirectory = f"UPDATE {sqlTableName} SET File_Directory = ? WHERE {sqlPrefix}_ID = ?"
    sqlUpdateName = f"UPDATE {sqlTableName} SET File_Name = ? WHERE {sqlPrefix}_ID = ?"

    ########################################################################

    def __init__(self):
        pass #print("class start")
        
    def create(self, File_Type, File_Directory, File_Name):
        return runQuery(self.sqlCreate, (File_Type, File_Directory, File_Name))

    def delete(self, Attachment_ID):
        return runQuery(self.sqlDelete, (Attachment_ID, ))

    def getByID(self, Attachment_ID):
        return runQuery(self.sqlGetByID, (Attachment_ID, ))[0]

    def getAll(self):
        return runQuery(self.sqlGetAll, None)

    def updateType(self, Attachment_ID, type):
        return runQuery(self.sqlUpdateType, (type, Attachment_ID, ))

    def updateDirectory(self, Attachment_ID, directory):
        return runQuery(self.sqlUpdateDirectory, (directory, Attachment_ID, ))

    def updateName(self, Attachment_ID, name):
        return runQuery(self.sqlUpdateName, (name, Attachment_ID, ))
#########################################################################################



checkDBSetup()


#print (temp.getAll())