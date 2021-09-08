import pandas as pd

from tkinter import *
import os

from bokeh.plotting import figure, show, output_file
from bokeh.models import LinearAxis, ColumnDataSource, Range1d, LabelSet, Label, TableColumn, DataTable

redoFlagStructure = False
exportFinalFiles = False

scatter_FrameWidth = 1200
scatter_FramHeight = 800

#region nova subfolders
dict_readTheseSubFiles_nova = {
    '_ FINE nova ALL AC PWR':                   0,
    '_ FINE nova ALL AC Reheating Flow per FZ': 0,
    '_ FINE nova ALL BLR Different Figures':    0,
    '_ FINE nova ALL BT PWR':                   0,
    '_ FINE nova ALL Chilled WTR Temp per FZ':  0,
    '_ FINE nova ALL CSW Pumps PWR':            0,
    '_ FINE nova ALL DG ACTIVE PWR':                1,
    '_ FINE nova ALL DG POWER Factor':          0,
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
    '_ FINE nova ALL GSP POD TOT PWR':          0,
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
    '_ FINE smeralda ALL DG POWER Factor':          0,
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
    '_ FINE smeralda ALL GSP POD TOT PWR':          0,
    '_ FINE smeralda ALL GSP TSC GVR VENT':         0,
    '_ FINE smeralda ALL GVU FLOW ME':                   1,
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
    '_ FINE smeralda ALL NAV Signals':                   1,
    '_ FINE smeralda ALL POD CAU FAN PWR':          0,
    '_ FINE smeralda ALL POD PROP MTR PWR':              1,
    '_ FINE smeralda ALL POD PWR':                       1,
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

flag_rawData_EngineLoadPercent_DG1 = "DG1 load percent"
flag_rawData_EngineLoadPercent_DG2 = "DG1 load percent"
flag_rawData_EngineLoadPercent_DG3 = "DG1 load percent"
flag_rawData_EngineLoadPercent_DG4 = "DG1 load percent"
#endregion

dict_ships = {
    "ship_nova": "AIDAnova",
    "ship_smeralda": "Costa Smeralda"
}

dict_colorsForScatter = {
    1: '#7e59eb', #'#8ddbbc',
    2: '#8f455f',
    3: '#0b963c',
    4: '#b33d0e',
    5: '#24c9c9',
    6: '#bf370d',
    7: '#33babf',
    8: '#7e59eb',
    9: '#8f455f'
}

' #####################################################################################################################'
def f_readAllFilesInSubfolders(
    df_thisShip,
    dict_signalsThisShip,
    shipName
):
    print("\n#################################################\n#################################################"
          " \nSCAN all files in XL-Class DATA FOLDER and load data for " + shipName)

    folder_location = 'E:\\001_CMG\\HOME\\XL-Class-Automation-Data'

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
    print("LNG SOFC for " + thisShip + " and engine " + flag_SFOC)

    thisDF[flag_SFOC] = 0

    if not func_isThisColumnAvailable(thisDF, thisShip, flag_GVU_Flow):
        return thisDF

    if not func_isThisColumnAvailable(thisDF, thisShip, flag_DGx_ACTIVE_PWR_kW):
        return thisDF

    thisDF = f_doTheSFOC(
        thisDF, flag_SFOC, flag_GVU_Flow, flag_DGx_ACTIVE_PWR_kW)

    return thisDF

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
def func_printSFOC(
    thisDF,
    thisShip
):
    scatter_dotTransparency = 0.85
    scatter_dotSize = 1

    scatterFrame_rawDataOverTime = f_prepareTheScatterFrame(
            scatter_FrameWidth, scatter_FramHeight, (0, 100),
            (0, 300),
            str(thisShip + " SFOC LNG per engine")
        )

    scatterFrame_rawDataOverTime.circle(
        thisDF[thisDF[flag_rawData_SFOC_LNG_DG1] > 100][flag_rawData_EngineLoadPercent_DG1],
        thisDF[thisDF[flag_rawData_SFOC_LNG_DG1] > 100][flag_rawData_SFOC_LNG_DG1],
        size=scatter_dotSize, color=dict_colorsForScatter[1],
        alpha=scatter_dotTransparency,
        legend_label=thisShip + " SFOC DG1"
    )

    thisFileName = thisShip + " SFOC LNG per engine"
    output_file(thisFileName + '.html', #dict_subFolderName["subfolder_exportGraphs"] + "/"
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

    scatterFrame_rawDataOverTime.xaxis.axis_label = "TIME"
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
def func_doTheLoadPercentForThisEngine(
    thisDF,
    thisShip,
    flag_engineLoad_ABS,
    flag_engineLoad_Pct
):
    thisDF[flag_engineLoad_Pct] = 0

    if not func_isThisColumnAvailable(thisDF, thisShip, flag_engineLoad_ABS):
        return thisDF
    else:
        thisDF.loc[
            (thisDF[flag_engineLoad_ABS] > 100),
            flag_engineLoad_Pct] = \
        round(
            thisDF.loc[
                (thisDF[flag_engineLoad_ABS] > 100),
                flag_engineLoad_ABS] / 15440 * 100, 1
        )

    return thisDF

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
' #####################################################################################################################'
' #####################################################################################################################'

df_nova = pd.DataFrame()
df_smeralda = pd.DataFrame()

df_nova = f_readAllFilesInSubfolders(df_nova, dict_readTheseSubFiles_nova, dict_ships["ship_nova"])
df_smeralda = f_readAllFilesInSubfolders(df_smeralda, dict_readTheseSubFiles_smeralda, dict_ships["ship_smeralda"])

if redoFlagStructure:
    for thisColumn in df_nova.columns:
        print("flag_rawData_" + func_getNameWithoutBlanks(thisColumn)+ " = " + "'" + thisColumn + "'")

df_nova = func_getEngineLoadPercent(df_nova, dict_ships["ship_nova"])
df_smeralda = func_getEngineLoadPercent(df_smeralda, dict_ships["ship_smeralda"])

df_nova = func_calc_LNG_SFOC(df_nova, dict_ships["ship_nova"])
df_smeralda = func_calc_LNG_SFOC(df_smeralda, dict_ships["ship_smeralda"])

func_printSFOC(df_nova, dict_ships["ship_nova"])
func_printSFOC(df_smeralda, dict_ships["ship_smeralda"])



if exportFinalFiles:
    df_nova.to_csv("df_nova.csv", sep = ";", decimal = ".")
    df_smeralda.to_csv("df_smeralda.csv", sep = ";", decimal = ".")