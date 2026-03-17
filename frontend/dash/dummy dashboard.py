import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import math
import datetime
from dateutil.relativedelta import relativedelta

# --- Data Generation Logic (matches the React version) ---
def generate_base_truth():
    base_truth = []
    for i in range(48):
        trend = math.sin(i / 8) * 1.8
        cycle = math.cos(i / 3) * 0.8
        shock = -2.5 if i == 15 else (1.5 if i == 35 else 0)
        base_truth.append(2.2 + trend + cycle + shock)
    return base_truth

base_truth = generate_base_truth()
start_date = datetime.date(2022, 1, 1)
dates = [start_date + relativedelta(months=i) for i in range(48)]
date_strings = [d.strftime('%b %y') for d in dates]

# --- App Setup ---
app = dash.Dash(__name__)
app.title = "Macro Forecasting"

# --- Shared Styles (Mimicking the Dark Theme) ---
COLORS = {
    'bg_main': '#0a0f18',
    'bg_panel': '#0f172a',
    'bg_card': '#0f172a',
    'border': '#1e293b',
    'text_primary': '#f8fafc',
    'text_secondary': '#94a3b8',
    'historical': '#f1f5f9',
    'ar_model': '#3b82f6',
    'rf_model': '#10b981',
    'bridge_model': '#f97316',
}

# --- Layout ---
app.layout = html.Div(style={
    'display': 'flex', 'height': '100vh', 'width': '100vw', 
    'backgroundColor': COLORS['bg_main'], 'color': COLORS['text_primary'],
    'fontFamily': 'system-ui, -apple-system, sans-serif', 'margin': '0', 'overflow': 'hidden'
}, children=[
    
    # LEFT SIDEBAR
    html.Div(style={
        'width': '250px', 'borderRight': f'1px solid {COLORS["border"]}',
        'backgroundColor': COLORS['bg_panel'], 'display': 'flex', 'flexDirection': 'column'
    }, children=[
        html.Div("🏛️ Central Bank", style={'padding': '24px', 'fontSize': '18px', 'fontWeight': 'bold', 'borderBottom': f'1px solid {COLORS["border"]}'}),
        html.Div(style={'padding': '24px', 'display': 'flex', 'flexDirection': 'column', 'gap': '12px'}, children=[
            html.Div("📊 Output & GDP", style={'color': COLORS['ar_model'], 'backgroundColor': 'rgba(59, 130, 246, 0.1)', 'padding': '12px', 'borderRadius': '8px'}),
            html.Div("📈 Inflation Tracker", style={'color': COLORS['text_secondary'], 'padding': '12px'}),
            html.Div("👥 Labor Market", style={'color': COLORS['text_secondary'], 'padding': '12px'}),
            html.Div("🌍 Global Trade", style={'color': COLORS['text_secondary'], 'padding': '12px'}),
        ])
    ]),

    # MAIN CONTENT
    html.Div(style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'padding': '32px', 'overflowY': 'auto'}, children=[
        
        # Header
        html.Div(style={'marginBottom': '32px'}, children=[
            html.H2("Real GDP Growth Forecasting", style={'margin': '0 0 8px 0'}),
            html.P("Multi-model econometric projections with uncertainty fan charts.", style={'margin': '0', 'color': COLORS['text_secondary']})
        ]),

        # KPI Ribbon
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '24px', 'marginBottom': '32px'}, children=[
            html.Div(style={'backgroundColor': COLORS['bg_card'], 'border': f'1px solid {COLORS["border"]}', 'padding': '20px', 'borderRadius': '12px'}, children=[
                html.Div("COMBINED NOWCAST", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '8px', 'fontWeight': 'bold'}),
                html.Div(id='kpi-nowcast', style={'fontSize': '32px', 'fontWeight': 'bold', 'color': COLORS['text_primary']})
            ]),
            html.Div(style={'backgroundColor': COLORS['bg_card'], 'border': f'1px solid {COLORS["border"]}', 'padding': '20px', 'borderRadius': '12px'}, children=[
                html.Div("4-QUARTER FORECAST", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '8px', 'fontWeight': 'bold'}),
                html.Div(id='kpi-forecast', style={'fontSize': '32px', 'fontWeight': 'bold', 'color': COLORS['text_primary']})
            ]),
            html.Div(style={'backgroundColor': COLORS['bg_card'], 'border': f'1px solid {COLORS["border"]}', 'padding': '20px', 'borderRadius': '12px'}, children=[
                html.Div("CONFIDENCE INTERVAL", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '8px', 'fontWeight': 'bold'}),
                html.Div(id='kpi-interval', style={'fontSize': '32px', 'fontWeight': 'bold', 'color': COLORS['ar_model']})
            ])
        ]),

        # Hero Chart
        html.Div(style={
            'flex': '1', 'backgroundColor': COLORS['bg_card'], 'border': f'1px solid {COLORS["border"]}', 
            'borderRadius': '12px', 'padding': '24px', 'display': 'flex', 'flexDirection': 'column', 'minHeight': '450px'
        }, children=[
            html.H3("Trajectory & Projections", style={'margin': '0 0 16px 0', 'fontSize': '16px'}),
            dcc.Graph(id='main-chart', config={'displayModeBar': False}, style={'flex': '1'})
        ])
    ]),

    # RIGHT CONTROL PANEL
    html.Div(style={
        'width': '320px', 'borderLeft': f'1px solid {COLORS["border"]}',
        'backgroundColor': 'rgba(15, 23, 42, 0.8)', 'padding': '24px', 'display': 'flex', 'flexDirection': 'column'
    }, children=[
        html.H3("⚙️ Model Controls", style={'margin': '0 0 32px 0', 'fontSize': '18px'}),
        
        # Time Travel Slider
        html.Div(style={'marginBottom': '40px'}, children=[
            html.Div("Historical Time-Travel", style={'fontSize': '14px', 'fontWeight': 'bold', 'marginBottom': '8px'}),
            html.P("Shift the 'nowcast' anchor historically.", style={'fontSize': '12px', 'color': COLORS['text_secondary'], 'marginBottom': '16px'}),
            dcc.Slider(
                id='time-slider', min=12, max=40, step=1, value=28,
                marks={12: 'Past', 40: 'Present'},
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Div(id='slider-date-label', style={'textAlign': 'center', 'color': COLORS['ar_model'], 'marginTop': '12px', 'fontWeight': 'bold', 'fontSize': '14px'})
        ]),

        # Model Checkboxes
        html.Div("Econometric Models", style={'fontSize': '12px', 'fontWeight': 'bold', 'color': COLORS['text_secondary'], 'marginBottom': '16px', 'letterSpacing': '1px'}),
        dcc.Checklist(
            id='model-checklist',
            options=[
                {'label': ' AR Benchmark', 'value': 'ar'},
                {'label': ' Random Forest', 'value': 'rf'},
                {'label': ' Bridge Model', 'value': 'bridge'}
            ],
            value=['ar', 'rf'],
            style={'display': 'flex', 'flexDirection': 'column', 'gap': '16px'},
            inputStyle={'marginRight': '10px', 'transform': 'scale(1.2)'},
            labelStyle={'display': 'flex', 'alignItems': 'center', 'fontSize': '14px', 'fontWeight': 'bold'}
        )
    ])
])

# --- Callbacks for Interactivity ---
@app.callback(
    [Output('kpi-nowcast', 'children'),
     Output('kpi-forecast', 'children'),
     Output('kpi-interval', 'children'),
     Output('slider-date-label', 'children'),
     Output('main-chart', 'figure')],
    [Input('time-slider', 'value'),
     Input('model-checklist', 'value')]
)
def update_dashboard(cutoff_index, active_models):
    # 1. Generate Data Series
    hist_x = dates[:cutoff_index+1]
    hist_y = base_truth[:cutoff_index+1]
    
    forecast_x = dates[cutoff_index:]
    ar_y, rf_y, bridge_y = [], [], []
    upper_band, lower_band = [], []
    
    true_val = base_truth[cutoff_index]
    
    for i in range(cutoff_index, 48):
        step = i - cutoff_index
        if step == 0:
            ar_y.append(true_val); rf_y.append(true_val); bridge_y.append(true_val)
            upper_band.append(true_val); lower_band.append(true_val)
        else:
            mean_rev = 2.0
            ar_fc = true_val + (mean_rev - true_val) * (1 - math.exp(-0.15 * step))
            rf_fc = ar_fc + math.sin(step) * 0.4
            bridge_fc = ar_fc - math.cos(step / 2) * 0.5
            
            ar_y.append(ar_fc); rf_y.append(rf_fc); bridge_y.append(bridge_fc)
            
            unc_spread = step * 0.25 + (math.log(step) * 0.3 if step > 6 else 0)
            upper_band.append(ar_fc + unc_spread)
            lower_band.append(ar_fc - unc_spread)

    # 2. Calculate KPIs
    now_ar, now_rf, now_bridge = ar_y[0], rf_y[0], bridge_y[0]
    combined_nowcast = f"{((now_ar + now_rf + now_bridge) / 3):.2f}%"
    
    q4_index = min(3, len(ar_y)-1)
    q4_forecast = f"{ar_y[q4_index]:.2f}%" if 'ar' in active_models else f"{rf_y[q4_index]:.2f}%"
    conf_interval = f"±{((upper_band[q4_index] - lower_band[q4_index]) / 2):.2f}%" if len(upper_band) > q4_index else "N/A"
    
    current_date_str = date_strings[cutoff_index]

    # 3. Build Plotly Figure
    fig = go.Figure()

    # Uncertainty Bands (Fill between lines)
    if 'ar' in active_models:
        fig.add_trace(go.Scatter(
            x=forecast_x, y=upper_band, mode='lines', line=dict(width=0),
            showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_x, y=lower_band, mode='lines', line=dict(width=0),
            fill='tonexty', fillcolor='rgba(59, 130, 246, 0.15)',
            name='Uncertainty', showlegend=False, hoverinfo='skip'
        ))

    # Historical Data
    fig.add_trace(go.Scatter(
        x=hist_x, y=hist_y, mode='lines', 
        line=dict(color=COLORS['historical'], width=3), name='Historical'
    ))

    # Forecast Lines
    if 'ar' in active_models:
        fig.add_trace(go.Scatter(x=forecast_x, y=ar_y, mode='lines', line=dict(color=COLORS['ar_model'], width=2.5, dash='dash'), name='AR Benchmark'))
    if 'rf' in active_models:
        fig.add_trace(go.Scatter(x=forecast_x, y=rf_y, mode='lines', line=dict(color=COLORS['rf_model'], width=2.5, dash='dash'), name='Random Forest'))
    if 'bridge' in active_models:
        fig.add_trace(go.Scatter(x=forecast_x, y=bridge_y, mode='lines', line=dict(color=COLORS['bridge_model'], width=2.5, dash='dash'), name='Bridge Model'))

    # Chart Layout Styling
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor=COLORS['border'], tickfont=dict(color=COLORS['text_secondary'])),
        yaxis=dict(gridcolor=COLORS['border'], tickfont=dict(color=COLORS['text_secondary']), ticksuffix="%"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=COLORS['text_secondary'])),
        hovermode="x unified"
    )

    return combined_nowcast, q4_forecast, conf_interval, current_date_str, fig

if __name__ == '__main__':
    app.run(debug=True)