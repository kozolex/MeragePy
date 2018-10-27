import os
import numpy as np
import cv2

def listDirectory(directory, fileExtList):
    u"zwraca listę obiektów zawierających metadane dla plików o podanych rozszerzeniach"
    fileList = os.listdir(directory)
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    return fileList
sizeList = []
findText = 'log2.tif'
fileList = listDirectory('E:/ZIARNA/NoweStanowisko/180708/', '.tif')
file = open('c:/180708.txt','w') 
for oneFile in fileList:
    print(oneFile)
    if os.path.isdir(oneFile):
        fileList2 = listDirectory(oneFile+'/', '.tif')
        for oneFile2 in fileList2:
            if findText in oneFile2:
                #print(oneFile2)
                #print(oneFile2[-5:-4]) #znak pomiędzy 5 a 4 od końca
                dirPath, fileName = os.path.split(oneFile2)
                #print(dirPath+filePath)

                srcImgPath = oneFile2
                srcMaskPath = oneFile2[:-5] + "3" + oneFile2[-4:]

                srcImage = cv2.imread(srcImgPath,1)      # 0-grayscale 1-rgb -1-alpha channel
                maskImage = cv2.imread(srcMaskPath,0)
                if srcImage is not None:

                    th, result = cv2.threshold(maskImage,10,255,cv2.THRESH_BINARY)
                    result2 = cv2.cvtColor(result,cv2.COLOR_GRAY2BGR )
                    # Now black-out the area of logo in ROI
                    height,width = srcImage.shape[:2]
                    file.write(fileName +','+str(height)+','+ str(width)+'\n' )
                    roi = srcImage[0:height, 0:width ]
                    srcImage2 = cv2.bitwise_and(roi,roi,mask = result)
                    newDirectory = 'C'+dirPath[1:]
                    #print(newDirectory)
                    if not os.path.exists(newDirectory):
                        os.makedirs(newDirectory)
                    cv2.imwrite(newDirectory+ '/'+fileName[:-3]+'png',srcImage2)
                print(srcImgPath)
file.close() 

                #cv2.imshow('image',srcImage)
                #cv2.imshow('image2',srcImage2)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

#flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
#print (flags)