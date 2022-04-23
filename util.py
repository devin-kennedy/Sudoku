import cv2 as cv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import numpy as np


def find_board(w):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://www.{w}.com")
    driver.save_screenshot("fullscreen.png")

    image = cv.imread("fullscreen.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    ret, binary = cv.threshold(gray, 100, 255, cv.THRESH_OTSU)
    inverted_binary = ~binary

    cnts, hierarchy = cv.findContours(inverted_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    board = sorted(cnts, key=cv.contourArea)[-1]

    x, y, w, h = cv.boundingRect(board)
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    roi = image[y:y + h, x:x + w]

    cv.imwrite("screen.png", roi)
    driver.quit()
