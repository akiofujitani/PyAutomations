'''
If still relevant for someone on windows:

In my opinion the issue is, that the current version of pyscreeze utilizing ImageGrab (Pillow) on windows only uses single-screen grab.

A dirty quick fix in pyscreeze could be:

enable all_screen grabbing:

In file: pyscreeze/__init__.py, function: def _screenshot_win32(imageFilename=None, region=None):
change im = ImageGrab.grab() to im = ImageGrab.grab(all_screens= True)

handle new introduced negative coordinates due to multiple monitor:
In file: pyscreeze/__init__.py, function: def locateOnScreen(image, minSearchTime=0, **kwargs): behind retVal = locate(image, screenshotIm, **kwargs) add


'''

if retVal and sys.platform == 'win32':
    # get the lowest x and y coordinate of the monitor setup
    monitors = win32api.EnumDisplayMonitors()
    x_min = min([mon[2][0] for mon in monitors])
    y_min = min([mon[2][1] for mon in monitors])
    # add negative offset due to multi monitor
    retVal = Box(left=retVal[0] + x_min, top=retVal[1] + y_min, width=retVal[2], height=retVal[3])

# don't forget to add the import win32api
# In file: pyscreeze/__init__.py,:

if sys.platform == 'win32': # TODO - Pillow now supports ImageGrab on macOS.
    import win32api # used for multi-monitor fix
    from PIL import ImageGrab




from platform import python_branch
import PyPDF2
from mss import mss


'''
PIP upgrade all

'''

#  pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}

'''
PIP install list

'''
# pip install pywin32
# pip install pyautogui
# pip install screeninfo
# pip install PyPDF2
# pip install mss
# pip install pytesseract
# pip install pdf2image
# pip install opencv-python
# pip install auto-py-to-exe

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlibs
# pip install pygsheets