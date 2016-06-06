# coding: utf-8

from glob import glob
import sys
import re

def chunk(filen):
    inp = open(filen, encoding='utf8').read()
    inp = re.sub("[)(«»]", "", inp)
    inp = inp.replace("ё", "е")
    lines = inp.strip().split("\n")
    nps = []
    suit = ['N', 'A', 'P', 'M']
    pron = ["мой", "твой", "свой", "его", "ее", "её", "их", "он", "она", "они", "я", "мы", "ты", "вы", "наш", "ваш", "себя", "который"]
    pers_pron = ["он", "она", "они", "я", "мы", "ты", "вы"]
    link = ['штат', 'город', "аэропорт", "господин", "президент", "мистер", ]
    sent = 1
    for index, line in enumerate(lines):
        parts = line.split("\t")
        np = []
        if "SENT" in line:
            sent += 1
        if len(parts) > 1:
            word = parts[0]
            pos = parts[1]
            lem = parts[2]
            if lem in pron:
                nps.append([sent]+[line])
                np.append(line)
            if lem in pers_pron:
                pass
            elif pos[0] in suit or pos.startswith("Vmp"): 
                if pos[0] == 'P' or pos[0] == 'A':
                    case = pos[5]
                    num = pos[4]
                    gen = pos[3]
                elif (pos[0] == 'N' and len(pos) < 7) or (pos[0] == 'M' and len(pos) > 2):
                    case = pos[4]
                    num = pos[3]
                    gen = pos[2]
                    if pos == 'N':
                        case = pos[-1]
                elif pos[0] == 'V':
                    try:
                        case = pos[10]
                    except IndexError:
                        np == []
                np.append(line)
                for i in range(index+1, len(lines)-1):
                    if "SENT" in lines[i]:
                        break
                    elif i < len(lines):
                        parts = lines[i-1].split("\t")
                        word = parts[0]
                        pos = parts[1]
                        lem = parts[2]
                        if pos[0] in suit or pos.startswith("Vmp"): 
                            if pos[0] == 'P' or pos[0] == 'A':
                                case = pos[5]
                                num = pos[4]
                                gen = pos[3]
                            elif (pos[0] == 'N' and len(pos) < 7) or (pos[0] == 'M' and len(pos) > 2):
                                case = pos[4]
                                num = pos[3]
                                gen = pos[2]
                                if pos == 'N':
                                    case = pos[-1]
                            elif pos[0] == 'V':
                                try:
                                    case = pos[10]
                                except IndexError:
                                    break
                        nword, npos, nl = lines[i].split("\t")
                        if len(npos) == 1:
                            break
                        elif npos[0] == 'P' or npos == 'A':
                            ncase = npos[5]
                            nnum = pos[4]
                            ngen = pos[3]
                        elif (npos[0] == 'N' and len(pos) < 7) or (npos[0] == 'M' and len(npos) > 2):
                            ncase = npos[4]
                            nnum = pos[3]
                            ngen = pos[2]
                            if npos == 'N':
                                ncase = npos[-1]                        
                        else:
                            ncase = ''
#                         if (npos.startswith("Np") or nword.istitle()) and not (pos.startswith("Np") or word.istitle()):
#                             if ncase == 'n':
#                                 np.append(lines[i])
#                             break
#                         if ncase == 'n' and case != 'n':
#                             if pos.startswith("Np") or lem.istitle() or npos.startswith("Np") or nword.istitle():
#                                 np.append(lines[i]) 
#                                 break
                        if npos[0] == 'N':
                            if npos.startswith("Np") or (nword.istitle()):
                                if (pos.startswith("Np") or (word.istitle()) or lem in link) and ncase == case or ncase == 'n':
                                    np.append(lines[i])
                                else:
                                    break
                            else:
                                np.append(lines[i])
                        elif npos[0] == 'A':
                            if pos[0] == 'A' and ngen == gen and nnum == num:
                                np.append(lines[i])
                        elif npos[0] == 'M' and case == '-' and npos[-1] == 'd':
                            np.append(lines[i])
                        elif npos[0] == 'S':
                            nps.append(np)
                            case = npos[3] # break
                            if pos.startswith("Np") or (pos.startswith("Nc") and lem.istitle()): 
                                break
                            elif not (pos.startswith("Np") or (pos.startswith("Nc") and lem.istitle())):
                                np.append(lines[i])
                        elif (npos[0] == 'N'or npos[0] == 'M') and ncase == case :
                            np.append(lines[i])   
                        elif (npos[0] == 'N' or npos[0] == 'P') and ncase != case and ncase != 'a':
                            if not (pos.startswith("Np") or word.istitle()):
                                np.append(lines[i]) 
                            else:
                                break
                        else:
                            break
            else:
                np=[]
            if len(np) > 1:
                nps.append([sent]+np)
            elif pos[0] == 'N' or pos[0] == 'P' or (pos[0] == 'A' and lem.istitle()):
                if len(pos) > 3 and pos[-2] !='-': 
                    nps.append([sent]+np)

#     remove repetitions in nps
    nnps = [] # normalized nps
    for np in nps:
        nnp = [np[0]]
        for i in range(1, len(np)):
            if np[i] == np[i-1]: 
                pass
            else:
                nnp.append(np[i])
        nnps.append(nnp)
        
#     remove repetitions between nps
    nnpse = [nnps[0]] # normalized nps + edited
    for i in range(1, len(nnps)):
        if nnps[i] == nnps[i-1]:
            pass
        else:
            nnpse.append(nnps[i])
            
#     remove trailing pronouns
    for i in range(len(nnpse)):
        if len(nnpse[i]) > 2 and (nnpse[i][-1].split("\t")[1].startswith("P") or nnpse[i][-1].split("\t")[1].startswith("S")):
            nnpse[i] = nnpse[i][:-1]
        
#     join proper names
    pnenps = [nnpse[0]] # proper normalized edited nps
    for i in range(1, len(nnpse)):
        if len(nnpse[i]) == 1 and isinstance(nnpse[i], str):
            if nnpse[i][0].split()[1].startswith('Np') or nnpse[i][0].split()[-1].istitle():
                if nnpse[i-1][0].split()[1].startswith('Np'):
                    pass
                elif nnpse[i-1][0].split()[-1].istitle():
                    pass
            else:
                pnenps.append(nnpse[i])
        else:
                pnenps.append(nnpse[i])

#     mark head: if: noun or pronoun; not genitive if other cases; 
    for np in pnenps:
        case = ''
        for n in range(1, len(np)):
            if len(np) == 2:
                np[1] += '\tHEAD'
            else:
                word,pos,lem = np[n].split("\t")[:3]
                if pos[0] == 'N' or (pos[0] == 'P' and pos[6] == 'n'):
                    if not case:
                        case = pos[4]
                        if pos[0] == 'N' and len(pos) == 7:
                            case = pos[-1]
                        np[n] += '\tHEAD'
                    if n > 1 and (pos.startswith("Np") or lem.istitle()):
                        pword,ppos,plem = np[n-1].split("\t")[:3]
                        if (ppos.startswith("Np") or plem.istitle()) and np[n-1].endswith('HEAD'):
                            np[n] += '\tHEAD'
                elif  npos[0] == 'P' or npos[0] == 'A':
                    if not case:
                        case = pos[5]  

#     remove repetitions between nps
    fpnenps = [pnenps[0]] # final proper normalized edited nps
    for i in range(1, len(pnenps)):
        if "".join(pnenps[i-1][1:]).endswith("".join(pnenps[i][1:])):
            pass
        else:
            fpnenps.append(pnenps[i])

    return enumerate(fpnenps)

def main(src):
    a = glob(src)
    for text in a:
        for i, np in chunk(text):
            outp = "\t".join([str(a).replace("\t", ",") for a in np])
            with open("{0}-chunked.txt".format(text.replace(".txt", "")), 'a+', encoding='utf8') as out:
                out.write(outp+"\n")

if '--launch' in sys.argv:
    main(sys.argv[-1]+'*.txt')
else:
    main("*.txt")

