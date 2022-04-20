from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyscreenshot
from time import sleep
import cv2 as cv
from imutils import contours
import numpy as np
import pytesseract
from main import Sudoku
from alive_progress import alive_bar
import argparse

argParser = argparse.ArgumentParser()

argParser.add_argument('-s', '--saved', action="store_false", help="Use saved board")

args = argParser.parse_args()

if args.saved:
    # Save the board image
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.websudoku.com")
    sleep(5)
    img = pyscreenshot.grab(bbox=(615, 425, 920, 730))
    img.save("screen.png")
    driver.quit()

# Parse the board image
image = cv.imread("screen.png")
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 57, 5)

cnts = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv.contourArea(c)
    if area < 1000:
        cv.drawContours(thresh, [c], -1, (0, 0, 0), -1)

vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 5))
thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, vertical_kernel, iterations=9)

horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 1))
thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, horizontal_kernel, iterations=4)

invert = 255 - thresh
cnts = cv.findContours(invert, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

sudoku_rows = []
row = []
for (i, c) in enumerate(cnts, 1):
    area = cv.contourArea(c)
    if area < 50000:
        row.append(c)
        if i % 9 == 0:
            (cnts, _) = contours.sort_contours(row, method='left-to-right')
            sudoku_rows.append(cnts)
            row = []

whitelist = [str(i) for i in range(1, 10)]
out = []
with alive_bar(81) as bar:
    for row in sudoku_rows:
        for c in row:
            mask = np.zeros(image.shape, dtype=np.uint8)
            cv.drawContours(mask, [c], -1, (255, 255, 255), -1)
            result = cv.bitwise_and(image, mask)
            result[mask==0] = 255
            config = r'--oem 3 --psm 10'
            num = pytesseract.image_to_string(result, lang="eng", config=config)
            num = num.split("\n")[0]
            if num in whitelist:
                out.append(num)
            else:
                out.append(".")
            bar()

mat = np.array([out])
shaped = mat[0].reshape((9, 9))

# Parse the array into the solver, then solve
board = """"""
for row in shaped:
    for cell in row:
        board += cell
    board += "\n"

parsed_board = Sudoku(board)
parsed_board.solve()

print(parsed_board)