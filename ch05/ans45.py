class Morph:
    def __init__(self, dc):
        self.surface = dc['surface']
        self.base = dc['base']
        self.pos = dc['pos']
        self.pos1 = dc['pos1']


class Chunk:
    def __init__(self, morphs, dst):
        self.morphs = morphs    # 形態素（Morphオブジェクト）のリスト
        self.dst = dst          # 係り先文節インデックス番号
        self.srcs = []          # 係り元文節インデックス番号のリスト


def parseCabocha(block):
    def checkCreateChunk(tmp):
        if len(tmp) > 0:
            c = Chunk(tmp, dst)
            res.append(c)
            tmp = []
        return tmp

    res = []
    tmp = []
    dst = None
    for line in block.split('\n'):
        if line == '':
            tmp = checkCreateChunk(tmp)
        elif line[0] == '*':
            dst = line.split(' ')[2].rstrip('D')
            tmp = checkCreateChunk(tmp)
        else:
            (surface, attr) = line.split('\t')
            attr = attr.split(',')
            lineDict = {
                'surface': surface,
                'base': attr[6],
                'pos': attr[0],
                'pos1': attr[1]
            }
            tmp.append(Morph(lineDict))

    for i, r in enumerate(res):
        res[int(r.dst)].srcs.append(i)
    return res


filename = 'ch05/neko.txt.cabocha'
with open(filename, mode='rt', encoding='utf-8') as f:
    blockList = f.read().split('EOS\n')
blockList = list(filter(lambda x: x != '', blockList))
blockList = [parseCabocha(block) for block in blockList]

for b in blockList:
    for m in b:
        if len(m.srcs) > 0:
            preMorphs = [b[int(s)].morphs for s in m.srcs]
            preMorphs = [list(filter(lambda x: '助詞' in x.pos, pm)) for pm in preMorphs]
            preSurface = [[p.surface for p in pm] for pm in preMorphs]
            preSurface = list(filter(lambda x: x != [], preSurface))
            preSurface = [p[0] for p in preSurface]
            postBase = [mo.base for mo in m.morphs]
            postPos = [mo.pos for mo in m.morphs]
            if len(preSurface) > 0 and '動詞' in postPos:
                print(postBase[0], ' '.join(preSurface), sep='\t')
