import sys

def getbinstr(input):
    return ''.join(map('{0:08b}'.format,bytearray(input.encode('ascii'))))
    
def bs2ba(binstr):
    return [c == '1' for c in binstr]

def getm(i, length):
    x = 2 ** i
    diff =  2 ** (i + 1) - 2 ** i
    res = [x]
    while 1:
        x += 1
        if not (x & (1 << i)):
            x += diff
        if x > length:
            break
        # res.append('{0:b}'.format(x))
        res.append(x)
    return res


def getparity(input):
    bs = getbinstr(input)
    ba = bs2ba(bs)
    blen = len(bs)
    plen = 0
    dlen = 0
    while dlen < blen:
        dlen += 2 ** plen - 1
        ba.insert(2 ** plen - 1, 0)
        plen += 1
    
    ps = []
    
    for i in range(plen):
        m = getm(i, len(ba))
        pi = ba[m[1] - 1]
        for j in range(2, len(m)):
            pi ^= ba[m[j] - 1]
        ps.append(pi)
        ba[2 ** i - 1] = pi
    
    ps = ''.join(['1' if b else '0' for b in ps])
    return ps, ba


def main():
    input = sys.argv[1]
    paritybits, h = getparity(input)
    print(paritybits)

if __name__ == '__main__':
    main()