import win32gui
import win32ui
import win32con
import win32api
import time
from PIL import Image
from pytesseract import pytesseract

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
	print(time.time()-start)
	# Save the grayscale image as a PNG file
	gray_img.save('screenshot_gray.png')
	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(hwin, hwindc)


def readt_text_from_image():
	path_to_tesseract = r"C:\src\GITHUB\OpenBraille\venv\Tesseract\tesseract.exe"
	image_path = r"screenshot_gray.png"
	  
	# Opening the image & storing it in an image object 
	img = Image.open(image_path) 
	  
	# Providing the tesseract executable 
	# location to pytesseract library 
	pytesseract.tesseract_cmd = path_to_tesseract 
	  
	# Passing the image object to image_to_string() function 
	# This function will extract the text from the image 
	text = pytesseract.image_to_string(img) 
	  
	# Displaying the extracted text 
	print(text[:-1])



start = time.time()
get_system_info(0)
readt_text_from_image()