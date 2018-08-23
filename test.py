# ============================================================================
# timing tests ... which approach is quicker?
# ============================================================================

import time

ITERATIONS = 1000000

def Assert(truth):
    if not truth: print("INCORRECT!")


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
