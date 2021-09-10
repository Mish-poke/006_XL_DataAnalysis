import pandas as pd

from tkinter import *
import os
import math
import getpass

from bokeh.plotting import figure, show, output_file
from bokeh.models import LinearAxis, ColumnDataSource, Range1d, LabelSet, Label, TableColumn, DataTable

redoFlagStructure = False
dict_exportFiles = {
    "export_nova":      0,
    "export_smeralda":  0
}

dict_filterRawData = {
    "filter_trueWind": 1
}
maxTrueWindValue = 30
#
#region nova subfolders
dict_readTheseSubFiles_nova = {
    '_ FINE nova ALL AC PWR':                   0,
    '_ FINE nova ALL AC Reheating Flow per FZ': 0,
    '_ FINE nova ALL BLR Different Figures':    0,
    '_ FINE nova ALL BT PWR':                   0,
    '_ FINE nova ALL Chilled WTR Temp per FZ':  0,
    '_ FINE nova ALL CSW Pumps PWR':            0,
    '_ FINE nova ALL DG ACTIVE PWR':                1,
    '_ FINE nova ALL DG POWER Factor':              1,
    '_ FINE nova ALL FANs AWP INC BIO':         0,
    '_ FINE nova ALL FANs BR-CHLR':             0,
    '_ FINE nova ALL Fans BT':                  0,
    '_ FINE nova ALL FANs Dryer FSH-MAST':      0,
    '_ FINE nova ALL FANs GHR':                 0,
    '_ FINE nova ALL FANs LNG-BS':              0,
    '_ FINE nova ALL FANs ME ROOM':             0,
    '_ FINE nova ALL FANs RMs STAB':            0,
    '_ FINE nova ALL FANs ROP NitTech':         0,
    '_ FINE nova ALL FCU HEATER per FZ':        0,
    '_ FINE nova ALL GSP BTR PRW':              0,
    '_ FINE nova ALL GSP POD AUX PWR':          0,
    '_ FINE nova ALL GSP POD TOT PWR':              1,
    '_ FINE nova ALL GSP TSC GVR VENT':         0,
    '_ FINE nova ALL GVU FLOW ME':                  1,
    '_ FINE nova ALL GVU TEMP':                     1,
    '_ FINE nova ALL HOTEL PWR per FZ':         0,
    '_ FINE nova ALL HVAC AHU per FZ':          0,
    '_ FINE nova ALL HVAC PWR per FZ':          0,
    '_ FINE nova ALL HVAC Standard':            0,
    '_ FINE nova ALL Ignition Fuel Flow':       0,
    '_ FINE nova ALL LAT LONG':                 0,
    '_ FINE nova ALL LT CIRC PUMP PWR':         0,
    '_ FINE nova ALL ME Reactive PWR':          0,
    '_ FINE nova ALL NAV Signals':                  1,
    '_ FINE nova ALL POD CAU FAN PWR':          0,
    '_ FINE nova ALL POD PROP MTR PWR':             1,
    '_ FINE nova ALL POD PWR':                      1,
    '_ FINE nova ALL Pools Jaccuzzies':         0,
    '_ FINE nova ALL RF PWR':                   0,
    '_ FINE nova ALL RMU per FZ':               0,
    '_ FINE nova ALL STEAM Flows':              0,
    '_ FINE nova ALL STRS':                         1,
    '_ FINE nova ALL TEMP Pressure Wind':       0,
    '_ FINE nova ALL WHR Signals':              0
}
#endregion

#region smeralda subfolders
dict_readTheseSubFiles_smeralda = {
    '_ FINE smeralda ALL AC PWR':                   0,
    '_ FINE smeralda ALL AC Reheating Flow per FZ': 0,
    '_ FINE smeralda ALL BLR Different Figures':    0,
    '_ FINE smeralda ALL BT PWR':                   0,
    '_ FINE smeralda ALL Chilled WTR Temp per FZ':  0,
    '_ FINE smeralda ALL CSW Pumps PWR':            0,
    '_ FINE smeralda ALL DG ACTIVE PWR':                1,
    '_ FINE smeralda ALL DG POWER Factor':              1,
    '_ FINE smeralda ALL FANs AWP INC BIO':         0,
    '_ FINE smeralda ALL FANs BR-CHLR':             0,
    '_ FINE smeralda ALL Fans BT':                  0,
    '_ FINE smeralda ALL FANs Dryer FSH-MAST':      0,
    '_ FINE smeralda ALL FANs GHR':                 0,
    '_ FINE smeralda ALL FANs LNG-BS':              0,
    '_ FINE smeralda ALL FANs ME ROOM':             0,
    '_ FINE smeralda ALL FANs RMs STAB':            0,
    '_ FINE smeralda ALL FANs ROP NitTech':         0,
    '_ FINE smeralda ALL FCU HEATER per FZ':        0,
    '_ FINE smeralda ALL GSP BTR PRW':              0,
    '_ FINE smeralda ALL GSP POD AUX PWR':          0,
    '_ FINE smeralda ALL GSP POD TOT PWR':              1,
    '_ FINE smeralda ALL GSP TSC GVR VENT':         0,
    '_ FINE smeralda ALL GVU FLOW ME':                  1,
    '_ FINE smeralda ALL GVU TEMP':                 0,
    '_ FINE smeralda ALL HOTEL PWR per FZ':         0,
    '_ FINE smeralda ALL HVAC AHU per FZ':          0,
    '_ FINE smeralda ALL HVAC PWR per FZ':          0,
    '_ FINE smeralda ALL HVAC Standard':            0,
    '_ FINE smeralda ALL Ignition Fuel Flow':       0,
    '_ FINE smeralda ALL LAT LONG':                 0,
    '_ FINE smeralda ALL LT CIRC PUMP PWR':         0,
    '_ FINE smeralda ALL ME PWR STRANGE SIGNAL':    0,
    '_ FINE smeralda ALL ME Reactive PWR':          0,
    '_ FINE smeralda ALL NAV Signals':                  1,
    '_ FINE smeralda ALL POD CAU FAN PWR':          0,
    '_ FINE smeralda ALL POD PROP MTR PWR':             1,
    '_ FINE smeralda ALL POD PWR':                      1,
    '_ FINE smeralda ALL Pools Jaccuzzies':         0,
    '_ FINE smeralda ALL RF PWR':                   0,
    '_ FINE smeralda ALL RMU per FZ':               0,
    '_ FINE smeralda ALL STEAM Flows':              0,
    '_ FINE smeralda ALL STRS':                         1,
    '_ FINE smeralda ALL TEMP Pressure Wind':       0,
    '_ FINE smeralda ALL WHR Signals':              0
}
#endregion

#region flags raw data
flag_rawData_timestamp = 'timestamp'
flag_rawData_MV1_DG1_ACTIVE_PWR_kW = 'MV1 DG1 ACTIVE PWR kW'
flag_rawData_MV1_DG2_ACTIVE_PWR_kW = 'MV1 DG2 ACTIVE PWR kW'
flag_rawData_MV2_DG3_ACTIVE_PWR_kW = 'MV2 DG3 ACTIVE PWR kW'
flag_rawData_MV2_DG4_ACTIVE_PWR_kW = 'MV2 DG4 ACTIVE PWR kW'
flag_rawData_ME1_FUEL_GAS_GVU_FLOW_x = 'ME1 FUEL GAS GVU FLOW_x'
flag_rawData_ME2_FUEL_GAS_GVU_FLOW_x = 'ME2 FUEL GAS GVU FLOW_x'
flag_rawData_ME3_FUEL_GAS_GVU_FLOW_x = 'ME3 FUEL GAS GVU FLOW_x'
flag_rawData_ME4_FUEL_GAS_GVU_FLOW_x = 'ME4 FUEL GAS GVU FLOW_x'
flag_rawData_GVU_ME1_AIR_FLOW_x = 'GVU ME1 AIR FLOW_x'
flag_rawData_GVU_ME2_AIR_FLOW_x = 'GVU ME2 AIR FLOW_x'
flag_rawData_GVU_ME3_AIR_FLOW_x = 'GVU ME3 AIR FLOW_x'
flag_rawData_GVU_ME4_AIR_FLOW_x = 'GVU ME4 AIR FLOW_x'
flag_rawData_ME1_FUEL_GAS_GVU_FLOW_y = 'ME1 FUEL GAS GVU FLOW_y'
flag_rawData_ME2_FUEL_GAS_GVU_FLOW_y = 'ME2 FUEL GAS GVU FLOW_y'
flag_rawData_ME3_FUEL_GAS_GVU_FLOW_y = 'ME3 FUEL GAS GVU FLOW_y'
flag_rawData_ME4_FUEL_GAS_GVU_FLOW_y = 'ME4 FUEL GAS GVU FLOW_y'
flag_rawData_GVU_ME1_AIR_FLOW_y = 'GVU ME1 AIR FLOW_y'
flag_rawData_GVU_ME2_AIR_FLOW_y = 'GVU ME2 AIR FLOW_y'
flag_rawData_GVU_ME3_AIR_FLOW_y = 'GVU ME3 AIR FLOW_y'
flag_rawData_GVU_ME4_AIR_FLOW_y = 'GVU ME4 AIR FLOW_y'
flag_rawData_ME1_GVU_F_GAS_IN_TEMP_x = 'ME1 GVU F.GAS IN TEMP_x'
flag_rawData_ME2_GVU_F_GAS_IN_TEMP_x = 'ME2 GVU F.GAS IN TEMP_x'
flag_rawData_ME3_GVU_F_GAS_IN_TEMP_x = 'ME3 GVU F.GAS IN TEMP_x'
flag_rawData_ME4_GVU_F_GAS_IN_TEMP_x = 'ME4 GVU F.GAS IN TEMP_x'
flag_rawData_GVU_FWD_SUPPLY_AIR_TEMP_x = 'GVU FWD SUPPLY AIR TEMP_x'
flag_rawData_GVU_AFT_SUPPLY_AIR_TEMP_x = 'GVU AFT SUPPLY AIR TEMP_x'
flag_rawData_ME1_GVU_F_GAS_IN_TEMP_y = 'ME1 GVU F.GAS IN TEMP_y'
flag_rawData_ME2_GVU_F_GAS_IN_TEMP_y = 'ME2 GVU F.GAS IN TEMP_y'
flag_rawData_ME3_GVU_F_GAS_IN_TEMP_y = 'ME3 GVU F.GAS IN TEMP_y'
flag_rawData_ME4_GVU_F_GAS_IN_TEMP_y = 'ME4 GVU F.GAS IN TEMP_y'
flag_rawData_GVU_FWD_SUPPLY_AIR_TEMP_y = 'GVU FWD SUPPLY AIR TEMP_y'
flag_rawData_GVU_AFT_SUPPLY_AIR_TEMP_y = 'GVU AFT SUPPLY AIR TEMP_y'
flag_rawData_INS_WATERDEP_BELOW_KEEL_x = 'INS WATERDEP.BELOW KEEL_x'
flag_rawData_INS_TRUE_WINDSPEED_x = 'INS TRUE WINDSPEED_x'
flag_rawData_INS_TRUE_WINDDIR_x = 'INS TRUE WINDDIR_x'
flag_rawData_INS_SPEED_THROUGH_WATER_x = 'INS SPEED THROUGH WATER_x'
flag_rawData_INS_SPEED_OVER_GROUND_x = 'INS SPEED OVER GROUND_x'
flag_rawData_INS_DEWPOINT_x = 'INS DEWPOINT_x'
flag_rawData_INS_HUMIDITY_x = 'INS HUMIDITY_x'
flag_rawData_INS_RATE_OF_TURN_x = 'INS RATE OF TURN_x'
flag_rawData_INS_WATERDEP_BELOW_KEEL_y = 'INS WATERDEP.BELOW KEEL_y'
flag_rawData_INS_TRUE_WINDSPEED_y = 'INS TRUE WINDSPEED_y'
flag_rawData_INS_TRUE_WINDDIR_y = 'INS TRUE WINDDIR_y'
flag_rawData_INS_SPEED_THROUGH_WATER_y = 'INS SPEED THROUGH WATER_y'
flag_rawData_INS_SPEED_OVER_GROUND_y = 'INS SPEED OVER GROUND_y'
flag_rawData_INS_DEWPOINT_y = 'INS DEWPOINT_y'
flag_rawData_INS_HUMIDITY_y = 'INS HUMIDITY_y'
flag_rawData_INS_RATE_OF_TURN_y = 'INS RATE OF TURN_y'
flag_rawData_POD1_PROP_ACTUAL_MTR_PWR_x = 'POD1 PROP ACTUAL MTR PWR_x'
flag_rawData_POD2_PROP_ACTUAL_MTR_PWR_x = 'POD2 PROP ACTUAL MTR PWR_x'
flag_rawData_POD1_PROP_ACTUAL_MTR_PWR_y = 'POD1 PROP ACTUAL MTR PWR_y'
flag_rawData_POD2_PROP_ACTUAL_MTR_PWR_y = 'POD2 PROP ACTUAL MTR PWR_y'
flag_rawData_MV1_POD1A_ACTIVE_PWR_kW_x = 'MV1 POD1A ACTIVE PWR kW_x'
flag_rawData_MV1_POD1B_ACTIVE_PWR_kW_x = 'MV1 POD1B ACTIVE PWR kW_x'
flag_rawData_MV1_POD1_ACTIVE_PWR_kW_x = 'MV1 POD1 ACTIVE PWR kW_x'
flag_rawData_MV2_POD2_ACTIVE_PWR_kW_x = 'MV2 POD2 ACTIVE PWR kW_x'
flag_rawData_MV2_POD2A_ACTIVE_PWR_kW_x = 'MV2 POD2A ACTIVE PWR kW_x'
flag_rawData_MV2_POD2B_ACTIVE_PWR_kW_x = 'MV2 POD2B ACTIVE PWR kW_x'
flag_rawData_MV1_POD1A_ACTIVE_PWR_kW_y = 'MV1 POD1A ACTIVE PWR kW_y'
flag_rawData_MV1_POD1B_ACTIVE_PWR_kW_y = 'MV1 POD1B ACTIVE PWR kW_y'
flag_rawData_MV1_POD1_ACTIVE_PWR_kW_y = 'MV1 POD1 ACTIVE PWR kW_y'
flag_rawData_MV2_POD2_ACTIVE_PWR_kW_y = 'MV2 POD2 ACTIVE PWR kW_y'
flag_rawData_MV2_POD2A_ACTIVE_PWR_kW_y = 'MV2 POD2A ACTIVE PWR kW_y'
flag_rawData_MV2_POD2B_ACTIVE_PWR_kW_y = 'MV2 POD2B ACTIVE PWR kW_y'
flag_rawData_MV1_S_TRS1_ACTIVE_PWR_kW_x = 'MV1 S-TRS1 ACTIVE PWR kW_x'
flag_rawData_MV1_S_TRS2_ACTIVE_PWR_kW_x = 'MV1 S-TRS2 ACTIVE PWR kW_x'
flag_rawData_MV2_S_TRS3_ACTIVE_PWR_kW_x = 'MV2 S-TRS3 ACTIVE PWR kW_x'
flag_rawData_MV2_S_TRS4_ACTIVE_PWR_kW_x = 'MV2 S-TRS4 ACTIVE PWR kW_x'
flag_rawData_MV1_S_TRS1_ACTIVE_PWR_kW_y = 'MV1 S-TRS1 ACTIVE PWR kW_y'
flag_rawData_MV1_S_TRS2_ACTIVE_PWR_kW_y = 'MV1 S-TRS2 ACTIVE PWR kW_y'
flag_rawData_MV2_S_TRS3_ACTIVE_PWR_kW_y = 'MV2 S-TRS3 ACTIVE PWR kW_y'
flag_rawData_MV2_S_TRS4_ACTIVE_PWR_kW_y = 'MV2 S-TRS4 ACTIVE PWR kW_y'
#endregion

#region added flags!
flag_rawData_SFOC_LNG_DG1 = "SFOC_LNG_DG1"
flag_rawData_SFOC_LNG_DG2 = "SFOC_LNG_DG2"
flag_rawData_SFOC_LNG_DG3 = "SFOC_LNG_DG3"
flag_rawData_SFOC_LNG_DG4 = "SFOC_LNG_DG4"

flag_rawData_DG1_LNG_absoluteConsumptionPerHour = "DG1 LNG MT/hour this sample"
flag_rawData_DG2_LNG_absoluteConsumptionPerHour = "DG2 LNG MT/hour this sample"
flag_rawData_DG3_LNG_absoluteConsumptionPerHour = "DG3 LNG MT/hour this sample"
flag_rawData_DG4_LNG_absoluteConsumptionPerHour = "DG4 LNG MT/hour this sample"

flag_rawData_EngineLoadPercent_DG1 = "DG1 load percent"
flag_rawData_EngineLoadPercent_DG2 = "DG2 load percent"
flag_rawData_EngineLoadPercent_DG3 = "DG3 load percent"
flag_rawData_EngineLoadPercent_DG4 = "DG4 load percent"

flag_rawData_enginesRunning = "DGs running"

flag_rawData_totalSTRSPower = "STRS TOTAL PWR"
flag_rawData_total_MainEngine_PWR = "Total Main Engine PWR"
flag_rawData_total_POD_PWR = "Total PROP PWR"
flag_rawData_total_POD_MTR_PRW = "Total POD MTR PWR"
flag_rawData_total_LNG_GVU_Flow = "TOTAL LNG FLOW"

flag_rawData_avgSFOC_runningEngines = "AVG SFOC running engines"
flag_rawData_avgLoad_runningEngines = "AVG Load Pct running engines"
#endregion

#region standard ship dict
dict_ships = {
    "ship_nova": "AIDAnova",
    "ship_smeralda": "Costa Smeralda"
}
#endregion

#region pre-defined scatter color - light
dict_colorsForScatter = {
    1: '#98b842', #'#8ddbbc',
    2: '#638aeb',
    3: '#cf7cf2',
    4: '#ed5c97'
}
#endregion

#region pre-defined scatter color - dark
dict_colorsForScatter_Dark = {
    1: '#475423', #'#8ddbbc',
    2: '#294996',
    3: '#923fb5',
    4: '#6e1a3c'
}
#endregion

#region ADJUST PLOTs
useDarkScatter = True
scatter_FrameWidth = 1200
scatter_FramHeight = 800

scatter_dotTransparency = 0.3
scatter_dotSize = 1

plotSFOC_Curves = True
plotSFOC_per_engine_overSpeed = False
plot_GVU_LNGCharts = False

dict_plotTheseShips = {
    "plot_nova": 1,
    "plot_smeralda": 1
}

dict_generic_x_signal = {
    "flag_rawData_INS_SPEED_OVER_GROUND_x": 0,
    "flag_rawData_INS_SPEED_THROUGH_WATER_x": 1,
}

# >>> UPDATE this function for every new signal
# def func_getRealFlagNotJustStr
dict_generic_y_signal = {
    "flag_rawData_totalSTRSPower":          0,
    "flag_rawData_total_POD_PWR":           0,
    "flag_rawData_total_POD_MTR_PRW":       0,
    "flag_rawData_total_MainEngine_PWR":    1,
    "flag_rawData_avgSFOC_runningEngines":  0,
    "flag_rawData_avgLoad_runningEngines":  0,
}

dict_plotTheseGenericGraphs = {
    "plot_signal_overSpeed": 1,
    "plot_signal_perNMsailed_overSpeed": 1,
    "plot_signal_perDollar_perNMSailed_overSpeed": 0
}
#endregion

' #####################################################################################################################'
def f_readAllFilesInSubfolders(
    df_thisShip,
    dict_signalsThisShip,
    shipName
):
    print("\n#################################################\n#################################################"
          " \nSCAN all files in XL-Class DATA FOLDER and load data for " + shipName)

    if username == "TR@FI_02":
        folder_location = 'E:\\001_CMG\\HOME\\XL-Class-Automation-Data'

    if username == "500095":
        folder_location = 'C:\\Users\\500095\\OneDrive - Carnival Corporation\\Desktop\\HOME\\XL-Class-Automation-Data'

    subDF = pd.DataFrame()
    list_filesToBeLoaded = []

    print("LETS LOOP through all folders and subfolders within " + str(folder_location))
    for subdir, dirs, files in os.walk(folder_location):
        splitString = r'\''
        subDirFolderName = subdir.split(splitString[:1])

        thisSubfolderName = subDirFolderName[len(subDirFolderName)-1]
        if thisSubfolderName in dict_signalsThisShip:
            if dict_signalsThisShip[thisSubfolderName]:
                print("#########################")
                print("subdir   " + str(subdir))
                print("dirs     " + str(dirs))
                print("files    " + str(files))

                print(">>> we need all files in here <<<")
                for thisFile in files:
                    filepath = subdir + os.sep + thisFile
                    if filepath.endswith(".csv"):
                        print("load me " + str(filepath))
                        list_filesToBeLoaded.append(filepath)

    for thisFile in list_filesToBeLoaded:
        print("lets read next file >>: " + str(thisFile))
        if df_thisShip.shape[0] == 0:
            df_thisShip = pd.read_csv(thisFile, sep=";", decimal=".")
            df_thisShip[flag_rawData_timestamp] = pd.to_datetime(df_thisShip[flag_rawData_timestamp])
        else:
            subDF = pd.read_csv(thisFile, sep=";", decimal=".")
            subDF[flag_rawData_timestamp] = pd.to_datetime(subDF[flag_rawData_timestamp])

            if subDF[flag_rawData_timestamp].min() > df_thisShip[flag_rawData_timestamp].max():
                df_thisShip = pd.concat([df_thisShip, subDF])
            else:
                df_thisShip = f_mergeDataFramesByTimeStamp(
                    df_thisShip, subDF, 'df_strsAC1',
                    flag_rawData_timestamp,
                    flag_rawData_timestamp)

    return df_thisShip

' #####################################################################################################################'
def f_mergeDataFramesByTimeStamp(
    masterDF,
    dfToBeMatched,
    dataframeName,
    mergeOnThisColumn,
    mergeByThisColumn
):
    initialLines = masterDF.shape[0]

    if len(dfToBeMatched) > 0:
        dfFinal = pd.merge_asof(masterDF, dfToBeMatched, on=mergeOnThisColumn, by=mergeByThisColumn)
    else:
        dfFinal = masterDF
        print("NO MERGE DONE DF is empty")

    remainingLines = masterDF.shape[0]

    print("ROWS AFTER MERGING both dataframes: " + str(remainingLines) + " MISSING LINES: " +
          str(remainingLines - initialLines)
    )

    return (dfFinal)

' #####################################################################################################################'
def func_getNameWithoutBlanks(
    thisColumnName
):
    # finalString = ""
    # parts = thisColumnName.split(" ")
    #
    # for thisPart in parts:
    #     finalString = finalString + thisPart

    finalString = thisColumnName.replace(" ", "_")
    finalString = finalString.replace("-", "_")

    return finalString.replace(".", "_")

' #####################################################################################################################'
def func_isThisColumnAvailable(
    thisDF,
    thisShip,
    thisFlag
):
    if thisFlag not in thisDF.columns:
        print(">> COLUMN: " + thisFlag + " missing for " + thisShip)
        return False

    return True

' #####################################################################################################################'
def func_calc_LNG_SFOC(
    thisDF,
    thisShip
):
    thisDF = func_SFOC_ThisEngine(
        thisDF, thisShip, flag_rawData_SFOC_LNG_DG1, flag_rawData_ME1_FUEL_GAS_GVU_FLOW_x,
        flag_rawData_MV1_DG1_ACTIVE_PWR_kW)

    thisDF = func_SFOC_ThisEngine(
        thisDF, thisShip, flag_rawData_SFOC_LNG_DG2, flag_rawData_ME2_FUEL_GAS_GVU_FLOW_x,
        flag_rawData_MV1_DG2_ACTIVE_PWR_kW)

    thisDF = func_SFOC_ThisEngine(
        thisDF, thisShip, flag_rawData_SFOC_LNG_DG3, flag_rawData_ME3_FUEL_GAS_GVU_FLOW_x,
        flag_rawData_MV2_DG3_ACTIVE_PWR_kW)

    thisDF = func_SFOC_ThisEngine(
        thisDF, thisShip, flag_rawData_SFOC_LNG_DG4, flag_rawData_ME4_FUEL_GAS_GVU_FLOW_x,
        flag_rawData_MV2_DG4_ACTIVE_PWR_kW)

    return thisDF

' #####################################################################################################################'
def func_SFOC_ThisEngine(
    thisDF,
    thisShip,
    flag_SFOC,
    flag_GVU_Flow,
    flag_DGx_ACTIVE_PWR_kW
):
    print("LNG SFOC for " + thisShip + " and engine " + flag_SFOC)

    thisDF[flag_SFOC] = 0

    if not func_isThisColumnAvailable(thisDF, thisShip, flag_GVU_Flow):
        return thisDF

    if not func_isThisColumnAvailable(thisDF, thisShip, flag_DGx_ACTIVE_PWR_kW):
        return thisDF

    thisDF = f_doTheSFOC(
        thisDF, flag_SFOC, flag_GVU_Flow, flag_DGx_ACTIVE_PWR_kW)

    return thisDF

' #####################################################################################################################'
def func_getScatterColor():
    dictColors = dict_colorsForScatter
    if useDarkScatter:
        dictColors = dict_colorsForScatter_Dark

    return dictColors

' #####################################################################################################################'
def f_doTheSFOC(
    thisDF,
    flag_SFOC,
    flag_GVU_Flow,
    flag_DGx_ACTIVE_PWR_kW
):

    thisDF.loc[
        (thisDF[flag_DGx_ACTIVE_PWR_kW] > 500),
        flag_SFOC
    ] =\
        thisDF.loc[
            (thisDF[flag_DGx_ACTIVE_PWR_kW] > 500),
            flag_GVU_Flow
            ] / \
        thisDF.loc[
            (thisDF[flag_DGx_ACTIVE_PWR_kW] > 500),
            flag_DGx_ACTIVE_PWR_kW
        ] * 1000

    return thisDF

' #####################################################################################################################'
def func_plotThisEnginesSFOC(
    thisDF, thisShip, scatterFrame_rawDataOverTime,
    flag_loadPercent, flag_engineSFOC, engineCount
):
    dictColors = func_getScatterColor()

    scatterFrame_rawDataOverTime.circle(
        thisDF[thisDF[flag_engineSFOC] > 100][flag_loadPercent],
        thisDF[thisDF[flag_engineSFOC] > 100][flag_engineSFOC],
        size=scatter_dotSize, color=dictColors[engineCount],
        alpha=scatter_dotTransparency,
        legend_label=thisShip + " SFOC DG" + str(engineCount)
    )

    return scatterFrame_rawDataOverTime

' #####################################################################################################################'
def func_printSFOC(
    thisDF,
    thisShip
):
    scatterFrame_rawDataOverTime = f_prepareTheScatterFrame(
            scatter_FrameWidth, scatter_FramHeight, (0, 100),
            (100, 260),
            str(thisShip + " SFOC LNG per engine")
        )

    scatterFrame_rawDataOverTime = func_plotThisEnginesSFOC(
        thisDF, thisShip, scatterFrame_rawDataOverTime,
        flag_rawData_EngineLoadPercent_DG1, flag_rawData_SFOC_LNG_DG1, 1
    )

    scatterFrame_rawDataOverTime = func_plotThisEnginesSFOC(
        thisDF, thisShip, scatterFrame_rawDataOverTime,
        flag_rawData_EngineLoadPercent_DG2, flag_rawData_SFOC_LNG_DG2, 2
    )

    scatterFrame_rawDataOverTime = func_plotThisEnginesSFOC(
        thisDF, thisShip, scatterFrame_rawDataOverTime,
        flag_rawData_EngineLoadPercent_DG3, flag_rawData_SFOC_LNG_DG3, 3
    )

    scatterFrame_rawDataOverTime = func_plotThisEnginesSFOC(
        thisDF, thisShip, scatterFrame_rawDataOverTime,
        flag_rawData_EngineLoadPercent_DG4, flag_rawData_SFOC_LNG_DG4, 4
    )

    thisFileName = thisShip + " SFOC LNG per engine"
    output_file(thisFileName + '.html', #dict_subFolderName["subfolder_exportGraphs"] + "/"
        title=thisFileName + '.py example'
    )

    citation = Label(
        x=scatter_FrameWidth - 200, y=5, x_units='screen', y_units='screen',
        text='TR@CMG 2021', render_mode='css',
        border_line_color='black', border_line_alpha=1.0,
        background_fill_color="#cbe6f5", background_fill_alpha=1.0
    )

    scatterFrame_rawDataOverTime.legend.location = "top_left"
    scatterFrame_rawDataOverTime.title.text_font_size = "14px"

    scatterFrame_rawDataOverTime.legend.click_policy = "hide"

    scatterFrame_rawDataOverTime.xaxis.axis_label = "ENGINE LOAD [%]"
    scatterFrame_rawDataOverTime.yaxis.axis_label = "SFOC g/kWh"

    scatterFrame_rawDataOverTime.add_layout(citation)

    show(scatterFrame_rawDataOverTime)

' #####################################################################################################################'
def f_prepareTheScatterFrame(
    width, height, xAxisRange, yAxisRange, masterTitle
):
    p = figure(
        plot_width=width,
        plot_height=height,
        x_range=xAxisRange,
        y_range=yAxisRange,
        title=masterTitle,
        background_fill_color="#faf9f5"
    )

    return p

' #####################################################################################################################'
def func_getEngineLoadPercent(
    thisDF,
    thisShip
):
    thisDF = func_doTheLoadPercentForThisEngine(
        thisDF, thisShip, flag_rawData_MV1_DG1_ACTIVE_PWR_kW, flag_rawData_EngineLoadPercent_DG1)

    thisDF = func_doTheLoadPercentForThisEngine(
        thisDF, thisShip, flag_rawData_MV1_DG2_ACTIVE_PWR_kW, flag_rawData_EngineLoadPercent_DG2)

    thisDF = func_doTheLoadPercentForThisEngine(
        thisDF, thisShip, flag_rawData_MV2_DG3_ACTIVE_PWR_kW, flag_rawData_EngineLoadPercent_DG3)

    thisDF = func_doTheLoadPercentForThisEngine(
        thisDF, thisShip, flag_rawData_MV2_DG4_ACTIVE_PWR_kW, flag_rawData_EngineLoadPercent_DG4)

    return thisDF

' #####################################################################################################################'
def func_doTheLoadPercentForThisEngine(
    thisDF,
    thisShip,
    flag_engineLoad_ABS,
    flag_engineLoad_Pct
):
    # print("\nADDING next load for this engine " + flag_engineLoad_Pct)
    minEngineLoadForAnyCounting = 250

    thisDF[flag_engineLoad_Pct] = 0

    if not func_isThisColumnAvailable(thisDF, thisShip, flag_engineLoad_ABS):
        return thisDF
    else:
        thisDF.loc[
            (thisDF[flag_engineLoad_ABS] > minEngineLoadForAnyCounting),
            flag_engineLoad_Pct] = \
        round(
            thisDF.loc[
                (thisDF[flag_engineLoad_ABS] > minEngineLoadForAnyCounting),
                flag_engineLoad_ABS] / 15440 * 100, 1
        )

    return thisDF

' #####################################################################################################################'
def func_getSubFlag(
    flag,
    flagSubDataToBeSummedUp_1,
    flagSubDataToBeSummedUp_2,
    flagSubDataToBeSummedUp_3,
    flagSubDataToBeSummedUp_4
):
    if flag == 1:
        return  flagSubDataToBeSummedUp_1

    if flag == 2:
        return flagSubDataToBeSummedUp_2

    if flag == 3:
        return flagSubDataToBeSummedUp_3

    return flagSubDataToBeSummedUp_4

' #####################################################################################################################'
def func_addNewSumColumnWithTotal(
    thisDF,
    thisShip,
    newFlag,
    flagSubDataToBeSummedUp_1,
    flagSubDataToBeSummedUp_2,
    flagSubDataToBeSummedUp_3 = "",
    flagSubDataToBeSummedUp_4 = ""
):
    thisDF[newFlag] = 0

    cntFlag = 1
    while cntFlag <= 4:
        subFlag = func_getSubFlag(
            cntFlag,
            flagSubDataToBeSummedUp_1, flagSubDataToBeSummedUp_2,
            flagSubDataToBeSummedUp_3, flagSubDataToBeSummedUp_4)

        if subFlag in thisDF.columns.unique():
            thisDF[newFlag] = \
                thisDF[newFlag] + \
                thisDF[subFlag]

        cntFlag+=1

    print(thisShip + " mean "+newFlag+" = " + str(thisDF[newFlag].mean()))

    return thisDF

' #####################################################################################################################'
def func_addConvertedColumn(
    thisDF,
    flag_ySignal,
    flag_xSignalToBeUsedAsDivider,
    flag_newNameYSignal
):
    thisDF[flag_newNameYSignal] = 0

    thisDF.loc[
        (thisDF[flag_xSignalToBeUsedAsDivider] > 0),
        flag_newNameYSignal] = \
    thisDF.loc[
        (thisDF[flag_xSignalToBeUsedAsDivider] > 0),
        flag_ySignal] / \
    thisDF.loc[
        (thisDF[flag_xSignalToBeUsedAsDivider] > 0),
        flag_xSignalToBeUsedAsDivider]

    return thisDF

' #####################################################################################################################'
def func_createSimpleScatter(
    thisDF,
    thisShip,
    min_x, max_x,
    min_y, max_y,
    graph_name,
    scatter_dotTransparency,
    scatter_dotSize,
    flag_xSignal,
    flag_ySignal,
    x_axisLabel,
    y_axisLabel,
    plotDataByAmountOfEnginesRunning = False,
    minSpeedToBeFilteredFor = 0,
    convert_y_into_value_per_NM = False,
    convert_MW_intoMTUsingCorrectSFOC = False
):
    scatterFrame_rawDataOverTime = f_prepareTheScatterFrame(
        scatter_FrameWidth, scatter_FramHeight,
        (min_x, max_x),
        (min_y, max_y),
        str(thisShip + " " + graph_name)
    )

    dictColors = func_getScatterColor()

    if convert_y_into_value_per_NM:
        flag_newNameYSignal = "MW/NM"
        thisDF = func_addConvertedColumn(thisDF, flag_ySignal, flag_rawData_INS_SPEED_THROUGH_WATER_x, flag_newNameYSignal)
        flag_ySignal = flag_newNameYSignal

    if plotDataByAmountOfEnginesRunning:
        thisEngine = 1
        while thisEngine <= 4:
            scatterFrame_rawDataOverTime.circle(
                thisDF[
                    (thisDF[flag_rawData_enginesRunning] == thisEngine) &
                    (thisDF[flag_rawData_INS_SPEED_THROUGH_WATER_x] >= minSpeedToBeFilteredFor)][flag_xSignal],
                thisDF[
                    (thisDF[flag_rawData_enginesRunning] == thisEngine) &
                    (thisDF[flag_rawData_INS_SPEED_THROUGH_WATER_x] >= minSpeedToBeFilteredFor)][flag_ySignal],
                size=scatter_dotSize, color=dictColors[thisEngine],
                alpha=scatter_dotTransparency,
                legend_label = thisShip + " " + graph_name + " " + str(thisEngine) +"DG running"
            )

            thisEngine+=1
    else:
        scatterFrame_rawDataOverTime.circle(
            thisDF[flag_xSignal],
            thisDF[flag_ySignal],
            size=scatter_dotSize, color=dictColors[1],
            alpha=scatter_dotTransparency,
            legend_label = thisShip + " " + graph_name
        )

    thisFileName = thisShip + graph_name
    output_file(thisFileName + '.html',  # dict_subFolderName["subfolder_exportGraphs"] + "/"
                title=thisFileName + '.py example'
                )

    citation = Label(
        x=scatter_FrameWidth - 220, y=5, x_units='screen', y_units='screen',
        text='TR@CMG 2021', render_mode='css',
        border_line_color='black', border_line_alpha=1.0,
        background_fill_color="#cbe6f5", background_fill_alpha=1.0
    )

    scatterFrame_rawDataOverTime.legend.location = "top_left"
    scatterFrame_rawDataOverTime.title.text_font_size = "14px"

    scatterFrame_rawDataOverTime.legend.click_policy = "hide"

    scatterFrame_rawDataOverTime.xaxis.axis_label = x_axisLabel
    scatterFrame_rawDataOverTime.yaxis.axis_label = y_axisLabel

    scatterFrame_rawDataOverTime.add_layout(citation)

    show(scatterFrame_rawDataOverTime)

' #####################################################################################################################'
def func_countForThisEngineFlag(
    thisDF,
    flag_thisEngineLoad
):
    thisDF.loc[
        (thisDF[flag_thisEngineLoad] > 500),
        flag_rawData_enginesRunning
    ] =\
        thisDF.loc[
            (thisDF[flag_thisEngineLoad] > 500),
            flag_rawData_enginesRunning
        ] + 1

    return thisDF

' #####################################################################################################################'
def func_getAmountOfEnginesRunning(
    thisDF,
    thisShip
):
    thisDF[flag_rawData_enginesRunning] = 0

    thisDF = func_countForThisEngineFlag(thisDF, flag_rawData_MV1_DG1_ACTIVE_PWR_kW)
    thisDF = func_countForThisEngineFlag(thisDF, flag_rawData_MV1_DG2_ACTIVE_PWR_kW)
    thisDF = func_countForThisEngineFlag(thisDF, flag_rawData_MV2_DG3_ACTIVE_PWR_kW)
    thisDF = func_countForThisEngineFlag(thisDF, flag_rawData_MV2_DG4_ACTIVE_PWR_kW)

    return thisDF

' #####################################################################################################################'
def func_calcAvgSfocRunningEngines(
    thisDF,
    thisShip
):
    thisDF[flag_rawData_avgSFOC_runningEngines] = 0

    thisDF.loc[
        (thisDF[flag_rawData_enginesRunning] > 0),
        flag_rawData_avgSFOC_runningEngines
    ] = \
        (
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_SFOC_LNG_DG1] +
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_SFOC_LNG_DG2] +
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_SFOC_LNG_DG3] +
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_SFOC_LNG_DG4]
        ) / thisDF.loc[
            (thisDF[flag_rawData_enginesRunning] > 0),
            flag_rawData_enginesRunning
        ]

    return thisDF

' #####################################################################################################################'
def func_calcAvgLoadRunningEngines(
    thisDF,
    thisShip
):
    thisDF[flag_rawData_avgLoad_runningEngines] = 0

    thisDF.loc[
        (thisDF[flag_rawData_enginesRunning] > 0),
        flag_rawData_avgLoad_runningEngines
    ] = \
        (
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_EngineLoadPercent_DG1] +
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_EngineLoadPercent_DG2] +
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_EngineLoadPercent_DG3] +
            thisDF.loc[
                (thisDF[flag_rawData_enginesRunning] > 0),
                flag_rawData_EngineLoadPercent_DG4]
        ) / thisDF.loc[
            (thisDF[flag_rawData_enginesRunning] >   0),
            flag_rawData_enginesRunning
        ]

    return thisDF

' #####################################################################################################################'
def func_preCalcSomeFurtherValues(
    df_nova,
    df_smeralda
):
    df_nova = func_getEngineLoadPercent(df_nova, dict_ships["ship_nova"])
    df_smeralda = func_getEngineLoadPercent(df_smeralda, dict_ships["ship_smeralda"])

    df_nova = func_calc_LNG_SFOC(df_nova, dict_ships["ship_nova"])
    df_smeralda = func_calc_LNG_SFOC(df_smeralda, dict_ships["ship_smeralda"])

    df_nova = func_getAmountOfEnginesRunning(df_nova, dict_ships["ship_nova"])
    df_smeralda = func_getAmountOfEnginesRunning(df_smeralda, dict_ships["ship_smeralda"])

    df_nova = func_calcAvgSfocRunningEngines(df_nova, dict_ships["ship_nova"])
    df_smeralda = func_calcAvgSfocRunningEngines(df_smeralda, dict_ships["ship_smeralda"])

    df_nova = func_calcAvgLoadRunningEngines(df_nova, dict_ships["ship_nova"])
    df_smeralda = func_calcAvgLoadRunningEngines(df_smeralda, dict_ships["ship_smeralda"])

    #region flag_rawData_totalSTRSPower
    df_nova = func_addNewSumColumnWithTotal(
        df_nova, dict_ships["ship_nova"], flag_rawData_totalSTRSPower,
        flag_rawData_MV1_S_TRS1_ACTIVE_PWR_kW_x, flag_rawData_MV1_S_TRS2_ACTIVE_PWR_kW_x,
        flag_rawData_MV2_S_TRS3_ACTIVE_PWR_kW_x, flag_rawData_MV2_S_TRS4_ACTIVE_PWR_kW_x
    )
    df_smeralda = func_addNewSumColumnWithTotal(
        df_smeralda, dict_ships["ship_smeralda"], flag_rawData_totalSTRSPower,
        flag_rawData_MV1_S_TRS1_ACTIVE_PWR_kW_x, flag_rawData_MV1_S_TRS2_ACTIVE_PWR_kW_x,
        flag_rawData_MV2_S_TRS3_ACTIVE_PWR_kW_x, flag_rawData_MV2_S_TRS4_ACTIVE_PWR_kW_x
    )
    #endregion

    #region flag_rawData_total_MainEngine_PWR
    df_nova = func_addNewSumColumnWithTotal(
        df_nova, dict_ships["ship_nova"], flag_rawData_total_MainEngine_PWR,
        flag_rawData_MV1_DG1_ACTIVE_PWR_kW, flag_rawData_MV1_DG2_ACTIVE_PWR_kW,
        flag_rawData_MV2_DG3_ACTIVE_PWR_kW, flag_rawData_MV2_DG4_ACTIVE_PWR_kW
    )
    df_smeralda = func_addNewSumColumnWithTotal(
        df_smeralda, dict_ships["ship_smeralda"], flag_rawData_total_MainEngine_PWR,
        flag_rawData_MV1_DG1_ACTIVE_PWR_kW, flag_rawData_MV1_DG2_ACTIVE_PWR_kW,
        flag_rawData_MV2_DG3_ACTIVE_PWR_kW, flag_rawData_MV2_DG4_ACTIVE_PWR_kW
    )
    #endregion

    # region flag_rawData_total_MainEngine_PWR
    df_nova = func_addNewSumColumnWithTotal(
        df_nova, dict_ships["ship_nova"], flag_rawData_total_POD_PWR,
        flag_rawData_MV1_POD1_ACTIVE_PWR_kW_x, flag_rawData_MV2_POD2_ACTIVE_PWR_kW_x
    )
    df_smeralda = func_addNewSumColumnWithTotal(
        df_smeralda, dict_ships["ship_smeralda"], flag_rawData_total_POD_PWR,
        flag_rawData_MV1_POD1_ACTIVE_PWR_kW_x, flag_rawData_MV2_POD2_ACTIVE_PWR_kW_x
    )
    # endregion

    # region flag_rawData_total_MainEngine_PWR
    df_nova = func_addNewSumColumnWithTotal(
        df_nova, dict_ships["ship_nova"], flag_rawData_total_POD_MTR_PRW,
        flag_rawData_POD1_PROP_ACTUAL_MTR_PWR_x, flag_rawData_POD2_PROP_ACTUAL_MTR_PWR_x
    )
    df_smeralda = func_addNewSumColumnWithTotal(
        df_smeralda, dict_ships["ship_smeralda"], flag_rawData_total_POD_MTR_PRW,
        flag_rawData_POD1_PROP_ACTUAL_MTR_PWR_x, flag_rawData_POD2_PROP_ACTUAL_MTR_PWR_x
    )
    # endregion

    # region flag_rawData_total_LNG_GVU_Flow
    df_nova = func_addNewSumColumnWithTotal(
        df_nova, dict_ships["ship_nova"], flag_rawData_total_LNG_GVU_Flow,
        flag_rawData_ME1_FUEL_GAS_GVU_FLOW_x, flag_rawData_ME2_FUEL_GAS_GVU_FLOW_x,
        flag_rawData_ME3_FUEL_GAS_GVU_FLOW_x, flag_rawData_ME4_FUEL_GAS_GVU_FLOW_x
    )
    df_smeralda = func_addNewSumColumnWithTotal(
        df_smeralda, dict_ships["ship_smeralda"], flag_rawData_total_LNG_GVU_Flow,
        flag_rawData_ME1_FUEL_GAS_GVU_FLOW_x, flag_rawData_ME2_FUEL_GAS_GVU_FLOW_x,
        flag_rawData_ME3_FUEL_GAS_GVU_FLOW_x, flag_rawData_ME4_FUEL_GAS_GVU_FLOW_x
    )
    # endregion

    return df_nova, df_smeralda


' #####################################################################################################################'
def f_getBestFitScalingFactor(maxY):
    scalingFactor = 1

    if maxY < 1:
        scalingFactor = 1

    if maxY in range(1, 10):
        scalingFactor = 1

    if maxY in range(10, 100):
        scalingFactor = 10

    if maxY in range(100, 1000):
        scalingFactor = 100

    if maxY in range(1000, 10000):
        scalingFactor = 1000

    if maxY in range(10000, 100000):
        scalingFactor = 10000

    return scalingFactor

' #####################################################################################################################'
def f_roundToUsefulNextTensOfThousands(
    maxY,
    generic_y_signal
):
    if generic_y_signal == flag_rawData_avgLoad_runningEngines:
        return 100

    # if generic_y_signal == flag_rawData_total_POD_PWR:
    #     return 35000
    #
    # if generic_y_signal == flag_rawData_total_POD_MTR_PRW:
    #     return 35000

    scalingFactor = f_getBestFitScalingFactor(maxY)

    print("maxY before ceil up: " + str(maxY))
    maxY = math.ceil(maxY/(len(str(int(maxY)))*scalingFactor)) * (len(str(int(maxY)))*scalingFactor)
    print("maxY after ceil up: " + str(maxY))

    return maxY

' #####################################################################################################################'
def func_getSignalName(
    y_signal
):
    if y_signal == flag_rawData_totalSTRSPower:
        return "STRS PWR [MW]"

    if y_signal == flag_rawData_total_POD_PWR:
        return "POD-PROP PWR [MW]"

    if y_signal == flag_rawData_total_POD_MTR_PRW:
        return "POD-MTR PWR [MW]"

    if y_signal == flag_rawData_total_MainEngine_PWR:
        return "TOTAL ME PWR [MW]"

    if y_signal == flag_rawData_total_LNG_GVU_Flow:
        return "TOTAL LNG GVU FLOW [kg]"

    if y_signal == flag_rawData_avgLoad_runningEngines:
        return "AVG Load running engines [%]"

    return "SIGNAL not defined"

' #####################################################################################################################'
def func_getSignalNameAppendix(
    plotData_PWR_per_NM
):
    if plotData_PWR_per_NM:
        return " per NM sailed"

    return " over speed"

' #####################################################################################################################'
def func_get_x_axisLabel(
    xSignal
):
    if xSignal == flag_rawData_INS_SPEED_OVER_GROUND_x:
        return "SOG [kn]"

    if xSignal == flag_rawData_INS_SPEED_THROUGH_WATER_x:
        return "STW [kn]"

    return "x label not defined"

' #####################################################################################################################'
def func_get_y_axisLabel(
    powerSignal_NAME,
    plotData_PWR_per_NM,
    signalNameAppendix,
    convertSignalIntoDollar
):
    inDollar = ""
    if convertSignalIntoDollar:
        inDollar = " in $! "

    if plotData_PWR_per_NM:
        return powerSignal_NAME + inDollar + signalNameAppendix

    return powerSignal_NAME + inDollar

' #####################################################################################################################'
def func_plotGenericGraphs(
    df_nova,
    df_smeralda,
    generic_x_signal,
    generic_y_signal
):
    if generic_x_signal == "" or generic_y_signal == "":
        print("NO GENERIC SIGNAL DEFINED!!!")
        print("generic_x_signal: " + generic_x_signal)
        print("generic_y_signal: " + generic_y_signal)
        return

    powerSignal_NAME = func_getSignalName(generic_y_signal)

    plotDataEngineWise = True

    # region GENERIC SIGNAL over Speed
    if dict_plotTheseGenericGraphs["plot_signal_overSpeed"]:
        plotData_PWR_per_NM = False
        convertSignalIntoDollar = False
        signalNameAppendix = func_getSignalNameAppendix(plotData_PWR_per_NM)

        x_axisLabel = func_get_x_axisLabel(generic_x_signal)
        y_axisLabel = func_get_y_axisLabel(powerSignal_NAME, plotData_PWR_per_NM, signalNameAppendix, convertSignalIntoDollar)

        if dict_plotTheseShips["plot_nova"]:
            func_createSimpleScatter(
                df_nova, dict_ships["ship_nova"],
                0, 25, 0, f_roundToUsefulNextTensOfThousands(df_nova[generic_y_signal].max(), generic_y_signal),
                powerSignal_NAME + signalNameAppendix, scatter_dotTransparency, scatter_dotSize,
                generic_x_signal, generic_y_signal,
                x_axisLabel, y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
            )

        if dict_plotTheseShips["plot_smeralda"]:
            func_createSimpleScatter(
                df_smeralda, dict_ships["ship_smeralda"],
                0, 25, 0, f_roundToUsefulNextTensOfThousands(df_smeralda[generic_y_signal].max(), generic_y_signal),
                powerSignal_NAME + signalNameAppendix, scatter_dotTransparency, scatter_dotSize,
                generic_x_signal, generic_y_signal,
                x_axisLabel, y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
            )
    # endregion

    # region GENERIC SIGNAL relative per NM sailed
    if dict_plotTheseGenericGraphs["plot_signal_perNMsailed_overSpeed"]:
        plotData_PWR_per_NM = True
        convertSignalIntoDollar = False

        signalNameAppendix = func_getSignalNameAppendix(plotData_PWR_per_NM)

        x_axisLabel = func_get_x_axisLabel(generic_x_signal)
        y_axisLabel = func_get_y_axisLabel(powerSignal_NAME, plotData_PWR_per_NM, signalNameAppendix, convertSignalIntoDollar)

        if dict_plotTheseShips["plot_nova"]:
            func_createSimpleScatter(
                df_nova, dict_ships["ship_nova"],
                0, 25, 0, f_roundToUsefulNextTensOfThousands(df_nova[generic_y_signal].max(), generic_y_signal),
                powerSignal_NAME + signalNameAppendix, scatter_dotTransparency, scatter_dotSize,
                generic_x_signal, generic_y_signal,
                x_axisLabel, y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
            )

        if dict_plotTheseShips["plot_smeralda"]:
            func_createSimpleScatter(
                df_smeralda, dict_ships["ship_smeralda"],
                0, 25, 0, f_roundToUsefulNextTensOfThousands(df_smeralda[generic_y_signal].max(), generic_y_signal),
                powerSignal_NAME + signalNameAppendix, scatter_dotTransparency, scatter_dotSize,
                generic_x_signal, generic_y_signal,
                x_axisLabel, y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
            )
    # endregion

    # region PWR in $ relative per NM sailed
    if dict_plotTheseGenericGraphs["plot_signal_perDollar_perNMSailed_overSpeed"]:
        plotData_PWR_per_NM = False
        convertSignalIntoDollar = True

        signalNameAppendix = func_getSignalNameAppendix(plotData_PWR_per_NM)

        x_axisLabel = func_get_x_axisLabel(generic_x_signal)
        y_axisLabel = func_get_y_axisLabel(powerSignal_NAME, plotData_PWR_per_NM, signalNameAppendix, convertSignalIntoDollar)

        if dict_plotTheseShips["plot_nova"]:
            func_createSimpleScatter(
                df_nova, dict_ships["ship_nova"],
                0, 25, 0, f_roundToUsefulNextTensOfThousands(df_nova[generic_y_signal].max(), generic_y_signal),
                powerSignal_NAME + " per NM sailed", scatter_dotTransparency, scatter_dotSize,
                generic_x_signal, generic_y_signal,
                x_axisLabel, y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
            )

        if dict_plotTheseShips["plot_smeralda"]:
            func_createSimpleScatter(
                df_smeralda, dict_ships["ship_smeralda"],
                0, 25, 0, f_roundToUsefulNextTensOfThousands(df_smeralda[generic_y_signal].max(), generic_y_signal),
                powerSignal_NAME + " per NM sailed", scatter_dotTransparency, scatter_dotSize,
                generic_x_signal, generic_y_signal,
                x_axisLabel, y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
            )
    # endregion

' #####################################################################################################################'
def func_plot_GVU_Charts(
    df_nova,
    df_smeralda
):
    if not plot_GVU_LNGCharts:
        return

    # region TOTAL GVU over Speed
    plotDataEngineWise = True
    plotData_PWR_per_NM = False
    convertSignalIntoDollar = False

    generic_x_signal = flag_rawData_INS_SPEED_THROUGH_WATER_x
    generic_y_signal = flag_rawData_total_LNG_GVU_Flow
    powerSignal_NAME = func_getSignalName(generic_y_signal)

    plotData_PWR_per_NM = False
    convertSignalIntoDollar = False

    signalNameAppendix = func_getSignalNameAppendix(plotData_PWR_per_NM)
    y_axisLabel = func_get_y_axisLabel(powerSignal_NAME, plotData_PWR_per_NM, signalNameAppendix, convertSignalIntoDollar)

    if dict_plotTheseShips["plot_nova"]:
        func_createSimpleScatter(
            df_nova, dict_ships["ship_nova"],
            0, 25, 0, f_roundToUsefulNextTensOfThousands(df_nova[generic_y_signal].max(), generic_y_signal),
            powerSignal_NAME + " over speed", scatter_dotTransparency, scatter_dotSize,
            generic_x_signal, generic_y_signal,
            "STW [kn]", y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
        )

    if dict_plotTheseShips["plot_smeralda"]:
        func_createSimpleScatter(
            df_smeralda, dict_ships["ship_smeralda"],
            0, 25, 0, f_roundToUsefulNextTensOfThousands(df_smeralda[generic_y_signal].max(), generic_y_signal),
            powerSignal_NAME + "per NM sailed", scatter_dotTransparency, scatter_dotSize,
            generic_x_signal, generic_y_signal,
            "STW [kn]", y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
        )
    # endregion

    # region TOTAL GVU relative per NM sailed
    plotDataEngineWise = True
    plotData_PWR_per_NM = True
    convertSignalIntoDollar = False

    generic_x_signal = flag_rawData_INS_SPEED_THROUGH_WATER_x
    generic_y_signal = flag_rawData_total_LNG_GVU_Flow
    powerSignal_NAME = func_getSignalName(generic_y_signal)

    plotData_PWR_per_NM = True
    convertSignalIntoDollar = False

    signalNameAppendix = func_getSignalNameAppendix(plotData_PWR_per_NM)
    y_axisLabel = func_get_y_axisLabel(powerSignal_NAME, plotData_PWR_per_NM, signalNameAppendix, convertSignalIntoDollar)

    if dict_plotTheseShips["plot_nova"]:
        func_createSimpleScatter(
            df_nova, dict_ships["ship_nova"],
            0, 25, 0, f_roundToUsefulNextTensOfThousands(df_nova[generic_y_signal].max(), generic_y_signal),
            powerSignal_NAME + " per NM sailed", scatter_dotTransparency, scatter_dotSize,
            generic_x_signal, generic_y_signal,
            "STW [kn]", y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
        )

    if dict_plotTheseShips["plot_smeralda"]:
        func_createSimpleScatter(
            df_smeralda, dict_ships["ship_smeralda"],
            0, 25, 0, f_roundToUsefulNextTensOfThousands(df_smeralda[generic_y_signal].max(), generic_y_signal),
            powerSignal_NAME + "per NM sailed", scatter_dotTransparency, scatter_dotSize,
            generic_x_signal, generic_y_signal,
            "STW [kn]", y_axisLabel, plotDataEngineWise, 0, plotData_PWR_per_NM, convertSignalIntoDollar
        )
    # endregion

' #####################################################################################################################'
def func_plotSFOC_Curves():
    if plotSFOC_Curves:
        if dict_plotTheseShips["plot_nova"]:
            func_printSFOC(df_nova, dict_ships["ship_nova"])

        if dict_plotTheseShips["plot_smeralda"]:
            func_printSFOC(df_smeralda, dict_ships["ship_smeralda"])

' #####################################################################################################################'
def func_getRealFlagNotJustStr(genericSignal):
    if genericSignal == "flag_rawData_INS_SPEED_OVER_GROUND_x":
        return flag_rawData_INS_SPEED_OVER_GROUND_x

    if genericSignal == "flag_rawData_INS_SPEED_THROUGH_WATER_x":
        return flag_rawData_INS_SPEED_THROUGH_WATER_x

    if genericSignal == "flag_rawData_total_POD_PWR":
        return flag_rawData_total_POD_PWR

    if genericSignal == "flag_rawData_total_POD_MTR_PRW":
        return flag_rawData_total_POD_MTR_PRW

    if genericSignal == "flag_rawData_totalSTRSPower":
        return flag_rawData_totalSTRSPower

    if genericSignal == "flag_rawData_total_MainEngine_PWR":
        return flag_rawData_total_MainEngine_PWR

    if genericSignal == "flag_rawData_avgSFOC_runningEngines":
        return flag_rawData_avgSFOC_runningEngines

    if genericSignal == "flag_rawData_avgLoad_runningEngines":
        return flag_rawData_avgLoad_runningEngines

' #####################################################################################################################'
def func_readGenericSignal(
    generic_x_signal,
    generic_y_signal,
    thisSignalNumberInDict
):
    for thisSignal in dict_generic_x_signal:
        if dict_generic_x_signal[thisSignal]:
            generic_x_signal = thisSignal
            print("use this generic_x_signal " + generic_x_signal)
            generic_x_signal = func_getRealFlagNotJustStr(generic_x_signal)
            break

    subSignalCount = 0
    for thisSignal in dict_generic_y_signal:
        if dict_generic_y_signal[thisSignal]:
            subSignalCount+=1
            if subSignalCount == thisSignalNumberInDict:
                generic_y_signal = thisSignal
                print("use this generic_y_signal " + generic_y_signal)
                generic_y_signal = func_getRealFlagNotJustStr(generic_y_signal)
                break

    return generic_x_signal, generic_y_signal

' #####################################################################################################################'
def func_check_Y_signalAmount():
    signalCount = 0
    for thisSignal in dict_generic_y_signal:
        if dict_generic_y_signal[thisSignal]:
            print("show this generic signal " + thisSignal)
            signalCount+=1

    print("we have " +str(signalCount) + " generic signals activated")
    return signalCount

' #####################################################################################################################'
def func_exportFiles(
    df_nova,
    df_smeralda
):
    if dict_exportFiles["export_nova"]:
        df_nova.to_csv("df_nova.csv", sep=";", decimal=".")

    if dict_exportFiles["export_smeralda"]:
        df_smeralda.to_csv("df_smeralda.csv", sep=";", decimal=".")

' #####################################################################################################################'
def func_filterRawData(
    df_nova,
    df_smeralda
):
    if dict_filterRawData["filter_trueWind"]:
        if func_isThisColumnAvailable(df_nova, dict_ships["ship_nova"], flag_rawData_INS_TRUE_WINDSPEED_x):
            print(dict_ships["ship_nova"] + " len df before wind filter " + str(df_nova.shape[0]))
            df_nova = df_nova[abs(df_nova[flag_rawData_INS_TRUE_WINDSPEED_x]) <= maxTrueWindValue]
            df_nova.reset_index(drop=True)
            print("len df after wind filter " + str(df_nova.shape[0]))

        if func_isThisColumnAvailable(df_smeralda, dict_ships["ship_smeralda"], flag_rawData_INS_TRUE_WINDSPEED_x):
            print(dict_ships["ship_smeralda"] + " len df before wind filter " + str(df_smeralda.shape[0]))
            df_smeralda = df_smeralda[abs(df_smeralda[flag_rawData_INS_TRUE_WINDSPEED_x]) <= maxTrueWindValue]
            df_smeralda.reset_index(drop=True)
            print("len df after wind filter " + str(df_nova.shape[0]))

    return df_nova, df_smeralda

' #####################################################################################################################'
def func_getUserName():
    username = getpass.getuser()

    print("tool in use by: " + username)

    return username

' #####################################################################################################################'
' #####################################################################################################################'
' #####################################################################################################################'

username = func_getUserName()

generic_x_signal = ""
generic_y_signal = ""

df_nova = pd.DataFrame()
df_smeralda = pd.DataFrame()

df_nova = f_readAllFilesInSubfolders(df_nova, dict_readTheseSubFiles_nova, dict_ships["ship_nova"])
df_smeralda = f_readAllFilesInSubfolders(df_smeralda, dict_readTheseSubFiles_smeralda, dict_ships["ship_smeralda"])

df_nova, df_smeralda = func_filterRawData(df_nova, df_smeralda)

if redoFlagStructure:
    for thisColumn in df_nova.columns:
        print("flag_rawData_" + func_getNameWithoutBlanks(thisColumn)+ " = " + "'" + thisColumn + "'")

df_nova, df_smeralda = func_preCalcSomeFurtherValues(df_nova, df_smeralda)

func_plotSFOC_Curves()

activatedGenericSignals = func_check_Y_signalAmount()

if activatedGenericSignals > 0:
    thisSignal = 1
    while thisSignal <= activatedGenericSignals:
        generic_x_signal, generic_y_signal = func_readGenericSignal(generic_x_signal, generic_y_signal, thisSignal)

        func_plotGenericGraphs(df_nova, df_smeralda, generic_x_signal, generic_y_signal)

        thisSignal+=1

func_plot_GVU_Charts(df_nova, df_smeralda)

func_exportFiles(df_nova, df_smeralda)