from connection import app
from dash import html, dcc, callback_context
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_daq as daq
import numpy as np
import json
from flask_login import current_user,logout_user
# from login import logs_data
import datetime
from flask import session


raw_data = pd.read_excel('../data/Data.xlsx')
raw_data = raw_data.reset_index()

with open("../TooltipsText.json", 'r') as file:
    tooltips_texts = json.load(file)

layout = html.Div([
            dcc.Location(id='url_logout_', refresh=True),
            html.Br(),
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Activity Dashboard AMMIS course for:",
                                style = {'textAlign': 'center', 'flex': '90%'},
                                id='output-label',
                                ),
                        html.A("Instructions", 
                               href='https://merode.econ.kuleuven.be/files/Instructions.docx'
                               )
                               ], 
                                style={'display': 'flex','align-items': 'center', 'justify-content': 'center'}),
                    html.H6(id='user-div', 
                            style = {'textAlign': 'center'}, 
                            children='', 
                            )],
                            className="six columns",
                            style = {'width':'80%'}),
                html.Button('Logout', n_clicks=0, id = 'logout-button', className="six columns",
                            style = {'width':'15%'})
                    ], 
                    className='row'),

            html.Div([
                html.Div([
                    html.Div([
                        html.H6("Home Assignment grades",
                                style = {'flex': '96%','textAlign': 'center','font-weight':'bold'}),
                        # html.Img(id='image-tooltip-ha', src = 'assets/tooltip.svg', style={'flex': '4%'},
                        #         className="six columns", title=tooltips_texts['HA']
                        #         ),
                        html.Div([
                                    html.Button(id='button-tooltip-ha', children=[
                                        html.Img(src='../assets/tooltip.svg', title=tooltips_texts['HA']),
                                    ], style={'flex': '4%', 'padding': '0px', 'border': 'none'}),
                                    html.Div(id='ha-output-popup')
                                ])
                                                        
                                ], 
                                style={'display': 'flex','align-items': 'center', 'justify-content': 'center'}),
                    html.Hr(style = {
                                    'height': '2px', 
                                    'margin': '10px 0',  
                                    'background-color': 'black'}),
                    
                    html.Div([
                        html.Div(id='ha1-output',
                            className='six columns'),
                        html.Div(id='ha2-output',
                            className='six columns')]
                            )
                        ],
                        className='six columns',
                        style={"border": "1px solid grey"}
                        ),
                html.Div([
                    html.Div([
                        html.H6("Practice test", 
                                style = {'flex': '96%','textAlign': 'center','font-weight':'bold'}),
                        # html.Img(id='image-tooltip-practice-test', src = 'assets/tooltip.svg',
                        #          style={'flex': '4%'},className="six columns",
                        #          title=tooltips_texts['PracticeTest']
                        #         )
                        html.Div([
                                    html.Button(id='button-tooltip-test', children=[
                                        html.Img(src='../assets/tooltip.svg', title=tooltips_texts['PracticeTest']),
                                    ], style={'flex': '4%', 'padding': '0px', 'border': 'none'}),
                                    html.Div(id='test-output-popup')
                                ])
                            ],
                            style={'display': 'flex','align-items': 'center', 'justify-content': 'center'}),
                    html.Hr(style = {
                                    'height': '2px', 
                                    'margin': '10px 0',  
                                    'background-color': 'black'}),
                    html.Div(id='practice-test-markdown'),
                        ],
                        className='six columns',
                        style={"border": "1px solid grey"}
                        )

                    ],
                    className='row'),
            html.Hr(),
            html.Div([
                html.Div([
                    html.H6("Activity on edX: online exercise sessions",
                            style = {'flex': '98%','textAlign': 'center','font-weight':'bold'}),
                    # html.Img(id='image-tooltip-edx-es', src = 'assets/tooltip.svg',
                    #         style={'flex': '2%'},className="six columns",
                    #         title=tooltips_texts['edXES']
                    #         )
                    html.Div([
                                    html.Button(id='button-tooltip-edxES', children=[
                                        html.Img(src='../assets/tooltip.svg', title=tooltips_texts['edXES']),
                                    ], style={'flex': '4%', 'padding': '0px', 'border': 'none'}),
                                    html.Div(id='edxES-output-popup')
                                ])
                            ], 
                            style={'display': 'flex','align-items': 'center','justify-content': 'center'}),
                html.Hr(style = {
                                'height': '2px', 
                                'margin': '10px 0',  
                                'background-color': 'black'
                                }
                        ),
                html.Div([  
                    html.Div([
                        dcc.Graph(id='perf-avgquiz-plot')
                            ],
                            # className='six columns'
                            ), 
                    html.Div([
                        dcc.Graph(id='perf-quizzes-plot')
                            ],
                            # className='six columns'
                            )
                        ],
                        className='row'
                        )
                    ], 
                    style={"border": "1px solid grey"}
                    ),
            html.Hr(),
            html.Div([
                html.Div([
                    html.H6("Activity on edX: quizzes", 
                            style = {'flex': '98%','textAlign': 'center','font-weight':'bold'}),
                    # html.Img(id='image-tooltip-edx-quizzes', src = 'assets/tooltip.svg',
                    #          style={'flex': '2%'},className="six columns",
                    #          title=tooltips_texts['edXQuizzes']
                    #         )
                    html.Div([
                                    html.Button(id='button-tooltip-edxQuizzes', children=[
                                        html.Img(src='../assets/tooltip.svg', title=tooltips_texts['edXQuizzes']),
                                    ], style={'flex': '4%', 'padding': '0px', 'border': 'none'}),
                                    html.Div(id='edxQuizzes-output-popup')
                                ])
                            ], 
                            style={'display': 'flex','align-items': 'center', 'justify-content': 'center'}),
                html.Hr(style = {
                                'height': '2px', 
                                'margin': '10px 0',  
                                'background-color': 'black'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6("Average score",
                                    style={'text-align': 'center'}
                                    ),
                            dcc.Graph(id='avgquiz-plot')
                                ]
                                ),
                            ],
                            # className='six columns'
                            ), 
    
                    html.Div([
                        html.Div([
                            html.H6("#Quizzes Accumulated", 
                                    style={'text-align': 'center'}),
                            dcc.Graph(id='quizzes-plot')
                                ]
                                ),
                            ],
                            # className='six columns'
                            )
                        ],
                        className='row',
                        ),
                    ], 
                    style={"border": "1px solid grey"}
                    ),
            html.Hr(),
            html.Div([
                html.Div([
                    html.Div([
                        html.H6("Activity in Merlin",
                                style = {'flex': '96%','textAlign': 'center','font-weight':'bold'}),
                        # html.Img(id='image-tooltip-merlin', src = 'assets/tooltip.svg', style={'flex': '4%'},
                        #         className="six columns",title=tooltips_texts['Merlin']
                        #         )
                        html.Div([
                                    html.Button(id='button-tooltip-merlin', children=[
                                        html.Img(src='../assets/tooltip.svg', title=tooltips_texts['Merlin']),
                                    ], style={'flex': '4%', 'padding': '0px', 'border': 'none'}),
                                    html.Div(id='merlin-output-popup')
                                ])
                                ], 
                                style={'display': 'flex','align-items': 'center', 'justify-content': 'center'}
                            ),
                    html.Hr(style = {
                                    'height': '2px', 
                                    'margin': '10px 0',  
                                    'background-color': 'black'
                                    }
                            ),
                    dcc.Graph(id='models-line-plot')
                        ],
                        className='six columns',
                        style={"border": "1px solid grey"}),
                html.Div([
                    html.Div([
                        html.H6("Exercise sessions attendance", 
                                style={'flex': '96%', 'textAlign': 'center', 'font-weight': 'bold'}),
                        # html.Img(id='image-tooltip-ES', src = 'assets/tooltip.svg', style={'flex': '4%'},
                        #          className="six columns",title=tooltips_texts['ES'],
                        #         )
                        html.Div([
                                    html.Button(id='button-tooltip-ES', children=[
                                        html.Img(src='../assets/tooltip.svg', title=tooltips_texts['ES']),
                                    ], style={'flex': '4%', 'padding': '0px', 'border': 'none'}),
                                    html.Div(id='ES-output-popup')
                                ])
                                ], 
                                style={'display': 'flex','align-items': 'center', 'justify-content': 'center'}),
                    html.Hr(style = {
                                    'height': '2px', 
                                    'margin': '10px 0',  
                                    'background-color': 'black'
                                    }
                                    ),
                    html.Div([
                        html.Div(id="legend",
                                style={'font-size': '12px'}),
                        html.Div(id='attendance-chart',
                                style={"text-align": "center", 'font-size': '12px','justify-content': 'center',
                                       'display': 'flex','align-items': 'center'}),
                                                           
                            ],
                            className='row', 
                            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
                    html.Div(id = 'ES-avg')
                            ],
                            className='six columns',
                            style={"border": "1px solid grey"}),
                    ],
                    className='row'),
            html.Br(),
            html.Br()
                ],
                className='ten columns offset-by-one'
                )


@app.callback(
    Output('user-div', 'children'),
    [Input('user-div', 'id')])
def cur_user_v1(input1):
    username = current_user.id
    return username


@app.callback(
    Output('ha-output-popup', 'children'),
    [Input('button-tooltip-ha', 'n_clicks')]
)
def update_output_ha(n_clicks):
    if n_clicks is not None:
        if 'button' in callback_context.triggered[0]['prop_id']:
            return dcc.ConfirmDialog(
                id='confirm-ha',
                message=tooltips_texts['HA'],
                displayed=True
            )
        

@app.callback(
    Output('test-output-popup', 'children'),
    [Input('button-tooltip-test', 'n_clicks')]
)
def update_output_test(n_clicks):
    if n_clicks is not None:
        if 'button' in callback_context.triggered[0]['prop_id']:
            return dcc.ConfirmDialog(
                id='confirm-test',
                message=tooltips_texts['PracticeTest'],
                displayed=True
            )
        

@app.callback(
    Output('ES-output-popup', 'children'),
    [Input('button-tooltip-ES', 'n_clicks')]
)
def update_output_ES(n_clicks):
    if n_clicks is not None:
        if 'button' in callback_context.triggered[0]['prop_id']:
            return dcc.ConfirmDialog(
                id='confirm-ES',
                message=tooltips_texts['ES'],
                displayed=True
            )
        

@app.callback(
    Output('edxES-output-popup', 'children'),
    [Input('button-tooltip-edxES', 'n_clicks')]
)
def update_output_edxES(n_clicks):
    if n_clicks is not None:
        if 'button' in callback_context.triggered[0]['prop_id']:
            return dcc.ConfirmDialog(
                id='confirm-edxES',
                message=tooltips_texts['edXES'],
                displayed=True
            )
        

@app.callback(
    Output('edxQuizzes-output-popup', 'children'),
    [Input('button-tooltip-edxQuizzes', 'n_clicks')]
)
def update_output_edxQUizzes(n_clicks):
    if n_clicks is not None:
        if 'button' in callback_context.triggered[0]['prop_id']:
            return dcc.ConfirmDialog(
                id='confirm-edxQuizzes',
                message=tooltips_texts['edXQuizzes'],
                displayed=True
            )
        

@app.callback(
    Output('merlin-output-popup', 'children'),
    [Input('button-tooltip-merlin', 'n_clicks')]
)
def update_output_merlin(n_clicks):
    if n_clicks is not None:
        if 'button' in callback_context.triggered[0]['prop_id']:
            return dcc.ConfirmDialog(
                id='confirm-merlin',
                message=tooltips_texts['Merlin'],
                displayed=True
            )
  

@app.callback(Output('url_logout_', 'pathname'),
              [Input('logout-button', 'n_clicks'),
               Input('user-div', 'children')])
def logout(n_clicks, selected_index):
    if n_clicks > 0:
        current_session = session['id']
        return '/logout'
    


@app.callback(
    [Output('attendance-chart', 'children'),
     Output("legend", "children"),
      Output("ES-avg", "children")],
    [Input('user-div', 'children')]
)
def update_graph_v1(selected_index):
    data = [
            go.Bar(
                x=[class_name],
                y=[0.7],
                marker=dict(
                    color='green' if status == 1 else
                          'red' if status == 0 else
                          'white',
                ),
                hoverinfo="none",
                
            ) for class_name, status in zip(raw_data[[value for value in raw_data.columns if value.startswith('ES')]].columns,
                                             raw_data[raw_data['Student'] == selected_index][[value for value in raw_data.columns
                                                                                               if value.startswith('ES')]].values[0]
                                             )
        ]
    
    layout = go.Layout(
            width=460,  
            height=240,  
            xaxis={'showticklabels': True, 'fixedrange':True}, 
            yaxis={ 'showticklabels': False, 'fixedrange':True},
            bargap=0.05,
            showlegend=False ,
            font=dict(size=12)
        )
    
    legend = html.Div("🟩: Attended 🟥: Not attended ⬜️: Not yet available", style = {'text-align': 'center'})
    

    all_ES = raw_data[raw_data['Student'] == selected_index][[value for value in raw_data.columns if value.startswith('ES')]].values.flatten()
    progress = np.round(len(all_ES[all_ES == 1])/len(np.array([x for x in all_ES if isinstance(x, (int, float, np.int64))]))*100,2)
    
    return dcc.Graph(figure={"data":data, "layout": layout}, config={'displayModeBar': False}), legend, dcc.Markdown(f'''
             ###### You have attended {progress}% of exercise sessions so far
         ''', style = {'textAlign': 'center'})


@app.callback(
    Output('ha1-output', 'children'),
    [Input('user-div', 'children')]
)
def update_ha1(selected_index):

    if "HA1" in raw_data.columns:
        selected_value = raw_data[raw_data['Student'] == selected_index]['HA1'].values[0]
        max_grade = raw_data[raw_data['Student'] == selected_index]['MaxHA1'].values[0]
        if selected_value != 'not submitted':
            
    
            return dcc.Markdown(f'''

            ##### Your HA1 grade is {selected_value}/{max_grade}.
    
            ''', style = {'textAlign': 'center'})
        else:
            return dcc.Markdown(f'''

            ##### You did not submit HA1.
            ''', style = {'textAlign': 'center'})
    else:
        return dcc.Markdown(f'''

             ##### HA1: the results are not available yet.

            
         ''', style = {'textAlign': 'center'})



@app.callback(
    Output('ha2-output', 'children'),
    [Input('user-div', 'children')]
)
def update_ha2(selected_index):

    if "HA2" in raw_data.columns:
        selected_value = raw_data[raw_data['Student'] == selected_index]['HA2'].values[0]
        max_grade = raw_data[raw_data['Student'] == selected_index]['MaxHA2'].values[0]

        if selected_value == 'part 1 only':
            return dcc.Markdown(f'''

            ##### You submitted part 1 only.
            ''', style = {'textAlign': 'center'})
        
        if selected_value != 'not submitted':
            
    
            return dcc.Markdown(f'''

            ##### Your HA2 grade is {selected_value}/{max_grade}.

        
            ''', style = {'textAlign': 'center'})
        
        else:
            return dcc.Markdown(f'''

            ##### You did not submit HA2.
            ''', style = {'textAlign': 'center'})
    else:
        return dcc.Markdown(f'''

             ##### HA2: the results are not available yet.

            
         ''', style = {'textAlign': 'center'})
    

@app.callback(
    [Output('avgquiz-plot', 'figure'),
     Output('quizzes-plot', 'figure'),
     Output('models-line-plot', 'figure'),
     Output('perf-avgquiz-plot', 'figure'),
     Output('perf-quizzes-plot', 'figure'),
    ],
    [Input('user-div', 'children')]
)
def update_line_plots_v1(selected_index):
    selected_data = raw_data[raw_data['Student'] == selected_index]

    with open("../PublishingScheduleMasteryQuizzes.json", 'r') as file:
        data_dict = json.load(file)

    with open("../QuizTypesAtt.json", 'r') as file:
        quiz_types = json.load(file)
    
    avg_score_figure = {
        'data': [
            {
                'x': [value.replace(f'{i}MasteryAttemptsAvgAt', '') for value in selected_data.columns 
                    if value.startswith(f'{i}MasteryAttemptsAvgAt')],
                'y': selected_data[[value for value in selected_data.columns 
                    if value.startswith(f'{i}MasteryAttemptsAvgAt')]].iloc[0],
                'type': 'bar', 
                'name': f'Your {i} score',
                'marker': {'color': j}
            }
            for i,j in zip(quiz_types.keys(),['#4055A6','#4CA1D7','#2A8041','#88C641','#FEE06E', '#808080', '#BCBEC4'])
                ]
           ,
        'layout': 
        {
            'xaxis': {'titlefont': {'size': 12}},
            'yaxis': {'title': 'Avg. score', 'titlefont': {'size': 12}},
            'font': {'size': 12},
            'legend': 
            {
            'x': 0.5,  
            'y': 1.01,  
            'xanchor': 'center',  
            'yanchor': 'bottom',  
            'orientation': 'h',  
            'font': {'size': 10}
            },
        }
    }

    avg_score_figure['data'].append({
            'x': [value.replace('MasteryAttemptsAvgAt', '') for value in selected_data.columns if value.startswith('MasteryAttemptsAvgAt')],
            'y': raw_data[[value for value in selected_data.columns if value.startswith('MasteryPerfectAvgAt')]].iloc[0],
            'type': 'line',
            'name': f'Perfect score',
            'marker': {'color': '#ADD8E6'}
            })
    
    avg_score_figure['data'].append({'x': [value.replace('MasteryAttemptsAvgAt', '') for value in selected_data.columns if value.startswith('MasteryAttemptsAvgAt')],
            'y': selected_data[[value for value in selected_data.columns if value.startswith('MasteryAttemptsAvgAt')]].iloc[0],
            'type': 'scatter',
            'mode': 'marker',
            'name': f'Total score',
            'marker': {'color': 'purple'}
                })

    perf_avg_score_figure = {
        'data': [
            {
            'x': [value.replace('PerformanceAttemptsAvgAt', '') for value in selected_data.columns if value.startswith('PerformanceAttemptsAvgAt')],
            'y': raw_data[[value for value in selected_data.columns if value.startswith('PerformancePerfectAvgAt')]].iloc[0],
            'type': 'line',
            'name': f'Perfect score',
            'marker': {'color': '#ADD8E6'}
            },
            {'x': [value.replace('PerformanceAttemptsAvgAt', '') for value in selected_data.columns if value.startswith('PerformanceAttemptsAvgAt')],
              'y': selected_data[[value for value in selected_data.columns if value.startswith('PerformanceAttemptsAvgAt')]].iloc[0],
                'type': 'bar',
                  'name': 'Your Create score',
                  'marker': {'color': '#FF8D3F'}}
        ],
        'layout': {
            'title': {'text':'Average score','font':{'size':16}},
            'xaxis': {'titlefont': {'size': 12}},
            'yaxis': {'title': 'Avg. score', 'titlefont': {'size': 12}},
            'font': {'size': 12},
            'barmode': 'overlay'
        }
    }
    
    output_numbers = {}
    for j in quiz_types.keys():
        output_numbers[j] = []
        for i in [value.replace('MasteryAttemptsAt', '') for value in selected_data.columns if value.startswith('MasteryAttemptsAt')]:
            available_quizzes = data_dict[i]
            output_numbers[j].append(len(set(available_quizzes).intersection(set(quiz_types[j]))))

    missed_dict ={}
    for k in quiz_types.keys():
        for i,j,z in zip([value.replace(f'{k}MasteryAttemptsAt', '') for value in selected_data.columns if value.startswith(f'{k}MasteryAttemptsAt')],
                            selected_data[[value for value in selected_data.columns if value.startswith(f'{k}MasteryAttemptsAt')]].iloc[0],
                            output_numbers[k]):
            if j == 0:
                if i in missed_dict.keys():
                    missed_dict[i].append(f'{k}:{j}/{z}') 
                else:
                    missed_dict[i] = [f'{k}:{j}/{z}']

    annotations = []
    for x_value, y_value in zip([value.replace('MasteryAttemptsAt', '') for value in selected_data.columns if value.startswith('MasteryAttemptsAt')],
                                selected_data[[value for value in selected_data.columns if value.startswith('MasteryAttemptsAt')]].iloc[0],):
        if x_value in missed_dict:
            annotation_text_final = ''
            for annotation_text in missed_dict[x_value]:
                annotation_text_final += f"<br> {annotation_text}"
            
            annotations.append(dict(x=x_value,y=y_value+3, text=annotation_text_final, showarrow=False, font=dict(size=8), textangle = 30))
            
    quizzes_figure = {
        'data': [ {'x': [value.replace(f'{i}MasteryAttemptsAt', '') for value in selected_data.columns if value.startswith(f'{i}MasteryAttemptsAt')],
              'y': selected_data[[value for value in selected_data.columns if value.startswith(f'{i}MasteryAttemptsAt')]].iloc[0],
                'type': 'bar',
                  'name': f'Your {i} score',
                  'marker': {'color': j},
                  'text': [f'{i}/{j}'for i,j in zip(selected_data[[value for value in selected_data.columns if value.startswith(f'{i}MasteryAttemptsAt')]].iloc[0],
                                                 output_numbers[i])],
                  'texttemplate': '%{text}',
                  'textangle': 0,
                  'textfont': {'size': 10},
                  'insidetextanchor': 'middle',
                  'textposition': 'inside'
                  } for i,j in zip(quiz_types.keys(),['#4055A6','#4CA1D7','#2A8041','#88C641','#FEE06E', '#808080','#BCBEC4'])],

        'layout': {
            'xaxis': {'titlefont': {'size': 12}},
            'yaxis': {'title': '#Quizzes', 'titlefont': {'size': 12}, 'showgrid': True, 'gridwidth':0.5},
            'font': {'size': 12},
            'barmode': 'stack',
            'annotations':annotations,
            'legend': {
            'x': 0.5,  
            'y': 1.01,  
            'xanchor': 'center',  
            'yanchor': 'bottom',  
            'orientation': 'h',  
            'font': {'size': 10}
        },
        'uniformtext': {
            'mode': 'show',
            'minsize': 10  # Enforce minimum font size
        }
        }
    }

    quizzes_figure['data'].append({
            'x': [value.replace('MasteryAttemptsAt', '') for value in selected_data.columns if value.startswith('MasteryAttemptsAt')],
            'y': raw_data[[value for value in selected_data.columns if value.startswith('MasteryPerfectAt')]].iloc[0],
            'type': 'line',
            'name': f'Max. #quizzes',
            'marker': {'color': '#ADD8E6'}
    })

    perf_quizzes_figure = {
        'data': [
            {
            'x': [value.replace('PerformanceAttemptsAt', '') for value in selected_data.columns if value.startswith('PerformanceAttemptsAt')],
            'y': raw_data[[value for value in selected_data.columns if value.startswith('PerformancePerfectAt')]].iloc[0],
            'type': 'line',
            'name': f'Perfect score',
            'marker': {'color': '#ADD8E6'}
        },
            {'x': [value.replace('PerformanceAttemptsAt', '') for value in selected_data.columns if value.startswith('PerformanceAttemptsAt')],
            'y': selected_data[[value for value in selected_data.columns if value.startswith('PerformanceAttemptsAt')]].iloc[0],
            'type': 'bar',
            'name': f'Your Create score',
            'marker': {'color': '#FF8D3F'}
            }
        ],
        'layout': {
            'title': {'text':'#Online exercise sessions Accumulated','font':{'size':16}},
            'xaxis': {'titlefont': {'size': 12}},
            'yaxis': {'title': '#Online exercise sessions', 'titlefont': {'size': 12}},
            'font': {'size': 12},
            'barmode': 'overlay'
        }
    }

    models_figure = {
        'data': [
            {'x': [value.replace('Models', '') for value in selected_data.columns if value.startswith('Models')],
              'y': selected_data[[value for value in selected_data.columns if value.startswith('Models')]].iloc[0],
                'type': 'line', 'name': 'Your score', 'showlegend': True}
        ],
        'layout': {
            'title': {'text':'#Models accumulated','font':{'size':16}},
            'xaxis': {'titlefont': {'size': 10}, 'tickangle': -45},
            'yaxis': {'title': '#Models created', 'titlefont': {'size': 10}},
            'font': {'size': 12},
            'legend': {
            'x': 0.5,  
            'y': 1.01,  
            'xanchor': 'center',  
            'yanchor': 'bottom',  
            'orientation': 'h',  
            'font': {'size': 10}}
        }
    }

    return avg_score_figure, quizzes_figure, models_figure, perf_avg_score_figure, perf_quizzes_figure


@app.callback(
    Output('practice-test-markdown', 'children'),
    [Input('user-div', 'children')]
)
def update_practice_test(selected_index):

    if "Cijfer" in raw_data.columns:
        max_grade = raw_data[raw_data['Student'] == selected_index]['Practice grade max'].values[0]
        selected_value = raw_data[raw_data['Student'] == selected_index]['Cijfer'].values[0]
        if selected_value != 'not submitted':
   
            return dcc.Markdown(f'''

            ###### Your practice test grade is {selected_value}/{max_grade}.

        
        ''', style = {'textAlign': 'center'})
        else:
            return dcc.Markdown(f'''

            ###### You did not do the practice test.

        
        ''', style = {'textAlign': 'center'})

    else:
        return dcc.Markdown(f'''

             ###### The results are not available yet.

            
         ''', style = {'textAlign': 'center'})