import plotly.graph_objects as go
gridcolor = 'rgba(255,255,255,0.15)'
textcolor = 'rgba(255,255,255,0.4)'
bgcolor = '#262628'


degScoreProjectionStyle = {

    'layout': {
            'title_x': 0.042,
            'font': {'size': 15, 'family': 'sans-serif', 'color': textcolor},
            'plot_bgcolor': bgcolor,
            'paper_bgcolor': bgcolor,
            
        },

    'axes': {
        
        'xaxis': { 
            'gridcolor': bgcolor},

        'yaxis': {
            'gridcolor': gridcolor, 
            'gridwidth': 3 
            },
        

    },

    

}