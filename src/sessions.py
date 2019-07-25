import os
class session:
    basedir = os.getcwd()
    fileSession = '/session'
    dirfile = None
    def __init__(self):
        if os.path.isfile(self.basedir + self.fileSession) != True:
            os.mknod(self.basedir + self.fileSession)
        self.dirfile = self.basedir + self.fileSession
    def load(self):
        file = open(self.dirfile, "r")
        parse = file.read().split("|")

        if len(parse) != 6:
            return None
        return {'dir':parse[0],
                'name':parse[1],
                'rate':parse[2],
                'pad':parse[3],
                'format':parse[4],
                'quality':parse[5]
                }
    def save(self, dir, name, rate, pad, format, quality):
        file = open(self.dirfile, "w")
        file.write('|'.join([str(dir),
                             str(name),
                             str(rate),
                             str(pad),
                             str(format),
                             str(quality)]))
        file.close()
