

class DataHandler:

    baseSqlQuerys = {
        "add" : "INSERT INTO %s (%s_Name, %s_Description) VALUES(?,?)",
        "delete" : "DELETE FROM %s WHERE %s_ID = ?",

        "update-value" : "UPDATE %s SET %s = ? WHERE %s_ID = ?",
        
        "get-one" : "SELECT * FROM %s WHERE %s_ID = ?",
        "get-all" : "SELECT * FROM %s"
    }

    sqlQuerys = {
        "Parts" : {
            "add" : baseSqlQuerys["add"] % ("Parts", "Part", "Part"),
            "delete" : baseSqlQuerys["delete"] % ("Parts", "Part"),

            "update-name" : baseSqlQuerys["update-value"] % ("Parts", "Part_Name", "Part"),
            "update-description" : baseSqlQuerys["update-value"] % ("Parts", "Part_Description", "Part"),
            
            "get-one" : baseSqlQuerys["get-one"] % ("PARTS", "Part"),
            "get-all" : baseSqlQuerys["get-all"] % ("PARTS")
        },
        "Tags": {
            "add" : baseSqlQuerys["add"] % ("Tags", "Tag", "Tag"),
            "delete" : baseSqlQuerys["delete"] % ("Tags", "Tag"),

            "update-name" : baseSqlQuerys["update-value"] % ("Tags", "Tag_Name", "Tag"),
            "update-description" : baseSqlQuerys["update-value"] % ("Tags", "Tag_Description", "Tag"),
            
            "get-one" : baseSqlQuerys["get-one"] % ("TagS", "Tag"),
            "get-all" : baseSqlQuerys["get-all"] % ("TagS")
        },
        "Location" :{
            "add" : baseSqlQuerys["add"] % ("Storage_Location", "Location", "Location"),
            "delete" : baseSqlQuerys["delete"] % ("Storage_Location", "Location"),

            "update-name" : baseSqlQuerys["update-value"] % ("Storage_Location", "Location_Name", "Location"),
            "update-description" : baseSqlQuerys["update-value"] % ("Storage_Location", "Location_Description", "Location"),
            "update-spaceleft" : baseSqlQuerys["update-value"] % ("Storage_Location", "Space_Left", "Location"),
            
            "get-one" : baseSqlQuerys["get-one"] % ("Storage_Location", "Location"),
            "get-all" : baseSqlQuerys["get-all"] % ("Storage_Location")
        },
        "Attachments":{
            "add" : "INSERT INTO Attachments (File_Type, File_Directory, File_Name) VALUES(?,?,?)",
            "delete" : baseSqlQuerys["delete"] % ("Attachments", "Attachment"),

            "update-type" : baseSqlQuerys["update-value"] % ("Attachments", "File_Type", "Attachment"),
            "update-name" : baseSqlQuerys["update-value"] % ("Attachments", "File_Name", "Attachment"),
            "update-directory" : baseSqlQuerys["update-value"] % ("Attachments", "File_Directory", "Attachment"),
            
            "get-one" : baseSqlQuerys["get-one"] % ("Attachments", "Attachment"),
            "get-all" : baseSqlQuerys["get-all"] % ("Attachments")
        },
        "Parts_In_Storage":{
            "add" : "INSERT INTO Parts_In_Storage (Part_ID, Location_ID, Quantity) VALUES(?,?,?)",
            "delete" : baseSqlQuerys["delete"] % ("Parts_In_Storage", "PS"),

            "update-location" : baseSqlQuerys["update-value"] % ("Parts_In_Storage", "Location_ID", "PS"),
            "update-quantity" : baseSqlQuerys["update-value"] % ("Parts_In_Storage", "Quantity", "PS"),
            
            "get-one" : baseSqlQuerys["get-one"] % ("Parts_In_Storage", "PS"),
            "get-all" : baseSqlQuerys["get-all"] % ("Parts_In_Storage")
        },
        "Part_History":{
            "add" : "INSERT INTO Part_History (Event_ID, PS_ID, Date, Quantity, Note) VALUES(?,?,?,?,?)",
            "delete" : baseSqlQuerys["delete"] % ("Part_History", "Event"),

            "update-quantity" : baseSqlQuerys["update-value"] % ("Part_History", "Quantity", "Event"),
            "update-note" : baseSqlQuerys["update-value"] % ("Part_History", "Note", "Event"),
            
            "get-one" : baseSqlQuerys["get-one"] % ("Part_History", "Event"),
            "get-all" : baseSqlQuerys["get-all"] % ("Part_History")
        }
    }

    def addEntry(self, tablename, entryDataList):
        return runQuery(self.sqlQuerys[tablename]["add"], entryDataList)

    def deleteEntry(self, tablename, entryDataList):
        return runQuery(self.sqlQuerys[tablename]["delete"], entryDataList)

    def getEntryByID(self, tablename, entryID):
        return runQuery(self.sqlQuerys[tablename]["get-one"], (entryID, ))

    def getAllEntrys(self, tablename):
        return runQuery(self.sqlQuerys[tablename]["get-all"], None)

    def updateEntry(self, tablename, attribute, entryID, value):
        return runQuery(self.sqlQuerys[tablename]["update-" + attribute], (value, entryID))
