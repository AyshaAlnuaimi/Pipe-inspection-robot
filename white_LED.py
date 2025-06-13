
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 16, brightness=0.5, auto_write=True, pixel_order=neopixel.GRBW)

pixels.fill((255, 255, 255, 255))  # Full white (RGBW)

