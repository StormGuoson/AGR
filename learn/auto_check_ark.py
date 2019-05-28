import time

import uiautomator2 as at


class Main(object):
    def __init__(self):
        self.d = at.connect_usb()

    def go_home(self):
        self.d.click(0.248, 0.058)
        time.sleep(.3)
        self.d.click(0.118, 0.384)
        time.sleep(1)

    def action(self):
        while True:
            self.d.click(0.841, 0.888)
            time.sleep(2)


if __name__ == '__main__':
    m = Main()
    m.action()
