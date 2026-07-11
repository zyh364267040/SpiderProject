# -*- coding = utf-8 -*-
# @Time: 2022/10/19 12:42
import requests
import time
import random
from pyautogui import *


PAUSE = 1


def control():
    # 移动鼠标
    moveTo(825, 46, duration=1)
    # 点击浏览器
    click()

    # 移动鼠标
    moveTo(87, 85, duration=1)
    # 点击刷新按钮
    click()
    time.sleep(5)

    # 移动
    moveTo(394, 628, duration=1)
    # 向下滚动鼠标
    scroll(-300)

    # 移动
    moveTo(396, 720, duration=1)
    # 点击
    click()

    # 移动
    moveTo(662, 706, duration=1)
    # 向下滚动鼠标
    scroll(-300)
    # 右键
    rightClick()
    # 移动
    moveTo(517, 530, duration=1)
    # 点击
    click()

    # 移动
    moveTo(183, 832, duration=1)
    # 点击
    click()
    # 粘贴
    hotkey('command', 'v')
    # 回车
    hotkey('enter')


def main():
    control()


if __name__ == '__main__':
    main()
