import json
import glob

PATH = 'Stepchart.sm'

path2 = glob.glob('../../../giochi/StepMania 5/Songs/**/*.sm', recursive=True)

songList = []

def addSong():
    keyList = {}
    i = 0
    j = 0
    while True:
        try:
            text = simFile.readline()
        except UnicodeDecodeError:
            text = "#ELEMENT:unknown;"
        if not text:
            break
        if text and text[0] == '#':
            line = text.split(':')
            if line[0] == '#NOTES':
                mode = simFile.readline().replace(' ', '')[:-2]
                steps = simFile.readline().replace(' ', '')[:-2]
                difficulty = simFile.readline().replace(' ', '')[:-2]
                level = simFile.readline().replace(' ', '')[:-2]
                i += 1
                if i < 6:
                    keyList.update({'#MODE'+str(i): mode})
                    keyList.update({'#STEPS'+str(i): steps})
                    keyList.update({'#DIFFICULTY'+str(i): difficulty})
                    keyList.update({'#LEVEL'+str(i): level})
            elif len(line) > 1 and len(line[1]) > 0 and not line[1][0] == ';':
                if line[0] == '#BPMS':
                    bpms = line[1].split(',')
                    listVal = []
                    lenB = len(bpms)
                    k = 0
                    while k < lenB:

                        if bpms[k].rfind(';'):
                            bpms[k] = bpms[k][:-2]
                        val = bpms[k].split('=')
                        if len(val) < 2:
                            bpms = simFile.readline().split(',')
                            lenB = len(bpms)
                            k = 0
                        else:
                            listVal.insert(0, float(val[1]))
                            k += 1
                    maxB = round(max(listVal))
                    minB = round(min(listVal))
                    keyList.update({'#BPMIN': str(minB)})
                    keyList.update({'#BPMAX': str(maxB)})
                else:
                    line[1] = line[1][:-2]
                    keyList.update({line[0]: line[1]})
        j += 1
    print(keyList)
    songList.append(keyList)


for el in path2:
    simFile = open(el, 'r')
    #length = len(simFile)
    addSong()

with open('songs.json', 'w') as outfile:
    json.dump(songList, outfile)

