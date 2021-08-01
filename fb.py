import os
import time

import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

print("please enter facebook link here")
print("EX : 'https://www.facebook.com/XXX.xxxxxxx12_123/'")

link = input('Link : ')
name = input('Name : ')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

prefs = {"profile.default_content_setting_values.notification": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path='/bin/chromedriver', chrome_options=chrome_options)

# open the webpage
driver.get("http://www.facebook.com")

# target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

# enter username and password
username.clear()
username.send_keys("Your email")
password.clear()
password.send_keys("Your password")

# target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
time.sleep(10)
images = []
hrefs = None

def filter_picture(images, img_src):
    if "emoji" in img_src:
        pass
    elif ".png" in img_src:
        pass
    elif ".jpg" in img_src and img_src not in images:
        print(img_src)
        images.append(img_src)
    return images


for i in ['photos_of', 'photos_by']:
    print("--------------------Starting %s--------------------" % i)

    driver.get(link + i)
    time.sleep(5)

    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    n_scrolls = 20
    for j in range(1, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        anchors = []
        anchors = driver.find_elements_by_css_selector("[href*='https://www.facebook.com/photo.php?']")
    hrefs = [a.get_attribute('href') for a in anchors]
    if hrefs:
        for a in hrefs:
            driver.get(a)
            time.sleep(2)
            img_list = driver.find_elements_by_tag_name("img")
            for image in img_list:
                img = image.get_attribute('src')
                images = filter_picture(images, img)

path = name

try:
    os.mkdir(path)
except:
    pass

counter = 0
for image in images:
    save_as = os.path.join(path, str(counter) + '.jpg')
    wget.download(image, save_as)
    counter += 1
