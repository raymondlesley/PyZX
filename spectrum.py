# ZX Spectrum Emulator
# Vadim Kataev
# www.technopedia.org
#
# ver.0.1 2005
# ver.0.2 June 2008
#
# from https://www.pygame.org/project/173/1347
# converted for Python 3.6, Tkinter August 2018 Raymond Lesley
# updated for Python 3.8 May 2020 Raymond lesley

import sys
import Z80
import video

#
# Configuration constants - define machine
#

CPUFREQ = 3.5  # MHz
ROMFILE = '48.rom'
# ROMFILE = '48-modified.rom'
# ROMFILE = '48-busysoft-140.rom'
# ROMFILE = 'spectrum.rom'
# ROMFILE = 'trdos-501.rom'


def test_program():
	# txt = """
	# 3E 03       LD A,3
	# 67          LD H,A
	# 18 02       JR (PC+e)
	# C6 03       ADD A,3
	# C6 03       ADD A,3
	# """
	# code = [0x3E, 0x03, 0x67, 0x18, 0x01, 0xC6, 0xC6, 0xC6]
	# code = [0x3E, 0x03, 0xC6, 0x03, 0xC6, 0x03, 0xC6, 0x03]
	code = [0x3E, 0x03, 0x67, 0x18, 0x02, 0xC6, 0x03, 0xC6, 0x03]
	return code


def load_rom(filename):
	rom = open(filename, 'rb').read()
	# rom = test_programm()
	for index, item in enumerate(rom):
		# op = ord(item)
		op = item
		Z80.mem[index] = (op + 256) & 0xff
	print('Loaded %d bytes of ROM' % (len(rom)))


def run():
	try:
		Z80.execute()
	except KeyboardInterrupt:
		return


video.init()
Z80.Z80(CPUFREQ)  # CPU freq in MhZ

load_rom(ROMFILE)
Z80.reset()
Z80.outb(254, 0xff, 0)  # white border on startup

sys.setswitchinterval(0.5)  # we don't use threads, so reduce task switching frequency

# import load
# load.loadZ80('./games/INVADERS.Z80')
# load.loadZ80('./games/KLORE-TR.Z80')
# PAWS.Z80
# DIZZY1YS.Z80
# COSTCAPR.Z80
# F1.Z80
# RAINBOW.Z80 ---unsup
# DRAGTORC.Z80
# EARTHOLD.Z80
# F15_EAGL.Z80
# FLYSHARK.Z80
# HEADHEEL.Z80
# JSWAPRIL.Z80
# OBLIVION.Z80
# SABOT2PL.Z80
# SENTNEL.Z80

run()
