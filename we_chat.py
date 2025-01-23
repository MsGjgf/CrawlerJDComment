# _*_ coding : utf-8 _*_
# @Time : 2024/9/15 22:43
# @Author : 哥几个佛
# @File : we_chat
# @Project : CrawlerJDComment
import time

import pyautogui
from wxauto import WeChat

# 获取微信实例
wx = WeChat()

# 获取好友和群组信息
# friends = wx.GetAllFriends()

# print(friends)

who = "网易荒野行动"

wx.ChatWith(who=who, timeout=10)

pyautogui.press('tab')
pyautogui.press('tab')
# pyautogui.press('tab')
# pyautogui.press('tab')
# pyautogui.press('tab')
pyautogui.press('enter')
pyautogui.press('down')
pyautogui.press('down')
pyautogui.press('enter')
time.sleep(2)
megs = wx.GetAllMessage()
for msg in megs:
    print(msg)
print(megs[len(megs)-1])
pyautogui.press('esc')
# for i in range(12):
#     pyautogui.press('tab')
# for i in range(10):
#     pyautogui.press('down')
# pyautogui.press('enter')
# pyautogui.hotkey('ctrl','c')
# wx.SendMsg("AI TEST...",who)

# 读取聊天记录
# who = '三国杀移动版'
# msgs = wx.GetChatMessage(who)

# 发送文本消息
# message = '消息内容'
# wx.SendMsg(message, '接收对象')

# 发送图片消息
# image_path = '图片路径'
# wx.SendImage(image_path, '接收对象')
