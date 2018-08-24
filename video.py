
from tkinter import Tk, Canvas, PhotoImage, mainloop
import Z80, keyboard
import time # for performance monitoring

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

perf_count = time.monotonic()

def elapsed_time():
	global perf_count
	previous = perf_count
	perf_count = time.monotonic()
	return perf_count - previous

def refreshWholeScreen():
	for i in xrange(firstAttr):
		next[i] = i - 1
		last[i] = (~mem[i + 16384]) & 0xff
	for i in range(firstAttr, lastAttr):
		next[i] = -1
		last[i] = mem[i + 16384]
	first = firstAttr - 1;
	FIRST = -1

# TODO: handle and bind window close event
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
	screen.update()
	return

def rgb_to_string(rgb):
	# tuple (r, g, b) to '#rrggbb'
	colour = '#{0:02X}{1:02X}{2:02X}'.format(*rgb)
	return colour

pixel_buffer = [['#999900' for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

def set_at(coords, colour):
	colour_string = rgb_to_string(colour)
	pixel_buffer[coords[1]][coords[0]] = colour_string

BIT7 = 0x80
BIT6 = 0x40
BIT5 = 0x20
BIT4 = 0x10
BIT3 = 0x08
BIT2 = 0x04
BIT1 = 0x02
BIT0 = 0x01

def fill_screen_map():
	global screen, Z80
	mem = Z80.mem
	for addr in range(buf_start, buf_end + 1):
		y = ((addr & 0x00e0) >> 2) + ((addr & 0x0700) >> 8) + ((addr & 0x1800) >> 5)
		attr_x = (addr & 0x1f)
		sx = attr_x << 3

		attr = mem[22528 + attr_x | ((y >> 3) << 5)]
		bright = ((attr >> 3) & 0x08)
		ink = (attr & 0x07) | bright
		pap = ((attr >> 3) & 0x07) | bright

		byte = mem[addr]

		if BIT7 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT6 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT5 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT4 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT3 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT2 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT1 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])
		sx += 1
		if BIT0 & byte:
			color = ink
		else:
			color = pap
		set_at((sx, y), brightColors[color])

	screen_string = " ".join(["{" + " ".join([pixel for pixel in row]) + "}" for row in pixel_buffer])
	screen_img.put(screen_string, to=(0, 0)) # , SCREEN_WIDTH, SCREEN_HEIGHT))

def update(cpu_freq):
	global screen
	fill_screen_map()
	video_freq = 1.0 / elapsed_time()
	screen.title("PyZX [%3.1fMhz / %1.1fHz]" % (cpu_freq, video_freq))
	screen.update()
