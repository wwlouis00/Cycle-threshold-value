from turtle import color
from matplotlib.axis import XAxis
import plotly.graph_objs as go
import pandas as pd
import os

if not os.path.isdir('./result'):
    print("Directory 'result' does not exist.")
    os.mkdir('./result')


df = pd.read_csv('./result/Cali_result/2022-01-03 11-43-38CT_Value_MA_data.csv')
df = df.fillna(0)
print(df)

well_num = 16
wellList_MA5_NOR = []

for n in range(1,well_num+1,1):
    wellList_MA5_NOR.append("well" f"{n}""_NOR")

colorTab_More4 = ['#333c41','#eb0973','#39a6dd','#91be3e',
                  '#96cbb3','#0081b4','#e990ab','#e5352b',
                  '#ffd616','#29245c','#85b7e2','#00af3e',
                  '#ef9020','#9f1f5c','#f47b7b','#949483']

colorTab_AirBus = ['#4298b5','#005670','#00205b','#009f4d',
                  '#84bd00','#efdf00','#fe5000','#e4002b',
                  '#da1884','#a51890','#0077c8','#008eaa',
                  '#74d2e7','#48a9c5','#0085ad','#8db9ca']



fig = go.Figure([
    #Well1
    go.Scatter(
        name = 'A1',
        x=df['index'],
        y=df['well1'],
        mode='lines',
        marker=dict(color=colorTab_More4[0], size=6),
        showlegend=True
    ),
    #Well2
    go.Scatter(
        name = 'A2',
        x=df['index'],
        y=df['well2'],
        mode='lines',
        marker=dict(color=colorTab_More4[1], size=6),
        showlegend=True
    ),
     #Well3
    go.Scatter(
        name = 'A3',
        x=df['index'],
        y=df['well3'],
        mode='lines',
        marker=dict(color=colorTab_More4[2], size=6),
        showlegend=True
    ),
    #Well4
    go.Scatter(
        name = 'A4',
        x=df['index'],
        y=df['well4'],
        mode='lines',
        marker=dict(color=colorTab_More4[3], size=6),
        showlegend=True
    ),
    #Well5
    go.Scatter(
        name = 'A5',
        x=df['index'],
        y=df['well5'],
        mode='lines',
        marker=dict(color=colorTab_More4[4], size=6),
        showlegend=True
    ),
    #Well6
    go.Scatter(
        name = 'A6',
        x=df['index'],
        y=df['well6'],
        mode='lines',
        marker=dict(color=colorTab_More4[5], size=6),
        showlegend=True
    ),
     #Well7
    go.Scatter(
        name = 'A7',
        x=df['index'],
        y=df['well7'],
        mode='lines',
        marker=dict(color=colorTab_More4[6], size=6),
        showlegend=True
    ),
    #Well8
    go.Scatter(
        name = 'A8',
        x=df['index'],
        y=df['well8'],
        mode='lines',
        marker=dict(color=colorTab_More4[7], size=6),
        showlegend=True
    ),
    #Well9
    go.Scatter(
        name = 'B1',
        x=df['index'],
        y=df['well9'],
        mode='lines',
        marker=dict(color=colorTab_More4[8], size=6),
        showlegend=True
    ),
    #Well10
    go.Scatter(
        name = 'B2',
        x=df['index'],
        y=df['well10'],
        mode='lines',
        marker=dict(color=colorTab_More4[9], size=6),
        showlegend=True
    ),
     #Well11
    go.Scatter(
        name = 'B3',
        x=df['index'],
        y=df['well11'],
        mode='lines',
        marker=dict(color=colorTab_More4[10], size=6),
        showlegend=True
    ),
    #Well12
    go.Scatter(
        name = 'B4',
        x=df['index'],
        y=df['well12'],
        mode='lines',
        marker=dict(color=colorTab_More4[11], size=6),
        showlegend=True
    ),
    #Well13
    go.Scatter(
        name = 'B5',
        x=df['index'],
        y=df['well13'],
        mode='lines',
        marker=dict(color=colorTab_More4[12], size=6),
        showlegend=True
    ),
    #Well14
    go.Scatter(
        name = 'B6',
        x=df['index'],
        y=df['well14'],
        mode='lines',
        marker=dict(color=colorTab_More4[13], size=6),
        showlegend=True
    ),
     #Well15
    go.Scatter(
        name = 'B7',
        x=df['index'],
        y=df['well15'],
        mode='lines',
        marker=dict(color=colorTab_More4[14], size=6),
        showlegend=True
    ),
    #Well16
    go.Scatter(
        name = 'B8',
        x=df['index'],
        y=df['well16'],
        mode='lines',
        marker=dict(color=colorTab_More4[15], size=6),
        showlegend=True
    )
])
fig.update_layout(
    xaxis_title = 'Time(min)',
    yaxis_title='Normalized fluorescent intensity',
    title='Amplification curve',
    hovermode="x"
)
fig.show()