import json
import glob
from collections import defaultdict


PATH = 'Stepchart.sm'

path2 = glob.glob('../../../../giochi/StepMania 5/Songs/**/*.sm', recursive=True)

#path2 = glob.glob('../../../../giochi/StepMania 5/Songs/all songs pack/Okkusenman (Hardcore Mix) (CuoReNeRo)/Okkusenman (Hardcore Mix).sm', recursive=True)

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
                    if difficulty == 'Challenge':
                        keyList.update({'#MODE'+str(i): mode})
                        keyList.update({'stepsL1': steps})
                        keyList.update({'#DIFFICULTY'+str(i): difficulty})
                        keyList.update({'l1': level})
                    elif difficulty == 'Hard':
                        keyList.update({'#MODE' + str(i): mode})
                        keyList.update({'stepsL2': steps})
                        keyList.update({'#DIFFICULTY' + str(i): difficulty})
                        keyList.update({'l2': level})
                    elif difficulty == 'Medium':
                        keyList.update({'#MODE' + str(i): mode})
                        keyList.update({'stepsL3': steps})
                        keyList.update({'#DIFFICULTY' + str(i): difficulty})
                        keyList.update({'l3': level})
                    elif difficulty == 'Easy':
                        keyList.update({'#MODE' + str(i): mode})
                        keyList.update({'stepsL4': steps})
                        keyList.update({'#DIFFICULTY' + str(i): difficulty})
                        keyList.update({'l4': level})
                    elif difficulty == 'Beginner':
                        keyList.update({'#MODE' + str(i): mode})
                        keyList.update({'stepsL5': steps})
                        keyList.update({'#DIFFICULTY' + str(i): difficulty})
                        keyList.update({'l5': level})
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
                    keyList.update({'bpm1': str(minB)})
                    keyList.update({'bpm2': str(maxB)})
                elif line[0] == '#TITLE':
                    line[1] = line[1][:-2]
                    keyList.update({'name': line[1]})
                elif line[0] == '#ARTIST':
                    line[1] = line[1][:-2]
                    keyList.update({'artist': line[1]})
                else:
                    line[1] = line[1][:-2]
                    keyList.update({line[0]: line[1]})
        elif len(text) > 7 and '#TITLE:' in text:  # when the title is corrupted
            cleanString = text.split('#TITLE:')
            keyList.update({'name': cleanString[1][:-2]})
        j += 1
    if 'name' not in keyList and '#TITLETRANSLIT' in keyList:
        titleTranslit = keyList['#TITLETRANSLIT']
        keyList.update({'name': titleTranslit})
    if 'name' in keyList and ('l1' in keyList or 'l2' in keyList or 'l3' in keyList or 'l4' in keyList or 'l5' in keyList):
        print(keyList)
        songList.append(keyList)




for el in path2:
    simFile = open(el, 'r')
    #length = len(simFile)
    addSong()

songPack = defaultdict(dict)
songPack.update({'Songs': songList})

with open('songs.json', 'w') as outfile:
    json.dump(songPack, outfile)

