# import pygame
# from pygame.locals import *

b4 = 0x10
b3 = 0x08
b2 = 0x04
b1 = 0x02
b0 = 0x01

keyboard = [0xff] * 8
key_events = []


_B_SPC  = 0
_H_ENT  = 1
_Y_P    = 2
_6_0    = 3
_1_5    = 4
_Q_T    = 5
_A_G    = 6
_CAPS_V = 7

def reset_keyboard():
	global _B_SPC, _H_ENT, _Y_P, _6_0, _1_5, _Q_T, _A_G, _CAPS_V, key_events
	keyboard[_B_SPC]  = 0xff
	keyboard[_H_ENT]  = 0xff
	keyboard[_Y_P]    = 0xff
	keyboard[_6_0]    = 0xff
	keyboard[_1_5]    = 0xff
	keyboard[_Q_T]    = 0xff
	keyboard[_A_G]    = 0xff
	keyboard[_CAPS_V] = 0xff
	key_events = []

# constants (from pygame) [see http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html]
KMOD_SHIFT = 0x0001
KMOD_LOCK = 0x0002
KMOD_CTRL = 0x0004
KMOD_ALT = 0x0080
K_SPACE = ' '
K_RETURN = '\r'
K_TAB = '\t'
K_BACKSPACE = 'Backspace'
K_LEFT = 'Left'
K_DOWN = 'Down'
K_UP = 'Up'
K_RIGHT = 'Right'
K_RALT = 'Alt_R'
K_LCTRL = 'Control_L'
K_0 = '0'
K_5 = '5'
K_6 = '6'
K_7 = '7'
K_8 = '8'


signals = {
'1': [_1_5, b0],  #K_1:[_1_5, b0],
'2': [_1_5, b1],  #K_2:[_1_5, b1],
'3': [_1_5, b2],  #K_3:[_1_5, b2],
'4': [_1_5, b3],  #K_4:[_1_5, b3],
'5': [_1_5, b4],  #K_5:[_1_5, b4],

'6': [_6_0, b4],  #K_6:[_6_0, b4],
'7': [_6_0, b3],  #K_7:[_6_0, b3],
'8': [_6_0, b2],  #K_8:[_6_0, b2],
'9': [_6_0, b1],  #K_9:[_6_0, b1],
'0': [_6_0, b0],  #K_0:[_6_0, b0],

'q': [_Q_T, b0],  #K_q:[_Q_T, b0],
'w': [_Q_T, b1],  #K_w:[_Q_T, b1],
'e': [_Q_T, b2],  #K_e:[_Q_T, b2],
'r': [_Q_T, b3],  #K_r:[_Q_T, b3],
't': [_Q_T, b4],  #K_t:[_Q_T, b4],

'y': [_Y_P, b4],  #K_y:[_Y_P, b4],
'u': [_Y_P, b3],  #K_u:[_Y_P, b3],
'i': [_Y_P, b2],  #K_i:[_Y_P, b2],
'o': [_Y_P, b1],  #K_o:[_Y_P, b1],
'p': [_Y_P, b0],  #K_p:[_Y_P, b0],

'a': [_A_G, b0],  #K_a:[_A_G, b0],
's': [_A_G, b1],  #K_s:[_A_G, b1],
'd': [_A_G, b2],  #K_d:[_A_G, b2],
'f': [_A_G, b3],  #K_f:[_A_G, b3],
'g': [_A_G, b4],  #K_g:[_A_G, b4],

'h': [_H_ENT, b4],  #K_h:[_H_ENT, b4],
'j': [_H_ENT, b3],  #K_j:[_H_ENT, b3],
'k': [_H_ENT, b2],  #K_k:[_H_ENT, b2],
'l': [_H_ENT, b1],  #K_l:[_H_ENT, b1],
K_RETURN: [_H_ENT, b0],  #K_RETURN:[_H_ENT, b0],

K_LCTRL: [_CAPS_V, b0],  #K_LCTRL:[_CAPS_V, b0],
'z': [_CAPS_V, b1],  #K_z:[_CAPS_V, b1],
'x': [_CAPS_V, b2],  #K_x:[_CAPS_V, b2],
'c': [_CAPS_V, b3],  #K_c:[_CAPS_V, b3],
'v': [_CAPS_V, b4],  #K_v:[_CAPS_V, b4],

'b': [_B_SPC, b4],  #K_b:[_B_SPC, b4],
'n': [_B_SPC, b3],  #K_n:[_B_SPC, b3],
'm': [_B_SPC, b2],  #K_m:[_B_SPC, b2],
'Alt_R': [_B_SPC, b1],  #K_RALT:[_B_SPC, b1],
' ': [_B_SPC, b0],  #K_SPACE:[_B_SPC, b0],
}


keymap = {
	49: '1',
	50: '2',
	51: '3',
	52: '4',
	53: '5',
	54: '6',
	55: '7',
	56: '8',
	57: '9',
	48: '0',

	81: 'q',
	87: 'w',
	69: 'e',
	82: 'r',
	84: 't',
	89: 'y',
	85: 'u',
	73: 'i',
	79: 'o',
	80: 'p',

	65: 'a',
	83: 's',
	68: 'd',
	70: 'f',
	71: 'g',
	72: 'h',
	74: 'j',
	75: 'k',
	76: 'l',
	13: '\r',

	16: K_LCTRL,
	90: 'z',
	88: 'x',
	67: 'c',
	86: 'v',
	66: 'b',
	78: 'n',
	77: 'm',
	# 17: 'Sym',
	32: ' ',

	8: K_BACKSPACE,
	37: K_LEFT,
	38: K_UP,
	39: K_RIGHT,
	40: K_DOWN
}

def map_keys(key):
	if key == '\x08':  key = K_BACKSPACE
	return key

# TODO: call do_key() directly; remove key_events; empty do_keys()
def key_down(event):
	mods = event.state

	try:
		key = keymap[event.keycode]
	except KeyError:
		key = ''

	#key_events.append((True, key, mods))
	do_key(True, key, mods)

def key_up(event):
	mods = event.state

	try:
		key = keymap[event.keycode]
	except KeyError:
		key = ''

	#key_events.append((False, key, mods))
	do_key(False, key, mods)


def do_keys():
	global key_events

	for event in key_events:
		do_key(event[0], event[1], event[2])
	key_events = []  # reset event buffer


def do_key(down, ascii, mods):
	CAPS = (mods & KMOD_SHIFT)!=0
	SYMB = (mods & KMOD_CTRL)!=0
	SHIFT = (mods & KMOD_LOCK)!=0

	if ascii == K_SPACE: CAPS = SHIFT
	if ascii == K_RETURN: CAPS = SHIFT
	if ascii == K_TAB: CAPS = True; SYMB = True
	if ascii == K_BACKSPACE: CAPS = True; ascii = K_0
	if ascii == K_LCTRL: CAPS = True

	if ascii == K_LEFT: CAPS = True; ascii = K_5
	if ascii == K_DOWN: CAPS = True; ascii = K_6
	if ascii == K_UP: CAPS = True; ascii = K_7
	if ascii == K_RIGHT: CAPS = True; ascii = K_8

	try:

		sig = signals[ascii]

		if down:
			keyboard[sig[0]] &= ~sig[1]
		else:
			keyboard[sig[0]] |= sig[1]
	
		if SYMB & down:
			sig = signals[K_RALT]
			keyboard[sig[0]] &= ~sig[1]
		else:
			sig = signals[K_RALT]
			keyboard[sig[0]] |= sig[1]
	
		if CAPS & down:
			sig = signals[K_LCTRL]
			keyboard[sig[0]] &= ~sig[1]
		else:
			sig = signals[K_LCTRL]
			keyboard[sig[0]] |= sig[1]

	except KeyError:
		pass







