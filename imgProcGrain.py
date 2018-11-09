#Work flow
#1.Listowanie Katalogu
#2.odczyt obrazu
#3.modyfikacje obrazu
import os
import cv2

class GrainImg():
    def __init__ (self):
        list
    fileList = []

    def listDirectory(directory, fileExtList):
    u"zwraca listę obiektów zawierających metadane dla plików o podanych rozszerzeniach"
    fileList = os.listdir(directory)
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    return fileList
