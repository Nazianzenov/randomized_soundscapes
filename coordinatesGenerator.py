import random
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
import time



def genCoord(bound):
    return random.uniform(-bound,bound)

if __name__ == '__main__':

    # webpage init
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.google.fr/maps")
    print(driver.title)
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button").click()
    driver.implicitly_wait(5)
    for i in range(0,20):
        search_bar = driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div[3]/div/input[1]")
        lat = genCoord(70)
        lon = genCoord(180)
        search_bar.send_keys(str(lat) + " " + str(lon))
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            image = driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[1]/div[1]/button/img")
        except:
            driver.switch_to_window(driver.window_handles[0])
            driver.get("https://www.google.fr/maps")
            time.sleep(3)
        else:
            src = image.get_attribute("src")
            string_open = "window.open('"+str(src)+ "', '_blank');"
            driver.execute_script(string_open)
            driver.switch_to_window(driver.window_handles[min(i+1,len(driver.window_handles)-1)])
            driver.find_element_by_xpath("/html/body/img").screenshot("img" + str(i) + ".png")
            i+=1
            print(string_open)
            driver.switch_to_window(driver.window_handles[0])
            driver.get("https://www.google.fr/maps")
            time.sleep(3)

