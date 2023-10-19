import pyautogui
import time
import pyperclip
import pyscreenshot as ImageGrab
import numpy as np
import jieba
import pickle
import re


def find_cn(q_list, find):
    # 定义一个待查找的字符串
    q_list = q_list.encode('utf-8').decode('utf-8')
    # 定义一个正则表达式模式
    pattern = u''+find+''
    # 在字符串中搜索第一个匹配的位置
    match = re.search(pattern, q_list)
    # 输出匹配的位置
    if match:
        start = match.start()
        end = match.end()
        return start, end
    else:
        return 0


def find_all(string, sub):
    start = 0
    pos = []
    while True:
        start = string.find(sub, start)
        if start == -1:
            return pos
        pos.append(start)
        start += len(sub)


def add_to_list(question, answer):
    with open('data.pickle', 'rb') as f:
        list_qa = pickle.load(f)
        print(list_qa)
    list_qa[question] = answer
    with open('data.pickle', 'wb') as f:
        pickle.dump(list_qa, f)


def get_message():
    pyautogui.click(650, 550, button='right')  # 单击右键
    pyautogui.keyDown('command')
    pyautogui.keyDown('c')
    time.sleep(1)
    pyautogui.keyUp('c')
    pyautogui.keyUp('command')
    return pyperclip.paste()


def goto_wechat(friend):
    pyautogui.keyDown('command')
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('w')
    time.sleep(1)
    pyautogui.keyUp('w')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('command')
    # 搜索好友
    time.sleep(1)
    pyautogui.keyDown('command')
    pyautogui.keyDown('f')
    time.sleep(1)
    pyautogui.keyUp('f')
    pyautogui.keyUp('command')
    # 复制好友昵称到粘贴板
    pyperclip.copy(friend)
    # 模拟键盘 ctrl + v 粘贴
    pyautogui.keyDown('command')
    pyautogui.keyDown('v')
    time.sleep(1)
    pyautogui.keyUp('v')
    pyautogui.keyUp('command')
    pyautogui.press('enter')


def send_sent(sent):
    pyperclip.copy(sent)
    pyautogui.keyDown('command')
    pyautogui.keyDown('v')
    time.sleep(1)
    pyautogui.keyUp('v')
    pyautogui.keyUp('command')
    pyautogui.press('enter')


def send_message(message):
    if len(message) == 0:
        print('我不太理解你的意思')
        send_sent("我不太理解你的意思,可以输入'进入训练'，对我进行训练")
    else:
        for i in range(len(message)):
            print(f'{message[i]}')
            send_sent(f'{message[i]}')


def wait_message():
    while True:
        im = ImageGrab.grab(bbox=(560, 520, 600, 560))  # X1,Y1,X2,Y2
        if np.mean(im) != 246:
            q_list = get_message()
            return q_list


def break_chat(q_list):
    if q_list == '退出聊天':
        send_sent('好的，已退出自动聊天')
        return 1
    else:
        return 0


def break_teach(q_list):
    if q_list == '退出训练':
        send_sent('好的，已退出自动训练')
        return 1
    else:
        return 0


def deal_with_message(q_list, list_qa):
    q_str = []
    a_str = []
    q_list = jieba.cut(q_list)
    q_list = '/'.join(q_list)
    print(q_list)
    a = find_all(q_list, '/')
    if len(a) == 0:
        q_str.append(q_list)
    else:
        q_str.append(q_list[0:a[0]])
        for i in range(len(a)):
            if i == len(a) - 1:
                q_str.append(q_list[a[i] + 1:len(q_list)])
            else:
                q_str.append(q_list[a[i] + 1:a[i + 1]])
    a_str = organize_la(q_str, list_qa)
    send_message(a_str)


def deal_with_message_teach(q_list):
    if find_cn(q_list, '如果我说') == 0:
        send_sent('请注意格式')
        return 0
    else:
        temp, question_start = find_cn(q_list, '如果我说')
        question_end, answer_start = find_cn(q_list, '你应该回复')
        answer_end = len(q_list)
        return q_list[question_start:question_end-1], q_list[answer_start:answer_end]


def organize_la(q_str, list_qa):
    a_str = []
    for i in range(len(q_str)):
        if list_qa.get(q_str[i], 0):
            a_str.append(list_qa.get(q_str[i], 0))
    return a_str


def go_to_teach(q_list):
    if q_list == '进入训练':
        return 1
    else:
        return 0


def teach_mode():
    question = []
    answer = []
    send_sent("正在进入指导模式，请严格输入语句'如果我说什么，你应该回复什么',目前只支持词语的输入，请勿输入语句，回复可以是语句")
    while True:
        wait_message()
        q_list = get_message()
        if break_teach(q_list):
            break
        question, answer = deal_with_message_teach(q_list)
        add_to_list(question, answer)
        send_sent(f'当你说{question}时我会回复你{answer}')
        send_sent("如果你要继续指导，请继续输入指导语句，如果想要退出请输入严格输入'退出训练'")
