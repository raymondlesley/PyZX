# ============================================================================
# timing tests ... which approach is quicker?
# ============================================================================

import time
import random

ITERATIONS = 1000000

def Assert(truth):
    if not truth:
        print("INCORRECT!")
        raise ValueError


# ============================================================================
# word registers - quicker to store as bytes, words or both?

# bytes
_B = 0
_C = 0

def BC(word):
    B(word >> 8)
    C(word & 0x00ff)
def getBC():
    return _B << 8 | _C
def B(byte):
    global _B
    _B = byte
def getB():
    return _B
def C(byte):
    global _C
    _C = byte
def getC():
    return _C

# word
_DE = 0

def DE(word):
    global _DE
    _DE = word
def getDE():
    return _DE
def D(byte):
    global _DE
    _DE = (byte << 8) | (_DE & 0x00ff)
def getD():
    return _DE >> 8
def E(byte):
    global _DE
    _DE = (_DE & 0xff00) | byte
def getE():
    global _DE
    return _DE & 0xff

# both
_F = 0
_G = 0
_FG = 0

def FG(word):
    global _F, _G, _FG
    _FG = word
    _F = word >> 8
    _G = word & 0x00ff
def getFG():
    return _FG
def F(byte):
    global _FG, _F
    _FG = (byte << 8) | (_FG & 0x00ff)
    _F = byte
def getF():
    return _F
def G(byte):
    global _FG, _G
    _FG = (_FG & 0xff00) | byte
    _G = byte
def getG():
    return _G


# tests

print("inline code:")

start = time.process_time()
for repeat in range(ITERATIONS):
    BC(0x1234)
    Assert(getBC() == 0x1234)
    Assert((getB() == 0x12) and (getC() == 0x34))
    B(0x43)
    C(0x21)
    Assert(getBC() == 0x4321)
    Assert((getB() == 0x43) and (getC() == 0x21))
stop = time.process_time()
print("BC (store bytes): %fs" % (stop - start))

start = time.process_time()
for repeat in range(ITERATIONS):
    DE(0x1234)
    Assert(getDE() == 0x1234)
    Assert((getD() == 0x12) and (getE() == 0x34))
    D(0x43)
    E(0x21)
    Assert(getDE() == 0x4321)
    Assert((getD() == 0x43) and (getE() == 0x21))
stop = time.process_time()
print("DE (store word): %fs" % (stop - start))

start = time.process_time()
for repeat in range(ITERATIONS):
    FG(0x1234)
    Assert(getFG() == 0x1234)
    Assert((getF() == 0x12) and (getG() == 0x34))
    F(0x43)
    G(0x21)
    Assert(getFG() == 0x4321)
    Assert((getF() == 0x43) and (getG() == 0x21))
stop = time.process_time()
print("FG (store both): %fs" % (stop - start))

print("in a class:")

# same again, in a class
class Registers:
    # bytes
    _B = 0
    _C = 0

    def BC(self, word):
        self.B(word >> 8)
        self.C(word & 0x00ff)

    def getBC(self):
        return self._B << 8 | self._C

    def B(self, byte):
        self._B = byte

    def getB(self):
        return self._B

    def C(self, byte):
        self._C = byte

    def getC(self):
        return self._C

    # word
    _DE = 0

    def DE(self, word):
        self._DE = word

    def getDE(self):
        return self._DE

    def D(self, byte):
        self._DE = (byte << 8) | (self._DE & 0x00ff)

    def getD(self):
        return self._DE >> 8

    def E(self, byte):
        self._DE = (self._DE & 0xff00) | byte

    def getE(self):
        return self._DE & 0xff

    # both
    _F = 0
    _G = 0
    _FG = 0

    def FG(self, word):
        self._FG = word
        self._F = word >> 8
        self._G = word & 0x00ff

    def getFG(self):
        return self._FG

    def F(self, byte):
        self._FG = (byte << 8) | (self._FG & 0x00ff)
        self._F = byte

    def getF(self):
        return self._F

    def G(self, byte):
        self._FG = (self._FG & 0xff00) | byte
        self._G = byte

    def getG(self):
        return self._G

    def test(self):
        start = time.process_time()
        for repeat in range(ITERATIONS):
            self.BC(0x1234)
            Assert(self.getBC() == 0x1234)
            Assert((self.getB() == 0x12) and (self.getC() == 0x34))
            self.B(0x43)
            self.C(0x21)
            Assert(self.getBC() == 0x4321)
            Assert((self.getB() == 0x43) and (self.getC() == 0x21))
        stop = time.process_time()
        print("BC (store bytes): %fs" % (stop - start))

        start = time.process_time()
        for repeat in range(ITERATIONS):
            self.DE(0x1234)
            Assert(self.getDE() == 0x1234)
            Assert((self.getD() == 0x12) and (self.getE() == 0x34))
            self.D(0x43)
            self.E(0x21)
            Assert(self.getDE() == 0x4321)
            Assert((self.getD() == 0x43) and (self.getE() == 0x21))
        stop = time.process_time()
        print("DE (store word): %fs" % (stop - start))

        start = time.process_time()
        for repeat in range(ITERATIONS):
            self.FG(0x1234)
            Assert(self.getFG() == 0x1234)
            Assert((self.getF() == 0x12) and (self.getG() == 0x34))
            self.F(0x43)
            self.G(0x21)
            Assert(self.getFG() == 0x4321)
            Assert((self.getF() == 0x43) and (self.getG() == 0x21))
        stop = time.process_time()
        print("FG (store both): %fs" % (stop - start))


r = Registers()
r.test()


# ============================================================================
# opcode map - quicker with multiple if/tehn - or in a map?

def op():
    pass

print("opcode mapping:")

start = time.process_time()
for repeat in range(ITERATIONS):
    opcode = random.randint(0, 255)
    if opcode == 0: op(); continue
    if opcode == 1: op(); continue
    if opcode == 2: op(); continue
    if opcode == 3: op(); continue
    if opcode == 4: op(); continue
    if opcode == 5: op(); continue
    if opcode == 6: op(); continue
    if opcode == 7: op(); continue
    if opcode == 8: op(); continue
    if opcode == 9: op(); continue
    if opcode == 10: op(); continue
    if opcode == 11: op(); continue
    if opcode == 12: op(); continue
    if opcode == 13: op(); continue
    if opcode == 14: op(); continue
    if opcode == 15: op(); continue
    if opcode == 16: op(); continue
    if opcode == 17: op(); continue
    if opcode == 18: op(); continue
    if opcode == 19: op(); continue
    if opcode == 20: op(); continue
    if opcode == 21: op(); continue
    if opcode == 22: op(); continue
    if opcode == 23: op(); continue
    if opcode == 24: op(); continue
    if opcode == 25: op(); continue
    if opcode == 26: op(); continue
    if opcode == 27: op(); continue
    if opcode == 28: op(); continue
    if opcode == 29: op(); continue
    if opcode == 30: op(); continue
    if opcode == 31: op(); continue
    if opcode == 32: op(); continue
    if opcode == 33: op(); continue
    if opcode == 34: op(); continue
    if opcode == 35: op(); continue
    if opcode == 36: op(); continue
    if opcode == 37: op(); continue
    if opcode == 38: op(); continue
    if opcode == 39: op(); continue
    if opcode == 40: op(); continue
    if opcode == 41: op(); continue
    if opcode == 42: op(); continue
    if opcode == 43: op(); continue
    if opcode == 44: op(); continue
    if opcode == 45: op(); continue
    if opcode == 46: op(); continue
    if opcode == 47: op(); continue
    if opcode == 48: op(); continue
    if opcode == 49: op(); continue
    if opcode == 50: op(); continue
    if opcode == 51: op(); continue
    if opcode == 52: op(); continue
    if opcode == 53: op(); continue
    if opcode == 54: op(); continue
    if opcode == 55: op(); continue
    if opcode == 56: op(); continue
    if opcode == 57: op(); continue
    if opcode == 58: op(); continue
    if opcode == 59: op(); continue
    if opcode == 60: op(); continue
    if opcode == 61: op(); continue
    if opcode == 62: op(); continue
    if opcode == 63: op(); continue
    if opcode == 64: op(); continue
    if opcode == 65: op(); continue
    if opcode == 66: op(); continue
    if opcode == 67: op(); continue
    if opcode == 68: op(); continue
    if opcode == 69: op(); continue
    if opcode == 70: op(); continue
    if opcode == 71: op(); continue
    if opcode == 72: op(); continue
    if opcode == 73: op(); continue
    if opcode == 74: op(); continue
    if opcode == 75: op(); continue
    if opcode == 76: op(); continue
    if opcode == 77: op(); continue
    if opcode == 78: op(); continue
    if opcode == 79: op(); continue
    if opcode == 80: op(); continue
    if opcode == 81: op(); continue
    if opcode == 82: op(); continue
    if opcode == 83: op(); continue
    if opcode == 84: op(); continue
    if opcode == 85: op(); continue
    if opcode == 86: op(); continue
    if opcode == 87: op(); continue
    if opcode == 88: op(); continue
    if opcode == 89: op(); continue
    if opcode == 90: op(); continue
    if opcode == 91: op(); continue
    if opcode == 92: op(); continue
    if opcode == 93: op(); continue
    if opcode == 94: op(); continue
    if opcode == 95: op(); continue
    if opcode == 96: op(); continue
    if opcode == 97: op(); continue
    if opcode == 98: op(); continue
    if opcode == 99: op(); continue
    if opcode == 100: op(); continue
    if opcode == 101: op(); continue
    if opcode == 102: op(); continue
    if opcode == 103: op(); continue
    if opcode == 104: op(); continue
    if opcode == 105: op(); continue
    if opcode == 106: op(); continue
    if opcode == 107: op(); continue
    if opcode == 108: op(); continue
    if opcode == 109: op(); continue
    if opcode == 110: op(); continue
    if opcode == 111: op(); continue
    if opcode == 112: op(); continue
    if opcode == 113: op(); continue
    if opcode == 114: op(); continue
    if opcode == 115: op(); continue
    if opcode == 116: op(); continue
    if opcode == 117: op(); continue
    if opcode == 118: op(); continue
    if opcode == 119: op(); continue
    if opcode == 120: op(); continue
    if opcode == 121: op(); continue
    if opcode == 122: op(); continue
    if opcode == 123: op(); continue
    if opcode == 124: op(); continue
    if opcode == 125: op(); continue
    if opcode == 126: op(); continue
    if opcode == 127: op(); continue
    if opcode == 128: op(); continue
    if opcode == 129: op(); continue
    if opcode == 130: op(); continue
    if opcode == 131: op(); continue
    if opcode == 132: op(); continue
    if opcode == 133: op(); continue
    if opcode == 134: op(); continue
    if opcode == 135: op(); continue
    if opcode == 136: op(); continue
    if opcode == 137: op(); continue
    if opcode == 138: op(); continue
    if opcode == 139: op(); continue
    if opcode == 140: op(); continue
    if opcode == 141: op(); continue
    if opcode == 142: op(); continue
    if opcode == 143: op(); continue
    if opcode == 144: op(); continue
    if opcode == 145: op(); continue
    if opcode == 146: op(); continue
    if opcode == 147: op(); continue
    if opcode == 148: op(); continue
    if opcode == 149: op(); continue
    if opcode == 150: op(); continue
    if opcode == 151: op(); continue
    if opcode == 152: op(); continue
    if opcode == 153: op(); continue
    if opcode == 154: op(); continue
    if opcode == 155: op(); continue
    if opcode == 156: op(); continue
    if opcode == 157: op(); continue
    if opcode == 158: op(); continue
    if opcode == 159: op(); continue
    if opcode == 160: op(); continue
    if opcode == 161: op(); continue
    if opcode == 162: op(); continue
    if opcode == 163: op(); continue
    if opcode == 164: op(); continue
    if opcode == 165: op(); continue
    if opcode == 166: op(); continue
    if opcode == 167: op(); continue
    if opcode == 168: op(); continue
    if opcode == 169: op(); continue
    if opcode == 170: op(); continue
    if opcode == 171: op(); continue
    if opcode == 172: op(); continue
    if opcode == 173: op(); continue
    if opcode == 174: op(); continue
    if opcode == 175: op(); continue
    if opcode == 176: op(); continue
    if opcode == 177: op(); continue
    if opcode == 178: op(); continue
    if opcode == 179: op(); continue
    if opcode == 180: op(); continue
    if opcode == 181: op(); continue
    if opcode == 182: op(); continue
    if opcode == 183: op(); continue
    if opcode == 184: op(); continue
    if opcode == 185: op(); continue
    if opcode == 186: op(); continue
    if opcode == 187: op(); continue
    if opcode == 188: op(); continue
    if opcode == 189: op(); continue
    if opcode == 190: op(); continue
    if opcode == 191: op(); continue
    if opcode == 192: op(); continue
    if opcode == 193: op(); continue
    if opcode == 194: op(); continue
    if opcode == 195: op(); continue
    if opcode == 196: op(); continue
    if opcode == 197: op(); continue
    if opcode == 198: op(); continue
    if opcode == 199: op(); continue
    if opcode == 200: op(); continue
    if opcode == 201: op(); continue
    if opcode == 202: op(); continue
    if opcode == 203: op(); continue
    if opcode == 204: op(); continue
    if opcode == 205: op(); continue
    if opcode == 206: op(); continue
    if opcode == 207: op(); continue
    if opcode == 208: op(); continue
    if opcode == 209: op(); continue
    if opcode == 210: op(); continue
    if opcode == 211: op(); continue
    if opcode == 212: op(); continue
    if opcode == 213: op(); continue
    if opcode == 214: op(); continue
    if opcode == 215: op(); continue
    if opcode == 216: op(); continue
    if opcode == 217: op(); continue
    if opcode == 218: op(); continue
    if opcode == 219: op(); continue
    if opcode == 220: op(); continue
    if opcode == 221: op(); continue
    if opcode == 222: op(); continue
    if opcode == 223: op(); continue
    if opcode == 224: op(); continue
    if opcode == 225: op(); continue
    if opcode == 226: op(); continue
    if opcode == 227: op(); continue
    if opcode == 228: op(); continue
    if opcode == 229: op(); continue
    if opcode == 230: op(); continue
    if opcode == 231: op(); continue
    if opcode == 232: op(); continue
    if opcode == 233: op(); continue
    if opcode == 234: op(); continue
    if opcode == 235: op(); continue
    if opcode == 236: op(); continue
    if opcode == 237: op(); continue
    if opcode == 238: op(); continue
    if opcode == 239: op(); continue
    if opcode == 240: op(); continue
    if opcode == 241: op(); continue
    if opcode == 242: op(); continue
    if opcode == 243: op(); continue
    if opcode == 244: op(); continue
    if opcode == 245: op(); continue
    if opcode == 246: op(); continue
    if opcode == 247: op(); continue
    if opcode == 248: op(); continue
    if opcode == 249: op(); continue
    if opcode == 250: op(); continue
    if opcode == 251: op(); continue
    if opcode == 252: op(); continue
    if opcode == 253: op(); continue
    if opcode == 254: op(); continue
    if opcode == 255: op(); continue
stop = time.process_time()
print("if/then: %fs" % (stop - start))

opmap = {}
for code in range(256):
    opmap[code] = op

start = time.process_time()
for repeat in range(ITERATIONS):
    opcode = random.randint(0, 255)
    opfn = opmap[opcode]
    opfn()
stop = time.process_time()
print("mapped: %fs" % (stop - start))

opmap = [0]*256
for code in range(256):
    opmap[code] = op

start = time.process_time()
for repeat in range(ITERATIONS):
    opcode = random.randint(0, 255)
    opfn = opmap[opcode]
    opfn()
stop = time.process_time()
print("indexed: %fs" % (stop - start))

# ============================================================================
# iff - function or lambda?

def iif_fn(x, a, b):
	if x:
		return a
	else:
		return b

iif_lambda = lambda x, a, b : a if x else b

print("iif:")

start = time.process_time()
for repeat in range(ITERATIONS):
    Assert(iif_fn(True, 1, 2) == 1)
    Assert(iif_fn(False, 1, 2) == 2)
stop = time.process_time()
print("procedure: %fs" % (stop - start))

start = time.process_time()
for repeat in range(ITERATIONS):
    Assert(iif_fn(True, 1, 2) == 1)
    Assert(iif_fn(False, 1, 2) == 2)
stop = time.process_time()
print("lambda: %fs" % (stop - start))
