import sys

def getbinstr(input):
    return ''.join(map('{0:08b}'.format,bytearray(input.encode('ascii'))))

def bin2str(binstr):
    return ''.join([chr(int(binstr[i:i + 8], 2)) for i in range(0, len(binstr), 8)])
    
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

def ba2data(ba):
    plen = 0
    hlen = 0
    ps = []
    data = []
    while hlen < len(ba):
        diff = 2 ** plen
        ps.append(ba[hlen])
        for i in range(hlen + 1, min(hlen + diff, len(ba))):
            data.append(ba[i])
        plen += 1
        hlen += diff
    
    data = ''.join(['1' if b else '0' for b in data])
    ps = ''.join(['1' if b else '0' for b in ps])
    return ps, data

def corerr(ps, input):
    ips, iba = getparity(input)
    
    inset = None
    ninset = None

    for i in range(len(ps)):
        m = getm(i, len(iba))

        iba[2 ** i - 1] = ps[i] == '1'
        
        if ps[i] == ips[i]:
            if ninset is None:
                ninset = set(m)
            else:
                ninset |= set(m)
        else:
            if inset is None:
                inset = set(m)
            else:
                inset &= set(m)

    if inset is not None and ninset is not None:
        remain = inset.difference(ninset)
        widx = next(iter(remain)) - 1
        iba[widx] = not iba[widx]
        cps, cdata = ba2data(iba)
        return cps, bin2str(cdata)
            
    return ps, input


def main():
    pbits = sys.argv[1]
    input = sys.argv[2]
    cpbits, cdata = corerr(pbits, input)
    print(cpbits)
    print(cdata)

if __name__ == '__main__':
    main()