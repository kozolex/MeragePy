"""Workflow:
1. odczyt zawartości katalogów
2.  ...
"""
import numpy as np 
import cv2
import os
import sys

#listowanie wskazanego 
def stripnulls(data):
    u"usuwa białe znaki i nulle"
    return data.replace("\00", " ").strip()

class FileInfo(dict):
    u"przechowuje metadane pliku"
    def __init__(self, filename=None):
        dict.__init__(self)
        self["plik"] = filename
    
class MP3FileInfo(FileInfo):
    u"przechowuje znaczniki ID3v1.0 MP3"
    tagDataMap = {u"tytuł"    : (  3,  33, stripnulls),
                  "artysta"   : ( 33,  63, stripnulls),
                  "album"     : ( 63,  93, stripnulls),
                  "rok"       : ( 93,  97, stripnulls),
                  "komentarz" : ( 97, 126, stripnulls),
                  "gatunek"   : (127, 128, ord)}
    
    def __parse(self, filename):
        u"parsuje znaczniki ID3v1.0 z pliku MP3"
        self.clear()
        try:
            fsock = open(filename, "rb", 0)
            try:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)
            finally:
                fsock.close()
            if tagdata[:3] == 'TAG':
                for tag, (start, end, parseFunc) in self.tagDataMap.items():
                    self[tag] = parseFunc(tagdata[start:end])
        except IOError:
            pass

    def __setitem__(self, key, item):
        if key == "plik" and item:
            self.__parse(item)
        FileInfo.__setitem__(self, key, item)

def listDirectory(directory, fileExtList):
    u"zwraca listę obiektów zawierających metadane dla plików o podanych rozszerzeniach"
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    return fileList

#listaKat = listDirectory("D:\\ziarno2\\TIFF", [".tif"])
listaKatLog1 = listDirectory("D:\\ziarno2\\TIFF\\Wybity", [".tif"])
findText = "log1.tif"
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
    idList = idList+1                       #incremet idList to find second image
    imgToBigCounter = 0                     #Counter how many image is too big to target resolution
    if imgID in mylist[idList]:
        image2= cv2.imread(mylist[idList])
        print(mylist[idList-1]+ "\n" + mylist[idList])

        print(imgStr[-5:-4])
        imgStrCheck = imgStr[:-5] + "2" + imgStr[-4:]
        image1Check = cv2.imread(imgStrCheck) 
        #print(imgStrCheck)

        #size of images FULL SIZE 396 x 920
        hMax = 920
        wMax = 396
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
            #cv2.imwrite("test.png",merageImg)
            cv2.waitKey(5)



#1 os.listdir(directory) zwraca listę wszystkich plików i podkatalogów w katalogu directory.
#2 Iterując po liście z użyciem zmiennej f, wykorzystujemy os.path.normcase(f), aby znormalizować wielkość liter zgodnie z domyślną wielkością liter w systemem operacyjnym. Funkcja normcase jest użyteczną, prostą funkcją, która stanowi równoważnik pomiędzy systemami operacyjnymi, w których wielkość liter w nazwie pliku nie ma znaczenia, w którym np. mahadeva.mp3 i mahadeva.MP3 są takimi samymi plikami. Na przykład w Windowsie i Mac OS, normcase będzie konwertował całą nazwę pliku na małe litery, a w systemach kompatybilnych z UNIX-em funkcja ta będzie zwracała niezmienioną nazwę pliku.
#3 Iterując ponownie po liście z użyciem f, wykorzystujemy os.path.splitext(f), aby podzielić nazwę pliku na nazwę i jej rozszerzenie.
#4 Dla każdego pliku sprawdzamy, czy rozszerzenie jest w liście plików, o które nam chodzi (czyli fileExtList, która została przekazana do listDirectory).
#5 Dla każdego pliku, który nas interesuje, wykorzystujemy os.path.join(directory, f), aby skonstruować pełną ścieżkę pliku i zwrócić listę zawierającą pełne ścieżki.
#Information icon4.svg
#Jeśli to możliwe, powinniśmy korzystać z funkcji w modułach os i os.path do manipulacji plikami, katalogami i ścieżkami. Te moduły opakowują moduły specyficzne dla konkretnego systemu, więc funkcje takie, jak os.path.split poprawnie działają w systemach UNIX, Windows, Mac OS i we wszystkich innych systemach wspieranych przez Pythona.
#Jest jeszcze inna metoda dostania się do zawartości katalogu. Metoda ta jest bardzo potężna i używa zestawu symboli wieloznacznych (ang. wildcard), z którymi można się spotkać pracując w linii poleceń.
