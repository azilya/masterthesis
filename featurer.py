# coding: utf-8

from glob import glob
import os

def makefeat(src):
    inf = open(src, encoding='utf8').read()
    lines = inf.split("\n")
    for line in lines[:-2]:
        parts = line.split("\t")
        sent = parts[0]
        words = [a.split(",")[0] for a in parts[1:]]
        pos = [a.split(",")[1] for a in parts[1:]]
        lemmas = [a.split(",")[2] for a in parts[1:]]
        head_id = [parts.index(part) for part in parts if "HEAD" in part]
        head = [words[h-1] for h in head_id]
        head_l = [lemmas[h-1] for h in head_id]
        head_p = [pos[h-1] for h in head_id]
        head_case = []
        for h in head_p:
            if h[0] == 'N':
                head_case.append(h[4])
            elif h[0] == 'P':
                head_case.append(h[5])
        head_case = set(head_case)
        head_num = []
        for h in head_p:
            if h[0] == 'N':
                head_num.append(h[3])
            elif h[0] == 'P':
                head_num.append(h[4])
        head_num = set(head_num)    
        for j, n_line in enumerate(lines[lines.index(line)+1:-1]):
            nparts = n_line.split("|")
            nsent = nparts[0]
            nwords = [a.split(",")[0] for a in nparts[1:]]
            npos = [a.split(",")[1] for a in nparts[1:]]
            nlemmas = [a.split(",")[2] for a in nparts[1:]]
            nhead_id = [nparts.index(npart) for npart in nparts if "HEAD" in npart]
            try:
                nhead = [nwords[nh-1] for nh in nhead_id]
            except IndexError:
                print(nwords, nhead_id)
            nhead_l = [nlemmas[nh-1] for nh in nhead_id]
            nhead_p = [npos[nh-1] for nh in nhead_id]
            nhead_case = []
            for h in nhead_p:
                if h[0] == 'N':
                    nhead_case.append(h[4])
                elif h[0] == 'P':
                    nhead_case.append(h[5])
            nhead_case = set(nhead_case)
            nhead_num = []
            for h in nhead_p:
                if h[0] == 'N':
                    nhead_num.append(h[3])
                elif h[0] == 'P':
                    nhead_num.append(h[4])
            nhead_num = set(nhead_num) 
            if int(nsent) - int(sent) < 3:
                dist_sent = int(nsent) - int(sent)
                dist_gr = j
                if words == nwords:
                    groups_identical = 1
                else:
                    groups_identical = 0
                if head == nhead:
                    head_identical = 1
                else:
                    head_identical = 0
                if head_l == nhead_l:
                    lem_head_identical = 1
                else:
                    lem_head_identical = 0            
                if head_l in nhead_l:
                    head_prev_less = 1
                else:
                    head_prev_less = 0
                if nhead_l in head_l:
                    head_next_less = 1
                else:
                    head_next_less = 0
                if len(pos) == 1 and pos[0].startswith("P"):
                    prev_pron = 1
                    if lemmas[0] in ["он", "она", "они", "я", "мы", "ты", "вы"]:
                        prev_pron_type = 'pers'
                    elif lemmas[0] in ["мой", "твой", "его", "ее", "их", "наш", "ваш"]:
                        prev_pron_type = 'poss'
                    elif lemmas[0] in ["свой", "себя"]: 
                        prev_pron_type = 'refl'
                    elif lemmas[0] in ["который", "тот"]: 
                        prev_pron_type = 'rel'
                else:
                    prev_pron = 0
                    prev_pron_type = 'none'
                if len(npos) == 1 and npos[0].startswith("P"):
                    next_pron = 1
                    if nlemmas[0] in ["он", "она", "они", "я", "мы", "ты", "вы"]:
                        next_pron_type = 'pers'
                    elif nlemmas[0] in ["мой", "твой", "его", "ее", "их", "наш", "ваш"]:
                        next_pron_type = 'poss'
                    elif nlemmas[0] in ["свой", "себя"]: 
                        next_pron_type = 'refl'
                    elif nlemmas[0] in ["который", "тот"]: 
                        next_pron_type = 'rel'
                else:
                    next_pron = 0
                    next_pron_type = 'none'
                if any((p[0] == 'N' or p[0] == 'P') and p[5] == 'y' for p in head_p):
                    prev_anim = 1
                else:
                    prev_anim = 0
                if any((np[0] == 'N' or np[0] == 'P') and np[5] == 'y' for np in nhead_p):
                    next_anim = 1
                else:
                    next_anim = 0
                if nhead_case == head_case:
                    same_case = 1
                else:
                    same_case = 0
                if head_case != set('n'):
                    case_prev = ''.join(list(head_case.difference(set('n'))))
                else:
                    case_prev = 'n'
                if nhead_case != set('n'):
                    case_next = ''.join(list(nhead_case.difference(set('n'))))
                else:
                    case_next = 'n'
                if nhead_num == head_num:
                    same_num = 1
                else:
                    same_num = 0
                num_prev = ''.join(head_num)
                num_next = ''.join(nhead_num)
                if any(p.startswith("Np") for p in head_p):
                    prev_prop = 1
                else:
                    prev_prop = 0
                if any(np.startswith("Np") for np in nhead_p):
                    next_prop = 1
                else:
                    next_prop = 0       
                feats = ["".join(pos), "".join(lemmas), "".join(npos), "".join(nlemmas), "".join(head_l), "".join(nhead_l)
                         dist_sent, dist_gr, groups_identical, head_identical, lem_head_identical, head_prev_less, 
                         head_next_less, prev_anim, next_anim, same_case, case_prev, case_next, same_num, num_prev,
                         num_next, prev_pron, prev_pron_type, next_pron, next_pron_type, prev_prop, next_prop]

                if dist_gr < 12:
                    yield feats

def main(src):
    src = glob(src)
    with open("output.csv", 'a+', encoding='utf8') as out:
        out.write("pos,lemmas,npos,nlemmas,dist_sent,dist_gr,groups_identical,head_identical,lem_head_identical,head_prev_less,head_next_less,prev_prop,next_prop,prev_anim,next_anim,same_case,case_prev,case_next,same_num,num_prev,num_next,prev_pron,prev_pron_type,next_pron,next_pron_type,prev_prop,next_prop\n")
        for text in src:
            for line in makefeat(text):
                out.write(str(line).replace('[', ''). replace(']', '').replace(' ', '')+'\n')

if '--launch' in sys.argv:
    main(sys.argv[-1]+'*.txt')
else:
    main("*.txt")

