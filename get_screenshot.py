from pytesseract import pytesseract

import windowmanagerclass as WMC


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
def get_window(index):
    WM = WMC.WindowManager() # cria objeto
    window_info_dict = WM.listall()

    # Now window_info_dict contains a dictionary with indices as keys and information about each open window as values
    if debug == True:

	    for index, window_info in window_info_dict.items():
	        print(f"Index: {index}: {window_info}")

    selected_window = WM.select_window(index)

    return selected_window

def main()

	get_window(1)
  

if __name__ == '__main__':
	main()