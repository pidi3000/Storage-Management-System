
import os
from shutil import copyfile

from DB_Handler import *


def handleNewPart(part_Data):
    handlerParts = PartsHandler()

    # TODO check file name is unique
    image_File_Name = os.path.basename(part_Data["part_ImageWebPath"])

    old_Image_Path = "data/" + part_Data["part_ImageWebPath"]

    new_Image_Path = "data/attachment/" + image_File_Name
    new_Image_Web_Path = "attachment/" + image_File_Name

    copyfile(old_Image_Path, new_Image_Path)
    os.remove(old_Image_Path)

    handlerParts.create(
        part_Data["part_Name"],
        part_Data["part_Description"],
        new_Image_Web_Path)


    return True


def handleEditPart(partID, part_Data):
    handlerParts = PartsHandler()

    # Handle Image
    oldImage_Web_Path = handlerParts.getImageByID(partID)
    print(oldImage_Web_Path)
    if oldImage_Web_Path != part_Data["part_ImageWebPath"]: # Check if image has changed
        # Move image files
        # TODO check file name is unique
        newImage_File_Name = os.path.basename(part_Data["part_ImageWebPath"])

        newImage_OldPath = "data/attachment/temp/" + newImage_File_Name
        newImage_NewPath = "data/attachment/" + newImage_File_Name

        copyfile(newImage_OldPath, newImage_NewPath)
        os.remove(newImage_OldPath)
        #os.remove("data/" + oldImage_Web_Path)

        # Update DB
        newImage_NewWebPath = "attachment/" + newImage_File_Name
        handlerParts.updateImage(partID, newImage_NewWebPath)


    


def handleDeletePart(partID):
    handlerParts = PartsHandler()
    handlerPartInStorage = PartInStorageHandler()

    allTag_IDs = handlerParts.getConnectedTags(partID)
    allAttachmnet_IDs = handlerParts.getConnectedAttachments(partID)
    allPartLocation_IDs = handlerPartInStorage.getAllPartLocationIDs(partID)

    for tagID in allTag_IDs:
        handlerParts.disconnectTag(partID, tagID)

    for attachmentID in allAttachmnet_IDs:
        handlerParts.disconnectAttachment(partID, attachmentID)


    for partLocationID in allPartLocation_IDs:
        handlerPartInStorage.remove(partLocationID)

    handlerParts.delete(partID)
    return True
