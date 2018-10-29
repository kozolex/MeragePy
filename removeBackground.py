import os
import numpy as np
import cv2

def listDirectory(directory, fileExtList):
    u"zwraca listę obiektów zawierających metadane dla plików o podanych rozszerzeniach"
    fileList = os.listdir(directory)
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    return fileList
findText = 'log2.tif'  #nazwa szukanego pliku
fileList = listDirectory('E:/ZIARNA/NoweStanowisko/180708/', '.tif')# 180708 180919
file = open('c:/180708.txt','w') #otwarcie pliku do zapisu (nadpisuje wczesniej istjenijący plik)
for oneFile in fileList:        #przeglądanie katalogu głównego - podkatalogi
    print(oneFile)              #wyświetlanie bierzącego katalogu
    if os.path.isdir(oneFile):  #przeglądanie plików w poszczególnych katalogach
        fileList2 = listDirectory(oneFile+'/', '.tif')  
        for oneFile2 in fileList2:
            if findText in oneFile2:

                #print(oneFile2[-5:-4]) #znak pomiędzy 5 a 4 od końca
                dirPath, fileName = os.path.split(oneFile2) #podzielenie stringu na ścieżkę i nazwę pliku

                srcImgPath = oneFile2
                srcMaskPath = oneFile2[:-5] + "3" + oneFile2[-4:]

                srcImage = cv2.imread(srcImgPath,1)      # 0-grayscale 1-rgb -1-alpha channel
                maskImage = cv2.imread(srcMaskPath,0)
                if srcImage is not None and maskImage is not None:
                    th, result = cv2.threshold(maskImage,10,255,cv2.THRESH_BINARY)
                    result2 = cv2.cvtColor(result,cv2.COLOR_GRAY2BGR )
                    # Now black-out the area of logo in ROI
                    height,width = srcImage.shape[:2]

                    file.write(dirPath + ',' + fileName + ',' + str(height)+ ',' + str(width) + '\n' )

                    roi = srcImage[0:height, 0:width ]
                    srcImage2 = cv2.bitwise_and(roi,roi,mask = result)
                    newDirectory = 'C'+dirPath[1:]
                    #print(newDirectory)
                    if not os.path.exists(newDirectory):
                        os.makedirs(newDirectory)
                    cv2.imwrite(newDirectory+ '/'+fileName[:-3]+'png',srcImage2)
                else:
                    print(srcImgPath)
                    file.write(dirPath+'/'+fileName +',0,0\n' )
                
file.close()