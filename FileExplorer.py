import os
import random
import cv2
import numpy as np

import shutil                                      #usuwanie katalogu z zawartością

class FileExplorer:
    def __init__(self, input_root):         
        self.input_root = input_root               #przechowywanie stringa ścieżki głównej
        self.visitors = []
        
    def add_visitor(self, visitor):                #Lista Wizytorów
        self.visitors.append(visitor)
        
    def get_dirs(self):                            #listowanie katalogu
        dirs = []
        for d in os.listdir(self.input_root):
            path = os.path.join(self.input_root, d)
            if os.path.isdir(path):
                dirs.append(path)
        return dirs
        
    def process_dir(self, input_dir, limit=None):
        files = os.listdir(input_dir)
        if limit is not None:        
            files = files[:limit]
        for f in files:
            input_file = os.path.join(input_dir, f)
            self.process_file((
                    self.input_root, 
                    os.path.relpath(input_dir, self.input_root),
                    f))
            
    def process_file(self, input_file):
        for visitor in self.visitors:
            visitor.visit(input_file)

class CropVisitor:
    def __init__(self, root):
        self.root = root
    
    def find_bigCountour(self, srcImage, lowTh = 20, hiTh = 255, kernelSize = 3):
        "Szukanie największego konturu zgodnie z wartościami progowymi"
        self.srcImage = srcImage
        self.lowTh = lowTh
        self.hiTh = hiTh
        self.kernelSize = kernelSize
        gray = cv2.cvtColor(srcImage, cv2.COLOR_RGB2GRAY)
        ## 3. Do morph-close-op and Threshold
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize,kernelSize))
        th, threshed = cv2.threshold(gray, lowTh, hiTh, 0)
        #cv2.imshow("threshed", threshed)
        threshed = cv2.morphologyEx(threshed,cv2.MORPH_CLOSE, kernel)
        #cv2.imshow("Close", threshed)
        threshed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel)
        #cv2.imshow("Open", threshed)
        #cv2.waitKey(0)
        ## 4. Findcontours and filter by Area
        im2, contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        bigContourArea = 0
        bigContourId = 0
        for i, idContours in enumerate(contours):
            contourArea = cv2.contourArea(contours[i])
            if contourArea > bigContourArea:
                bigContourArea = contourArea
                bigContourId = i
        
        rect = cv2.minAreaRect(contours[bigContourId])
        box = cv2.boxPoints(rect)
        x,y,w,h = cv2.boundingRect(contours[bigContourId])
        return contours[bigContourId], x,y,w,h
    
    def saveResult(self,fname):
        return 0
     
    def visit(self, file_path):
        input_root, fdir, fname = file_path
        
        if fname.find("ext.") == -1:
            image_path = os.path.join(*file_path)
            #print(file_path)
            srcImage = cv2.imread(image_path, cv2.IMREAD_COLOR)
#Szukanie największego konturu
            contourBig, x,y,w,h = self.find_bigCountour(srcImage, 35) # self.metod 
#Walidacja styku z krawędzią obrazu
            srcImageSizeY, srcImageSizeX = srcImage.shape[:2]   #Najpierw Y potem X !!
            #print("IMG= ",srcImageSizeX,srcImageSizeY)
            padding = 10
            paddingTop = y-padding
            paddingDown = y+h+padding
            paddingLeft = x-padding
            paddingRight = x+w+padding
            #print("ROI= ",paddingTop,paddingDown,paddingLeft,paddingRight)
            cv2.waitKey(0)
            if paddingTop < 0:
                paddingTop = 0
            if paddingLeft < 0:
                paddingLeft = 0            
            if paddingRight > srcImageSizeX:
                paddingRight = srcImageSizeX
            if paddingDown > srcImageSizeY:
                paddingDown = srcImageSizeY
            #print("ROI2= ",paddingTop,paddingDown,paddingLeft,paddingRight)         
            roi = srcImage[paddingTop : paddingDown, paddingLeft : paddingRight] # Y1:Y2 , X1:X2
            roiSizeY, roiSizeX = roi.shape[:2]
            #print("ROI result= ",roiSizeX,roiSizeY)
#II etap bineralizacji
            mask = np.zeros((paddingDown - paddingTop , paddingRight - paddingLeft ),np.uint8)
            contourBig, x,y,w,h  = self.find_bigCountour(roi, 15) # self.metod
            
            paddingX = int((4*MOD_SIZE_X - w)/2)
            paddingY = int((4*MOD_SIZE_Y - h)/2)
            cv2.drawContours(mask,[contourBig],0,255,-1)
            try:
                roi = cv2.bitwise_and(roi,roi,mask = mask)
                roi = roi[y : y+h, x : x+w]
            
                roi = cv2.copyMakeBorder(roi, paddingY, paddingY, paddingX, paddingX, cv2.BORDER_CONSTANT, None, 0)
                x,y = roi.shape[:2]
                #cv2.imshow("ROI",roi)

                roi = cv2.resize(roi,(MOD_SIZE_X,MOD_SIZE_Y), cv2.INTER_CUBIC)
#ZAPIS PLIKU
                (fn, fext) = os.path.splitext(fname)                #fn - file name fext - file extention
                out_path = os.path.join(self.root, fdir, fname)
                #print("root= ", self.root)
                #print("fdir= ", fdir)
                #print("fname= ", fname)
                #cv2.waitKey(0)
                out_dir = os.path.dirname(out_path)

                if not os.path.exists(out_dir):
                    print ("CreatingC", out_dir)
                    os.makedirs(out_dir)
                cv2.imwrite(out_path, roi) 

            except:
                print("Bug = ",file_path  )
                #cv2.imshow("error",srcImage)
                #cv2.imshow("ROI",roi)
                #cv2.waitKey(0)
                #print(file_path)
                (fn, fext) = os.path.splitext(fname)                #fn - file name fext - file extention
                out_path = os.path.join(self.root,'errors', fdir, fname)
                out_dir = os.path.dirname(out_path)

                if not os.path.exists(out_dir):
                    print ("CreatingC", out_dir)
                    os.makedirs(out_dir)
                cv2.imwrite(out_path, roi)    

class ExpanderVisitor(CropVisitor):
    def __init__(self, root):
        CropVisitor.__init__(self, root)
        self.num_extra = 20
        
    def visit(self, file_path):
        input_root, fdir, fname = file_path
        if fname.find("ext.") == -1:
            image_path = os.path.join(*file_path)
            #srcImage = PilImage.open(image_path)
            
            for i in range(0, self.num_extra):
                #modified = PilImage.new(srcImage.mode, (MOD_SIZE, MOD_SIZE))
                #angle = random.randint(-5,5) + 180 * random.randint(0, 1)

                #paste_x = (MOD_SIZE - srcImage.width)//2 + random.randint(-20,20)
                #paste_y = (MOD_SIZE - srcImage.height)//2 + random.randint(-20,20)
                #modified.paste(srcImage, (paste_x, paste_y))
                #modified = modified.rotate(angle)            
                
                (fn, fext) = os.path.splitext(fname)
                
                out_path = os.path.join(self.root, fdir, "%s.%d%s" % (fn, i, fext))
                out_dir = os.path.dirname(out_path)
                
                if not os.path.exists(out_dir):
                    print ("CreatingEV", out_dir)
                    #os.makedirs(out_dir)
                #cv2.imwrite(out_path)
                #modified.(out_path)

def process_dataset(input_root, visitor, dir_index=None, limit=None):
    print ("Processing", input_root)
    explorer = FileExplorer(input_root)             #Obiekt klasy FileExplorer
    explorer.add_visitor(visitor)                   #

    dirs = explorer.get_dirs()
    dirs.sort()

    #import warnings
    #warnings.simplefilter("ignore")

    if dir_index is not None:
        #print "Processing dir", dirs[dir_index]
        explorer.process_dir(dirs[dir_index], limit=limit)
    else:
        for i in range(len(dirs)):
            #print "Processing dir", dirs[i]
            explorer.process_dir(dirs[i], limit=limit)

MOD_SIZE_X = 224
MOD_SIZE_Y = 224
input_root = 'C:/ZIARNA/NS2/NoweStanowisko/180708' # D:\NoweStanowisko\180708
#input_root = 'D:\\NoweStanowisko\\180708' # D:\NoweStanowisko\180708
output_root = 'C:/NS_224_NR/180708'

if os.path.exists(output_root):
    print ("Removing", output_root)
    shutil.rmtree(output_root, ignore_errors=True)  #usunięcie katalogu bez względu na zawartość

visitor = CropVisitor(output_root)
process_dataset(input_root, visitor, dir_index=None, limit=None)