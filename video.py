
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

def set_pixel(coords, colour):
	colour_string = rgb_to_string(colour)
	offset = coords[0]+coords[1]*SCREEN_WIDTH
	pixel_buffer[coords[1]][coords[0]] = colour_string

def set_at(coords, colour):
	# global screen_img
	# colour_string = rgb_to_string(colour)
	# screen_img.put(colour_string, coords)
	colour_string = rgb_to_string(colour)
	pixel_buffer[coords[1]][coords[0]] = colour_string

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

	screen_string = " ".join(["{" + " ".join([pixel for pixel in row]) + "}" for row in pixel_buffer])
	screen_img.put(screen_string, to=(0, 0)) # , SCREEN_WIDTH, SCREEN_HEIGHT))

def update(ticks):
	global screen
	# start = time.monotonic()
	fill_screen_map()
	# update_time = time.monotonic() - start
	cpu_rate = ticks / 1.0e6
	video_rate = 1.0 / elapsed_time()
	screen.title("PyZX [%3.1fMhz/ %1.1fHz]" % (cpu_rate, video_rate))
	screen.update()
