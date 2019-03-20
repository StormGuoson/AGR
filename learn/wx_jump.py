from selenium import webdriver

btn_commit = 'el-button btn-box btn-book el-button--default'

username = 'v_guoyuqiang'
password = 'Gyq1994719'

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('http://meeting.baidu.com/index.html#/home')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('emailLogin').click()
