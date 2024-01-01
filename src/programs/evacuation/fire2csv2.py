#!/usr/bin/python3
import sys, bz2
from math import fabs

delim = ","          #delimeter for .csv file
decimalpoint = "."   #decimal point for .csv file
assert delim != decimalpoint, "Decimal point and delimeter can not be the same"


layfwall = ("fwalls",)
layfexit = ("fexit",)
layfgrid = ("fgrid",)
fwalls = []
fexit = []
fgrid = []


def pymain():
    "Start here."
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 {} <thcx_file>".format(sys.argv[0]))
        sys.exit(1)
    fn = sys.argv[1]
    conv(fn)


def conv(fn):
    "Convert BIM .thcx file which contains fire evacuation floor plan, .csv file."
    fr, ierr = __openBZ2(fn, "utf-8")
    if ierr == 0:  #If no error in opening, read file
        ierr = readthcxlines(fr)
        fr.close()
    if ierr == 0:  #If no error in reading, check results
        ierr = checkresults()
    if ierr == 0:  #If no error in checking, write asc file
        fwalls.sort()  #So that we have consistent sequence after superficial changes to the drawing (eg if only the color changes)
        ierr = writecsv(fn)
    if ierr != 0:
        print("Errors recorded. Program stops.")
        sys.exit(1)


def checkresults():
    "Test if any walls are exits ar defined."
    if len(fwalls) == 0:
        print("No walls were found.")
        return 1
    if len(fexit) == 0:
        print("No exit was found.")
        return 1
    autogrid()
    return 0


def autogrid():
    "If the grid is not defined, compute the least enclosing eractngle."
    xymm = [1e30, 1e30, -1e30, -1e30]
    for xcen, ycen, b, h in fwalls+fexit:
        xymm[0] = min(xymm[0], xcen-b)
        xymm[1] = min(xymm[1], ycen-h)
        xymm[2] = max(xymm[2], xcen+b)
        xymm[3] = max(xymm[3], ycen+h)
    if xymm[0] < -0.1 or xymm[0] > 0.1 or xymm[1] < -0.1 or xymm[1] > 0.1:
        print("Warning: the min x and y of the walls and exit must be zero.")
        print("         Now they are xmin={}  ymin={}".format(xymm[0], xymm[1]))

    b = xymm[2]/2
    h = xymm[3]/2
    if len(fgrid) > 0:
        w = fgrid[0]
        if fabs(w[2]-b)>0.1 or fabs(w[3]-h)>0.1:
            print("Warning: the defined grid is not minimum enclosing rectangle of the walls and the exit.")
    else:
        print("Warning: no grid was found: autocomputing grid")
        fgrid.append(getcensize(xymm))


def writecsv(fn):
    "Write the data to an .csv file."
    i = fn.find(".")
    if i < 0: fna = fn    +".csv"
    else:     fna = fn[:i]+".csv"
    try:
        fw = open(fna, "w")
    except OSError:
        print("Could not open file {}".format(fna))
        return 1
    #wrdelim(fw, "_X__Y\n")
    wrdelim(fw, "{}__{}\n".format(fgrid[0][2]*2, fgrid[0][3]*2))
    wrdelim(fw, "{}__{}\n".format(fexit[0][0], fexit[0][1]))

    #wrdelim(fw, "_Center X_Center Y_Half of Width_Half of Height\n")
    for i,w in enumerate(fwalls):
        wrdelim(fw, "{}_{}_{}_{}_{}\n".format(i+1, w[0], w[1], w[2], w[3]))
    fw.close()
    return 0


def wrdelim(fw, t):
    "Write text to file with delimeters."
    t = t.replace("_", delim)
    t = t.replace(".", decimalpoint)
    fw.write(t)

#--------------------------------------------------------------------------------------------------
#Read BIM grid, exit, walls related functions

def readthcxlines(fr):
    "Read lines from a ThanCad drawing."
    ierr, dline = reSkip2(fr, None, '<ELEMENTS>', None)
    if ierr != 0:
        print("'<ELEMENTS>' was not found. Invalid thcx file: {}".format(fn))
        return ierr
    while True:
        ierr, dline = reSkip2(fr, None, ('<LINE>', '<FILLEDLINE>'), "</ELEMENTS>")
        if ierr == 1: return 0   #normal end of file
        if ierr == -1:
            print("Warning: '</ELEMENTS>' was not found before end of file.")
            return 0   #Pretend normal end of file
        ierr, lay, coor = readthancadline(fr)
        if ierr == 1: continue   #Invalid line try to continue
        if ierr == -1: return 0  #end of file, pretend that the file finished ok
        saveline(lay, coor)


def saveline(lay, coor):
    "Save the lines that are in cetrain layers and check if lines are rectangle parallel to x,y."
    lay = lay.lower()
    if lay in layfwall:
        xymm = checkrectangle(coor)
        if xymm is None:
            print("Ignoring non-rectangular wall")
            return
        fwalls.append(getcensize(xymm))
    elif lay in layfexit:
        xymm = checkrectangle(coor)
        if xymm is None:
            print("Ignoring non-rectangular exit")
            return
        if len(fexit) == 0:
            fexit.append(getcensize(xymm))
        else:
            print("Warning: ignoring second exit")
    elif lay in layfgrid:
        xymm = checkrectangle(coor)
        if xymm is None:
            print("Ignoring non-rectangular grid")
            return
        if len(fgrid) == 0:
            fgrid.append(getcensize(xymm))
        else:
            print("Warning: ignoring second grid")


def getcensize(xymm):
    "Get center and size of rectangular parallel to x, y."
    xcen = (xymm[0]+xymm[2])*0.5
    ycen = (xymm[1]+xymm[3])*0.5
    b = (xymm[2] - xymm[0]) * 0.5   #half width
    h = (xymm[3] - xymm[1]) * 0.5   #half height
    return xcen, ycen, b, h


def checkrectangle(coor):
    "Check if line is rectangle parallel to x,y."
    if len(coor) == 5:
        if not thanNear2(coor[0], coor[-1]): return None   #5 nodes: not a rectangle
    elif len(coor) != 4:
        return None   #not 4 nodes: not a rectangle
    xmin = min(temp[0] for temp in coor)
    ymin = min(temp[1] for temp in coor)
    xmax = max(temp[0] for temp in coor)
    ymax = max(temp[1] for temp in coor)
    for x1, y1, _ in coor:
        if not thanNearx(x1, xmin) and not thanNearx(x1, xmax): return None
        if not thanNearx(y1, ymin) and not thanNearx(y1, ymax): return None
    return xmin, ymin, xmax, ymax

#--------------------------------------------------------------------------------------------------
#Read .thcx related functions

def readthancadline(fr):
    "Read the layer and the coordinates of a ThanCad line."
    for dline in fr:
        break
    else:
        print("Warning: '/LINE' was not found before end of file.")
        return -1, None, None
    lay = dline.strip().strip('"').strip()
    ierr, dline = reSkip2(fr, None, '<NODES>', "</LINE>")
    if ierr == 1:
        print("Warning: damaged line: 'NODES' was not found.")
        return 1, None, None
    elif ierr != 0:
        print("Warning: damaged line: 'NODES' was not found before end of file.")
        return -1, None, None
    coor = []
    for dline in fr:
        if dline.strip() == "</NODES>": break
        try:
            x, y, z = map(float, dline.split())
        except (ValueError, IndexError):
            print("Warning: damaged line: syntax error while reading nodes.")
            return 1, None, None
        coor.append((x, y, z))
    return 0, lay, coor


def reSkip2(uMhk, uCop, sent1, sent2):
      """Continuously read lines until sent1 is found, or sent2.

      If sent1 is found return the line that contained in ibuf and ierr=0.
      If sent2 is found before sent1, then set ierr=1, and return the line that contained sent2.
      If end of file is found before sent1 or sent2 set ierr=-1
      if uCop != None, the lines read are going to written to file unit uCop."""
      sent1 = tuple(sent1x.strip() for sent1x in sent1)
      n1 = tuple(len(sent1x) for sent1x in sent1)
      if sent2 is not None:
          sent2 = sent2.strip()
          n2 = len(sent2)
      for dline in uMhk:
          temp = dline.strip()
          for sent1x, n1x in zip(sent1, n1):
              if temp[:n1x] == sent1x: return 0, dline
          if sent2 is not None:
              if temp[:n2] == sent2: return 1, dline
          if uCop is not None: uCom.write(dline)
      else:
          return -1, ""   #end of file

#--------------------------------------------------------------------------------------------------
#Open .thcx related functions
def __openBZ2(fn, encoding):
    "Open thcx file stored as either BZ2 compessed or text, with encoding."
    try:
        fr = bz2.open(fn, "rt", compresslevel=1, encoding=encoding, errors="surrogateescape")
        if not isBz2(fr):    #If not a bzip2 file, then it is normal text file
            fr.close()
            fr = open(fn, encoding=encoding, errors="surrogateescape")
        else:
            fr.close()
            fr = bz2.open(fn, "rt", compresslevel=1, encoding=encoding, errors="surrogateescape")
        return fr, 0
    except Exception as e:
        print("Could not open file {}".format(fn))
        return None, 1


def isBz2(fr):
    "Checks if the file opened is real a bzip2 file."
    try:
        next(fr)
    except OSError as why:     #In python 3.3 IOError was merged to OSError
        why = str(why).lower()            #If not transformed to string the in operator does not work
        if "invalid" in why and "data" in why: return False
        raise       #If other IOError propagate
    except EOFError as why:     #EOFError is not a subclass of OSError (or IOError)
        #EOFError: Compressed file ended before the end-of-stream marker was reached
        return False  #This realy means invalid data (or completely empty file)
    else:
        return True


#--------------------------------------------------------------------------------------------------
#Math library functions
from math import fabs
thanThresholdx = 1e-10  # Threshold for coordinate difference; if less the coordinates are the same
                        # This constant acommodates ThanCad too.

def thanNear2(a, b):
    "Checks if two 2dimensional points coincide taking numerical error into account."
    xa, ya = a[:2]
    xb, yb = b[:2]
    d = fabs(xb-xa) + fabs(yb-ya)
    v = (fabs(xa)+fabs(xb)+fabs(ya)+fabs(yb))*0.5
    if v < thanThresholdx: return d < thanThresholdx
    return d < v*thanThresholdx


def thanNearx(xa, xb):
    "Checks if two coordinates (x or y) coincide taking numerical error into account."
    d = fabs(xb-xa)
    v = (fabs(xa)+fabs(xb))*0.5
    if v < thanThresholdx: return d < thanThresholdx
    return d < v*thanThresholdx


if __name__ == "__main__":
    pymain()
