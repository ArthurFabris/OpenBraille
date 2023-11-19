import win32gui
import win32ui
import win32con
import win32api
import time
from PIL import Image

def get_system_info(MNTRSLCT):

	displays = win32api.EnumDisplayMonitors()
	display = displays[MNTRSLCT]

	WIDTH = displays[MNTRSLCT][2][2] - displays[MNTRSLCT][2][0]
	HEIGHT = displays[MNTRSLCT][2][3] - displays[MNTRSLCT][2][1]

	offset_x = displays[MNTRSLCT][2][0]
	offset_y = displays[MNTRSLCT][2][1]

	hwin = win32gui.GetDesktopWindow()
	hwindc = win32gui.GetWindowDC(hwin)
	srcdc = win32ui.CreateDCFromHandle(hwindc) # source of image 
	memdc = srcdc.CreateCompatibleDC() # memory screenshot for bitmap

	bmp = win32ui.CreateBitmap()
	bmp.CreateCompatibleBitmap(srcdc, WIDTH, HEIGHT)

	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (WIDTH, HEIGHT), srcdc, (offset_x, offset_y), win32con.SRCCOPY)

	bmpinfo = bmp.GetInfo()
	bmpstr = bmp.GetBitmapBits(True)
	img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

	# Convert the RGB image to grayscale
	gray_img = img.convert('L')

	# Save the grayscale image as a PNG file
	gray_img.save('screenshot_gray.png')
	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(hwin, hwindc)



start = time.time()
get_system_info(1)
print(time.time()-start)