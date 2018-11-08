import os
import random
#from PIL import Image as PilImage
import cv2
import numpy as np

class FileExplorer:
    def __init__(self, input_root):         
        self.input_root = input_root                   #przechowywanie stringa ścieżki głównej
        self.visitors = []                             #
        
    def add_visitor(self, visitor):                     #
        self.visitors.append(visitor)
        
    def get_dirs(self):                             #listowanie katalogu
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
        
    def visit(self, file_path):
        input_root, fdir, fname = file_path
        if fname.find("ext.") == -1:
            image_path = os.path.join(*file_path)

            srcImage = cv2.imread(image_path, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(srcImage, cv2.COLOR_RGB2GRAY)

            ## 3. Do morph-close-op and Threshold
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            morphed = cv2.morphologyEx(gray,cv2.MORPH_CLOSE, kernel)
            cv2.imshow("morphed",morphed)

            th, threshed = cv2.threshold(morphed, 50, 255, 0)

            cv2.imshow("threshed",threshed)
            ## 4. Findcontours and filter by Area
            im2, contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            canvas = np.zeros_like(srcImage, np.uint8)
            bigContourArea = 0
            bigContourId = 0
            for i, idContours in enumerate(contours):
                contourArea = cv2.contourArea(contours[i])
                if contourArea > bigContourArea:
                    bigContourArea = contourArea
                    bigContourId = i
            print(bigContourId, fname, bigContourArea )
            rect = cv2.minAreaRect(contours[bigContourId])
            box = cv2.boxPoints(rect)
            cv2.drawContours(srcImage, contours[bigContourId], -1, (0,255,0), 5, cv2.FILLED)

            #for cnt in contours:
               # if cv2.contourArea(cnt) < AREA:
               #     cv2.drawContours(canvas, [cnt], -1, (0,255,0), 5, cv2.LINE_AA)

            ## 
            cv2.imshow("img",srcImage)
            cv2.waitKey(0)
            #srcImage = PilImage.open(image_path)
            #modified = PilImage.new(srcImage.mode, (MOD_SIZE, MOD_SIZE))
            


            #paste_x = (MOD_SIZE - srcImage.width)//2
            #paste_y = (MOD_SIZE - srcImage.height)//2
            #modified.paste(srcImage, (paste_x, paste_y))     

            (fn, fext) = os.path.splitext(fname)

            out_path = os.path.join(self.root, fdir, fname)
            out_dir = os.path.dirname(out_path)

            if not os.path.exists(out_dir):
                print ("CreatingC", out_dir)
                os.makedirs(out_dir)
            #modified.save(out_path)
    

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

MOD_SIZE = 1000
input_root = 'C:/ZIARNA/NS2/NoweStanowisko/180708'
output_root = 'C:\TEST'

if os.path.exists(output_root):
    print ("Removing", output_root)
    try:
        os.removedirs(output_root)
    except:
        print("Removing error")

visitor = CropVisitor(output_root)

process_dataset(input_root, visitor, dir_index=None, limit=2)