import jieba
import control
import data
import pyscreenshot as ImageGrab
import numpy as np
import pyautogui
import pyperclip
import time
import pickle


def find_all(string, sub):
    start = 0
    pos = []
    while True:
        start = string.find(sub, start)
        if start == -1:
            return pos
        pos.append(start)
        start += len(sub)


# with open('data.pickle', 'wb') as f:
#     pickle.dump(data.list_qa, f)
with open('data.pickle', 'rb') as f:
    list_qa = pickle.load(f)
    print(list_qa)
friend = input('请输入你的聊天托管对象')
control.goto_wechat(friend)
control.send_sent('您好，我是聊天机器人，接下来的对话由我接管')
while True:
    # 等待用户回复
    q_list = control.wait_message()
    # 进入训练
    if control.go_to_teach(q_list):
        control.teach_mode()
        with open('data.pickle', 'rb') as f:
            list_qa = pickle.load(f)
            print(list_qa)
    # 退出聊天
    if control.break_chat(q_list):
        break
    # 剪切语句,处理语句v
    control.deal_with_message(q_list, list_qa)


