import win32api
import win32con
import win32gui
import win32ui
import psutil
from PIL import Image, ImageDraw
import win32process


class WindowManager:
    def __init__(self, monitor_select):
        self.WIDTH = 0
        self.HEIGHT = 0
        self.offset_x = 0
        self.offset_y = 0

    def get_system_info(self):
        displays = win32api.EnumDisplayMonitors()
        display = displays[self.monitor_select]

        self.WIDTH = display[2][2] - display[2][0]
        self.HEIGHT = display[2][3] - display[2][1]

        self.offset_x = display[2][0]
        self.offset_y = display[2][1]

        return display, self.offset_x, self.offset_y

    def get_open_windows(self):
        def window_enum_handler(hwnd, result_dict):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                rect = win32gui.GetWindowRect(hwnd)
                x, y, width, height = rect
                z_index = self.get_z_index(hwnd)
                monitor_info = self.get_monitor_info(rect)
                process_path = self.get_process_path(hwnd)
                result_dict[len(result_dict)] = {
                    'window_title': win32gui.GetWindowText(hwnd),
                    'z_index': z_index,
                    'position': (x - self.offset_x, y - self.offset_y),
                    'size': (width - (x - self.offset_x), height - (y - self.offset_y)),
                    'monitor': monitor_info,
                    'path': process_path
                }

        open_windows = {}
        win32gui.EnumWindows(window_enum_handler, open_windows)
        return open_windows

    def get_z_index(self, hwnd):
        z_index = 0
        prev = win32gui.GetWindow(hwnd, win32con.GW_HWNDPREV)
        while prev:
            z_index += 1
            prev = win32gui.GetWindow(prev, win32con.GW_HWNDPREV)
        return z_index

    def get_monitor_info(self, rect):
        monitor = win32api.MonitorFromRect(rect, win32con.MONITOR_DEFAULTTONEAREST)
        monitor_info = win32api.GetMonitorInfo(monitor)
        return monitor_info['Device']

    def get_process_path(self, hwnd):
        try:
            pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid[1])
            return process.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    def select_window(self, index):
        if index in self.listall():
            window_info = self.listall()[index]

            hwnd = win32gui.FindWindow(None, window_info['window_title'])

            if hwnd:
                rect = win32gui.GetWindowRect(hwnd)
                image = self.capture_window(hwnd, rect)
                return image

    def capture_window(self, hwnd, rect):
        # Capture the content of the window
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
        
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        # Convert the RGB image to grayscale
        gray_img = img.convert('L')
        cDC.DeleteDC()
        dcObj.DeleteDC()

        return gray_img

    

    def listall(self):
        display, offset_x, offset_y = self.get_system_info()

        open_windows = self.get_open_windows()

        window_dict = {}
        for index, window_info in open_windows.items():
            # Adjust the position based on the monitor offset
            adjusted_x = window_info['position'][0]
            adjusted_y = window_info['position'][1]

            # Calculate the size using the position
            size_of_window = (window_info['size'][0], window_info['size'][1])

            window_dict[index] = window_info

        return window_dict

if __name__ == '__main__':
    # Assuming you have already called get_system_info with the appropriate MNTRSLCT value
    monitor = 1
    WM = WindowManager(monitor-1) # cria objeto
    window_info_dict = WM.listall()

    # Now window_info_dict contains a dictionary with indices as keys and information about each open window as values
    print(window_info_dict)
    print(type(window_info_dict))
    for index, window_info in window_info_dict.items():
        print(f"Index: {index}")
        print(window_info)

    selected_index = 1
    save_path = f"captured_window_{selected_index}.png"
    selected_window = WM.select_window(selected_index)

    selected_window.save(save_path)

