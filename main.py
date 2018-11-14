"""Workflow:
1. odczyt zawartości katalogów
2.  ...
"""
import numpy as np 
import cv2
import os
import sys

def listDirectory(directory, fileExtList):
    u"zwraca listę obiektów zawierających metadane dla plików o podanych rozszerzeniach"
    fileList = os.listdir(directory)
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    return fileList



    return image3

#listaKat = listDirectory("D:\\ziarno2\\TIFF", [".tif"])
listaKatLog1 = listDirectory("E:/ZIARNA/NoweStanowisko/180708/Zdrowe", [".tif"])
findText = "log2.tif"
imgToBigCounter = 0 
mylist = []
#Create new list with only tif RGB images
for i in listaKatLog1:
    if findText in i:
        #print(i)
        mylist.append(i)

for idList in range(0,len(mylist)):
    imgStr = mylist[idList]
#04336_t.png_log1.tif ID[-20:-15] TYPE[-14:-13] 
    imgID = imgStr[-20:-15]                 #Grain ID 
    imgCamSide = imgStr[-14:-13]            #What side of camera b or t (back / top)
    image1= cv2.imread(mylist[idList])      #read first image to matrix
    if idList<=len(mylist):
        idList = idList+1                       #incremet idList to find second image
                        #Counter how many image is too big to target resolution
    if imgID in mylist[idList]:
        image2= cv2.imread(mylist[idList])
        #print(mylist[idList-1]+ "\n" + mylist[idList])

        #print(imgStr[-5:-4])
        imgStrCheck = imgStr[:-5] + "3" + imgStr[-4:]
        image1Check = cv2.imread(imgStrCheck) 
        #print(imgStrCheck)

        #size of images FULL SIZE 396 x 920
        hMax = 850
        wMax = 400
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]
        hPadding1 = (hMax-h1)//2
        hPadding2 = (hMax-h2)//2
        wPadding1 = (wMax-w1)//2
        wPadding2 = (wMax-w2)//2
        if h1 > hMax or h2 > hMax or w1 > wMax or w2 > wMax:
            imgToBigCounter+=1
            print (str(imgToBigCounter) + "images is to big")
            
        else:
            merageImg = np.zeros((hMax, wMax*2, 3), np.uint8)

            if image1Check[h1//2,w1//2][2]==255:
                print("switch")
                merageImg [hPadding2: h2 + hPadding2, wPadding2+wPadding1:w2 + wPadding2+wPadding1] = image2
                merageImg [hPadding1: h1 + hPadding1, w2+wPadding2+wPadding1:w2+w1+wPadding2+wPadding1] = image1
            else:
                merageImg [hPadding1: h1 + hPadding1, wPadding2+wPadding1:w1 + wPadding2+wPadding1] = image1
                merageImg [hPadding2: h2 + hPadding2, w1+wPadding2+wPadding1:w1+w2+wPadding2+wPadding1] = image2

            cv2.imshow("Merage Image", merageImg)
            #cv2.imwrite("D:/ziarno2/PNG/ZielZadesz/"+imgID+".png",merageImg)
            cv2.waitKey(500)
