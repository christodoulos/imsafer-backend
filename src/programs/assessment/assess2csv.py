#!/usr/bin/python3
import sys, bz2
from math import fabs
import json

delim = ","          #delimeter for .csv file
decimalpoint = "."   #decimal point for .csv file
assert delim != decimalpoint, "Decimal point and delimeter can not be the same"


layabimcolumn = ("assess_columns",)
layarhocm = ("assess_cm",)
abimcolumns = []
arhocm = {}


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
        ierr = readthcxelems(fr)
        fr.close()
    if ierr == 0:  #If no error in reading, check results
        ierr = checkresults()
    if ierr == 0:  #If no error in checking, write asc file
        abimcolumns.sort()  #So that we have consistent sequence of BIM columns
        ierr = writecsv(fn)
    if ierr != 0:
        print("Errors recorded. Program stops.")
        sys.exit(1)


def checkresults():
    "Test if any BIM collumns are defined, and if center of mass and rhomin and rhomax are defined."
    ierr = 0
    if len(abimcolumns) == 0:
        print("Error: No BIM columns were found.")
        ierr = 1
    for lab in "cm", "rhomin", "rhomax":
        if lab not in arhocm:
            print("Error: %s was not found." % (lab,))
            ierr = 1
    abimcolumns.sort()  #So that we have consistent sequence of BIM columns
    for i, temp in enumerate(abimcolumns):
        if temp[0] != i+1:
            print("Error: Column number %d is missing" % (i+1,))
            ierr = 1
    return ierr


def writecsv(fn):
    "Write the data to an .csv file."
    i = fn.find(".")
    if i < 0: fna = fn    +".csv"
    else:     fna = fn[:i]+".csv"
    try:
        fw = open(fna, "w")
    except OSError:
        print("Error: could not open file {}".format(fna))
        return 1
    wrdelim(fw, "{}_{}\n".format(arhocm["cm"][0], arhocm["cm"][1]))
    wrdelim(fw, "{}_{}\n".format(arhocm["rhomin"], arhocm["rhomax"]))
    t = []
    for temp in abimcolumns:
        t.clear()
        for j in range(1,16):
            t.append("{}".format(temp[j]))
        dline = "_".join(t) + "\n"
        wrdelim(fw, dline)
    fw.close()
    return 0


def wrdelim(fw, t):
    "Write text to file with delimeters."
    t = t.replace("_", delim)
    t = t.replace(".", decimalpoint)
    fw.write(t)

#--------------------------------------------------------------------------------------------------
#Read BIM Column related functions

def readthcxelems(fr):
    "Read lines from a ThanCad drawing."
    ierr, dline = reSkip2(fr, None, ('<ELEMENTS>',), None)
    if ierr != 0:
        print("Error: '<ELEMENTS>' was not found. Invalid thcx file: {}".format(fn))
        return ierr
    while True:
        ierr, dline = reSkip2(fr, None, ('<BIMCOLUMN>', '<NAMEDPOINT>', '<TEXT>'), "</ELEMENTS>")
        if ierr == 1: return 0   #normal end of file
        if ierr == -1:
            print("Warning: '</ELEMENTS>' was not found before end of file.")
            return 0   #Pretend normal end of file

        if dline.strip() == '<BIMCOLUMN>':
            ierr, temp = readthancadbimcolumn(fr)
            if ierr == 1: continue   #Invalid bimcolumn: try to continue
            if ierr == -1: return 0  #end of file, pretend that the file finished ok
            savebimcolumn(*temp)
        elif dline.strip() == '<NAMEDPOINT>':
            ierr, temp = readthancadnamedpoint(fr)
            if ierr == 1: continue   #Invalid namedpoint try to continue
            if ierr == -1: return 0  #end of file, pretend that the file finished ok
            savenamedpoint(*temp)
        elif dline.strip() == '<TEXT>':
            ierr, temp = readthancadtext(fr)
            if ierr == 1: continue   #Invalid text try to continue
            if ierr == -1: return 0  #end of file, pretend that the file finished ok
            savetext(*temp)
        else:
            assert 0, "error in reSkip2() ?"


def saveline(lay, coor):
    "Save the lines that are in certain layers and check if lines are rectangle parallel to x,y."
    lay = lay.lower()
    if lay in layfwall:
        xymm = checkrectangle(coor)
        if xymm is None:
            print("Warning: Ignoring non-rectangular wall")
            return
        fwalls.append(getcensize(xymm))
    elif lay in layfexit:
        xymm = checkrectangle(coor)
        if xymm is None:
            print("Warning: Ignoring non-rectangular exit")
            return
        if len(fexit) == 0:
            fexit.append(getcensize(xymm))
        else:
            print("Warning: ignoring second exit")
    elif lay in layfgrid:
        xymm = checkrectangle(coor)
        if xymm is None:
            print("Warning: Ignoring non-rectangular grid")
            return
        if len(fgrid) == 0:
            fgrid.append(getcensize(xymm))
        else:
            print("Warning: ignoring second grid")


def savebimcolumn(lay, cc, name, ds, atts):
    "Save the bimcolumns that are in certain layers and check attributes."
    lay = lay.lower()
    if lay in layabimcolumn:
        iaa = deciphername(name)
        if iaa is None: return
    try:
        temp = (iaa, ds[1], ds[0], atts["entRhoInitial"], cc[0], cc[1], atts["entLamCrack"],
                atts["entThickTo"], atts["entRhoTo"], 0.0, 0.0, 
                atts["entEc"], atts["entEs"], atts["entL"], atts["entN"], atts["entTnewMax"],
               )
    except KeyError as e:
        print("Warning: Incomplete attributes of BIMCOLUMN")
        return
    abimcolumns.append(temp)


def deciphername(temp):
    "Try to get the integer code of temp."
    temp = temp.strip()
    for i in range(0, len(temp)):
        iaa = inte(temp[i:])
        if iaa is not None: return iaa
    print("Warning: Could not decipher integer of column name '%s'" % (temp,))
    return None


def savenamedpoint(lay, cc, name):
    "Save the namedpointss that are in certain layers and check attributes."
    lay = lay.lower()
    if lay not in layarhocm: return
    name = name.lower()
    if name != "cm": return    #Not the point we are looking for
    if name in arhocm:
        print("Warning: Ignoring additional namedpoint (center of mass)")
        return
    arhocm[name] = cc[:2]    #Coordinates of the center of mass


def savetext(lay, name):
    "Save the texts that are in certain layers and check attributes."
    lay = lay.lower()
    if lay not in layarhocm: return
    name = name.lower()
    dl = name.split(":")
    lab = dl[0].strip()
    if lab not in ("rhomin", "rhomax"): return   #Not what we are looking for
    if lab in arhocm:
        print("Warning: Ignoring additional '%'" % (lab,))
        return
    try:
        rho = float(dl[1])
        if rho <= 0.0: raise ValueError("%s <= 0" % (lab,))
    except (ValueError,IndexError) as e:
        print("Warning: Bad value of %s" % (lab,))
        return
    arhocm[lab] = rho    #rhomin, or rhomax


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
    ierr, dline = reSkip2(fr, None, ('<NODES>',), "</LINE>")
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


def readthancadbimcolumn(fr):
    "Read the layer and the coordinates of a ThanCad BIM Column."
    ierr, dline = read1e(fr, '/BIMCOLUMN')
    if ierr != 0: return ierr, None
    lay = dline.strip().strip('"').strip()

    ierr, dline = skip2e(fr, "BIMCOLUMN", '<SECTION', "</BIMCOLUMN>")
    if ierr != 0: return ierr, None
    ierr, dline = read1e(fr, '/BIMCOLUMN')
    if ierr != 0: return ierr, None
    name = dline.strip().strip('"').strip()

    ierr, cc = getlabelednumbers(fr, "BIMCOLUMN", '<NODE>', "</BIMCOLUMN>", 3)
    if ierr != 0: return ierr, None
    ierr, ds = getlabelednumbers(fr, "BIMCOLUMN", '<DIMENSIONS', "</BIMCOLUMN>", 6)
    if ierr != 0: return ierr, None

    ierr, dline = skip2e(fr, "BIMCOLUMN", '<CARGO>', "</BIMCOLUMN>")
    if ierr != 0: return ierr, None
    ierr, dlines = copy2e(fr, "BIMCOLUMN", '</CARGO>', "</BIMCOLUMN>")
    if ierr != 0: return ierr, None

    atts = {}
    if len(dlines) > 0:
        jsondata = "".join(dlines)        #dlines already has a \n at the end of the line 
        #print(jsondata)
        #stop()
        try:
            atts = json.loads(jsondata)  #May raise JSONDecodeError which is a subclass of ValueError
        except ValueError:
            print("Warning: Bad BIMCOLUMN attributes")
            return 1, None
    return 0, (lay, cc, name, ds, atts)


def readthancadnamedpoint(fr):
    "Read the layer and the coordinates of a ThanCad named point."
    ierr, dline = read1e(fr, '/NAMEDPOINT')
    if ierr != 0: return ierr, None
    lay = dline.strip().strip('"').strip()

    ierr, cc = getlabelednumbers(fr, "NAMEDPOINT", '<NODE>', "</NAMEDPOINT>", 3)
    if ierr != 0: return ierr, None

    for i in range(2):
        ierr, dline = read1e(fr, '/NAMEDPOINT')
        if ierr != 0: return ierr, None
    name = dline.strip().strip('"').strip()

    return 0, (lay, cc, name)


def readthancadtext(fr):
    "Read the layer and the string of a ThanCad text."
    ierr, dline = read1e(fr, '/TEXT')
    if ierr != 0: return ierr, None
    lay = dline.strip().strip('"').strip()

    for i in range(5):
        ierr, dline = read1e(fr, '/TEXT')
        if ierr != 0: return ierr, None
    text = dline.strip().strip('"').strip()

    return 0, (lay, text)


def read1e(fr, sent2):
    "Read a line; print error message."
    for dline in fr:
        break
    else:
        print("Warning: '%s' was not found before end of file." % sent2)
        return 1, None
    if dline.strip() == sent2:
        print("Warning: a line was expcted before '%s'" % (sent2,))
        return -1, None
    return 0, dline


def copy2e(fr, elemname, sent1, sent2):
    "Copy all lines until sent1; print error message."
    ierr, dlines = copy2(fr, elemname, sent1, sent2)
    if ierr == 1:
        print("Warning: damaged %s: '%s' was not found." % (elemname, sent1))
        return 1, None
    elif ierr != 0:
        print("Warning: damaged %s: '%s' was not found before end of file." % (elemname, sent1))
        return -1, None
    return 0, dlines


def copy2(fr, elemname, sent1, sent2):
    "Copy all lines until sent1."
    dlines = []
    for dline in fr:
        temp = dline.strip()
        if temp == sent1: return 0, dlines
        if temp == sent2: return 1, dlines
        dlines.append(dline)
    else:
        return -1, ""   #end of file


def getlabelednumbers(fr, elemname, sent1, sent2, n):
    "Gets n numebrs which follow a lebel."
    ierr, dline = skip2e(fr, elemname, sent1, sent2)
    if ierr != 0: return ierr, dline
    dl = dline.split()
    try:
        cc = list(map(float, dl[1:-1]))
        if len(cc) < n: raise ValueError("Less numbers than expected")
    except (ValueError, IndexError) as e:
        print("Warning: damaged BIMCOLUMN: bad NODE coordinates.")
        return 1, None
    return 0, cc


def skip2e(fr, elemname, sent1, sent2):
    "Try to find sent1, and if not, print error message."
    ierr, dline = reSkip2(fr, None, (sent1,), sent2)
    if ierr == 1:
        print("Warning: damaged %s: '%s' was not found." % (elemname, sent1))
        return 1, None
    elif ierr != 0:
        print("Warning: damaged %s: '%s' was not found before end of file." % (elemname, sent1))
        return -1, None
    return 0, dline


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
        print("Error: Could not open file {}".format(fn))
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


def inte(a):
    try: return int(a)
    except ValueError: return None


if __name__ == "__main__":
    pymain()
