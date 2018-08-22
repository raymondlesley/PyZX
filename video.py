
from tkinter import Tk, Canvas, PhotoImage, mainloop
import Z80, keyboard

xscale = 1
yscale = 1

SCREEN_WIDTH = 256 * xscale;
SCREEN_HEIGHT = 192 * yscale
CENTRE_X = SCREEN_WIDTH // 2;
CENTRE_Y = SCREEN_HEIGHT // 2

sat = 238
norm = 128

black = (0, 0, 0)
blue = (0, 0, norm)
red = (norm, 0, 0)
magenta = (norm, 0, norm)
green = (0, norm, 0)
cyan = (0, norm, norm)
yellow = (norm, norm, 0)
white = (norm, norm, norm)

brightColors = [
	(0, 0, 0), (0, 0, sat), (sat, 0, 0), (sat, 0, sat), (0, sat, 0), (0, sat, sat), (sat, sat, 0), (sat, sat, sat),
	black, blue, red, magenta, green, cyan, yellow, white
]

borderWidth = 20  # absolute, not relative to pixelScale
pixelScale = 1  # scales pixels in main screen, not border

nPixelsWide = 256
nPixelsHigh = 192
nCharsWide = 32
nCharsHigh = 24

firstAttr = (nPixelsHigh * nCharsWide)
lastAttr = firstAttr + (nCharsHigh * nCharsWide)

first = -1
FIRST = -1
last = range((nPixelsHigh + nCharsHigh) * nCharsWide)
next = range((nPixelsHigh + nCharsHigh) * nCharsWide)

buf_start = 16384
buf_end = 22527
buf_length = buf_end - buf_start + 1
attr_start = 22528
attr_end = 23295


def refreshWholeScreen():
	for i in xrange(firstAttr):
		next[i] = i - 1
		last[i] = (~mem[i + 16384]) & 0xff
	for i in range(firstAttr, lastAttr):
		next[i] = -1
		last[i] = mem[i + 16384]
	first = firstAttr - 1;
	FIRST = -1


def init():
	global screen, screen_map, screen_img
	screen = Tk()
	screen.title("PyZX")
	screen_map = Canvas(screen, width=SCREEN_WIDTH+borderWidth*2, height=SCREEN_HEIGHT+borderWidth*2, bg='#FFFFFF')
	screen_img = PhotoImage(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
	screen_map.create_image((CENTRE_X+borderWidth, CENTRE_Y+borderWidth), image=screen_img, state="normal")
	screen_map.pack()
	screen.bind('<KeyPress>', keyboard.key_down)
	screen.bind('<KeyRelease>', keyboard.key_up)
	return

def rgb_to_string(rgb):
	# tuple (r, g, b) to '#rrggbb'
	colour = '#{0:02X}{1:02X}{2:02X}'.format(*rgb)
	return colour

def set_at(coords, colour):
	global screen_img
	colour_string = rgb_to_string(colour)
	screen_img.put(colour_string, coords)


def fill_screen_map():
	global screen, Z80
	mem = Z80.mem
	for addr in range(buf_start, buf_end + 1):
		y = ((addr & 0x00e0) >> 2) + ((addr & 0x0700) >> 8) + ((addr & 0x1800) >> 5)
		sx = (addr & 0x1f) << 3

		attr = mem[22528 + (addr & 0x1f) + ((y >> 3) * 32)]
		bright = ((attr >> 3) & 0x08)
		ink = (attr & 0x07) | bright
		pap = ((attr >> 3) & 0x07) | bright

		byte = mem[addr]

		if (1 << 7) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if (1 << 6) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if (1 << 5) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if (1 << 4) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if (1 << 3) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if (1 << 2) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if (1 << 1) & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if 1 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])


def update():
	global screen
	fill_screen_map()
	screen.update()