#!/usr/bin/python3
import pandas as pd
import plotly.graph_objects as go

# Settings
title = "Amplification Curve"
labels = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
          "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
colors = ["#e8a5eb", "#facc9e", "#e8e948", "#1bb763", "#24f2f3", "#1db3ea", "#d1aef8", "#c8c92c",
          "#f32020", "#fd9b09", "#406386", "#24a1a1", "#1414f8", "#959697", "#744a20", "#7b45a5"]
raw_file_path = "detection.csv"
ifc_file_path = "cali_factor.csv"



def normalize():
    for i in range(0, 16):
        df_current_well = df_raw[f'well{i+1}']
        df_current_ifc = df_ifc[f'well{i+1}']
        baseline = df_current_well[8:30].mean()
        df_normalization[f'well{i+1}'] = (df_raw[f'well{i+1}']-baseline)/df_current_ifc[0] # normalized = (IF(t)-IF(b))/IFc

def draw():
    # Source
    x_data = df_normalization["time"]
    y_data_series = [];
    for i in range(0,16):
        filling_value = df_normalization[f"well{i+1}"][7]
        y_data_series.append(df_normalization[f"well{i+1}"].rolling(window=7).mean().fillna(filling_value))


    fig = go.Figure()
    
    # add line
    for i in range(0,16):
        fig.add_trace(go.Scatter(x=x_data.index/2, y=y_data_series[i], 
                                 mode='lines', name=labels[i], line_shape='spline',
                                 line=dict(color=colors[i],
                                           width=4)))
    fig.update_layout(title=title,
                      width=840, height=500,
                      xaxis_title='Time(minutes)',
                      yaxis_title='Normalized relative fluorescence',
                      font=dict(
                        family="Arial",
                        size=16,
                        color="#555555"),
                      legend=dict(
                        font=dict(
                            family="Courier",
                            size=12,
                        )
                      )
                     )
    fig.update_xaxes(range=[0, x_data.size/2])
    fig.update_yaxes(range=[-0.1,1])
    #fig.show()
    fig.write_image("amplification_curve.png")


def draw_chart():
    global df_raw, df_ifc, df_normalization
    df_raw = pd.read_csv(raw_file_path)
    df_ifc = pd.read_csv(ifc_file_path)
    df_normalization = df_raw.copy()
    normalize()
    draw()

draw_chart()
