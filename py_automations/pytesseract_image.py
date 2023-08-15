import cv2
import pytesseract
from ntpath import join
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'c:/Program Files/Tesseract-OCR/tesseract'


def mark_region(image_path):
    
    im = cv2.imread(image_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (2200, y+h)])

        if y >= 2400 and x<= 2000:
            image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])

    cv2.imshow('image', im)
    return image, line_items_coordinates


def convert_grayscale(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def image_blur(image, param):
    image = cv2.medianBlur(image, param)
    return image


def threshould(image):
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return image


def image_boxes(image, image_file):
    h, w, c = image.shape

    boxes = pytesseract.image_to_boxes(image)

    for b in boxes.splitlines():
        b = b.split(' ')
        image =cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow(image_file, image)
    cv2.destroyAllWindows()
    return image


def isInt(str_value):
    try:
        int(str_value)
        return True
    except:
        return False


def returnOsNumber(os_values):
    for line in os_values:
        if 'ORDEM DE SERVIÇO' in line:
            values_splitted = line.split(' ')
            os_number_temp = len(values_splitted) - 1
            temp_value = ''
            for string_value in values_splitted:
                if isInt(string_value):
                    temp_value = temp_value + string_value
                print(temp_value)
            if len(temp_value) == 4:
                return temp_value
    return 'Not found'


def readPDFContents(pdf_file):
    pdf_converted = convert_from_path(pdf_file, 300)
    for pdf in pdf_converted:
        return pytesseract.image_to_string(pdf, lang='por').split('\n')


def get_os_number(path, file_name):
    pdfFile = join(path, file_name)
    pdfConverted = convert_from_path(pdfFile, 300)
    for pdf in pdfConverted:
        os_values = pytesseract.image_to_string(pdf, lang='por')
    return returnOsNumber(os_values.split('\n'))


# path = r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\Maintenance_Auto'
# pdf = '4899.pdf'

# pdfFile = join(path, pdf)
# pdfConverted = convert_from_path(pdfFile, 300)

# for pdf in pdfConverted:
#     os_values = pytesseract.image_to_string(pdf, lang='por')
#     returnOsNumber(os_values.split('\n'))







