import threading
import time

from selenium import webdriver


def single_thread():
    driver = webdriver.Firefox()
    driver.get('http://meeting.baidu.com/index.html#/home')
    driver.find_element_by_id('username').send_keys('v_guoyuqiang')
    driver.find_element_by_id('password').send_keys('Gyq1994719')
    driver.find_element_by_id('emailLogin').click()
    js = 'window.open("http://meeting.baidu.com/index.html#/home");'
    driver.execute_script(js)
    driver.execute_script(js)
    driver.execute_script(js)
    handles = driver.window_handles
    while int(time.strftime('%H', time.localtime(time.time()))) < 10:
        time.sleep(.1)
    for handle in handles:
        driver.switch_to.window(handle)
        driver.execute_script(
            'window.document.getElementsByClassName("el-button btn-box btn-book el-button--default")[0].click();')


def get_url():
    driver = webdriver.Firefox()
    drivers.append(driver)
    driver.get('http://meeting.baidu.com/index.html#/home')
    try:
        driver.find_element_by_id('username').send_keys('v_guoyuqiang')
        driver.find_element_by_id('password').send_keys('Gyq1994719')
        driver.find_element_by_id('emailLogin').click()
        driver.find_elements_by_class_name('el-dialog__headerbtn')[0].click()
    except IndexError:
        pass


def multi_thread():
    for i in range(4):
        threading.Thread(target=get_url).start()
        time.sleep(.5)

    while int(time.strftime('%H', time.localtime(time.time()))) < 10:
        # while int(time.strftime('%M', time.localtime(time.time()))) < 44:
        time.sleep(.15)
    for d in drivers:
        try:
            threading.Thread(target=lambda: d.execute_script(
                'window.document.getElementsByClassName("el-button '
                'btn-box btn-book el-button--default")[0].click();')).start()
        except Exception:
            pass


if __name__ == '__main__':
    drivers = []
    multi_thread()
