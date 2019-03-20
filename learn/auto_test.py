import colorsys
import os
import random
import sys
import threading
import time

from PIL import Image as img

import uiautomator2 as auto
from past.builtins import raw_input

start = '1'


def start_diangan():
    while True:
        diangan_move()


def diangan_fix_screenshot():
    shot = d.screenshot()
    # shot = img.open('diangan.jpg')
    (x, y) = shot.size
    box = (x / 2 - 100, y / 3, x / 2 + 100, y / 2)
    reg = shot.crop(box)
    # reg.save('fix.jpg')
    return reg


def diangan_move():
    im = diangan_fix_screenshot()
    y = im.size[1]
    # 右跳
    for i in range(10, 70):
        rgb = im.getpixel((50, i))
        if rgb[0] in range(40, 50):
            # if rgb == (45, 47, 86):
            d.click(0.75, 0.867)
            print(i)
            print('jump right')
            return
    # 左跳
    for i in range(10, 70):
        rgb = im.getpixel((150, i))
        if rgb[0] in range(40, 50):
            # if rgb == (45, 47, 85):
            d.click(0.273, 0.863)
            print(i)
            print('jump left')
            return
    print('free jump')
    d.click(0.273, 0.863)


def start_hudui():
    p0 = [0.273, 0.863]  # left
    p1 = [0.75, 0.867]  # right
    res = raw_input('左右模式')
    if res == 'r':
        pos = p1
    else:
        pos = p0
    threading.Thread(target=hudui_signal).start()
    for t in range(10):
        threading.Thread(target=hudui_tap, args=(pos,)).start()


def hudui_signal():
    global start
    while True:
        print('waiting')
        start = raw_input()


def hudui_tap(pos):
    while True:
        if start == '1':
            d.click(pos[0], pos[1])


def jump_fix_img():
    shot = d.screenshot()
    (x, y) = shot.size
    box = (0, y / 3, x, y)
    reg = shot.crop(box)
    reg.save('fix.jpg')
    return reg


def jump_swipe():
    find_top = False
    find_human = False
    top_xy = [-1, -1]
    final_color = [-1, -1, -1]
    human_point = [-1, -1]
    img = jump_fix_img()
    (width, height) = img.size
    # 找小人坐标
    for y in range(height - 1, -1, -1):
        if not find_human:
            for x in range(width - 1):
                rgb = img.getpixel((x, y))
                if rgb[0] in range(77, 82) and rgb[1] in range(60, 65) and rgb[2] in range(104, 108):
                    human_point[0] = x
                    human_point[1] = y
                    find_human = True
                    break
        else:
            break
    # 找最高点坐标
    for y in range(1, height):
        if find_top:
            break
        for x in range(1, width):
            if x in range(human_point[0] - 30, human_point[0] + 30):
                continue
            rgb = img.getpixel((x, y))
            r, g, b = rgb[0], rgb[1], rgb[2]
            hsv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h, s = hsv[0], hsv[1]
            rgb = img.getpixel((x, y - 1))
            r1, g1, b1 = rgb[0], rgb[1], rgb[2]
            hsv1 = colorsys.rgb_to_hsv(r1 / 255.0, g1 / 255.0, b1 / 255.0)
            fh, fs = hsv1[0], hsv1[1]
            if abs(h - fh) > 0.1 or abs(s - fs) > 0.1:
                # if abs(x - human_point[0]) < 50:
                #     continue
                top_xy[0], top_xy[1] = x, y
                final_color[0], final_color[1], final_color[2] = r, g, b
                find_top = True
                break

    if not find_human or top_xy[0] == -1:
        print('没找到小人！！！已停止')
        sys.exit(0)
    distance = abs(top_xy[0] - human_point[0])
    # distance = abs(lg)
    # print('平台坐标 %s' % jump_point)
    duration = distance / 3000.0
    print('小人坐标 %s' % human_point)
    print('水平距离 %s' % distance)
    print('平台颜色 %s' % final_color)
    print('')

    points = [[random.randint(400, 800), random.randint(400, 800)],
              [random.randint(400, 800), random.randint(400, 800)],
              [random.randint(400, 800), random.randint(400, 800)],
              [random.randint(400, 800), random.randint(400, 800)]]
    # if distance in range(151, 200):
    #     d.swipe_points(points, duration * 0.75)
    # elif distance in range(201, 250):
    #     d.swipe_points(points, duration * 0.7)
    # elif distance in range(251, 300):
    #     d.swipe_points(points, duration * 0.65)
    # elif distance in range(401, 450):
    #     d.swipe_points(points, duration * 0.55)
    # elif distance in range(451, 470):
    #     d.swipe_points(points, duration * 0.5)
    # elif distance in range(471, 500):
    #     d.swipe_points(points, duration * 0.45)

    d.swipe_points(points, duration * .55)
    # if distance < 350:
    #     os.popen('adb shell input swipe %s %s %s %s %s' % (
    #         str(random.randint(400, 800)), str(random.randint(400, 800)), str(random.randint(400, 800)),
    #         str(random.randint(400, 800)), str(int(distance * 1.63))))
    # elif distance < 450:
    #     os.popen('adb shell input swipe %s %s %s %s %s' % (
    #         str(random.randint(400, 800)), str(random.randint(400, 800)), str(random.randint(400, 800)),
    #         str(random.randint(400, 800)), str(int(distance * 1.61))))
    # elif distance < 550:
    #     os.popen('adb shell input swipe %s %s %s %s %s' % (
    #         str(random.randint(400, 800)), str(random.randint(400, 800)), str(random.randint(400, 800)),
    #         str(random.randint(400, 800)), str(int(distance * 1.59))))
    # else:
    #     os.popen('adb shell input swipe %s %s %s %s %s' % (
    #         str(random.randint(400, 800)), str(random.randint(400, 800)), str(random.randint(400, 800)),
    #         str(random.randint(400, 800)), str(int(distance * 1.57))))


if __name__ == '__main__':
    d = auto.connect('85608d6e')
    # d(resourceId='android:id/text2').click()
    # dev(resourceId='com.baidu.speech.demo.skyworth:id/btn_back').click()
    # d.app_start('com.baidu.speech.demo.skyworth', 'com.baidu.speech.demo.skyworth.act.Activity01ASR')
    # d.press('back')
    # start_hudui()
    # start_diangan()
    # points = []
    # d.swipe_points()
    while True:
        jump_swipe()
        time.sleep(2)
