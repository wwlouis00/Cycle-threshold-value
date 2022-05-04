from turtle import color
from matplotlib.axis import XAxis
import plotly.graph_objs as go
import pandas as pd
import os
from datetime import datetime, time

if not os.path.isdir('./result'):
    print("Directory 'result' does not exist.")
    os.mkdir('./result')
raw_file_path = "./data/2022_04_11_17_23_03RP4.csv"

def get_accumulation_time():
    df_time = df_normalization['time']
    time_ori = datetime.strptime(df_time[0], "%H:%M:%S")
    time_delta = []
    for time in df_time:
        time_now = datetime.strptime(time, "%H:%M:%S")
        time_delta.append((time_now - time_ori).seconds/60)
    df_normalization.insert(1, column="accumulation", value=time_delta)
    

def get_StdDev_and_Avg():
    StdDev = []
    Avg = []
    for i in range(0, 16):
        df_current_well = df_normalization[f'well_{i+1}']
        StdDev.append(df_current_well[first_time*2:twice_time*2].std())
        Avg.append(df_current_well[first_time:twice_time].mean())
    return StdDev, Avg

def normalize():
    for i in range(0, 16):
        df_current_well = df_raw[f'well_{i+1}']
        baseline = df_current_well[first_time*2:twice_time*2].mean()
        df_normalization[f'well{i+1}'] = (df_raw[f'well_{i+1}']-baseline) / baseline # normalized = (IF(t)-IF(b))/IF(b)

def Moving_Average():
    for i in range(0,16,1):
        well_move_average.append(df_raw["well_" + str(i+1)].rolling(window=5).mean())


def get_ct_threshold():
    threshold_value = []
    StdDev, Avg = get_StdDev_and_Avg()
    for i in range(0, 16):
        threshold_value.append(n_sd*StdDev[i] + Avg[i])
    return threshold_value    
def get_ct_value(threshold_value):
    Ct_value = []
    for i in range(0, 16):
        df_current_well = df_normalization[f'well_{i+1}']
        df_accumulation = df_normalization['accumulation']
        try:
            for j, row in enumerate(df_current_well):
                if row >= threshold_value[i]:
                    # print(f"row: {row}")
                    thres_lower = df_current_well[j-1]
                    thres_upper = df_current_well[j]                
                    acc_time_lower = df_accumulation[j-1]
                    acc_time_upper = df_accumulation[j+1]
                    
                    # linear regression
                    x2 = acc_time_upper
                    y2 = thres_upper
                    x1 = acc_time_lower
                    y1 = thres_lower
                    y = threshold_value[i]
                    x = (x2-x1)*(y-y1)/(y2-y1)+x1

                    Ct_value.append(round(x, 2))
                    # print(f"Ct of well_{i+1} is {round(x, 2)}")
                    break

                # if there is no Ct_value availible
                elif j == len(df_current_well)-1:
                    Ct_value.append(99.99)
        except Exception as e:
            Ct_value.append(99.99)

    return Ct_value
def ct_calculation():
    global df_raw, df_normalization ,first_time,twice_time,n_sd,well_move_average,Csv_well
    well_move_average =[]
    first_time = int(input("Input Start time:   "))
    twice_time = int(input("Input End time:   "))
    n_sd = int(input("Input Std:   "))   
    df_raw = pd.read_csv(raw_file_path)
    df_normalization = df_raw.copy()    #將df_raw複製給df_df_normalization
    get_accumulation_time()
    normalize()
    threshold_value = get_ct_threshold()
    Moving_Average()
    Ct_value = get_ct_value(threshold_value)
    print(Ct_value)


def main():
    ct_calculation()
if __name__ == '__main__':
    main()
















# raw_file_path = pd.read_csv('./result/Cali_result/2022-01-03 11-43-38CT_Value_MA_data.csv')
# raw_file_path = raw_file_path.fillna(0)
# print(raw_file_path)

# well_num = 16
# wellList_MA5_NOR = []

# for n in range(1,well_num+1,1):
#     wellList_MA5_NOR.append("well" f"{n}""_NOR")

# colorTab_More4 = ['#333c41','#eb0973','#39a6dd','#91be3e',
#                   '#96cbb3','#0081b4','#e990ab','#e5352b',
#                   '#ffd616','#29245c','#85b7e2','#00af3e',
#                   '#ef9020','#9f1f5c','#f47b7b','#949483']

# colorTab_AirBus = ['#4298b5','#005670','#00205b','#009f4d',
#                   '#84bd00','#efdf00','#fe5000','#e4002b',
#                   '#da1884','#a51890','#0077c8','#008eaa',
#                   '#74d2e7','#48a9c5','#0085ad','#8db9ca']



# fig = go.Figure([
#     #Well1
#     go.Scatter(
#         name = 'A1',
#         x=df['index'],
#         y=df['well1'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[0], size=6),
#         showlegend=True
#     ),
#     #Well2
#     go.Scatter(
#         name = 'A2',
#         x=df['index'],
#         y=df['well2'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[1], size=6),
#         showlegend=True
#     ),
#      #Well3
#     go.Scatter(
#         name = 'A3',
#         x=df['index'],
#         y=df['well3'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[2], size=6),
#         showlegend=True
#     ),
#     #Well4
#     go.Scatter(
#         name = 'A4',
#         x=df['index'],
#         y=df['well4'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[3], size=6),
#         showlegend=True
#     ),
#     #Well5
#     go.Scatter(
#         name = 'A5',
#         x=df['index'],
#         y=df['well5'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[4], size=6),
#         showlegend=True
#     ),
#     #Well6
#     go.Scatter(
#         name = 'A6',
#         x=df['index'],
#         y=df['well6'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[5], size=6),
#         showlegend=True
#     ),
#      #Well7
#     go.Scatter(
#         name = 'A7',
#         x=df['index'],
#         y=df['well7'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[6], size=6),
#         showlegend=True
#     ),
#     #Well8
#     go.Scatter(
#         name = 'A8',
#         x=df['index'],
#         y=df['well8'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[7], size=6),
#         showlegend=True
#     ),
#     #Well9
#     go.Scatter(
#         name = 'B1',
#         x=df['index'],
#         y=df['well9'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[8], size=6),
#         showlegend=True
#     ),
#     #Well10
#     go.Scatter(
#         name = 'B2',
#         x=df['index'],
#         y=df['well10'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[9], size=6),
#         showlegend=True
#     ),
#      #Well11
#     go.Scatter(
#         name = 'B3',
#         x=df['index'],
#         y=df['well11'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[10], size=6),
#         showlegend=True
#     ),
#     #Well12
#     go.Scatter(
#         name = 'B4',
#         x=df['index'],
#         y=df['well12'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[11], size=6),
#         showlegend=True
#     ),
#     #Well13
#     go.Scatter(
#         name = 'B5',
#         x=df['index'],
#         y=df['well13'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[12], size=6),
#         showlegend=True
#     ),
#     #Well14
#     go.Scatter(
#         name = 'B6',
#         x=df['index'],
#         y=df['well14'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[13], size=6),
#         showlegend=True
#     ),
#      #Well15
#     go.Scatter(
#         name = 'B7',
#         x=df['index'],
#         y=df['well15'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[14], size=6),
#         showlegend=True
#     ),
#     #Well16
#     go.Scatter(
#         name = 'B8',
#         x=df['index'],
#         y=df['well16'],
#         mode='lines',
#         marker=dict(color=colorTab_More4[15], size=6),
#         showlegend=True
#     )
# ])
# fig.update_layout(
#     xaxis_title = 'Time(min)',
#     yaxis_title='Normalized fluorescent intensity',
#     title='Amplification curve',
#     hovermode="x"
# )
# fig.show()