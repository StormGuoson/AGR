from appium import webdriver

if __name__ == '__main__':
    caps = {
        'platformName': 'Android',
        'platformVersion': '4.4.4',
        'deviceName': '192.168.56.101:5555',
        'appPackage': 'com.android.calculator2',
        'appActivity': 'com.android.calculator2.Calculator'
    }
    d = webdriver.Remote(desired_capabilities=caps)
    d.find_element_by_id('digit3').click()
    d.find_element_by_id('mul').click()
    d.find_element_by_id('digit8').click()
    d.find_element_by_id('equal').click()
    res = d.find_element_by_class_name('android.widget.EditText').id
    print(res)
