import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
from dash import Dash, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv("Dininghall_r.csv")

#extra helpful stuff
#qualitative stuff
num_avail = sum(df["Why_Not_Qualitative"].str.contains("Availability")==True)
num_qual = sum(df["Why_Not_Qualitative"].str.contains("Quality")==True)
num_var = sum(df["Why_Not_Qualitative"].str.contains("Variety")==True)
num_aller = sum(df["Why_Not_Qualitative"].str.contains("Accessibility")==True)
num_price = sum(df["Why_Not_Qualitative"].str.contains("Price")==True)

#key takeaways
num_respondents= df["Responder_Number"].count()
percent_bringback = round(df["Bring_Back"].value_counts()["Yes"]/df["Bring_Back"].count()*100,3)
most_factor = df["Main_Factor"].value_counts().idxmax()

#opp cost
potential_freq = round(df["Takeout_Freq"].mean(),2)
def transform_pay(x):
    if x == 4:
        x = 3
    elif x == 5:
        x = 7.5
    elif x == 10:
        x = 12.5
    return x
df["Max_Pay_Edit"] = df["Max_Pay"].transform(transform_pay)
potential_price = round(df["Max_Pay_Edit"].mean(),2)
potential_rev = int(potential_price * potential_freq * 3000 * 40)

#n = 
num_bringback = df["Bring_Back"].count()
num_takeoutfreq = df["Takeout_Freq"].count()
num_maxpay = df["Max_Pay"].count()
num_mainfactor = df["Main_Factor"].count()
num_scales = (int(df["Cost_Factor"].count() +
              df["Speed_Factor"].count() +
              df["Quality_Factor"].count() +
              df["Variety_Factor"].count())/4)
num_foodthievery = df["Food_Thievery"].count()
num_boughttakeout = df["Bought_Takeout"].count()
num_deliveryfreq = df["Delivery_Freq"].count()


#Chart fixes
labels_takeoutfreq = {0: "0x a week",
                      1: "0-1x a week",
                      2: "2-3x a week",
                      4: "4+x a week"}
df["Takeout_Freq"] = df["Takeout_Freq"].map(labels_takeoutfreq)

labels_maxpay = {      0: "$0",
                      4: "<$5",
                      5: "$5-$10",
                      10: "$10-$15",
                      15: ">$15"}
df["Max_Pay"] = df["Max_Pay"].map(labels_maxpay)

df["Delivery_Freq"] = df["Delivery_Freq"].map(labels_takeoutfreq) #works dw about it

labels_mainfactor = {"Schedule": "Eating at convenient times",
                      "Place": "Ability to eat elsewhere",
                      "Speed": "Getting food quickly",
                      "Waste": "Reducing food waste",
}
df["Main_Factor"] = df["Main_Factor"].map(labels_mainfactor)


'''
mycolorpalette={"Never": "#636efa",
                "Sometimes": "#ef553b",
                "Often": "#00cc96",
                "Rarely": "#ad68f9"}
'''

#GRAPHS!!!!!
'''
def custom_legend_name(new_names, fig):
    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name
'''

#Why takeout over dine in?
Main_Factor = px.bar(
    df,
    x=df["Main_Factor"].value_counts().index,
    y=df["Main_Factor"].value_counts().values,
    color = df["Main_Factor"].value_counts().index,
    title = "Why takeout over dine in?<br>(n=" + str(num_mainfactor)+")",
    labels = dict(x="Main Factor",
                  y = "Count (n)")
    )
'''
custom_legend_name(['Getting food quickly',
                    'Ability to eat elsewhere',
                    'Eating at convenient times',
                    'Reducing food waste'], Main_Factor)
'''

#Max ud pay?
Max_Pay = px.bar(
    df,
    x=df["Max_Pay"].value_counts().index,
    y=df["Max_Pay"].value_counts().values,
    color = df["Max_Pay"].value_counts().index.astype(str),
    title = "What's the maximum you'd <br> pay for McGill takeout?<br>(n=" + str(num_maxpay) +")",
    labels = dict(x="Max Price",
                  y = "Count (n)")
    )
'''
Max_Pay.update_layout(xaxis_type='category') #legend is a little fucky
custom_legend_name(['$0',
                    '$0-$5',
                    '$5-$10',
                    '$10-$15'], Max_Pay)
'''

#Have you taken food from the dining hall before?
dff = (df.groupby(
    ['Food_Thievery_YN', 'Food_Thievery'])
    ['Responder_Number'].count().reset_index(drop=0).rename(
    columns={'Responder_Number': 'Count'}))
Food_Thievery = px.bar(
    dff,
    x = "Food_Thievery_YN",
    y = "Count",
    color = "Food_Thievery",
    barmode = "relative",
    title = "Have you ever taken out food <br> from the dining halls before?<br>(n=" + str(num_foodthievery) +")",
)
Food_Thievery.update_layout(legend_title=None,
                            xaxis_title = "Taken food")

#Uber eats freq
Delivery_Freq = px.bar(
    df,
    x=df["Delivery_Freq"].value_counts().index,
    y=df["Delivery_Freq"].value_counts().values,
    color = df["Delivery_Freq"].value_counts().index.astype(str),
    title = "How many times in a week do you<br>buy takeout from delivery apps?<br>(n=" + str(num_deliveryfreq) +")",
    labels = dict(x="Frequency",
                  y = "Count (n)")
    )
Delivery_Freq.update_layout(xaxis_type='category') #legend is a little fucky



#Likert scales
df = df.rename(
    columns={"Cost_Factor": "Price",
             "Speed_Factor": "Speed",
             "Quality_Factor": "Quality",
             "Variety_Factor": "Variety"}
)
vars = ["Price", "Speed", "Quality", "Variety"]
Scales = make_subplots(rows=1, cols=len(vars))
for i, var in enumerate(vars):
    Scales.add_trace(
        go.Box(y=df[var],
        name=var),
        row=1, col=i+1
    )
Scales.update_traces(
    boxpoints='all',
    jitter=.3,
)
Scales.update_layout(
    title = ("How important is each of these <br> takeout factors? <br>(n=" 
             + str(num_takeoutfreq)
             +")")
)

#How frequently would you get takeout?
Takeout_Freq = px.pie(
                            df,
                                names = df["Takeout_Freq"].value_counts().index,
                                values = df["Takeout_Freq"].value_counts().values,
                                labels = df["Takeout_Freq"].value_counts().index, #make lbels work
                                title = "How often would you get takeout <br> if McGill dining halls offered it?<br>(n=" + str(num_takeoutfreq) +")",
                            )

#Have u bought grab n go?
Bought_Takeout = px.pie(
                            df,
                                names = df["Bought_Takeout"].value_counts().index,
                                values = df["Bought_Takeout"].value_counts().values,
                                labels = df["Bought_Takeout"].value_counts().index, #make lbels work
                                title = "Have you ever bought <br> current Grab n Go takeout?<br>(n=" + str(num_boughttakeout) +")",
                            )

#Do you want takeout back
Bring_Back = px.pie(
                df,
                    names = df["Bring_Back"].value_counts().index,
                    values = df["Bring_Back"].value_counts().values,
                    labels = df["Bring_Back"].value_counts().index, #make lbels work
                    title = "Do you think McGill dining halls <br> should offer takeout again?<br>(n=" + str(num_bringback) +")",
                )

#Chart fixes
Max_Pay.update_layout(showlegend=False)
Main_Factor.update_layout(showlegend=False)
Delivery_Freq.update_layout(showlegend=False)


# Bring_Back.update_layout(title_x=0.5) <- overlapped too much lol

#initial stuff

external_stylesheets = ['dbc.themes.BOOTSTRAP']
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server

#APP!!!!!

first_card = dbc.Card(
                dbc.CardBody(
                    html.Div([
                        html.H4(str(potential_freq) + "x"),
                        "weekly takeouts",
                    ]
                    ),
                ),
            )

second_card = dbc.Card(
                dbc.CardBody(
                    html.Div([
                        html.H4(str(potential_price) + "$"),
                        "willingness to pay",
                    ]
                    ),                
                ),
            )


app.layout = html.Div(
    [
        #nav bar
        dbc.Col(
            [
            #Key Takeaways
            dbc.Row([
                dbc.Col(
                        [
                        dbc.Row(
                            html.H2("Key Takeaways:"
                                ),
                            ),
                        dbc.Row(
                            [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [html.H2(str(percent_bringback) + "%"),
                                        "of students want takeout back"
                                        ]
                                    ),
                                ),
                                ),
                            ],
                            style={
                                "margin-bottom": "5%",
                            },
                            ),
                        dbc.Row(
                            [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [html.H2(num_respondents),
                                        "Student respondents"
                                        ]
                                    ),
                                ),
                                ),
                            ],
                            ),
                        dbc.Row(
                            [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [html.H2(most_factor),
                                        "was the most important takeout factor"     
                                        ]            
                                   ),                                                                                                        ),
                                ),
                            ],
                            style={
                                "margin-top": "5%",
                            },                            
                            ),                                                        
                        ],
                        ),
                ],
                justify="center",
                style={
                    "margin-top": "8%",
                }
            ),
            #opp cost
            dbc.Row([
                    html.Div(
                            [
                                html.H2("Potential takeout revenue:"),
                                dbc.Card(
                                    dbc.CardBody(
                                        html.H2(str(potential_rev) + "$"),
                                    ),
                                    style={
                                        "margin-bottom": "3%",
                                    }
                                ),
                                "With students potentially averaging",
                                dbc.Row(
                                    [
                                    dbc.Col(first_card, width = 6),
                                    dbc.Col(second_card, width = 6),
                                    ],
                                    style={
                                        "margin-bottom": "3%",
                                        "margin-top": "3%",
                                    }
                                ),
                                html.Small(
                                    "*3000 students, 40 weeks in residence",
                                    className="card-text text-muted",
                                )
                            ]
                        ),
            ],
                justify="center",
                style={
                    "margin-top": "8%",
                }
            )
        ],
        width = {"size": 3},
        style={
            "backgroundColor": "#f1f1f2",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "right": 0,
            "padding": "1.5%",
            "padding-left": "2%",
            "padding-right": "2%",
            "height": "100%"
            },
        ),
        #stuff
        dbc.Col(
            [
            #Header
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H1("Dining Hall Takeout Survey")
                            ),
                    width={"size": 12},
                    style={"backgroundColor": "ffffff",
                            "text-align": "center",
                            "padding-bottom": "1.5%",
                            "padding-top": "1.5%",
                            },
                ),
                className="g-0",
                justify="center",
                style={"box-shadow": "0 0 20px 3px #e9e9ee",
                    "textAlign": "center"
                        },
            ),

            #Element row
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                figure = Bring_Back,
                                style={
                                    "height": "25vh",
                                }
                            )
                        ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-right": "2%",
                            "backgroundColor": "ffffff",
                            "padding": "2%",
                            },
                    ),                    
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                figure = Takeout_Freq,
                                style={
                                    "height": "25vh",
                                }
                            )
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            },
                    ),
                    dbc.Col(
                        html.Div(
                            [dcc.Graph(
                                figure = Max_Pay,
                                style={
                                    "height": "25vh",
                                }
                            ),
                            html.Div(
                            "Note: No respondents chose the >$15 option",
                            className='text-center',
                            )
                        ]
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-left": "2%",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            }, 
                    ),
                ],
            justify="center",
            style={"padding-left": "5%",
                "padding-right": "5%",
                "margin-top": "2%",
                },
            className="h-25",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                figure = Main_Factor,
                                style={
                                    "height": "25vh",
                                }
                            )
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-right": "2%",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            },
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                figure = Scales,
                                style={
                                    "height": "25vh",
                                }                            
                            )
                    ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "backgroundColor": "ffffff",
                            "border-radius": "4%",
                            }, 
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                figure = Food_Thievery,
                                style={
                                    "height": "25vh",
                                }                            
                            )
                        ),
                        style={"width": "30%",
                            "box-shadow": "0 0 20px 3px #e9e9ee",
                            "margin-left": "2%",
                            "backgroundColor": "ffffff",
                            },
                    ),
                ],
            justify="center",
            style={"padding-left": "5%",
                "padding-right": "5%",
                "margin-top": "2%"
                }
            ),
            dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            figure = Bought_Takeout,
                            style={
                                "height": "25vh",
                            }
                        )
                ),
                    style={"width": "30%",
                           "box-shadow": "0 0 20px 3px #e9e9ee",
                           "margin-right": "2%",
                           "backgroundColor": "ffffff",
                           "border-radius": "4%",
                           },
                ),
                dbc.Col(
                    html.Div(
                        [
                        html.B("Common Grab n Go concerns expressed by respondents who did not want to buy Grab n Go included:"),
                        html.Br(),
                        html.Br(),
                        "Lack of Availability: " + str(num_avail),
                        html.Br(),
                        "High Prices: " + str(num_price),
                        html.Br(),
                        "Low Quality: " + str(num_qual),
                        html.Br(),
                        "Lack of Variety: " + str(num_var),
                        html.Br(),
                        "Accessibility/Allergies: " + str(num_aller),
                        ],
                    ),
                    style={"width": "30%",
                           "box-shadow": "0 0 20px 3px #e9e9ee",
                           "backgroundColor": "ffffff",
                           "padding": "2%",
                           },
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            figure = Delivery_Freq,
                            style={
                                "height": "25vh",
                            }                            
                        )
                ),
                    style={"width": "30%",
                           "box-shadow": "0 0 20px 3px #e9e9ee",
                           "margin-left": "2%",
                           "backgroundColor": "ffffff",
                           "border-radius": "4%",
                           }, 
                ),
            ],
        justify="center",
        style={"padding-left": "5%",
               "padding-right": "5%",
               "margin-top": "2%"
               }
        ),
            ],
        width = {"size": 9,
                 "offset": 3},
        ),
    ],
    style={
        "height": "relative",
    }
)

if __name__ == '__main__':
    app.run(debug=True)
