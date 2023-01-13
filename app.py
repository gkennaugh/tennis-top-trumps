from dash import Input, Output, Dash, dcc, html, State, dash_table
import dash_bootstrap_components as dbc
from random import randrange
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import os
import random

external_stylesheets = [dbc.themes.DARKLY]
load_figure_template('darkly')

totaldf = pd.read_csv('tennis_atp-master/totaldf.csv')
playersdf = pd.read_csv('playersdf_300.csv')

chosen_w = ['minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms',
   'w_bpSaved', 'w_bpFaced', 'winner_rank', 'winner_rank_points']
chosen_l = ['minutes', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn',
   'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'loser_rank', 'loser_rank_points']
chosen = ['Total Minutes', 'Aces', 'Double Faults', 'Service Points', '1st Serve %', '1st Serve Won', '2nd Serve Won', 'Service Games',
   'Break Points Saved', 'Break Points Faced', 'Average Rank', 'Average Rank Points']

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = dbc.Container([
    
    dcc.Store(id='cards_store'),
    dbc.Row([
        dbc.Col([
        dbc.Col([
            html.Div([
                dbc.Card([
                    html.Div([
                        html.H4(id='name1', style={'margin-bottom':-30}),
                        html.H4(id='number1', style={'margin-bottom':0, 'margin-top':0, 'text-align':'right'}),
                        #html.H4(id='country1', style={'margin-right':50, 'margin-top':20, 'margin-bottom':-50, 'text-align':'right'})
                        html.Img(id='country1', style={'margin-right':50, 'margin-top':0, 'margin-bottom':0})
                    ]),
                    dbc.CardImg(id='card-img1', style={'margin-bottom': -350}),
                    html.Div([
                        dbc.CardBody(id='card-body1', className='border rounded'),
                        dbc.CardBody(id='card-body1a', className='border rounded')
                    ], style={'display':'flex'}),
                    dbc.Button('Generate', id='button', n_clicks=0, n_clicks_timestamp=0, style={'margin-top': 30})
                ])
            ])
        ]),

        dbc.Col([
            html.Div([
                dbc.Card([
                    html.Div([
                        html.H4(id='name2', style={'margin-bottom':-30}),
                        html.H4(id='number2', style={'margin-bottom':0, 'margin-top':0, 'text-align':'right'}),
                        html.Img(id='country2', style={'margin-right':50, 'margin-top':0, 'margin-bottom':0})
                    ]),
                    dbc.CardImg(id='card-img2', style={'margin-bottom': -350}),
                    html.Div([
                        dbc.CardBody(id='card-body2', className='border rounded'),
                        dbc.CardBody(id='card-body2a', className='border rounded')
                    ], style={'display':'flex'}),
                    dbc.Button('', id='button2', n_clicks_timestamp=0, style={'margin-top': 30})
                ])
            ]),
            html.Div(id='result', hidden=True),
            html.P(id='hidden_i', hidden=True)
        ]),
        ], sm=12, md=12, lg=6, style={'display':'flex'}),
        dbc.Col([
            html.H3('Welcome to ATP Top Trumps'),
            html.P('You both start with ten cards. Yours are on the left.'),
            html.P('Choose one of the player stats you think is the best. If it is better than your opponents card you win their card. If it is worse then you lose your card.'),
            html.P('Click Generate to show your next card'),
            html.P('The first to hold all the cards wins'),
            html.P(id='cards1', hidden=True),
            html.P(id='cards2', hidden=True),
            dbc.Button('Restart Game', id='button_reset_score',  n_clicks_timestamp=0),
            html.H3('Your Score'),
            html.H4(0, id='score'),
            html.H1(id='result_text', style={'color':'#d2db24'})
        ], sm=6, md=6, lg=2)
        
    ], justify='center', align='center', style={'height':'100vh'})
    
], fluid=True, className="mt-3")

@app.callback(
    Output('cards_store', 'data'),
    [Input('button', 'n_clicks'),
     Input('button', 'n_clicks_timestamp'),
    Input('button_reset_score', 'n_clicks_timestamp')],
     [State('result', 'children'),
      State('cards_store', 'data'),
     State('number1', 'children'),
     State('number2', 'children')]
)
def update_store(n_clicks, n_clicks_timestamp, n, win, data, n1, n2):
    if n_clicks == 0:
        cards_total = random.sample(range(0,299), 20)
        cards1 = cards_total[:10]
        cards2 = cards_total[10:]
    if n_clicks > 0:
        cards1 = data[0]
        cards2 = data[1]
    if win == 'winner':
        cards1.remove(n1)
        cards1.append(n1)
        cards1.append(n2)
        cards2.remove(n2)
    elif win == 'loser':
        cards1.remove(n1)
        cards2.remove(n2)
        cards2.append(n2)
        cards2.append(n1)
    if n > n_clicks_timestamp:
        cards_total = random.sample(range(0,299), 20)
        cards1 = cards_total[:2]
        cards2 = cards_total[18:]
    return [cards1, cards2]

@app.callback(
    [Output('cards1', 'children'),
     Output('cards2', 'children')],
    Input('cards_store', 'data')
)
def update_cards(data):
    return str(data[0]), str(data[1])
    
@app.callback(
    [Output('name1', 'children'),
     Output('number1', 'children'),
     Output('country1', 'src'),
    Output('card-img1', 'src'),
     Output('card-body1', 'children'),
    Output('card-body1a', 'children')],
    #Input('button', 'n_clicks_timestamp'),
    [Input('button', 'n_clicks'),
    Input('cards_store', 'data')]
)
def update_card(n, data):
    cards1 = data[0]
    #if n > 0:
    #    i = randrange(0,299)
    #else:
    #    i = 0
    i = cards1[0]
    df = pd.DataFrame([totaldf[totaldf['winner_name']==playersdf['0'][i]][chosen_w].mean().values,totaldf[totaldf['loser_name']==playersdf['0'][i]][chosen_l].mean().values], columns=chosen).mean().astype('int')
    if playersdf['0'][i]+'.png' in os.listdir('static/assets/atp'):
        image = playersdf['0'][i]
    else:
        image = 'not'
    country_text = totaldf[totaldf['winner_name']==playersdf['0'][i]]['winner_ioc'].max().lower()
    country = 'static/assets/img/flags/'+country_text+'.gif'
    #return totaldf['winner_name'].unique()[i], 'static/assets/atp/'+totaldf['winner_name'].unique()[i]+'.png', html.Div([html.H6(df.index[x]+': '+str(df[x]), style={'display':'flex', 'align':'center'}) for x in range(10)])
    return playersdf['0'][i], playersdf.index[i], country, 'static/assets/atp/'+image+'.png', html.Div([html.Button(df.index[x]+': '+str(df[x]), id='btn'+str(x), n_clicks_timestamp=0, style={'width':'100%', 'margin':'3px'}) for x in [0,1,2,3,4]], style={'width': '98%', 'display': 'inline-block'}), html.Div([html.Button(df.index[x]+': '+str(df[x]), id='btn'+str(x), n_clicks_timestamp=0, style={'width':'100%', 'margin':'3px'}) for x in [5,6,7,8,9]], style={'width': '98%', 'display': 'inline-block'})



@app.callback(
    [Output('result', 'children'),
     Output('result_text', 'children'),
     Output('name2', 'children'),
     Output('number2', 'children'),
     Output('country2', 'src'),
    Output('card-img2', 'src'),
     Output('card-body2', 'children'),
    Output('card-body2a', 'children'),
    Output('hidden_i', 'children')],
    [Input('button', 'n_clicks_timestamp'),
    Input('btn0', 'n_clicks_timestamp'),
     Input('btn1', 'n_clicks_timestamp'),
    Input('btn2', 'n_clicks_timestamp'),
    Input('btn3', 'n_clicks_timestamp'),
    Input('btn4', 'n_clicks_timestamp'),
    Input('btn5', 'n_clicks_timestamp'),
    Input('btn6', 'n_clicks_timestamp'),
    Input('btn7', 'n_clicks_timestamp'),
    Input('btn8', 'n_clicks_timestamp'),
    Input('btn9', 'n_clicks_timestamp')],
    [State('btn0', 'children'),
     State('btn1', 'children'),
     State('btn2', 'children'),
     State('btn3', 'children'),
     State('btn4', 'children'),
     State('btn5', 'children'),
     State('btn6', 'children'),
     State('btn7', 'children'),
     State('btn8', 'children'),
     State('btn9', 'children'),
     State('name1', 'children'),
    State('cards_store', 'data'),
    State('button', 'n_clicks')]
)
def update_result(n,n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,name,data,n_clicks):
    buttons = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9]
    try:
        data[0]
    except NameError:
        cards1 = []
    else:
        cards1 = data[0]
    try:
        data[1]
    except NameError:
        cards2 = []
    else:
        cards2 = data[1]
    if ([n]+buttons)[([n]+buttons).index(max([n]+buttons))] == n:
        i = 300
    else:
        i = cards2[0]
    v = buttons.index(max(buttons))
    v_list = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9]
    #i = 20
    df = pd.DataFrame([totaldf[totaldf['winner_name']==name][chosen_w].mean().values,totaldf[totaldf['loser_name']==name][chosen_l].mean().values], columns=chosen).mean().astype('int')
    df2 = pd.DataFrame([totaldf[totaldf['winner_name']==playersdf['0'][i]][chosen_w].mean().values,totaldf[totaldf['loser_name']==playersdf['0'][i]][chosen_l].mean().values], columns=chosen).mean().astype('int')
    if max(buttons) > 1:
        if v in [1,3,4,5,6,7,8]:
            if int(v_list[v].split(':')[1]) > df2[v]:
                v_win = 'winner'
            else:
                v_win = 'loser'
        else:
            if int(v_list[v].split(':')[1]) < df2[v]:
                v_win = 'winner'
            else:
                v_win = 'loser'
    else:
        v_win = 'waiting'
    if len(cards1) == 0:
        v_win = 'Game Over. You Lose!'
    if len(cards2) == 0:
        v_win = 'Game Over. You Win!'
    if playersdf['0'][i]+'.png' in os.listdir('static/assets/atp'):
        image = playersdf['0'][i]
    else:
        image = 'not'
        #buttons.index(max(buttons)
    if i == 300:
        index_no = '...'
        country = 'static/assets/img/flags/empty.gif'
    else:
        index_no = playersdf.index[i]
        country_text = totaldf[totaldf['winner_name']==playersdf['0'][i]]['winner_ioc'].max().lower()
        country = 'static/assets/img/flags/'+country_text+'.gif'
        #country = totaldf[totaldf['winner_name']==playersdf['0'][i]]['winner_ioc'].max()
    return v_win, v_win, playersdf['0'][i], index_no, country, 'static/assets/atp/'+image+'.png', html.Div([html.Button(df2.index[x]+': '+str(df2[x]), id='btna'+str(x), n_clicks_timestamp=0, style={'width':'100%', 'margin':'3px'}) for x in [0,1,2,3,4]], style={'width': '98%', 'display': 'inline-block'}), html.Div([html.Button(df2.index[x]+': '+str(df2[x]), id='btna'+str(x), n_clicks_timestamp=0, style={'width':'100%', 'margin':'3px'}) for x in [5,6,7,8,9]], style={'width': '98%', 'display': 'inline-block'}), i
    
@app.callback(
    Output('score', 'children'),
    [Input('button_reset_score', 'n_clicks_timestamp'),
     Input('button', 'n_clicks_timestamp')],
     [State('result', 'children'),
    State('score', 'children')]
)
def update_score(n1, n2, verdict, score):
    if n1 > n2:
        score = 0
    if verdict == 'winner':
        score += 1
    elif verdict == 'loser':
        score -= 1
    elif verdict == 'waiting':
        score = score
    return score
    
if __name__=='__main__':
    app.run_server(debug=True, port=8061)