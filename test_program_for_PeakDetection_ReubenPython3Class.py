# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 01/03/2026

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

###########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
###########################################################

###########################################################
from CSVdataLogger_ReubenPython3Class import *
from EntryListWithBlinking_ReubenPython2and3Class import *
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import traceback
import numpy
import math
import keyboard

from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.VoltageRatioInput import *
###########################################################

########################################################### For peak detection
import scipy.signal
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):
    
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]
        
            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":
    
                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":
    
                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0
        
                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % SinusoidalInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue
        
                A = abs(MaxValue - MinValue)
                P = Period
    
                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":
    
                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
                
                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################
            
            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            return -11111.0
            #traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

######################################################################################################
######################################################################################################
def UpdateFrequencyCalculation_MainThread_Filtered():

    global CurrentTime_CalculatedFromMainThread
    global LastTime_CalculatedFromMainThread
    global LoopCounter_CalculatedFromMainThread
    global DataStreamingDeltaT_CalculatedFromMainThread
    global DataStreamingFrequency_CalculatedFromMainThread_Filtered
    global LowPassFilterForDictsOfLists_Object

    try:
        DataStreamingDeltaT_CalculatedFromMainThread = CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread

        if DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
            DataStreamingFrequency_CalculatedFromMainThread = 1.0/DataStreamingDeltaT_CalculatedFromMainThread
            VariablesDict_Temp = LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromMainThread", [DataStreamingFrequency_CalculatedFromMainThread])]))
            DataStreamingFrequency_CalculatedFromMainThread_Filtered = VariablesDict_Temp["DataStreamingFrequency_CalculatedFromMainThread"]["Filtered_MostRecentValuesList"][0]

            if DataStreamingFrequency_CalculatedFromMainThread_Filtered <= 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_Filtered = 0.001

        LastTime_CalculatedFromMainThread = CurrentTime_CalculatedFromMainThread
        LoopCounter_CalculatedFromMainThread = LoopCounter_CalculatedFromMainThread + 1
        
    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation_MainThread_Filtered, exceptions: %s" % exceptions)
        traceback.print_exc()
######################################################################################################
######################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

######################################################################################################
######################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
######################################################################################################
######################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global CurrentTime_CalculatedFromMainThread
    global DataStreamingFrequency_CalculatedFromMainThread_Filtered

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    global DebuggingInfo_Label
    global voltageRatioInput0_Value
    global PeakMaxDataList_X
    global PeakMaxDataList_Y
    global PeakMinDataList_X
    global PeakMinDataList_Y
    global YaxisData
    global LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger

    global DataDerivative_Threshold

    if USE_GUI_FLAG == 1:

        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            DebuggingInfo_Label["text"] = "MainThread, Time: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(CurrentTime_CalculatedFromMainThread, 0, 3) +\
                                            "\t\t\tFrequency: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DataStreamingFrequency_CalculatedFromMainThread_Filtered, 0, 3) +\
                                            "\nDataDerivative_Threshold: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DataDerivative_Threshold, 0, 3) +\
                                            "\nvoltageRatioInput0_Value: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(voltageRatioInput0_Value, 0, 3) +\
                                            "\nLowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger: " + str(LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger) +\
                                            "\nYaxisData: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(YaxisData, 0, 1)

            if len(PeakMaxDataList_X) > 0 and len(PeakMaxDataList_Y) > 0:
                DebuggingInfo_Label["text"] = DebuggingInfo_Label["text"] + \
                                                "\n" + "PeakMaxDataList: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(PeakMaxDataList_X[0], 0, 3) + ", " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(PeakMaxDataList_Y[0], 0, 3) + "]"
                
            if len(PeakMinDataList_X) > 0 and len(PeakMinDataList_X) > 0:
                DebuggingInfo_Label["text"] = DebuggingInfo_Label["text"] + \
                                                "\n" + "PeakMinDataList: [" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(PeakMinDataList_X[0], 0, 3) + ", " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(PeakMinDataList_Y[0], 0, 3) + "]"
                   
            #########################################################

            #########################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if EntryListWithBlinking_OPEN_FLAG == 1:
                EntryListWithBlinking_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_Object.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_IsSavingFlag

    print("ExitProgram_Callback event fired!")

    if CSVdataLogger_IsSavingFlag == 0:
        EXIT_PROGRAM_FLAG = 1
    else:
        print("ExitProgram_Callback, ERROR! Still saving data.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_PeakDetection_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_CSVdataLogger
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_CSVdataLogger = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global DebuggingInfo_Label
    DebuggingInfo_Label = Label(Tab_MainControls, text="DebuggingInfo_Label", width=120, font=("Helvetica", 10))
    DebuggingInfo_Label.grid(row=10, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    ######################################################################################################
    ######################################################################################################
    global PeriodicInputGuiFrame
    PeriodicInputGuiFrame = Frame(Tab_MainControls)
    PeriodicInputGuiFrame.grid(row=1, column=0, padx=1, pady=1, rowspan=1, columnspan=1, sticky='w')
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    global PeriodicInput
    global PeriodicInput_Radiobutton_SelectionVar
    PeriodicInput_Radiobutton_SelectionVar = StringVar()
    PeriodicInput_Radiobutton_SelectionVar.set(PeriodicInput)

    global PeriodicInput_RadioButtonObjectsList
    PeriodicInput_RadioButtonObjectsList = list()
    for Index, PeriodicInputString in enumerate(PeriodicInput_AcceptableValues):
        PeriodicInput_RadioButtonObjectsList.append(Radiobutton(PeriodicInputGuiFrame,
                                                      text=PeriodicInputString,
                                                      state="normal",
                                                      width=15,
                                                      anchor="w",
                                                      variable=PeriodicInput_Radiobutton_SelectionVar,
                                                      value=PeriodicInputString,
                                                      command=lambda name=PeriodicInputString: PeriodicInput_Radiobutton_Response(name)))
        PeriodicInput_RadioButtonObjectsList[Index].grid(row=0, column=Index, padx=1, pady=1, columnspan=1, rowspan=1)
    ######################################################################################################
    ######################################################################################################

    #################################################
    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.CreateGUIobjects(TkinterParent=Tab_CSVdataLogger)
    #################################################
    #################################################

    #################################################
    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.CreateGUIobjects(TkinterParent=Tab_MainControls)
    #################################################
    #################################################

    #################################################
    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.CreateGUIobjects(TkinterParent=Tab_MyPrint)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

######################################################################################################
######################################################################################################
def PeriodicInput_Radiobutton_Response(name):
    global PeriodicInput_Radiobutton_SelectionVar
    global PeriodicInput
    global PeriodicInput_NeedsToBeChangedFlag

    #print("name: " + name)

    PeriodicInput = PeriodicInput_Radiobutton_SelectionVar.get()
    PeriodicInput_NeedsToBeChangedFlag = 1
    print("PeriodicInput set to: " + PeriodicInput)
######################################################################################################
######################################################################################################

##########################################################################################################
##########################################################################################################
def onVoltageRatioInput0_VoltageRatioChange(self, voltageRatio):
    global voltageRatioInput0_Value

    voltageRatioInput0_Value = voltageRatio
    #print("VoltageRatio [0]: " + str(voltageRatio))
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def onVoltageRatioInput0_Attach(self):
    print("Attach [0]!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def onVoltageRatioInput0_Detach(self):
    print("Detach [0]!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def onVoltageRatioInput0_Error(self, code, description):
    print("Code [0]: " + ErrorEventCode.getName(code))
    print("Description [0]: " + str(description))
    print("----------")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def InitializePhidgets():
    global voltageRatioInput0

    try:
        voltageRatioInput0 = VoltageRatioInput()

        voltageRatioInput0.setIsHubPortDevice(True)
        voltageRatioInput0.setHubPort(0)

        voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioInput0_VoltageRatioChange)
        voltageRatioInput0.setOnAttachHandler(onVoltageRatioInput0_Attach)
        voltageRatioInput0.setOnDetachHandler(onVoltageRatioInput0_Detach)
        voltageRatioInput0.setOnErrorHandler(onVoltageRatioInput0_Error)

        voltageRatioInput0.openWaitForAttachment(5000)
        voltageRatioInput0.setDataInterval(10)
        voltageRatioInput0.setVoltageRatioChangeTrigger(0)

    except PhidgetException as ex:
        traceback.print_exc()
        print("InitializePhidgets, PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_LowPassFilterForDictsOfLists_FLAG
    USE_LowPassFilterForDictsOfLists_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_EntryListWithBlinking_FLAG
    USE_EntryListWithBlinking_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_Keyboard_FLAG
    USE_Keyboard_FLAG = 1

    global USE_VINThub_FLAG
    USE_VINThub_FLAG = 0

    global FindPeaksFlag
    FindPeaksFlag = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 3

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_EntryListWithBlinking
    global GUI_COLUMN_EntryListWithBlinking
    global GUI_PADX_EntryListWithBlinking
    global GUI_PADY_EntryListWithBlinking
    global GUI_ROWSPAN_EntryListWithBlinking
    global GUI_COLUMNSPAN_EntryListWithBlinking
    GUI_ROW_EntryListWithBlinking = 2

    GUI_COLUMN_EntryListWithBlinking = 0
    GUI_PADX_EntryListWithBlinking = 1
    GUI_PADY_EntryListWithBlinking = 1
    GUI_ROWSPAN_EntryListWithBlinking = 1
    GUI_COLUMNSPAN_EntryListWithBlinking = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 4

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global LoopCounter_CalculatedFromMainThread
    LoopCounter_CalculatedFromMainThread = 0

    global CurrentTime_CalculatedFromMainThread
    CurrentTime_CalculatedFromMainThread = -11111.0

    global StartingTime_CalculatedFromMainThread
    StartingTime_CalculatedFromMainThread = -11111.0

    global LastTime_CalculatedFromMainThread
    LastTime_CalculatedFromMainThread = -11111.0

    global DataStreamingFrequency_CalculatedFromMainThread
    DataStreamingFrequency_CalculatedFromMainThread = -1

    global DataStreamingFrequency_CalculatedFromMainThread_Filtered
    DataStreamingFrequency_CalculatedFromMainThread_Filtered = -1

    global DataStreamingDeltaT_CalculatedFromMainThread
    DataStreamingDeltaT_CalculatedFromMainThread = -1

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_CSVdataLogger
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global NewValue_Raw
    NewValue_Raw = 0.0

    global NewValue_Filtered
    NewValue_Filtered = 0.0

    global Threshold0to1
    Threshold0to1 = 0.001

    global MinimumDistance
    MinimumDistance = 2

    global IsThresholdAbsolute
    IsThresholdAbsolute = True

    global PeakDetectionHistoryListLength
    PeakDetectionHistoryListLength = 100 #Prominence doesn't work if this is too low (10)

    global YaxisData
    YaxisData = []

    global DataList
    DataList = numpy.zeros((int(PeakDetectionHistoryListLength), 2), float)
    
    global DataDerivative
    DataDerivativeList = 0.0

    global DataDerivative_Threshold
    DataDerivative_Threshold = -10.0
    
    global LowPassFilterForDictsOfLists_UseMedianFilterFlag_DataDerivative
    LowPassFilterForDictsOfLists_UseMedianFilterFlag_DataDerivative = 0

    global LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative #HAS TO BE HEAVILY FILTERED TO GET THE PEAK-DETECTION-TUNING RIGHT
    LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative = 0.7  # new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

    global PeakMaxDataList_X
    PeakMaxDataList_X = []

    global PeakMaxDataList_Y
    PeakMaxDataList_Y = []
    
    global PeakMinDataList_X
    PeakMinDataList_X = []

    global PeakMinDataList_Y
    PeakMinDataList_Y = []

    global InvertDataFlag
    InvertDataFlag = 0

    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["GUI", "VINThub", "Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput
    PeriodicInput = "Sine"

    global PeriodicInput_MinValue
    PeriodicInput_MinValue = -3.0

    global PeriodicInput_MaxValue
    PeriodicInput_MaxValue = 3.0

    global PeriodicInput_Period
    PeriodicInput_Period = 1.0

    global ScipySignalFindPeaks_height
    ScipySignalFindPeaks_height = 0.4

    global ScipySignalFindPeaks_threshold
    ScipySignalFindPeaks_threshold = 0.0

    global ScipySignalFindPeaks_distance
    ScipySignalFindPeaks_distance = 1

    global ScipySignalFindPeaks_prominence
    ScipySignalFindPeaks_prominence = 1e-3

    global ScipySignalFindPeaks_width
    ScipySignalFindPeaks_width = 0.0

    global ScipySignalFindPeaks_wlen
    ScipySignalFindPeaks_wlen = 2

    global ScipySignalFindPeaks_rel_height
    ScipySignalFindPeaks_rel_height = 0.0

    global ScipySignalFindPeaks_plateau_size
    ScipySignalFindPeaks_plateau_size = 0.0
    #################################################
    #################################################

    ####################################################
    ####################################################
    global LowPassFilterForDictsOfLists_Object

    global LowPassFilterForDictsOfLists_OPEN_FLAG
    LowPassFilterForDictsOfLists_OPEN_FLAG = -1

    global LowPassFilterForDictsOfLists_MostRecentDict
    LowPassFilterForDictsOfLists_MostRecentDict = dict()

    global LowPassFilterForDictsOfLists_UseMedianFilterFlag
    LowPassFilterForDictsOfLists_UseMedianFilterFlag = 0

    global LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda #HAS TO BE HEAVILY FILTERED TO GET THE PEAK-DETECTION-TUNING RIGHT
    LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda = 0.2  # new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

    global LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger
    LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger = 0#-9 Could be negative
    ####################################################
    ####################################################

    #################################################
    #################################################
    global CSVdataLogger_Object

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0

    global CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread
    CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = -11111.0

    global CSVdataLogger_MostRecentDict_AcceptNewDataFlag
    CSVdataLogger_MostRecentDict_AcceptNewDataFlag = -1

    global CSVdataLogger_MostRecentDict_IsSavingFlag
    CSVdataLogger_MostRecentDict_IsSavingFlag = -1

    global CSVdataLogger_MostRecentDict_DataQueue_qsize
    CSVdataLogger_MostRecentDict_DataQueue_qsize = -1

    global CSVdataLogger_MostRecentDict_VariableNamesForHeaderList
    CSVdataLogger_MostRecentDict_VariableNamesForHeaderList = []

    global CSVdataLogger_MostRecentDict_FilepathFull
    CSVdataLogger_MostRecentDict_FilepathFull = ""

    global CSVdataLogger_HeaderWrittenYetFlag
    CSVdataLogger_HeaderWrittenYetFlag = 0

    global CSVdataLogger_IsSavingFlag
    CSVdataLogger_IsSavingFlag = 0

    global CSVdataLogger_CSVfile_DirectoryPath
    CSVdataLogger_CSVfile_DirectoryPath = os.path.join(os.getcwd(), "CSVfiles")

    #################################################
    global CSVdataLogger_SetupDict_VariableNamesForHeaderList
    CSVdataLogger_SetupDict_VariableNamesForHeaderList = ["Time",
                                                        "NewValue_Raw",
                                                        "NewValue_Filtered"]
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object

    global EntryListWithBlinking_OPEN_FLAG
    EntryListWithBlinking_OPEN_FLAG = -1

    global EntryListWithBlinking_MostRecentDict
    EntryListWithBlinking_MostRecentDict = dict()

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber = 0

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = -1

    EntryWidth = 10
    LabelWidth = 80
    FontSize = 8
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_Object

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = -1

    global LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global VINThub_OPEN_FLAG
    VINThub_OPEN_FLAG = 0

    global voltageRatioInput0

    global voltageRatioInput0_Value
    voltageRatioInput0_Value = -1

    global voltageRatioInput0_Value_Raw
    voltageRatioInput0_Value_Raw = -1

    global voltageRatioInput0_Value_Filtered
    voltageRatioInput0_Value_Filtered = -1
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global LowPassFilterForDictsOfLists_DictOfVariableFilterSettings
    LowPassFilterForDictsOfLists_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromMainThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.5)])),
                                                                      ("voltageRatioInput0_Value", dict([("UseMedianFilterFlag", LowPassFilterForDictsOfLists_UseMedianFilterFlag), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda)])),
                                                                      ("DataDerivative", dict([("UseMedianFilterFlag", LowPassFilterForDictsOfLists_UseMedianFilterFlag_DataDerivative), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative)]))])

    if USE_LowPassFilterForDictsOfLists_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            LowPassFilterForDictsOfLists_Object = LowPassFilterForDictsOfLists_ReubenPython2and3Class(dict([("DictOfVariableFilterSettings", LowPassFilterForDictsOfLists_DictOfVariableFilterSettings)]))
            LowPassFilterForDictsOfLists_OPEN_FLAG = LowPassFilterForDictsOfLists_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_LowPassFilterForDictsOfLists_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if LowPassFilterForDictsOfLists_OPEN_FLAG != 1:
                print("Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global CSVdataLogger_GUIparametersDict
    CSVdataLogger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                            ("EnableInternal_MyPrint_Flag", 1),
                                            ("NumberOfPrintLines", 10),
                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                            ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                            ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                            ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                            ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                            ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    global CSVdataLogger_SetupDict
    CSVdataLogger_SetupDict = dict([("GUIparametersDict", CSVdataLogger_GUIparametersDict),
                                    ("NameToDisplay_UserSet", "CSVdataLogger"),
                                    ("CSVfile_DirectoryPath", CSVdataLogger_CSVfile_DirectoryPath),
                                    ("FileNamePrefix", "CSV_file_"),
                                    ("VariableNamesForHeaderList", CSVdataLogger_SetupDict_VariableNamesForHeaderList),
                                    ("MainThread_TimeToSleepEachLoop", 0.010),
                                    ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_Object = CSVdataLogger_ReubenPython3Class(CSVdataLogger_SetupDict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global EntryListWithBlinking_GUIparametersDict
    EntryListWithBlinking_GUIparametersDict = dict([("UseBorderAroundThisGuiObjectFlag", 0),
                                                    ("GUI_ROW", GUI_ROW_EntryListWithBlinking),
                                                    ("GUI_COLUMN", GUI_COLUMN_EntryListWithBlinking),
                                                    ("GUI_PADX", GUI_PADX_EntryListWithBlinking),
                                                    ("GUI_PADY", GUI_PADY_EntryListWithBlinking),
                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_EntryListWithBlinking),
                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_EntryListWithBlinking)])

    global EntryListWithBlinking_Variables_ListOfDicts
    EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "LowPassFilterForDictsOfLists_UseMedianFilterFlag"),("Type", "int"),("StartingVal", LowPassFilterForDictsOfLists_UseMedianFilterFlag),("MinVal", 0),("MaxVal", 1),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda"),("Type", "float"),("StartingVal", LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger"),("Type", "int"),("StartingVal", LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger),("MinVal", -100.0),("MaxVal", 100.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "InvertDataFlag"),("Type", "int"),("StartingVal", InvertDataFlag),("MinVal", 0),("MaxVal", 1),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "PeriodicInput_MinValue"),("Type", "float"),("StartingVal", PeriodicInput_MinValue),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "PeriodicInput_MaxValue"),("Type", "float"),("StartingVal", PeriodicInput_MaxValue),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "PeriodicInput_Period"),("Type", "float"),("StartingVal", PeriodicInput_Period),("MinVal", 0.01),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "PeakDetectionHistoryListLength"),("Type", "int"),("StartingVal", PeakDetectionHistoryListLength),("MinVal", 1.0),("MaxVal", 10000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "Threshold0to1"),("Type", "float"),("StartingVal", Threshold0to1),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "MinimumDistance"),("Type", "float"),("StartingVal", MinimumDistance),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "IsThresholdAbsolute"),("Type", "int"),("StartingVal", IsThresholdAbsolute),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_height"),("Type", "float"),("StartingVal", ScipySignalFindPeaks_height),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_threshold"),("Type", "float"),("StartingVal", ScipySignalFindPeaks_threshold),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_distance"),("Type", "int"),("StartingVal", ScipySignalFindPeaks_distance),("MinVal", 1),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_prominence"),("Type", "float"),("StartingVal", ScipySignalFindPeaks_prominence),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_width"),("Type", "float"),("StartingVal", ScipySignalFindPeaks_width),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_wlen"),("Type", "int"),("StartingVal", ScipySignalFindPeaks_wlen),("MinVal", 2),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_rel_height"),("Type", "float"),("StartingVal", ScipySignalFindPeaks_rel_height),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "ScipySignalFindPeaks_plateau_size"),("Type", "float"),("StartingVal", ScipySignalFindPeaks_plateau_size),("MinVal", 0.0),("MaxVal", 1000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative"),("Type", "float"),("StartingVal", LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                dict([("Name", "DataDerivative_Threshold"),("Type", "float"),("StartingVal", DataDerivative_Threshold),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

    global EntryListWithBlinking_SetupDict
    EntryListWithBlinking_SetupDict = dict([("GUIparametersDict", EntryListWithBlinking_GUIparametersDict),
                                          ("EntryListWithBlinking_Variables_ListOfDicts", EntryListWithBlinking_Variables_ListOfDicts),
                                          ("DebugByPrintingVariablesFlag", 0),
                                          ("LoseFocusIfMouseLeavesEntryFlag", 0)])

    if USE_EntryListWithBlinking_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            EntryListWithBlinking_Object = EntryListWithBlinking_ReubenPython2and3Class(EntryListWithBlinking_SetupDict)
            EntryListWithBlinking_OPEN_FLAG = EntryListWithBlinking_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_EntryListWithBlinking_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if EntryListWithBlinking_OPEN_FLAG != 1:
                print("Failed to open EntryListWithBlinking_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPrint_GUIparametersDict
    MyPrint_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_SetupDict
    MyPrint_SetupDict = dict([("NumberOfPrintLines", 10),
                                ("WidthOfPrintingLabel", 200),
                                ("PrintToConsoleFlag", 1),
                                ("LogFileNameFullPath", os.path.join(os.getcwd(), "TestLog.txt")),
                                ("GUIparametersDict", MyPrint_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_SetupDict)
            MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GraphCanvasWidth", 890),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Channel0", "Channel0_Derivative", "Channel0_PeaksMax", "Channel0_PeaksMin"]),
                                                                                                            ("MarkerSizeList", [3, 3, 3, 3]),
                                                                                                            ("LineWidthList", [3, 3, 0, 0]),
                                                                                                            ("ColorList", ["Gray", "Orange", "Blue", "Red"])])),
                                                            ("NumberOfDataPointToPlot", 50),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 20.0),
                                                            ("Y_min", -30.0),
                                                            ("Y_max", 30.0),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    if USE_VINThub_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            InitializePhidgets()
            
            VINThub_OPEN_FLAG = 1
        except:
            exceptions = sys.exc_info()[0]
            print("VINThub, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_VINThub_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if VINThub_OPEN_FLAG != 1:
                print("Failed to open VINThub.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_Keyboard_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
        Tab_MainControls = None
        Tab_CSVdataLogger = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("Starting main loop 'test_program_for_CSVdataLogger_ReubenPython3Class.")
    StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ####################################################
        ####################################################
        CurrentTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromMainThread
        ####################################################
        ####################################################

        ################################################### GET's
        ###################################################
        if CSVdataLogger_OPEN_FLAG == 1:
            CSVdataLogger_IsSavingFlag = CSVdataLogger_Object.IsSaving()
        else:
            CSVdataLogger_IsSavingFlag = 0
        ###################################################
        ###################################################

        #################################################### GET's
        ####################################################
        if CSVdataLogger_OPEN_FLAG == 1:

            CSVdataLogger_MostRecentDict = CSVdataLogger_Object.GetMostRecentDataDict()

            if "Time" in CSVdataLogger_MostRecentDict:
                CSVdataLogger_MostRecentDict_Time = CSVdataLogger_MostRecentDict["Time"]
                CSVdataLogger_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = CSVdataLogger_MostRecentDict["DataStreamingFrequency_CalculatedFromMainThread"]
                CSVdataLogger_MostRecentDict_AcceptNewDataFlag = CSVdataLogger_MostRecentDict["AcceptNewDataFlag"]
                CSVdataLogger_MostRecentDict_IsSavingFlag = CSVdataLogger_MostRecentDict["IsSavingFlag"]
                CSVdataLogger_MostRecentDict_DataQueue_qsize = CSVdataLogger_MostRecentDict["DataQueue_qsize"]
                CSVdataLogger_MostRecentDict_VariableNamesForHeaderList = CSVdataLogger_MostRecentDict["VariableNamesForHeaderList"]
                CSVdataLogger_MostRecentDict_FilepathFull = CSVdataLogger_MostRecentDict["FilepathFull"]

                #print("CSVdataLogger_MostRecentDict: " + str(CSVdataLogger_MostRecentDict))

        ####################################################
        ####################################################

        ####################################################
        ####################################################

        ################################################### GET's
        if EntryListWithBlinking_OPEN_FLAG == 1:

            EntryListWithBlinking_MostRecentDict = EntryListWithBlinking_Object.GetMostRecentDataDict()

            if "DataUpdateNumber" in EntryListWithBlinking_MostRecentDict and EntryListWithBlinking_MostRecentDict["DataUpdateNumber"] != EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last:
                EntryListWithBlinking_MostRecentDict_DataUpdateNumber = EntryListWithBlinking_MostRecentDict["DataUpdateNumber"]
                #print("DataUpdateNumber = " + str(EntryListWithBlinking_MostRecentDict_DataUpdateNumber) + ", EntryListWithBlinking_MostRecentDict: " + str(EntryListWithBlinking_MostRecentDict))

                if EntryListWithBlinking_MostRecentDict_DataUpdateNumber > 1:

                    if EntryListWithBlinking_MostRecentDict["PeakDetectionHistoryListLength"] != PeakDetectionHistoryListLength:
                        PeakDetectionHistoryListLength = EntryListWithBlinking_MostRecentDict["PeakDetectionHistoryListLength"]
                        DataList = numpy.zeros((int(PeakDetectionHistoryListLength), 2), float)

                    InvertDataFlag = EntryListWithBlinking_MostRecentDict["InvertDataFlag"]
                    LowPassFilterForDictsOfLists_UseMedianFilterFlag = EntryListWithBlinking_MostRecentDict["LowPassFilterForDictsOfLists_UseMedianFilterFlag"]
                    LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda = EntryListWithBlinking_MostRecentDict["LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda"]
                    LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger = EntryListWithBlinking_MostRecentDict["LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger"]

                    LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative = EntryListWithBlinking_MostRecentDict["LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative"]


                    if LowPassFilterForDictsOfLists_OPEN_FLAG == 1:
                        try:
                            LowPassFilterForDictsOfLists_DictOfVariableFilterSettings["voltageRatioInput0_Value"]["ExponentialSmoothingFilterLambda"] = LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda
                            LowPassFilterForDictsOfLists_DictOfVariableFilterSettings["voltageRatioInput0_Value"]["UseMedianFilterFlag"] = LowPassFilterForDictsOfLists_UseMedianFilterFlag
                            LowPassFilterForDictsOfLists_DictOfVariableFilterSettings["DataDerivative"]["ExponentialSmoothingFilterLambda"] = LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda_DataDerivative

                            LowPassFilterForDictsOfLists_Object.AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram(LowPassFilterForDictsOfLists_DictOfVariableFilterSettings)
                        except:
                            pass

                    PeriodicInput_MinValue = EntryListWithBlinking_MostRecentDict["PeriodicInput_MinValue"]
                    PeriodicInput_MaxValue = EntryListWithBlinking_MostRecentDict["PeriodicInput_MaxValue"]
                    PeriodicInput_Period = EntryListWithBlinking_MostRecentDict["PeriodicInput_Period"]

                    Threshold0to1 = EntryListWithBlinking_MostRecentDict["Threshold0to1"]
                    MinimumDistance = EntryListWithBlinking_MostRecentDict["MinimumDistance"]
                    IsThresholdAbsolute = EntryListWithBlinking_MostRecentDict["IsThresholdAbsolute"]

                    ScipySignalFindPeaks_height = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_height"]
                    ScipySignalFindPeaks_threshold = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_threshold"]
                    ScipySignalFindPeaks_distance = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_distance"]
                    ScipySignalFindPeaks_prominence = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_prominence"]
                    ScipySignalFindPeaks_width = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_width"]
                    ScipySignalFindPeaks_wlen = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_wlen"]
                    ScipySignalFindPeaks_rel_height = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_rel_height"]
                    ScipySignalFindPeaks_plateau_size = EntryListWithBlinking_MostRecentDict["ScipySignalFindPeaks_plateau_size"]

                    DataDerivative_Threshold = EntryListWithBlinking_MostRecentDict["DataDerivative_Threshold"]
        ###################################################

        ###################################################
        EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = EntryListWithBlinking_MostRecentDict_DataUpdateNumber
        ###################################################

        ####################################################
        ####################################################

        #################################################### GET's
        ####################################################
        if LowPassFilterForDictsOfLists_OPEN_FLAG == 1:
            LowPassFilterForDictsOfLists_MostRecentDict = LowPassFilterForDictsOfLists_Object.GetMostRecentDataDict()
            #print("LowPassFilterForDictsOfLists_MostRecentDict: " + str(LowPassFilterForDictsOfLists_MostRecentDict))
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################

        ####################################################
        if LowPassFilterForDictsOfLists_OPEN_FLAG == 1:
            LowPassFilterForDictsOfLists_MostRecentDict = LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("voltageRatioInput0_Value", [voltageRatioInput0_Value])]))

            if "voltageRatioInput0_Value" in LowPassFilterForDictsOfLists_MostRecentDict:

                voltageRatioInput0_Value_Raw = LowPassFilterForDictsOfLists_MostRecentDict["voltageRatioInput0_Value"]["Raw_MostRecentValuesList"][0]
                voltageRatioInput0_Value_Filtered = LowPassFilterForDictsOfLists_MostRecentDict["voltageRatioInput0_Value"]["Filtered_MostRecentValuesList"][0]

        else:
            voltageRatioInput0_Value_Filtered = voltageRatioInput0_Value
        ####################################################

        ####################################################
        if PeriodicInput == "VINThub":
            NewValue_Raw = voltageRatioInput0_Value_Raw
            NewValue_Filtered = voltageRatioInput0_Value_Filtered
        ####################################################

        ####################################################
        elif PeriodicInput == "GUI":
            NewValue_Raw = NewValue_Raw
            NewValue_Filtered = NewValue_Raw
        ####################################################

        ####################################################
        else:
            NewValue_Raw = GetLatestWaveformValue(CurrentTime_CalculatedFromMainThread, PeriodicInput_MinValue, PeriodicInput_MaxValue, PeriodicInput_Period, PeriodicInput)
            NewValue_Filtered = NewValue_Raw
        ####################################################

        ####################################################
        if InvertDataFlag == 1:
            NewValue_Raw = -1.0*NewValue_Raw
            NewValue_Filtered = -1.0*NewValue_Filtered
        ####################################################
        
        ####################################################
        DataList = numpy.roll(DataList, 1, axis=0)
        DataList[0, :] = [CurrentTime_CalculatedFromMainThread, NewValue_Filtered]
        ####################################################

        ####################################################
        ####################################################

        ####################################################
        ####################################################
        DataColumnIndex = 1
        DataDerivative_temp = (DataList[0, DataColumnIndex] - DataList[1, DataColumnIndex])/(1.0/DataStreamingFrequency_CalculatedFromMainThread_Filtered)

        VariablesDict_Temp = LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("DataDerivative", [DataDerivative_temp])]))
        DataDerivative = VariablesDict_Temp["DataDerivative"]["Filtered_MostRecentValuesList"][0]

        ####################################################
        ####################################################

        #################################################### unicorn
        ####################################################
        ####################################################
        if FindPeaksFlag == 1:
            try:

                ####################################################
                ####################################################
                #PeakMaxDataList = []
                #PeakMaxDataList = numpy.empty((1,2), "float")
                PeakMaxDataList_X = []
                PeakMaxDataList_Y = []
                PeakMinDataList_X = []
                PeakMinDataList_Y = []

                YaxisData = DataList[:, 1]
                ####################################################
                ####################################################

                #'''
                #################################################### Using scipy.signal.find_peaks
                ####################################################
                try:
                    PeakMaxIndexes, _ = scipy.signal.find_peaks(numpy.array(YaxisData),
                                                                height=ScipySignalFindPeaks_height,
                                                                prominence=ScipySignalFindPeaks_prominence)

                    PeakMinIndexes = []
                except:
                    exceptions = sys.exc_info()[0]
                    print("scipy.signal.find_peaks: Exceptions: %s" % exceptions)

                    PeakMaxIndexes = []
                    PeakMinIndexes = []
                    #traceback.print_exc()
                ####################################################
                ####################################################
                #'''

                '''
                #################################################### Just looking at 1st derivative to find extrema
                ####################################################
                try:

                    PeakMaxIndexes = []
                    if DataDerivative <= DataDerivative_Threshold:
                        PeakMaxIndexes = [0]

                    PeakMinIndexes = []
                except:
                    exceptions = sys.exc_info()[0]
                    print("scipy.signal.find_peaks: Exceptions: %s" % exceptions)

                    PeakMaxIndexes = []
                    PeakMinIndexes = []
                    #traceback.print_exc()
                ####################################################
                ####################################################
                '''

                ####################################################
                ####################################################
                if len(PeakMaxIndexes) > 0:
                    for Index in PeakMaxIndexes:

                        PeakMaxIndexPoint = DataList[Index - LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger,:] #.tolist()

                        if 1: #PeakMaxIndexPoint[1] >= Threshold0to1:
                            PeakMaxDataList_X.append(PeakMaxIndexPoint[0])
                            PeakMaxDataList_Y.append(PeakMaxIndexPoint[1])
                ####################################################
                ####################################################

                ####################################################
                ####################################################
                if len(PeakMinIndexes) > 0:
                    for Index in PeakMinIndexes:
                        PeakMinIndexPoint = DataList[Index - LowPassFilterForDictsOfLists_PeakDetectionPhaseDelayCorrectionInteger,:] #.tolist()

                        if 1: #PeakMaxIndexPoint[1] >= Threshold0to1:
                            PeakMinDataList_X.append(PeakMinIndexPoint[0])
                            PeakMinDataList_Y.append(PeakMinIndexPoint[1])
                ####################################################
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("detect_peaks: NewValue_Filtered = " + str(NewValue_Filtered) + ", Exceptions: %s" % exceptions)
                traceback.print_exc()
        else:
            pass

        ###############################################
        ###############################################

        ####################################################
        ####################################################
        if CSVdataLogger_OPEN_FLAG == 1:
            CSVdataLogger_Object.AddDataToCSVfile_ExternalFunctionCall([CurrentTime_CalculatedFromMainThread,
                                                                                          NewValue_Raw,
                                                                                          NewValue_Filtered])
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            ####################################################
            try:

                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag == 1:
                        if CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"]/1000.0 + 0.001:
                            MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Channel0"], #, "Channel0_Derivative"
                                                                                                                [CurrentTime_CalculatedFromMainThread]*1,
                                                                                                                [NewValue_Filtered]) #, DataDerivative


                            if len(PeakMaxDataList_X) > 0 and len(PeakMaxDataList_Y) > 0:
                                MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Channel0_PeaksMax"],
                                                                                                                    [PeakMaxDataList_X[0]],
                                                                                                                    [PeakMaxDataList_Y[0]])

                            if len(PeakMinDataList_X) > 0 and len(PeakMinDataList_Y) > 0:
                                MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Channel0_PeaksMin"],
                                                                                                                    [PeakMinDataList_X[0]],
                                                                                                                    [PeakMinDataList_Y[0]])


                            LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_CalculatedFromMainThread

            ####################################################

            ####################################################
            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess_OPEN_FLAGExceptions: %s" % exceptions)
                print("PeakMaxDataList_X: " + str(PeakMaxDataList_X) + ", PeakMaxDataList_Y: " + str(PeakMaxDataList_Y))
                print("PeakMinDataList_X: " + str(PeakMinDataList_X) + ", PeakMinDataList_Y: " + str(PeakMinDataList_Y))
                traceback.print_exc()
            ####################################################

        ####################################################
        ####################################################

        UpdateFrequencyCalculation_MainThread_Filtered()
        time.sleep(0.002)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_CSVdataLogger_ReubenPython3Class.")

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################