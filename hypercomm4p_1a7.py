#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.7),
    on 五月 04, 2019, at 00:55
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""


from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import numpy as np 
import os  # handy system and path functions
import sys  # to get file system encoding
import time
import pandas as pd
import socket
from socket import AF_INET, SOCK_DGRAM
import json
import struct, math, time, datetime
from datetime import datetime
from os.path import expanduser
import select


payoff_nums = ['8', '2', '4', '6', '4', '6', '2', '8']
choice_nums = [(2, 8), (4, 6), (6, 4), (8, 6)]
right_dir = "RIGHT"
left_dir = "LEFT"
my_dir = ""

# Read config file
config_file='config_comm.json'
try:
    with open(config_file) as json_file:
        config = json.load(json_file)
except:
    print('[Error] Cannot read the config file: ' + config_file)
    sys.exit(0)
PracticeFlag    = config['PracticeFlag']
clientID        = config['clientID']
scannerID       = config['scannerID']
remote_serverID = config['remote_serverID']
runset_file     = config['runset_file']
FullScreenFlag  = config['FullScreenFlag']
FastModeFlag    = config['FastModeFlag']
SendTriggerTimeFlag = config['SendTriggerTimeFlag']
if SendTriggerTimeFlag == True:
    SendTriggerTime=1
else:
    SendTriggerTime=0

scanners       = config['scanners']
scannerports   = config['scannerports']
remote_servers = config['remote_servers']
ntpservers     = config['ntpservers']

scannerport = int(scannerports[scannerID])
ntpserver = ntpservers[scannerID]

screenSize = [1024, 768] if (FullScreenFlag == True) else [480, 360]
#screenSize = [1024, 768] if (FullScreenFlag == True) else [640, 480]

# define remote server
remote_server = remote_servers[remote_serverID]
#remote_server = remote_servers['NCKU8'] 
#remote_server = remote_servers['local']    # for standalone
#print(clientID, scannerID, scannerport, ntpserver, remote_server)
#sys.exit(1)

######################    
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# setting clock
ExperimentClock = core.Clock()

# setting routines time
if FastModeFlag==False:
    showIDScreenTime = 4.000000
    showPartnerScreenTime = 2
    Fixation4sTime = 4.000000
    Fixation3sTime = 3.000000
    PayoffScreenTime = 5.000000
    DEC1Time = 6.000000
    TRA1Time = 2.000000
    FB1Time = 2.000000
    IStageItime = 1.000000
    DEC2Time = 3.000000
    TRA2Time = 2.000000
    FB2Time = 2.000000
    ITITime = 2.000000
    EndingRunTime = 4.000000
else:
    showIDScreenTime = 1.000000
    showPartnerScreenTime = 1
    Fixation4sTime = 2.000000
    Fixation3sTime = 1.500000
    PayoffScreenTime = 2.500000
    DEC1Time = 3.000000
    TRA1Time = 1.000000
    FB1Time = 1.000000
    IStageItime = 0.500000
    DEC2Time = 1.500000
    TRA2Time = 1.000000
    FB2Time = 1.000000
    ITITime = 1.000000
    EndingRunTime = 2.000000

# record missing times
missedCountList = [0, 0, 0, 0]
missedCount = 0 # practice mode

# setting run
runNum = 6
runCount = 0

# setting total reward
totalReward = 0

# choice list
choiceList = ['X', 'Y']

# default first time has message_ret_data2
message_ret_data2 = '222'

# determine each blocks 's payoff 
payoffDict = { 'C1': np.array([[(1,6),(0,0)], [(0,0),(6,1)]]), 'C2': np.array([[(2,5),(0,0)], [(0,0),(5,2)]]),
               'C3': np.array([[(3,4),(0,0)], [(0,0),(4,3)]]) }

# group members' dictionary
groupMember_dict = {0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D'}

# A:light blue, B:green, C:orange, D:pink 
playerColor_dict = {'A': [-1.000,0.004,1.000], 'B': [-1.000,0.004,-1.000], 'C': [0.984,0.294,-0.984], 'D': [1.000,-0.686,0.161]}

# read prepare run's data
df = pd.read_csv(runset_file)


######################################################################
# Function Definitions
def getNTPTime(host = ntpserver):
    port = 123
    buf = 1024
    address = (host,port)
    msg = '\x1b' + 47 * '\0'

    # connect to server
    exit_flag=0
    while exit_flag==0:
        try:
            client = socket.socket( AF_INET, SOCK_DGRAM)
            client.settimeout(1)
            client.sendto(msg.encode(), address)
            msg, address = client.recvfrom( buf )
            exit_flag=1
        except:
            print ("Error: Couldn't connect to NTP server: " + ntpserver )
            raise 
    # End of while
    t1 = struct.unpack( "!12I", msg )[10] 
    t2 = float(struct.unpack( "!12I", msg )[11]) / 2**32    
    TIME1970 = 2208988800 # reference time (in seconds since 1900-01-01 00:00:00)
    t = t1 + t2 - TIME1970
    return t
    #return time.ctime(t).replace("  "," ")
    #return time.strftime("%H:%M:%S.%f", time.localtime(t))

def time_string(t):
    t1 = math.floor(t)
    t2 = int(round((t - t1)*1000,0))
    ts = '%s.%s' % (time.strftime("%H:%M:%S", time.localtime(t1)), t2)
    #ts = "{}.{}".format(time.strftime("%H:%M:%S", time.localtime(t1)), t2)
    return ts

# WinSize [1920,1080] to [1024,768]
def to_1024_768_2D(x1,y1):
    if int(win.size[0]) == 1024:
        x2 = x1*1.3*(1024/1920)
        y2 = y1*(768/1080)
        a = (x2,y2)
    else:
        a = (x1,y1)
    return a
def to_1024_768_1D(y):
    if int(win.size[0]) == 1024:
        y2 = y*(768/1080)
    else:
        y2 = y
    return y2
def stimuli_setting(stage, role, partner, counterbalance, **feedback):   # feedbck['role_idx', 'partner_idx','RunCommunication'] 
    user_name_table = {0:'pa', 1:'pb', 2:'pc', 3:'pd', 4:'pe', 5:'pf', 6:'pg', 7:'ph'}
    user_name = []
    img_PayoffMatrix.setImage('../new_images/Decision_ExcPos0_1.png')

    # DEC
    # textYou.setText('Player '+ str(role.capitalize()))
    # playerColor = playerColor_dict[str(role.capitalize())]
    #textYou.color = playerColor
    #textX.color = playerColor
    #textY.color = playerColor
    # textPosList = [[0.035, 0.2], [0.38, 0.2]]
    # textX.setPos(to_1024_768_2D(textPosList[0-counterbalance][0], textPosList[0-counterbalance][1]))
    # textY.setPos(to_1024_768_2D(textPosList[1-counterbalance][0], textPosList[1-counterbalance][1]))
    # textPartner.setText('Player '+str(partner))
    # textPartner.color = playerColor_dict[str(partner)]

    field_choice_pair = []
    # FB
    if len(feedback) != 0:
        data_list_list = [data_clients_list, data2_clients_list]
        computer_idx = 4
        for c in computer_choice:
            s1_choice = int(c[0]) - 1
            s2_choice = int(c[1]) - 1
            data_list_list[stage-1].append({user_name_table[computer_idx]:{"s1":choice_nums[s1_choice], "s2":choice_nums[s2_choice]}})
            computer_idx += 1
        for pair in field_pair_list:
            field = int(pair[0])
            user = user_name_table[pair[1]]
            choice = data_list_list[stage-1][pair[1]][user]
            field_choice_pair.append({field:choice})

        # selfFramePosList = [[0.035, -0.029], [0.38, -0.029]]
        # oppoFramePosList = [[0.034, -0.028], [0.034, -0.277]]

        # myKeyResponse = int(data_list_list[stage-1][feedback['role_idx']]['respondkeyp'+role])
        # oppoKeyResponse = int(data_list_list[stage-1][feedback['partner_idx']]['respondkeyp'+partner.lower()])

        # img_selfFrame.setImage(image_frame_list[feedback['role_idx']+4*(stage-1)])
        # img_oppoFrame.setImage(image_frame_list[8+feedback['partner_idx']+4*(stage-1)])
        # img_selfFrame.setPos(to_1024_768_2D(selfFramePosList[myKeyResponse-1][0], selfFramePosList[myKeyResponse-1][1])) 
        # if RunCommunication==0, oppo change pos
        # img_oppoFrame.setPos(to_1024_768_2D(oppoFramePosList[oppoKeyResponse-1+(feedback['RunCommunication']-1)][0], oppoFramePosList[oppoKeyResponse-1+(feedback['RunCommunication']-1)][1]))
        return field_choice_pair

def assign_reward(data2_clients_list, role_idx, partner_idx, role, partner, counterbalance):
    oppoKeyResponse = int(data2_clients_list[partner_idx]['respondkeyp'+partner.lower()])
    myKeyResponse = int(data2_clients_list[role_idx]['respondkeyp'+role])
    if oppoKeyResponse == 1 and myKeyResponse == 1:
        reward = int(space1)
        partner_reward = int(space2)
        img_circle.setPos(to_1024_768_2D(-0.02, -0.025))
    elif oppoKeyResponse == 1 and myKeyResponse == 2:
        reward = int(space3)
        partner_reward = int(space4)
        img_circle.setPos(to_1024_768_2D(0.32, -0.025))
    elif oppoKeyResponse == 2 and myKeyResponse == 1:
        reward = int(space5)
        partner_reward = int(space6)
        img_circle.setPos(to_1024_768_2D(-0.02, -0.27))
    elif oppoKeyResponse == 2 and myKeyResponse == 2:
        reward = int(space7)
        partner_reward = int(space8)
        img_circle.setPos(to_1024_768_2D(0.32, -0.27))

    return [reward, partner_reward]
def draw_components(x,time,t,frameN, show):
    if t >= 0.0 and x.status == NOT_STARTED:
        x.tStart = t
        x.frameNStart = frameN  # exact frame index
        x.setAutoDraw(show)
    frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
    if x.status == STARTED and t >= frameRemains:
        x.setAutoDraw(False)
def draw_stimuli(components, time,t,frameN):
	for c in components:
		draw_components(c,time,t,frameN, True)
def set_all_user_pos(stage, field_choice_pair, my_field, u1_icon, u2_icon, op1_icon, op2_icon, my_dir):
    my_field = int(my_field)
    if my_field & 1 == 1:
        partner_field = my_field +1
    else:
        partner_field = my_field -1
    
    if my_dir == left_dir:
        my_payoff_nums = payoff_nums[0:4]
        my_num_pos = small_num_pos[0:4]
        opp_payoff_nums = payoff_nums[4:8]
        opp_num_pos = small_num_pos[4:8]

    else:
        my_payoff_nums = payoff_nums[4:8]
        my_num_pos = small_num_pos[4:8]
        opp_payoff_nums = payoff_nums[0:4]
        opp_num_pos = small_num_pos[0:4]
    print(field_choice_pair)
    for p in field_choice_pair:
        # Unpacking with *
        # support python>=3.5 for find key
        key = [*p][0]
        
        if type(p[key]) is dict:
            # It means this choice p is made by computer
            defend_value = str(int(p[key][stage][1]))
        else:
            # This choice p is made by user
            defend_value = str(int(p[key][1]))
        
        if key == 1 or key == 5:
            u1_def = defend_value
            u1_def = my_payoff_nums.index(u1_def)
        if key == 2 or key == 6:
            u2_def = defend_value
            u2_def = my_payoff_nums.index(u2_def)
        if key == 3 or key == 7:
            op1_def = defend_value
            op1_def = opp_payoff_nums.index(op1_def)
        if key == 4 or key == 8:
            op2_def = defend_value
            op2_def = opp_payoff_nums.index(op2_def)


    # # my_def = str(my_choice[1])
    # # my_def = my_payoff_nums.index(my_def)
    # # partner_def = str(partner_choice[1])

    u1_icon.pos = my_num_pos[u1_def]
    u2_icon.pos = my_num_pos[u2_def]
    op1_icon.pos = opp_num_pos[op1_def]
    op2_icon.pos = opp_num_pos[op2_def]

    # partner_def = my_payoff_nums.index(partner_def)
    # u2_icon.pos = my_num_pos[partner_def]

# def draw_stimuli(time):
#     for c in choices_stimulis:
#         if t >= 0.0 and img_PayoffMatrix.status == NOT_STARTED:
#             img_PayoffMatrix.tStart = t
#             img_PayoffMatrix.frameNStart = frameN  # exact frame index
#             img_PayoffMatrix.setAutoDraw(True)
#         frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#         if img_PayoffMatrix.status == STARTED and t >= frameRemains:
#             img_PayoffMatrix.setAutoDraw(False)


#     if t >= 0.0 and img_PayoffMatrix.status == NOT_STARTED:
#         img_PayoffMatrix.tStart = t
#         img_PayoffMatrix.frameNStart = frameN  # exact frame index
#         img_PayoffMatrix.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if img_PayoffMatrix.status == STARTED and t >= frameRemains:
#         img_PayoffMatrix.setAutoDraw(False)
#     if t >= 0.0 and textPartner.status == NOT_STARTED:
#         textPartner.tStart = t
#         textPartner.frameNStart = frameN  # exact frame index
#         textPartner.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textPartner.status == STARTED and t >= frameRemains:
#         textPartner.setAutoDraw(False)
#     if t >= 0.0 and textYou.status == NOT_STARTED:
#         textYou.tStart = t
#         textYou.frameNStart = frameN  # exact frame index
#         textYou.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textYou.status == STARTED and t >= frameRemains:
#         textYou.setAutoDraw(False)
#     if t >= 0.0 and textX.status == NOT_STARTED:
#         textX.tStart = t
#         textX.frameNStart = frameN  # exact frame index
#         textX.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textX.status == STARTED and t >= frameRemains:
#         textX.setAutoDraw(False)
#     if t >= 0.0 and textY.status == NOT_STARTED:
#         textY.tStart = t
#         textY.frameNStart = frameN  # exact frame index
#         textY.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textY.status == STARTED and t >= frameRemains:
#         textY.setAutoDraw(False)
#     if t >= 0.0 and textSuccessRate.status == NOT_STARTED:
#         textSuccessRate.tStart = t
#         textSuccessRate.frameNStart = frameN  # exact frame index
#         textSuccessRate.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSuccessRate.status == STARTED and t >= frameRemains:
#         textSuccessRate.setAutoDraw(False)
#     if t >= 0.0 and textSpace1.status == NOT_STARTED:
#         textSpace1.tStart = t
#         textSpace1.frameNStart = frameN  # exact frame index
#         textSpace1.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace1.status == STARTED and t >= frameRemains:
#         textSpace1.setAutoDraw(False)
#     if t >= 0.0 and textSpace2.status == NOT_STARTED:
#         textSpace2.tStart = t
#         textSpace2.frameNStart = frameN  # exact frame index
#         textSpace2.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace2.status == STARTED and t >= frameRemains:
#         textSpace2.setAutoDraw(False)
#     if t >= 0.0 and textSpace3.status == NOT_STARTED:
#         textSpace3.tStart = t
#         textSpace3.frameNStart = frameN  # exact frame index
#         textSpace3.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace3.status == STARTED and t >= frameRemains:
#         textSpace3.setAutoDraw(False)
#     if t >= 0.0 and textSpace4.status == NOT_STARTED:
#         textSpace4.tStart = t
#         textSpace4.frameNStart = frameN  # exact frame index
#         textSpace4.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace4.status == STARTED and t >= frameRemains:
#         textSpace4.setAutoDraw(False)
#     if t >= 0.0 and textSpace5.status == NOT_STARTED:
#         textSpace5.tStart = t
#         textSpace5.frameNStart = frameN  # exact frame index
#         textSpace5.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace5.status == STARTED and t >= frameRemains:
#         textSpace5.setAutoDraw(False)
#     if t >= 0.0 and textSpace6.status == NOT_STARTED:
#         textSpace6.tStart = t
#         textSpace6.frameNStart = frameN  # exact frame index
#         textSpace6.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace6.status == STARTED and t >= frameRemains:
#         textSpace6.setAutoDraw(False)
#     if t >= 0.0 and textSpace7.status == NOT_STARTED:
#         textSpace7.tStart = t
#         textSpace7.frameNStart = frameN  # exact frame index
#         textSpace7.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace7.status == STARTED and t >= frameRemains:
#         textSpace7.setAutoDraw(False)
#     if t >= 0.0 and textSpace8.status == NOT_STARTED:
#         textSpace8.tStart = t
#         textSpace8.frameNStart = frameN  # exact frame index
#         textSpace8.setAutoDraw(True)
#     frameRemains = 0.0 + int(time)- win.monitorFramePeriod * 0.75  # most of one frame period left
#     if textSpace8.status == STARTED and t >= frameRemains:
#         textSpace8.setAutoDraw(False)

def get_field(my_idx, user_fields_num):
    my_field_num = user_fields_num[my_idx]
    field_list = []


    if my_field_num <=4:
        for user, f in enumerate(user_fields_num):
            if f <= 4 :
                field_list.append((f, user))
    else:
        for user, f in enumerate(user_fields_num):
            if f > 4 :
                field_list.append((f, user))
    
    my_field_num -= 1
    my_field_num %= 4
    if my_field_num < 2:
        my_dir = "LEFT"
    else:
        my_dir = "RIGHT"
    print(my_dir)
    return field_list, my_dir

def trans(role, stage, subject_choice_key, counterbalance, group, partner):
    tra = {}
    # create subject_choice_key to choice ['X','Y'] dictionary
    choices_dict     = {'1' : choice_nums[0], '2' : choice_nums[1], '3' : choice_nums[2],  '4' : choice_nums[3], 10000 : 'Missed'}
    # choices_exc_dict = {'1' : choiceList[1], '2' : choiceList[0], 10000 : 'Missed'}

    # if counterbalance == 0:
    #     choice = str(choices_dict[subject_choice_key])
    # else:
    #     choice = str(choices_exc_dict[subject_choice_key])

    tra['trialp'+role] = currentTrial
    tra['p'+role] = choices_dict[subject_choice_key]
    tra['stagep'+role] = stage
    tra['groupp'+role] = 1
    tra['group'+role] = 1
    tra['partnerp'+role] = partner
    tra['respondkeyp'+role] = subject_choice_key
    return tra

def switch_IME_English():
    try:
        from win32con import WM_INPUTLANGCHANGEREQUEST
        import win32api, win32gui
        hwnd = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, 0x00000409)
    except:
        print("Cannot load win32com, win32api, or win32gui")
        sys.exit(1)

###########################################################################
endExpNow = False  # flag for 'escape' or other condition => quit the exp
# Start Code - component code to be run before the window creation
expMode = {'PracticeFlag': PracticeFlag}
dlg_Mode = gui.DlgFromDict(dictionary=expMode, title='Mode', sortKeys=False)
if dlg_Mode.OK == False:
    core.quit() 
PracticeFlag=expMode['PracticeFlag']
if PracticeFlag == True:
    runNum = 1

expInfo = {'ID (A/B/C/D)': str(clientID), 'Pair/Run': 'a', 'Run': '1', 
    'FlagBehaviorExp' : '0', 'MRI': '1',
    'SendTriggerTime': SendTriggerTime, 'Server': remote_serverID, 'Full Screen': FullScreenFlag}

pair2num_dict = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4}
#　pair'a' : run1 -> run2 -> run3 -> run4 -> run5 -> run6
#　pair'b' : run6 -> run5 -> run4 -> run3 -> run2 -> run1
#　pair'c' : run2 -> run6 -> run1 -> run3 -> run4 -> run5
#　pair'd' : run3 -> run4 -> run1 -> run6 -> run2 -> run5

# 4 runs loop
for r in range(runNum):

    # update current run number
    runCount += 1

    # refresh each run current block
    currentBlock = 0

    # setting run's total reward
    runReward = 0

    # count every trial 1~18
    trialCount = 0

    # setting each trial duration list
    trialDurList = []
    for d in range(0,18):
        trialDurList.append(int(df.at[d,'ITItime']))
    trialDurList = list(map(lambda x: x + 18, trialDurList))
    
    # add show Partner Screen Time
    PartnerScreenTrialList = []
    for d in range(6,18,6):
        trialDurList[d] = trialDurList[d] + showPartnerScreenTime
        PartnerScreenTrialList.append(d+1)

    # Store info about the experiment session
    psychopyVersion = '3.0.7'
    expName = 'hypercomm4p'

    # if runCount == 1:
    #     # determine user automatically input Run or not
    #     if expInfo['Pair/Run'].isdigit() == False:
    #         pair = int(pair2num_dict[str(expInfo['Pair/Run']).lower()])
    #         expInfo['Run'] = int(df.at[(pair - 1)*6 + runCount - 1,'PairRun'])
    #         AutoRunInput = True
    #     else:
    #         pair = 'None'
    #         expInfo['Run'] = expInfo['Pair/Run']
    #         AutoRunInput = False

    # if runCount > 1:
    #     if AutoRunInput == True:
    #         defaultRun = int(df.at[(pair - 1)*6 + runCount - 1,'PairRun'])
    #         expInfo['Run']= defaultRun

    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, sortKeys=False)
    if dlg.OK == False:
        core.quit()  # user pressed cancel

    clientID=expInfo['ID (A/B/C/D)']
    expInfo['date'] = data.getDateStr(format="%Y%m%d_%H%M%S")  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion
    SendTriggerTime = int(expInfo['SendTriggerTime'])
    FullScreenFlag= expInfo['Full Screen']
    
    currentRun = int(expInfo['Run'])
    runCount = currentRun 
    currentTrial = 0
    currentCommunication = (currentRun-1)*18
    expRun = 'Run' + str(expInfo['Run'])
    expDate= data.getDateStr(format="%Y%m%d")
    expTime= data.getDateStr(format="%H%M%S")
    remote_server=remote_servers[expInfo['Server']]

    textRateTrigger='Success Rate is 11/12 \n    Wait for trigger...'

    #Save log for each run:
    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    #filename = _thisDir + os.sep + u'data/%s_%s_%s_%s_%s' % (expName, expDate, clientID, expRun, expTime)
    filename = u'%s_%s_%s_%s_%s' % (expName, expDate, clientID, expRun, expTime)
    filename = os.path.join(_thisDir, 'data', filename)
    #print(filename)
    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=os.path.abspath(__file__),
        savePickle=True, saveWideText=True,
        dataFileName=filename)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
        
    # Start Code - component code to be run before the window creation

    # decide window position
    yshift=30
    WinPositions={'A': [0, yshift], 'B': [screenSize[0], yshift],  
        'C': [0, screenSize[1]+yshift*2],  'D':[screenSize[0], screenSize[1]+yshift*2]}
    WinPos= WinPositions[clientID]
    #print(clientID, WinPos)

    # Setup the Window
    win = visual.Window(
        size=screenSize, fullscr=FullScreenFlag, screen=0, pos=WinPos,
        allowGUI=not(FullScreenFlag), allowStencil=False,
        monitor='testMonitor', color=[-1.000,-1.000,-1.000], colorSpace='rgb',
        blendMode='avg', units='height')
        #, winType='pyglet', caption="Test")
        # useFBO=True, removed because it causes problem in virtualbox
    win.winHandle.set_caption("Player_" + clientID)

    # Switch to English before wait for trigger (Since Chinese IME will cause problem.)
    if sys.platform == 'win32':
        try:
            switch_IME_English()
            #print("Switch to English IME")
        except:
            print("Cannot switch to English IME.")
            sys.exit(1)


    small_num_pos = [to_1024_768_2D(-0.16, 0.27), to_1024_768_2D(-0.05, 0.27), to_1024_768_2D(-0.16, 0.14), to_1024_768_2D(-0.05, 0.14)
                , to_1024_768_2D(0.05, 0.27), to_1024_768_2D(0.16, 0.27), to_1024_768_2D(0.05, 0.14), to_1024_768_2D(0.16, 0.14)]

    big_num_pos = [to_1024_768_2D(-0.23, 0.12), to_1024_768_2D(-0.08, 0.12), to_1024_768_2D(-0.23, -0.12), to_1024_768_2D(-0.08, -0.12)
                    , to_1024_768_2D(0.05, 0.27), to_1024_768_2D(0.16, 0.27), to_1024_768_2D(0.05, 0.14), to_1024_768_2D(0.16, 0.14)]

    choice_pos = [to_1024_768_2D(-0.29, -0.16), to_1024_768_2D(-0.25, -0.27), to_1024_768_2D(-0.11, -0.16), to_1024_768_2D(-0.07, -0.27), to_1024_768_2D(0.08, -0.16), 
                to_1024_768_2D(0.12, -0.27), to_1024_768_2D(0.26, -0.16), to_1024_768_2D(0.30, -0.27)]

    # Initialize components for Routine "WelcomeScreen"
    WelcomeScreenClock = core.Clock()
    text_welcome = visual.TextStim(win=win, name='text_welcome',
        text=textRateTrigger,
        font='Arial',
        pos=(0, 0), height=to_1024_768_1D(0.07), wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=-1.0);
    
    # Initialize components for Routine "countDown"
    countDownClock = core.Clock()
    textCountDown = visual.TextStim(win=win, name='textCountDown',
        text='default text',
        font='Arial',
        pos=(0, 0), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # Initialize components for Routine "showIDScreen"
    showIDScreenClock = core.Clock()
    textShowID = visual.TextStim(win=win, name='textShowID',
        text='textShowID',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # Initialize components for Routine "Fixation4s"
    Fixation4sClock = core.Clock()
    textFixation = visual.TextStim(win=win, name='textFixation',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0); 

    # Initialize components for Routine "showPartnerScreen"
    showPartnerScreenClock = core.Clock()
    textShowPartner = visual.TextStim(win=win, name='textShowPartner',
        text='textShowPartner',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # Initialize components for Routine "DEC1"
    DEC1Clock = core.Clock()
    img_PayoffMatrix = visual.ImageStim(
        win=win,
        name='img_PayoffMatrix', 
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=to_1024_768_2D(1.2, 0.9),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=0.0)
    
    image_PayoffMatrix_list = ['../new_images/Payoff Matrix_S1.png', '../images/Payoff Matrix_S2.png']
    text_depth = -5
    textSpace1 = visual.TextStim(win=win, name='textSpace1',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.16, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace2 = visual.TextStim(win=win, name='textSpace2',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.05, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace3 = visual.TextStim(win=win, name='textSpace3',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.16, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace4 = visual.TextStim(win=win, name='textSpace4',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.05, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace5 = visual.TextStim(win=win, name='textSpace5',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.05, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace6 = visual.TextStim(win=win, name='textSpace6',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.16, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace7 = visual.TextStim(win=win, name='textSpace7',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.05, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);
    textSpace8 = visual.TextStim(win=win, name='textSpace8',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.16, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=text_depth);


    choiceSpace1 = visual.TextStim(win=win, name='choiceSpace1',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.16, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace2 = visual.TextStim(win=win, name='choiceSpace2',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.05, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace3 = visual.TextStim(win=win, name='choiceSpace3',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.16, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace4 = visual.TextStim(win=win, name='choiceSpace4',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(-0.05, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace5 = visual.TextStim(win=win, name='choiceSpace5',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.05, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace6 = visual.TextStim(win=win, name='choiceSpace6',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.16, 0.27), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace7 = visual.TextStim(win=win, name='choiceSpace7',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.05, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    choiceSpace8 = visual.TextStim(win=win, name='choiceSpace8',
        text='default text',
        font='Arial',
        pos=to_1024_768_2D(0.16, 0.14), height=to_1024_768_1D(0.1), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    
    textSuccessRate = visual.TextStim(win=win, name='textSuccessRate',
        text='',
        font='Arial',
        pos=to_1024_768_2D(-0.21, 0.18), height=to_1024_768_1D(0.042), wrapWidth=None, ori=0, 
        color=[1.000,0.961,-0.765], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    textPartner = visual.TextStim(win=win, name='textPartner',
        text='',
        font='Arial',
        pos=to_1024_768_2D(-0.55, -0.17), height=to_1024_768_1D(0.07), wrapWidth=None, ori=270, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    textYou = visual.TextStim(win=win, name='textYou',
        text='',
        font='Arial',
        pos=to_1024_768_2D(0.21, 0.4), height=to_1024_768_1D(0.07), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    textX = visual.TextStim(win=win, name='textX',
        text='',
        font='Arial',
        pos=to_1024_768_2D(0.05, 0.2), height=to_1024_768_1D(0.11), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    textY = visual.TextStim(win=win, name='textY',
        text='',
        font='Arial',
        pos=to_1024_768_2D(0.39, 0.2), height=to_1024_768_1D(0.11), wrapWidth=None, ori=0, 
        color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    
    # Initialize components for Routine "AllianceCheckWait"
    AllianceCheckWaitClock = core.Clock()
    textWait = visual.TextStim(win=win, name='textWait',
        text='+',
        font='Arial',
        pos=(0, 0), height=to_1024_768_1D(0.07), wrapWidth=None, ori=0, 
        color='yellow', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    # Initialize components for Routine "TRA1"
    TRA1Clock = core.Clock()
    textTRA1 = visual.TextStim(win=win, name='textTRA1',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # Initialize components for Routine "FB1"
    FB1Clock = core.Clock()
    image_frame_list = ['../images/pa_dash.png',  '../images/pb_dash.png',  '../images/pc_dash.png',  '../images/pd_dash.png', 
                        '../images/pa_solid.png', '../images/pb_solid.png', '../images/pc_solid.png', '../images/pd_solid.png', 
                        '../images/oppopa_dash.png', '../images/oppopb_dash.png', '../images/oppopc_dash.png', '../images/oppopd_dash.png',
                        '../images/oppopa_solid.png', '../images/oppopb_solid.png', '../images/oppopc_solid.png', '../images/oppopd_solid.png']

    img_selfFrame = visual.ImageStim(
        win=win,
        name='img_selfFrame', 
        image='sin', mask=None,
        ori=0, pos=to_1024_768_2D(0.035, -0.029), size=to_1024_768_2D(0.33, 0.72),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-1)
    img_oppoFrame = visual.ImageStim(
        win=win,
        name='img_oppoFrame', 
        image='sin', mask=None,
        ori=0, pos=to_1024_768_2D(0.034, -0.028), size=to_1024_768_2D(1, 0.23),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-1)
    
    dash = visual.ImageStim(
        win=win,
        name='dash', 
        image='../new_images/choice_dash.png', mask=None,
        ori=0, pos=to_1024_768_2D(-0.27, -0.22), size=to_1024_768_2D(0.13, 0.26),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-3)
    
    u1_icon = visual.ImageStim(
        win=win,
        name='my_icon', 
        image='../new_images/G1_1.png', mask=None,
        ori=0, pos=to_1024_768_2D(0.035, -0.029), size=to_1024_768_2D(0.08, 0.08),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-3)
    u2_icon = visual.ImageStim(
        win=win,
        name='partner_icon', 
        image='../new_images/G1_2.png', mask=None,
        ori=0, pos=to_1024_768_2D(0.035, -0.029), size=to_1024_768_2D(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-2)
    op1_icon = visual.ImageStim(
        win=win,
        name='op1_icon', 
        image='../new_images/G2_1.png', mask=None,
        ori=0, pos=to_1024_768_2D(0.035, -0.029), size=to_1024_768_2D(0.08, 0.08),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-3)
    op2_icon = visual.ImageStim(
        win=win,
        name='op2_icon', 
        image='../new_images/G2_2.png', mask=None,
        ori=0, pos=to_1024_768_2D(0.035, -0.029), size=to_1024_768_2D(0.1, 0.1),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-2)
        
    # Initialize components for Routine "IStageI"
    IStageIClock = core.Clock()
    textIStageI = visual.TextStim(win=win, name='textIStageI',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    # Initialize components for Routine "DEC2"
    DEC2Clock = core.Clock()

    # Initialize components for Routine "TRA2"
    TRA2Clock = core.Clock()
    textTRA2 = visual.TextStim(win=win, name='textTRA2',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # Initialize components for Routine "FB2"
    FB2Clock = core.Clock()
    img_circle = visual.ImageStim(
        win=win,
        name='img_circle', 
        image='sin', mask=None,
        ori=0, pos=to_1024_768_2D(-0.02, -0.025), size=to_1024_768_2D(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=1024, interpolate=True, depth=-1)
    img_circle.setImage('../images/circle.png')
    textITI = visual.TextStim(win=win, name='textITI',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # Initialize components for Routine "ITI6s"
    ITI6sClock = core.Clock()
    textITI = visual.TextStim(win=win, name='textITI',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);


    payoff_nums_stimulis = [textSpace1, textSpace2, textSpace3, textSpace4, textSpace5, textSpace6, textSpace7, textSpace8]
    choices_stimulis = [choiceSpace1, choiceSpace2, choiceSpace3, choiceSpace4, choiceSpace5, choiceSpace6, choiceSpace7, choiceSpace8]


    # store frame rate of monitor if we can measure it
    expInfo['frameRate'] = win.getActualFrameRate()
    if expInfo['frameRate'] != None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
    
    # ------Prepare to start Routine "WelcomeScreen"-------
    t = 0
    WelcomeScreenClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    #    ===================(remove)
    # continueRoutine = False
    #    ===================
    
    
    # update component parameters for each repeat
    key_welcome = event.BuilderKeyResponse()

    # participant is subject's ID (A or B or C)
    clientID = str(expInfo['ID (A/B/C/D)'])
    clientID = clientID.capitalize()

    # keep track of which components have finished
    WelcomeScreenComponents = [text_welcome, key_welcome]
    for thisComponent in WelcomeScreenComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "WelcomeScreen"-------
    while continueRoutine:
        # get current time
        t = WelcomeScreenClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_welcome* updates
        if t >= 0.0 and text_welcome.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_welcome.tStart = t
            text_welcome.frameNStart = frameN  # exact frame index
            text_welcome.setAutoDraw(True)

        # *key_welcome* updates
        if t >= 0.0 and key_welcome.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_welcome.tStart = t
            key_welcome.frameNStart = frameN  # exact frame index
            key_welcome.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_welcome.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

        ### Tcpip socket (client part) ###
        # receive '5'
        if int(expInfo['MRI']) == 1:
                theseKeys = event.getKeys(keyList=['5'])
                if len(theseKeys) > 0:
                    if SendTriggerTime == 1 and PracticeFlag == False:
                        # after received trigger, get trigger time string from NTP server
                        #ntpserver="140.116.183.215"
                        TriggerTimeStamp = getNTPTime(ntpserver)
                        TriggerTimeStr = time_string(TriggerTimeStamp)
    
                        # send trigger time string back to communication server
                        #   note: must assign remote_ip & target_port 
                        exit_flag=0
                        #remote_server="140.116.182.232"
                        #scannerport=8769
                        while exit_flag==0:
                            try:
                                client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                client2.connect((remote_server, scannerport))
                                logging.info("Connected!")
                                exit_flag=1
                            except KeyboardInterrupt:
                                logging.info("KeyboardInterrupt")
                                raise
                            except:
                                sys.stdout.write(".")
                                sys.stdout.flush()
                        #End of while
                        client2.send(TriggerTimeStr.encode("utf-8"))
                        client2.shutdown(1); client2.close()
                    # endif SendTriggerTime
                    continueRoutine = False

        if int(expInfo['MRI']) == 0:
            message_5 = s.recv(1024)
            if str(message_5.decode()) == '5': 
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WelcomeScreenComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        #win.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
        #win.saveMovieFrames('WelcomeScreen.jpg')  # save with a descriptive and unique filename. 

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "WelcomeScreen"-------
    for thisComponent in WelcomeScreenComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # check responses
    if key_welcome.keys in ['', [], None]:  # No response was made
        key_welcome.keys=None

    # the Routine "WelcomeScreen" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # wait for 5 sec
    # ------Prepare to start Routine "countDown"-------
    # t = 0
    # countDownClock.reset()  # clock
    # frameN = -1
    # continueRoutine = True
    # routineTimer.add(5.000000)
    # # update component parameters for each repeat
    # countT = 1
    # # keep track of which components have finished
    # countDownComponents = [textCountDown]
    # for thisComponent in countDownComponents:
    #     if hasattr(thisComponent, 'status'):
    #         thisComponent.status = NOT_STARTED
    
    # # -------Start Routine "countDown"-------(close)
    # while continueRoutine and routineTimer.getTime() > 0:
    #     # get current time
    #     t = countDownClock.getTime()
    #     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    #     # update/draw components on each frame
        
    #     # *textCountDown* updates
    #     if t >= 0.0 and textCountDown.status == NOT_STARTED:
    #         # keep track of start time/frame for later
    #         textCountDown.tStart = t
    #         textCountDown.frameNStart = frameN  # exact frame index
    #         textCountDown.setAutoDraw(True)
    #     frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
    #     if textCountDown.status == STARTED and t >= frameRemains:
    #         textCountDown.setAutoDraw(False)
    #     if textCountDown.status == STARTED:  # only update if drawing
    #         textCountDown.setText(countT, log=False)

    #     time.sleep(0.9)
    #     countT -= 1
        
    #     # check for quit (typically the Esc key)
    #     if endExpNow or event.getKeys(keyList=["escape"]):
    #         core.quit()
        
    #     # check if all components have finished
    #     if not continueRoutine:  # a component has requested a forced-end of Routine
    #         break
    #     continueRoutine = False  # will revert to True if at least one component still running
    #     for thisComponent in countDownComponents:
    #         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
    #             continueRoutine = True
    #             break  # at least one component has not yet finished
        
    #     # refresh the screen
    #     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
    #         win.flip()  
    
    # # -------Ending Routine "countDown"-------
    # for thisComponent in countDownComponents:
    #     if hasattr(thisComponent, "setAutoDraw"):
    #         thisComponent.setAutoDraw(False)

    if PracticeFlag == False:

        ### Tcpip socket (client part) ###
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server IP
        host = remote_server
        port = 8077
        s.connect((host,port))
        s.settimeout(None)
        inout = [s]
        outputs = []
        print('Sucessfully Connect to Server')
    
    # ------Prepare to start Routine "showIDScreen"-------
    t = 0
    showIDScreenClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(showIDScreenTime)
    # update component parameters for each repeat
    textShowID.setText('ID : ' + str(clientID))
    # keep track of which components have finished
    showIDScreenComponents = [textShowID]
    for thisComponent in showIDScreenComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "showIDScreen"-------(close)
    # while continueRoutine and routineTimer.getTime() > 0:
    #     # get current time
    #     t = showIDScreenClock.getTime()
    #     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    #     # update/draw components on each frame
        
    #     # *textShowID* updates
    #     if t >= 0.0 and textShowID.status == NOT_STARTED:
    #         # keep track of start time/frame for later
    #         textShowID.tStart = t
    #         textShowID.frameNStart = frameN  # exact frame index
    #         textShowID.setAutoDraw(True)
    #     frameRemains = 0.0 + int(showIDScreenTime)- win.monitorFramePeriod * 0.75  # most of one frame period left
    #     if textShowID.status == STARTED and t >= frameRemains:
    #         textShowID.setAutoDraw(False)
        
    #     # check for quit (typically the Esc key)
    #     if endExpNow or event.getKeys(keyList=["escape"]):
    #         core.quit()
        
    #     # check if all components have finished
    #     if not continueRoutine:  # a component has requested a forced-end of Routine
    #         break
    #     continueRoutine = False  # will revert to True if at least one component still running
    #     for thisComponent in showIDScreenComponents:
    #         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
    #             continueRoutine = True
    #             break  # at least one component has not yet finished
        
    #     # refresh the screen
    #     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
    #         win.flip()
    
    # -------Ending Routine "showIDScreen"-------
    for thisComponent in showIDScreenComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "showIDScreen" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Fixation4s"-------
    t = 0
    Fixation4sClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(Fixation4sTime)
    # update component parameters for each repeat
    # keep track of which components have finished
    Fixation4sComponents = [textFixation]
    for thisComponent in Fixation4sComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "Fixation4s"-------(close)
    # while continueRoutine and routineTimer.getTime() > 0:
    #     # get current time
    #     t = Fixation4sClock.getTime()
    #     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    #     # update/draw components on each frame
        
    #     # *textFixation* updates
    #     if t >= 0.0 and textFixation.status == NOT_STARTED:
    #         # keep track of start time/frame for later
    #         textFixation.tStart = t
    #         textFixation.frameNStart = frameN  # exact frame index
    #         textFixation.setAutoDraw(True)
    #     frameRemains = 0.0 + int(Fixation4sTime)- win.monitorFramePeriod * 0.75  # most of one frame period left
    #     if textFixation.status == STARTED and t >= frameRemains:
    #         textFixation.setAutoDraw(False)
        
    #     # check for quit (typically the Esc key)
    #     if endExpNow or event.getKeys(keyList=["escape"]):
    #         core.quit()
        
    #     # check if all components have finished
    #     if not continueRoutine:  # a component has requested a forced-end of Routine
    #         break
    #     continueRoutine = False  # will revert to True if at least one component still running
    #     for thisComponent in Fixation4sComponents:
    #         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
    #             continueRoutine = True
    #             break  # at least one component has not yet finished
        
    #     # refresh the screen
    #     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
    #         win.flip()
    
    # -------Ending Routine "Fixation4s"-------
    for thisComponent in Fixation4sComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Fixation4s" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    if PracticeFlag == True:
        blockNums = 2
    else:
        blockNums = 6
    
    # set up handler to look after randomisation of conditions etc
    blocks = data.TrialHandler(nReps=blockNums, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='blocks')
    thisExp.addLoop(blocks)  # add the loop to the experiment
    thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    for thisBlock in blocks:
        currentLoop = blocks
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock:
                exec('{} = thisBlock[paramName]'.format(paramName))
        
        # adding blocks
        currentBlock += 1
        
        # each block the same
        user_fields = []
        user_list = ['group_pa', 'group_pb', 'group_pc', 'group_pd', 'group_pe', 'group_pf', 'group_pg', 'group_ph']
        user_idx_dict = {'A':0, 'B':1, 'C':2, 'D':3}
        my_idx = user_idx_dict[clientID]
        for u in user_list:
            user_fields.append(df.at[currentTrial, u])

        # (f, user)
        field_pair_list = []
        field_pair_list, my_dir = get_field(my_idx, user_fields)

        # assign subject's role in group
        for k in range(0, len(groupMember_dict)):
            d = groupMember_dict[k]
            if clientID == d :
                role = 'player' + str(d)
                role_alphabet = str(d.lower())
                role_idx = k
                # group_num = user_fields[k]
                group_num = -1
                # partner_idx = [j for j, e in enumerate(user_fields) if e == group_num and j != k][0]
                partner_idx = 0
                # partnerID = groupMember_dict[partner_idx]
                partnerID = 'A'
                if k < partner_idx:
                    order = 1
                else:
                    order = 2

        # ------Prepare to start Routine "showPartnerScreen"-------
        t = 0
        showPartnerScreenClock.reset()  # clock
        frameN = -1
        # only showing this screen when partner changes
        if currentBlock%2 != 0:
            continueRoutine = True
        else:
            continueRoutine = False
        routineTimer.reset()
        routineTimer.add(showPartnerScreenTime)
        textShowPartner.setText('Interacting With\nPlayer ' + str(partnerID))
        # keep track of which components have finished
        showPartnerScreenComponents = [textShowPartner]
        for thisComponent in showPartnerScreenComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # -------Start Routine "showPartnerScreen"-------(close)
        # while continueRoutine and routineTimer.getTime() > 0:
        #     # get current time
        #     t = showPartnerScreenClock.getTime()
        #     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
        #     # *textShowPartner* updates
        #     if t >= 0.0 and textShowPartner.status == NOT_STARTED:
        #         # keep track of start time/frame for later
        #         textShowPartner.tStart = t
        #         textShowPartner.frameNStart = frameN  # exact frame index
        #         textShowPartner.setAutoDraw(True)
        #     frameRemains = 0.0 + int(showPartnerScreenTime)- win.monitorFramePeriod * 0.75  # most of one frame period left
        #     if textShowPartner.status == STARTED and t >= frameRemains:
        #         textShowPartner.setAutoDraw(False)
            
        #     # check for quit (typically the Esc key)
        #     if endExpNow or event.getKeys(keyList=["escape"]):
        #         core.quit()
            
        #     # check if all components have finished
        #     if not continueRoutine:  # a component has requested a forced-end of Routine
        #         break
        #     continueRoutine = False  # will revert to True if at least one component still running
        #     for thisComponent in showPartnerScreenComponents:
        #         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
        #             continueRoutine = True
        #             break  # at least one component has not yet finished
            
        #     # refresh the screen
        #     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        #         win.flip()
        
        # -------Ending Routine "showPartnerScreen"-------
        for thisComponent in showPartnerScreenComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "showPartnerScreen" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler(nReps=3, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='trials')
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        for thisTrial in trials:
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))

            # update current trial
            currentTrial += 1
            trialCount += 1

            # update currentCommunication
            currentCommunication += 1

            # default client not missing
            oops = False
            oops2 = False

            # read 'runset'
            # RunCommunication = int(df.at[currentCommunication - 1,'Communication'])

            computer_choice_title = [('S1_choice_pe', 'S2_choice_pe'), ('S1_choice_pf', 'S2_choice_pf'), ('S1_choice_pg', 'S2_choice_pg'), ('S1_choice_ph', 'S2_choice_ph')]
            computer_choice = []
            
            for t in computer_choice_title:
                s1 = df.at[currentTrial - 1,t[0]] 
                s2 = df.at[currentTrial - 1,t[1]] 
                computer_choice.append((s1, s2))

            exc_stage1 = int(df.at[currentTrial - 1,'ExchangePos'])
            currentPayoff = df.at[currentTrial - 1,'Payoffmatrix']
            currentOpponent = str(df.at[currentTrial - 1,'InteractionType'])
            # currentComputerC = str(df.at[currentTrial - 1,'ComputerChoice'])
            # MRI ITI time
            if int(expInfo['FlagBehaviorExp']) != 1:
                ITITime = int(df.at[currentTrial - 1,'ITItime'])

            #　payoff dict transfer
            currentPayoff = payoffDict[str(currentPayoff)]

            # ------Prepare to start Routine "DEC1"-------
            t = 0
            DEC1Clock.reset()  # clock
            routineTimer.reset()
            routineTimer.add(DEC1Time)
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            key_resp_DEC1 = event.BuilderKeyResponse()

            # dertermine payoff matrix
            # coordinate game (e.g. C1/C9), player2 get C9
            # if order == 2 and int(currentPayoff[0][0][0]) != 0 and currentOpponent == 'H' and exc_stage1 == 0:
            if order == 2 and int(currentPayoff[0][0][0]) != 0 and exc_stage1 == 0:
                space1 = currentPayoff[0][0][1]
                space2 = currentPayoff[0][0][0]
                space3 = currentPayoff[0][1][1]
                space4 = currentPayoff[0][1][0]
                space5 = currentPayoff[1][0][1]
                space6 = currentPayoff[1][0][0]
                space7 = currentPayoff[1][1][1]
                space8 = currentPayoff[1][1][0]
            # counterbalance
            # elif order == 2 and int(currentPayoff[0][0][0]) != 0 and currentOpponent == 'H' and exc_stage1 == 1:
            elif order == 2 and int(currentPayoff[0][0][0]) != 0 and exc_stage1 == 1:
                space1 = currentPayoff[0][1][1]
                space2 = currentPayoff[0][1][0]
                space3 = currentPayoff[0][0][1]
                space4 = currentPayoff[0][0][0]
                space5 = currentPayoff[1][1][1]
                space6 = currentPayoff[1][1][0]
                space7 = currentPayoff[1][0][1]
                space8 = currentPayoff[1][0][0]

            elif exc_stage1 == 0:
                space1 = currentPayoff[0][0][0]
                space2 = currentPayoff[0][0][1]
                space3 = currentPayoff[0][1][0]
                space4 = currentPayoff[0][1][1]
                space5 = currentPayoff[1][0][0]
                space6 = currentPayoff[1][0][1]
                space7 = currentPayoff[1][1][0]
                space8 = currentPayoff[1][1][1]
            # counterbalance
            else:
                space1 = currentPayoff[0][1][0]
                space2 = currentPayoff[0][1][1]
                space3 = currentPayoff[0][0][0]
                space4 = currentPayoff[0][0][1]
                space5 = currentPayoff[1][1][0]
                space6 = currentPayoff[1][1][1]
                space7 = currentPayoff[1][0][0]
                space8 = currentPayoff[1][0][1]

            if (int(currentPayoff[0][0][0]) != 0 and exc_stage1 == 0) or (int(currentPayoff[0][0][0]) == 0 and exc_stage1 == 1):
                key1BigValue = space1
                key2BigValue = space7
            else:
                key1BigValue = space3
                key2BigValue = space5

            #stimuli_setting(stage, role, partner, counterbalance)
            stimuli_setting(1, role_alphabet, partnerID, exc_stage1)
            DEC1Components = [img_PayoffMatrix]
            
            # set text payoff
            for idx, t in enumerate(payoff_nums_stimulis):
                t.setText(payoff_nums[idx])
                DEC1Components.append(t)


            for idx, c in enumerate(choices_stimulis):
                c.pos = choice_pos[idx]
                c.setText(choice_nums[idx >> 1][idx & 1])
                DEC1Components.append(c)
										

            # # set color
            # partnerColor = playerColor_dict[str(partnerID)]
            # textSpace2.color = partnerColor
            # textSpace4.color = partnerColor
            # textSpace6.color = partnerColor
            # textSpace8.color = partnerColor

            # keep track of which components have finished
            
            for thisComponent in DEC1Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record start trial time(DecOns1)  
            startTrialT = ExperimentClock.getTime()
            has_answered = False
            # -------Start Routine "DEC1"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = DEC1Clock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # draw_stimuli(DEC1Time)
                draw_components(dash, DEC1Time,t,frameN, has_answered)
                draw_stimuli(DEC1Components, DEC1Time,t,frameN)
                # *key_resp_DEC1* updates
                if t >= 0.0 and key_resp_DEC1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_DEC1.tStart = t
                    key_resp_DEC1.frameNStart = frameN  # exact frame index
                    key_resp_DEC1.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_DEC1.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                frameRemains = 0.0 + int(DEC1Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if key_resp_DEC1.status == STARTED and t >= frameRemains:
                    key_resp_DEC1.status = FINISHED
                if key_resp_DEC1.status == STARTED:
                    theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0 and not has_answered:  # at least one key was pressed
                        key_resp_DEC1.keys = theseKeys[-1]  # just the last key pressed
                        key_resp_DEC1.rt = key_resp_DEC1.clock.getTime()
                        has_answered = True
                        dash.pos = to_1024_768_2D(-0.27+(int(theseKeys[0])-1)*0.185, -0.22)
                        dash.setAutoDraw(True)
                        # a response ends the routine
                        # continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in DEC1Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                #win.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
                #win.saveMovieFrames('DEC1.jpg')  # save with a descriptive and unique filename. 
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            # -------Ending Routine "DEC1"-------

            # record end alliance decesion time(Dec1End)
            Dec1End = ExperimentClock.getTime()
            
            # calculate how much time to compensate in DEC1
            patch_Dec1 = float(DEC1Time - (Dec1End-startTrialT))

            if trialCount == 1:
                standardTime = startTrialT

            for thisComponent in DEC1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            dash.setAutoDraw(False)

            # check responses
            if key_resp_DEC1.keys in ['', [], None]:  # No response was made
                key_resp_DEC1.keys=10000
            # the Routine "DEC1" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # record subjuct's key response
            subject_choice_key = key_resp_DEC1.keys

            # trans(role, stage, subject_choice_key, counterbalance, group, partner)
            tra1 = trans(role_alphabet, 1, subject_choice_key, exc_stage1, group_num, partnerID)

            # ------Prepare to start Routine "AllianceCheckWait"-------
            waitT = 0
            AllianceCheckWaitClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            # keep track of which components have finished
            AllianceCheckWaitComponents = [textWait]
            for thisComponent in AllianceCheckWaitComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            ### Tcpip socket (client part) ###
            if PracticeFlag == False:
                message_tra1 = json.dumps(tra1).encode('utf-8')
                s.sendall(message_tra1)
            else:
                continueRoutine = False
            message_ret_data = []

            # ==================
            waitT = 7
            # ==================


            # -------Start Routine "AllianceCheckWait"-------
            while continueRoutine and waitT <= 6:
                # get current time
                waitT = AllianceCheckWaitClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *textWait* updates
                if waitT >= 0.0 and textWait.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    textWait.tStart = waitT
                    textWait.frameNStart = frameN  # exact frame index
                    textWait.setAutoDraw(True)
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
                
                ### Tcpip socket (client part) ###
                # receive ret_data only when data exists
                infds, outfds, errfds = select.select(inout, inout, [], 5)
                if len(infds) != 0:
                    message_ret_data = s.recv(1024)
                    message_ret_data = message_ret_data.decode()
                    break
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in AllianceCheckWaitComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "AllianceCheckWait"-------
            for thisComponent in AllianceCheckWaitComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "AllianceCheckWait" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "TRA1"-------
            t = 0
            TRA1Clock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat

            ### For debug
            ### Directly assign the value to socket data
            message_ret_data = '[{"trialpa": 1, "pa": [2, 8], "stagepa": 1, "grouppa": 1, "groupa": 1, "partnerpa": "A", "respondkeypa": "1"}, {"trialpb": 1, "pb": [4, 6], "stagepb": 1, "grouppb": 1, "groupb": 1, "partnerpb": "A", "respondkeypb": "2"}, {"trialpc": 1, "pc": [6, 4], "stagepc": 1, "grouppc": 1, "groupc": 1, "partnerpc": "A", "respondkeypc": "3"}, {"trialpd": 1, "pd": [8, 6], "stagepd": 1, "grouppd": 1, "groupd": 1, "partnerpd": "A", "respondkeypd": "4"}]'
            
            whoMissed = ''
            if PracticeFlag == False:
                # escape from loop
                if len(message_ret_data) == 0:
                    stage1_choice = 'TRA1delay'
                    textTRA1.setText('Transmission Delay...')
                else:
                    # if escape from transmission loop in tra2, make sure whether client catch previous data (one data len approximate 400)
                    if len(message_ret_data) >= 600:
                        idx = message_ret_data.find('[', 1)
                        data_clients = json.loads(message_ret_data[idx:])
                    else:
                        data_clients = json.loads(message_ret_data)
                # print(data_clients)
                # check whether someone missed
                for k in range(len(data_clients)):
                    if data_clients[k][str(list(data_clients[k].keys())[1])] == 'Missed':
                        for q in range(0, len(groupMember_dict)):
                    	    if 'trialp' + str(groupMember_dict[q].lower()) in data_clients[k]:
                                missedCountList[q] += 1

                                # check whether that missing guy is me or my partner
                                if str(groupMember_dict[q].lower()) == str(role_alphabet) or str(groupMember_dict[q]) == str(partnerID):
                                    oops = True
                                    whoMissed += 'ID ' + str(groupMember_dict[q]) + ' Missing #' + str(missedCountList[q]) + '\n'
            else:
            	# check practice mode missing
            	if subject_choice_key == 10000:
            		missedCount += 1
            		oops = True
            		whoMissed += 'ID ' + str(role_alphabet.capitalize()) + ' Missing #' + str(missedCount) + '\n'

            if oops == True:
    	        whoMissed += 'Please Wait for Next Trial'
    	        textTRA1.setText(str(whoMissed))

            TRA1Components = [textTRA1]
            for thisComponent in TRA1Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record ISI on time
            ISIOnS1 = ExperimentClock.getTime()

            # escape from transmission loop
            if len(message_ret_data) == 0 and PracticeFlag == False:
            	delay_tra1 = float(ISIOnS1-Dec1End) - waitT
            # calculate how much time to cut, due to tral transimission delay
            else:
            	delay_tra1 = float(ISIOnS1-Dec1End)
    
            # escape from transmission loop
            if len(message_ret_data) == 0 and PracticeFlag == False:
            	TRA1_duration = TRA1Time + patch_Dec1 - delay_tra1 - 2 #先扣兩秒  
            else:
            	TRA1_duration = TRA1Time + patch_Dec1 - delay_tra1
            
            # -------Start Routine "TRA1"-------
            # while continueRoutine:
            #     # get current time
            #     t = TRA1Clock.getTime()
            #     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            #     # update/draw components on each frame
                
            #     # *textTRA1* updates
            #     if t >= 0.0 and textTRA1.status == NOT_STARTED:
            #         # keep track of start time/frame for later
            #         textTRA1.tStart = t
            #         textTRA1.frameNStart = frameN  # exact frame index
            #         textTRA1.setAutoDraw(True)
            #     frameRemains = 0.0 + TRA1_duration - win.monitorFramePeriod * 0.75  # most of one frame period left
            #     if textTRA1.status == STARTED and t >= frameRemains:
            #         textTRA1.setAutoDraw(False)
                
            #     # check for quit (typically the Esc key)
            #     if endExpNow or event.getKeys(keyList=["escape"]):
            #         core.quit()
                
            #     # check if all components have finished
            #     if not continueRoutine:  # a component has requested a forced-end of Routine
            #         break
            #     continueRoutine = False  # will revert to True if at least one component still running

            #     for thisComponent in TRA1Components:
            #         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            #             continueRoutine = True
            #             break  # at least one component has not yet finished
                
            #     # refresh the screen
            #     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            #         win.flip()
            
            # -------Ending Routine "TRA1"-------

            # record ISI end time
            ISIEndS1 = ExperimentClock.getTime()

            for thisComponent in TRA1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)

            routineTimer.reset()
            textTRA1.setText('+')
            
            # ------Prepare to start Routine "FB1"-------
            t = 0
            FB1Clock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # ==========================
            FB1Time = 5
            # ==========================
            routineTimer.add(FB1Time)
            # update component parameters for each repeat
            if oops == True or (len(message_ret_data) == 0 and PracticeFlag == False):
                continueRoutine = False

            else:
            	# create data client list contains 4 players for practice mode
                data_clients_list = []
                data2_clients_list = []
                for k in range(0, len(groupMember_dict)):
                    r = groupMember_dict[k].lower()
                    choiceList_fb1 = ['1', '2']

                    # trans(role, stage, subject_choice_key, counterbalance, group, partner)
                    data_clients_list.append(trans(r, 1, '1', 0, 0, 0))

                # replace with data_clients while it's online version
                if PracticeFlag == False:
                    for y in range(len(data_clients)):
                        data_client = data_clients[y]  
        
            	        # who's in the data_clients list
                        for z in range(len(data_clients)):
                            r = groupMember_dict[z].lower()    
        
                            if 'trialp'+str(r) in data_client:
                                data_clients_list[z] = data_client
                # player's data
                else:
                    data_clients_list[role_idx] = trans(role_alphabet, 1, subject_choice_key, exc_stage1, group_num, partnerID)

                field_choice_pair = stimuli_setting(1, role_alphabet, partnerID, exc_stage1, role_idx=role_idx, partner_idx=partner_idx)

            # keep track of which components have finished
            # FB1Components = [img_selfFrame, img_oppoFrame, img_PayoffMatrix, textPartner, textYou, textX, textY, textSuccessRate, textSpace1, textSpace2, textSpace3, textSpace4, textSpace5, textSpace6, textSpace7, textSpace8]
            # print(field_choice_pair)
            # print(user_fields[my_idx])

            set_all_user_pos('s1', field_choice_pair, user_fields[my_idx], u1_icon, u2_icon, op1_icon, op2_icon, my_dir)
            FB1Components = [img_PayoffMatrix, u1_icon, u2_icon]
            
            # set text payoff
            for idx, t in enumerate(payoff_nums_stimulis):
                t.setText(payoff_nums[idx])
                FB1Components.append(t)

            for idx, c in enumerate(choices_stimulis):
                c.pos = choice_pos[idx]
                c.setText(choice_nums[idx >> 1][idx & 1])
                FB1Components.append(c)
            
            for thisComponent in FB1Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record FB1 on time
            Fb1On = ExperimentClock.getTime()

            # -------Start Routine "FB1"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = FB1Clock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *img_selfFrame* updates
                # if t >= 0.0 and img_selfFrame.status == NOT_STARTED:
                #     # keep track of start time/frame for later
                #     img_selfFrame.tStart = t
                #     img_selfFrame.frameNStart = frameN  # exact frame index
                #     img_selfFrame.setAutoDraw(True)
                # frameRemains = 0.0 + int(FB1Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                # if img_selfFrame.status == STARTED and t >= frameRemains:
                #     img_selfFrame.setAutoDraw(False)

                # # *img_oppoFrame* updates
                # if t >= 0.0 and img_oppoFrame.status == NOT_STARTED:
                #     # keep track of start time/frame for later
                #     img_oppoFrame.tStart = t
                #     img_oppoFrame.frameNStart = frameN  # exact frame index
                #     img_oppoFrame.setAutoDraw(True)
                # frameRemains = 0.0 + int(FB1Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                # if img_oppoFrame.status == STARTED and t >= frameRemains:
                #     img_oppoFrame.setAutoDraw(False)

                # draw_stimuli(FB1Time)
                draw_stimuli(FB1Components, FB1Time, t, frameN)

                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in FB1Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                #win.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
                #win.saveMovieFrames('FB1.jpg')  # save with a descriptive and unique filename. 

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "FB1"-------
            # record feedback S1 end time
            Fb1End = ExperimentClock.getTime()

            for thisComponent in FB1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "FB1" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            # ------Prepare to start Routine "IStageI"-------
            t = 0
            IStageIClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(IStageItime)
            # update component parameters for each repeat
            # tell client whether they missed or unpaired, if so, then use fixation 補滿10secs. Otherwise, fixation shows 2s
            if oops == True or (len(message_ret_data) == 0 and PracticeFlag == False):
                continueRoutine = False

            # keep track of which components have finished
            IStageIComponents = [textIStageI]
            for thisComponent in IStageIComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record IStageI on time
            IStageIon = ExperimentClock.getTime()
            
            # -------Start Routine "IStageI"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = IStageIClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *textIStageI* updates
                if t >= 0.0 and textIStageI.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    textIStageI.tStart = t
                    textIStageI.frameNStart = frameN  # exact frame index
                    textIStageI.setAutoDraw(True)
                frameRemains = 0.0 + int(IStageItime) - win.monitorFramePeriod * 0.75  # most of one frame period left
                if textIStageI.status == STARTED and t >= frameRemains:
                    textIStageI.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running

                for thisComponent in IStageIComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "IStageI"-------

            # record IStageI end time
            IStageIoff = ExperimentClock.getTime()

            for thisComponent in IStageIComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            routineTimer.reset()
         
            # ------Prepare to start Routine "DEC2"-------
            t = 0
            DEC2Clock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(DEC2Time)
            # update component parameters for each repeat
            key_resp_DEC2 = event.BuilderKeyResponse()

            if oops == True or (len(message_ret_data) == 0 and PracticeFlag == False):
                continueRoutine = False
            else:
            	#stimuli_setting(stage, role, partner, counterbalance)
                stimuli_setting(2, role_alphabet, partnerID, exc_stage1)

            # keep track of which components have finished
            DEC2Components = [img_PayoffMatrix, textPartner, textYou, textX, textY, textSpace1, textSpace2, textSpace3, textSpace4, textSpace5, textSpace6, textSpace7, textSpace8]
            for thisComponent in DEC2Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record on distribution decesion time
            Dec2on = ExperimentClock.getTime()

            delay_ISIEndS1_Dec2on = float((Dec2on - ISIEndS1) - FB1Time - IStageItime)

            # -------Start Routine "DEC2"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = DEC2Clock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # draw_stimuli(DEC2Time)
                draw_stimuli(DEC2Components, DEC2Time, t, frameN)
                
                # *key_resp_DEC2* updates
                if t >= 0.0 and key_resp_DEC2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_DEC2.tStart = t
                    key_resp_DEC2.frameNStart = frameN  # exact frame index
                    key_resp_DEC2.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_DEC2.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                frameRemains = 0.0 + int(DEC2Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if key_resp_DEC2.status == STARTED and t >= frameRemains:
                    key_resp_DEC2.status = FINISHED
                if key_resp_DEC2.status == STARTED:
                    theseKeys = event.getKeys(keyList=['1', '2'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        key_resp_DEC2.keys = theseKeys[-1]  # just the last key pressed
                        key_resp_DEC2.rt = key_resp_DEC2.clock.getTime()
                        # a response ends the routine
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in DEC2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                #win.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
                #win.saveMovieFrames('DEC2.jpg')  # save with a descriptive and unique filename. 

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "DEC2"-------
            for thisComponent in DEC2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)

            # record end distribution decesion time
            Dec2End = ExperimentClock.getTime()

            # calculate how much time to compensate in DEC2
            patch_Dec2 = float(DEC2Time - (Dec2End-Dec2on))

            # check responses
            if key_resp_DEC2.keys in ['', [], None]:  # No response was made
                key_resp_DEC2.keys=10000

            # record subjuct's key response
            subject_choiceS2_key = key_resp_DEC2.keys

            # trans(role, stage, subject_choice_key, counterbalance, group, partner)
            tra2 = trans(role_alphabet, 2, subject_choiceS2_key, exc_stage1, group_num, partnerID)

            # the Routine "DEC2" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "ReceivingDataWait"-------
            waitTS2 = 0
            AllianceCheckWaitClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat
            if PracticeFlag == False:
                message_tra2 = json.dumps(tra2).encode('utf-8')
                s.sendall(message_tra2)
            else:
            	continueRoutine = False

            message_ret_data2 = []
            # keep track of which components have finished
            AllianceCheckWaitComponents = [textWait]
            for thisComponent in AllianceCheckWaitComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # -------Start Routine "ReceivingDataWait"-------
            while continueRoutine and waitTS2 <= 10:
                # get current time
                waitTS2 = AllianceCheckWaitClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *textWait* updates
                if waitTS2 >= 0.0 and textWait.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    textWait.tStart = waitTS2
                    textWait.frameNStart = frameN  # exact frame index
                    textWait.setAutoDraw(True)
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
    
                ### Tcpip socket (client part) ###
                # receive ret_data only when data exists
                infds, outfds, errfds = select.select(inout, inout, [], 5)
                if len(infds) != 0:
                    message_ret_data2 = s.recv(1024)
                    message_ret_data2 = message_ret_data2.decode()
                    break
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in AllianceCheckWaitComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "ReceivingDataWait"-------
            for thisComponent in AllianceCheckWaitComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
    
            # the Routine "AllianceCheckWait" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            # ------Prepare to start Routine "TRA2"-------
            t = 0
            TRA2Clock.reset()  # clock
            frameN = -1
            continueRoutine = True
            #print(message_ret_data2)

            whoMissed2 = ''
            if PracticeFlag == False:
                if oops == True:
                    textTRA2.setText(str(whoMissed))
                    data2_clients = json.loads(message_ret_data2)
                # if escape from transmission loop in tra1
                elif len(message_ret_data) == 0: 
                    # make sure whether client catch previous data (one data len approximate 215)
                    if len(message_ret_data2) >= 600:
                        idx = message_ret_data2.find('[', 1)
                        # prevent Extra data error
                        data2_clients = json.loads(message_ret_data2[idx:])
                    else:
                	    data2_clients = json.loads(message_ret_data2)
                    stage2_choice = 'TRA1delay'
                    textTRA2.setText('Transmission Delay...')
                # if escape from transmission loop in tra2
                elif len(message_ret_data2) == 0:
                    stage2_choice = 'TRA2delay'
                    textTRA2.setText('Transmission Delay...')
                else:
                    ### Tcpip socket (client part) ###
                    data2_clients = json.loads(message_ret_data2)

                    # check whether someone missed
                    for k in range(len(data2_clients)):
                        if data2_clients[k][str(list(data2_clients[k].keys())[1])] == 'Missed':
                            for q in range(0, len(groupMember_dict)):
                                if 'trialp' + str(groupMember_dict[q].lower()) in data2_clients[k]:
                                    missedCountList[q] += 1
    
                                    # check whether that missing guy is me or my partner
                                    if str(groupMember_dict[q].lower()) == str(role_alphabet) or str(groupMember_dict[q]) == str(partnerID):
                                        oops2 = True
                                        whoMissed2 += 'ID ' + str(groupMember_dict[q]) + ' Missing #' + str(missedCountList[q]) + '\n'
            else:
                # check practice mode missing
                if subject_choice_key == 10000:
                    textTRA2.setText(str(whoMissed))

                elif subject_choiceS2_key == 10000:
            	    missedCount += 1
            	    oops2 = True
            	    whoMissed2 += 'ID ' + str(role_alphabet.capitalize()) + ' Missing #' + str(missedCount) + '\n'
                
            if oops2 == True:
                textTRA2.setText(str(whoMissed2))
            
            TRA2Components = [textTRA2]
            for thisComponent in TRA2Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record ISI on time  # adjust according position in lastrun
            ISIOnS2 = ExperimentClock.getTime()
            
            # calculate how much time to cut, due to tral transimission delay
            # escape from transmission loop
            if (len(message_ret_data2) == 0 and PracticeFlag == False) or waitTS2 > 10:  # 變成負數
            	delay_tra2 = float(ISIOnS2 - Dec2End) - waitTS2
            else:
                delay_tra2 = float(ISIOnS2 - Dec2End)
            
            # TRA2 time
            if (len(message_ret_data) == 0 or len(message_ret_data2) == 0) and PracticeFlag == False:
            	TRA2_duration = TRA2Time + patch_Dec2 - delay_ISIEndS1_Dec2on - delay_tra2 - 2 # 再扣兩秒
            else:
                TRA2_duration = TRA2Time + patch_Dec2 - delay_ISIEndS1_Dec2on - delay_tra2
            
            # -------Start Routine "TRA2"-------
            while continueRoutine:
                # get current time
                t = TRA2Clock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *textTRA2* updates
                if t >= 0.0 and textTRA2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    textTRA2.tStart = t
                    textTRA2.frameNStart = frameN  # exact frame index
                    textTRA2.setAutoDraw(True)
                frameRemains = 0.0 + TRA2_duration- win.monitorFramePeriod * 0.75  # most of one frame period left
                if textTRA2.status == STARTED and t >= frameRemains:
                    textTRA2.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in TRA2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "TRA2"-------
            # record ISI end time
            ISIEndS2 = ExperimentClock.getTime()
            for thisComponent in TRA2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "TRA2" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            textTRA2.setText('+')
            
            # ------Prepare to start Routine "FB2"-------
            t = 0
            FB2Clock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(FB2Time)
            
            if oops2 == True or oops == True or ((len(message_ret_data) == 0 or len(message_ret_data2) == 0) and PracticeFlag == False):
                continueRoutine = False
                reward = 0
                partner_reward = 0
            else:
              # create data client list contains 4 players for practice mode
                data2_clients_list = []
                for k in range(0, len(groupMember_dict)):
                    r = groupMember_dict[k].lower()
                    choiceList_fb2 = ['1', '2']
                    # trans(role, stage, subject_choice_key, counterbalance, group, partner)
                    data2_clients_list.append(trans(r, 2, choiceList_fb2[int((currentTrial - 1 ) % 2)], 0, user_fields[k], groupMember_dict[[j for j, e in enumerate(user_fields) if e == user_fields[k] and j != k][0]]))
                
               # replace with data2_clients while it's online version
                if PracticeFlag == False:
                    for y in range(len(data2_clients)):
                        data2_client = data2_clients[y]  
        
            	        # who's in the data2_clients list
                        for z in range(len(data2_clients)):
                            r = groupMember_dict[z].lower()    
        
                            if 'trialp'+str(r) in data2_client:
                                data2_clients_list[z] = data2_client
                # player's data
                else:
                    data2_clients_list[role_idx] = trans(role_alphabet, 2, subject_choiceS2_key, exc_stage1, group_num, partnerID)

                field_choice_pair = stimuli_setting(2, role_alphabet, partnerID, exc_stage1, role_idx=role_idx, partner_idx=partner_idx) # no failed commu in stage2

                # assign_reward(data2_clients_list, role_idx, partner_idx, role, partner, counterbalance):
                reward = assign_reward(data2_clients_list, role_idx, partner_idx, role_alphabet, partnerID, exc_stage1)[0]
                partner_reward = assign_reward(data2_clients_list, role_idx, partner_idx, role_alphabet, partnerID, exc_stage1)[1]

            runReward += reward
            # update component parameters for each repeat
            # keep track of which components have finished
            FB2Components = [img_circle, img_selfFrame, img_oppoFrame, img_PayoffMatrix, textPartner, textYou, textX, textY, textSpace1, textSpace2, textSpace3, textSpace4, textSpace5, textSpace6, textSpace7, textSpace8]
            for thisComponent in FB2Components:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # record DistributionResult on time
            Fb2on = ExperimentClock.getTime()
            
            # -------Start Routine "FB2"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = FB2Clock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                if t >= 0.0 and img_circle.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    img_circle.tStart = t
                    img_circle.frameNStart = frameN  # exact frame index
                    img_circle.setAutoDraw(True)
                frameRemains = 0.0 + int(FB2Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if img_circle.status == STARTED and t >= frameRemains:
                    img_circle.setAutoDraw(False)

                # *img_selfFrame* updates
                if t >= 0.0 and img_selfFrame.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    img_selfFrame.tStart = t
                    img_selfFrame.frameNStart = frameN  # exact frame index
                    img_selfFrame.setAutoDraw(True)
                frameRemains = 0.0 + int(FB2Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if img_selfFrame.status == STARTED and t >= frameRemains:
                    img_selfFrame.setAutoDraw(False)

                # *img_oppoFrame* updates
                if t >= 0.0 and img_oppoFrame.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    img_oppoFrame.tStart = t
                    img_oppoFrame.frameNStart = frameN  # exact frame index
                    img_oppoFrame.setAutoDraw(True)
                frameRemains = 0.0 + int(FB2Time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if img_oppoFrame.status == STARTED and t >= frameRemains:
                    img_oppoFrame.setAutoDraw(False)

                # draw_stimuli(FB2Time)
                draw_stimuli(FB2Components, FB2Time, t, frameN)

                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in FB2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                #win.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
                #win.saveMovieFrames('FB2.jpg')  # save with a descriptive and unique filename. 

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "FB2"-------
            # record DistributionResult End time
            Fb2End = ExperimentClock.getTime() 

            for thisComponent in FB2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "FB2" was not non-slip safe, so reset the non-slip timer
            
            # ------Prepare to start Routine "ITI6s"-------
            t = 0
            ITI6sClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # update component parameters for each repeat

            if oops == True:
                textITI.setText(str(whoMissed))

            # keep track of which components have finished
            ITI6sComponents = [textITI]
            for thisComponent in ITI6sComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # record ITI on time  # adjust according position in lastrun
            ITIOn = ExperimentClock.getTime()

            # time control using standard time
            if currentTrial in PartnerScreenTrialList:
                ExpectTime = 18 + showPartnerScreenTime + standardTime
            else:
                ExpectTime = 18 + standardTime
            for k in range(trialCount-1):
                dur = trialDurList[k]
                ExpectTime = dur + ExpectTime
            ActualTime = ExperimentClock.getTime()
            timeGap = float(ActualTime - ExpectTime)
            
            # ITI6s time
            ITI_duration = float(ITITime - timeGap)

            # -------Start Routine "ITI6s"-------
            while continueRoutine:
                # get current time
                t = ITI6sClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *textITI* updates
                if t >= 0.0 and textITI.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    textITI.tStart = t
                    textITI.frameNStart = frameN  # exact frame index
                    textITI.setAutoDraw(True)
                frameRemains = float(ITI_duration) - win.monitorFramePeriod * 0.5 # most of one frame period left
                if textITI.status == STARTED and t >= frameRemains:
                    textITI.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ITI6sComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "ITI6s"-------
            # record ITI on time   
            ITIEnd = ExperimentClock.getTime()

            for thisComponent in ITI6sComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)

            textITI.setText('+')

            thisExp.nextEntry()
            
            partner_dict = {'A' : 1, 'B' : 2, 'C' : 3, 'D' : 4}
            trials.addData('startTrialT',startTrialT)
            trials.addData('Dec1End',Dec1End)
            trials.addData('patch_Dec1',patch_Dec1)
            trials.addData('delay_tra1',delay_tra1)
            trials.addData('ISIOnS1',ISIOnS1)
            trials.addData('ISIEndS1',ISIEndS1)
            trials.addData('Fb1On',Fb1On)
            trials.addData('Fb1End',Fb1End)
            trials.addData('IStageIon',IStageIon)
            trials.addData('IStageIoff',IStageIoff)
            trials.addData('Dec2on',Dec2on)
            trials.addData('Dec2End',Dec2End)
            trials.addData('patch_Dec2',patch_Dec2)
            trials.addData('delay_ISIEndS1_Dec2on',delay_ISIEndS1_Dec2on)
            trials.addData('delay_tra2',delay_tra2)
            trials.addData('ISIOnS2',ISIOnS2)
            trials.addData('ISIEndS2',ISIEndS2)
            trials.addData('Fb2on',Fb2on)
            trials.addData('Fb2End',Fb2End)
            trials.addData('timeGap',timeGap)
            trials.addData('ITIOn',ITIOn)
            trials.addData('ITIEnd',ITIEnd)
            trials.addData('ExpectEndTime',ExpectTime+ITITime)
            trials.addData('player',role)
            # trials.addData('sequence',pair)
            trials.addData('currentRun',currentRun)
            trials.addData('currentTrial',currentTrial)
            trials.addData('counterbalance',exc_stage1)

            trials.addData('value1',space1)
            trials.addData('value2',space2)
            trials.addData('value3',space3)
            trials.addData('value4',space4)
            trials.addData('value5',space5)
            trials.addData('value6',space6)
            trials.addData('value7',space7)
            trials.addData('value8',space8)
            trials.addData('key1BigValue',key1BigValue)
            trials.addData('key2BigValue',key2BigValue)
            
            #trials.addData('stage1_choice',str(stage1_choice))
            #if oops == False:
            #    trials.addData('stage2_choice',str(stage2_choice))
            #else:
            #    trials.addData('stage2_choice','Missed')

            trials.addData('key_resp_DEC1.keys',subject_choice_key)
            if key_resp_DEC1.keys != 10000:   
                trials.addData('key_resp_DEC1.rt', key_resp_DEC1.rt)
            else:
                trials.addData('key_resp_DEC1.rt', '10000')

            trials.addData('key_resp_DEC2.keys',subject_choiceS2_key)
            if key_resp_DEC2.keys != 10000:
                trials.addData('key_resp_DEC2.rt', key_resp_DEC2.rt)
            else:
                trials.addData('key_resp_DEC2.rt', '10000')

            trials.addData('partnerABCD', partner_dict[str(partnerID)])

            if oops == False:
                trials.addData('partner_key_resp_DEC1', partner_stage1_choice)
            else:
                trials.addData('partner_key_resp_DEC1', '10000')

            if oops == False and oops2 == False:
                trials.addData('partner_key_resp_DEC2', partner_stage2_choice)
            else:
                trials.addData('partner_key_resp_DEC2','10000')

            trials.addData('reward',reward)
            trials.addData('partner_reward',partner_reward)
            
        # completed 3 repeats of 'trials'
        
    # completed 8 repeats of 'blocks'

    # ------Prepare to start Routine "EndingRun4s"-------
    t = 0
    TRA2Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.reset()
    routineTimer.add(EndingRunTime)
    # update component parameters for each repeat
    # keep track of which components have finished
    TRA2Components = [textTRA2]
    for thisComponent in TRA2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #　change showing text
    print('Run',currentRun,'reward:',runReward)
    textTRA2.setText('Run Ending\nreward : ' + str(runReward))

    totalReward += runReward

    # record ITI on time  # adjust according position in lastrun
    EndingRunrOn = ExperimentClock.getTime()
        
    # -------Start Routine "EndingRun4s"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = TRA2Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
            
        # *textTRA2* updates
        if t >= 0.0 and textTRA2.status == NOT_STARTED:
            # keep track of start time/frame for later
            textTRA2.tStart = t
            textTRA2.frameNStart = frameN  # exact frame index
            textTRA2.setAutoDraw(True)
        frameRemains = 0.0 + EndingRunTime- win.monitorFramePeriod * 0.75  # most of one frame period left
        if textTRA2.status == STARTED and t >= frameRemains:
            textTRA2.setAutoDraw(False)
            
        # check for quit (typically the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
            
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TRA2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
            
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        
    # -------Ending Routine "EndingRun4s"-------

    # record ITI on time  
    EndingRunrEnd = ExperimentClock.getTime()

    for thisComponent in TRA2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    #　change showing text
    textTRA2.setText('+')

    # the Routine "ITI6s" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # store data for trials (time)
    trials.addData('EndingRunrOn',EndingRunrOn)
    trials.addData('EndingRunrEnd',EndingRunrEnd)

    # completed 5 repeats of 'runs'
    win.close()

    # close socket connection in the end of run
    if PracticeFlag == False:
        s.close()
    
    # Force Save data & log after each run
    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    logging.flush()
# completed 6 repeats of 'runNum'

print('Your total reward :',totalReward)
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
