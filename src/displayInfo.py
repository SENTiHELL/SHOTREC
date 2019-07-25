import re
from codecs import decode
from src import bash

class monitor:
    name = None
    display = None
    width = height = None
    x = y = None

class xrandr:

    def getRand(self):
        return bash.execLine('xrandr')

    def getXdpy(self):
        q = bash.exec('xdpyinfo -ext XINERAMA')
        q =  re.findall('(head #[0-9]): [0-9]+x[0-9]+ @ ([0-9]+,[0-9]+)', str(q))


        arr = []

        w=0
        for e in q:
            a = []
            a.append(e[0].replace(' #', '-'))
            a.append(re.split(',', e[1]))
            arr.append(a)
            w = w+1


        return arr
    def unSignSplit(array):
        arrSpt = array.splitlines()

        sort_array = []

        i = 0
        while i < len(arrSpt):
            if bool(arrSpt[i][0].strip()):
                try:
                    if i > 0:
                        sort_array.append(sorting)
                except:
                    pass
                sorting = ''
                sorting += arrSpt[i]
            elif i == len(arrSpt) - 1:
                sort_array.append(sorting)
            else:
                sorting += arrSpt[i]

            i = i + 1
        return sort_array

    def removeEmptySign(str):
        return str.replace(" ", "").replace('\n', '').replace('\t', '')

    def cutDouble(str, symb):
        str = str.decode("utf-8")

        dlen = len(str) / 2
        restr = ''
        i = 0

        while i < dlen:
            res = str[i * 2] + str[(i * 2) + 1]

            if symb == res:
                break

            restr += res
            i = i + 1
        return restr

    def getByteName(hex_str):
        return hex_str.split('00000fc00')[1]

    def getNameByPort(name):
        verbose = bash.exec("xrandr --verbose").decode("utf-8")
        bPars = xrandr.unSignSplit(verbose)

        for arr in bPars:
            if arr.split(" ")[0] == name:
                try:
                    edid_str = arr.split('EDID:')[1].split('BorderDimensions:')[0]
                    bGed = xrandr.removeEmptySign(edid_str);
                    cutRes = xrandr.cutDouble(xrandr.getByteName(bGed).encode('utf-8'), "00")
                    return decode(cutRes, "hex").strip().decode("utf-8")
                except:
                    return name
    def map(self, source, replace):
        map = []
        for s in source:
            if re.match(replace, s):
               map.append(s)
        return map

    def listConnect(self):
        r = self.getRand()
        dpy = self.getXdpy()

        self.__monitors = []
        ret = self.map(r, b'.*[^dis]connected')

        for s in ret:
            res = re.findall('[\S]+\s', s.decode())
            
            for obj in re.findall('[0-9]+x[0-9]+[^\+\s]', s.decode()):
                
                o = re.findall('[0-9]+',obj)
                width = o[0]
                height = o[1]
            position =  re.findall('(?<=\+)[0-9]+', s.decode())

            head = None
            for d in dpy:
                if position == d[1]:
                    head = d[0]

            monitor = {
                'port': res[0],
                'display': xrandr.getNameByPort(res[0].strip()),
                'head': head,
                'w': width,
                'h': height,
                'x': position[0],
                'y': position[1]
            }



            self.__monitors.append(monitor)

        return self.__monitors
    def workArea(self):
        r = self.getRand()
        ret = self.map(r, b'.*Screen \d')
        screens = []
        screen = {}
        for s in ret:
            name = re.split(':', s.decode())[0]

            minimum = re.findall('(?<=minimum\s)\d+\sx\s\d+', s.decode())  #['8 x 8']
            current = re.findall('(?<=current\s)\d+\sx\s\d+', s.decode())  # ['3840 x 1080']
            maximum = re.findall('(?<=maximum\s)\d+\sx\s\d+', s.decode())  # ['16384 x 16384']

            min = re.split(' x ', minimum[0])
            cur = re.split(' x ', current[0])
            max = re.split(' x ', maximum[0])

            screen = {
                'min' : { 'w': min[0], 'h': min[1]},
                'cur' : { 'w': cur[0], 'h': cur[1]},
                'max' : { 'w': max[0], 'h': max[1]}
            }
            screens.append(screen)
        return screens

#x = xrandr()
#x.listConnect()
