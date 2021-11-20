import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import math

NB_IMG = 10

def genCoord(bound):
    return random.uniform(-bound, bound)

def launch_driver(driver):
    driver.get("https://www.google.fr/maps")
    print(driver.title)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button").click()
    driver.implicitly_wait(5)

    # cyclic process : go to random location and download first picture.
    for i in range(0,NB_IMG):
        search_bar = driver.find_element(By.XPATH,
                                         "/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div["
                                         "3]/div/input[1]")
        lat = genCoord(70)
        lon = genCoord(155)
        if -13 > lon > -54:
            lon = -lon - 10
        search_bar.send_keys(str(lat) + " " + str(lon))
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            image = driver.find_element(By.XPATH,
                                        "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[1]/div[1]/button/img")
        except:
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://www.google.fr/maps")
            time.sleep(3)
        else:
            src = image.get_attribute("src")
            string_open = "window.open('" + str(src) + "', '_blank');"
            driver.execute_script(string_open)
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element(By.XPATH, "/html/body/img").screenshot("img" + str(i) + ".png")
            print(string_open)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://www.google.fr/maps")
            time.sleep(3)


def generate_AI_sound(driver,j):
    driver.implicitly_wait(5)
    time.sleep(3)
    driver.delete_all_cookies()
    driver.get("https://www.imaginarysoundscape.net/#/upload")
    for i in range(0,j):

        time.sleep(3)
        driver.find_element(By.ID,("input")).send_keys(os.getcwd()+"/img" + str(i) + ".png")
        sound = driver.find_element(By.XPATH, "/html/body/main/audio")
        src = sound.get_attribute("src")
        driver.execute_script("window.open('" + str(src) + "', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        audio = requests.get(src)
        with open("audio" + str(i) + ".mp3", 'wb') as f:
            f.write(audio.content)
        time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.delete_all_cookies()
        driver.get("https://www.imaginarysoundscape.net/#/upload")
        time.sleep(3)


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.getcwd(),"download.prompt_for_download": False}
    chrome_options.add_experimental_option('prefs', prefs)
    # webpage init
    driver = webdriver.Chrome('./chromedriver',options=chrome_options)
    driver.maximize_window()
    #launch_driver(driver)
    generate_AI_sound(driver,NB_IMG)




