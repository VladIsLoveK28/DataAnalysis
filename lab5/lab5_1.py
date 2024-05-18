import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, add_noise):
    t = np.linspace(0, 1, 1000)
    harmonic_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if add_noise:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), t.shape)
        signal_with_noise = harmonic_signal + noise
        return t, signal_with_noise, harmonic_signal
    return t, harmonic_signal, harmonic_signal

def moving_average_filter(signal, window_size):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

app = dash.Dash(__name__)

def create_slider(id, min, max, step, value, marks):
    return dcc.Slider(id=id, min=min, max=max, step=step, value=value, marks=marks)

app.layout = html.Div([
    html.H1("Harmonic with Noise and Filter"),
    html.Div([
        # Повзунки для різних параметрів
        html.Div([
            html.Label('Amplitude'),
            create_slider('amplitude-slider', 0.1, 10, 0.1, 1, {i: str(i) for i in range(0, 11)}),
        ], style={'margin': '10px 0'}),
        html.Div([
            html.Label('Frequency'),
            create_slider('frequency-slider', 0.1, 10, 0.1, 1, {i: str(i) for i in range(0, 11)}),
        ], style={'margin': '10px 0'}),
        html.Div([
            html.Label('Phase'),
            create_slider('phase-slider', 0, 2*np.pi, 0.1, 0, {0: '0', np.pi/2: 'π/2', np.pi: 'π', 3*np.pi/2: '3π/2', 2*np.pi: '2π'}),
        ], style={'margin': '10px 0'}),
        html.Div([
            html.Label('Noise Mean'),
            create_slider('noise-mean-slider', -1, 1, 0.1, 0, {i: str(i) for i in range(-1, 2)}),
        ], style={'margin': '10px 0'}),
        html.Div([
            html.Label('Noise Covariance'),
            create_slider('noise-cov-slider', 0.01, 1, 0.01, 0.1, {i/10: str(i/10) for i in range(0, 11)}),
        ], style={'margin': '10px 0'}),
        html.Div([
            # Дроп меню для вибору сигналів для відображення
            html.Label('Select Signal to Show'),
            dcc.Dropdown(
                id='signal-dropdown',
                options=[
                    {'label': 'Harmonic Signal', 'value': 'harmonic'},
                    {'label': 'Signal with Noise', 'value': 'noise'},
                    {'label': 'Filtered Signal', 'value': 'filtered'}
                ],
                value=['harmonic', 'noise', 'filtered'],
                multi=True
            )
        ], style={'margin': '10px 0'}),
        # Reset
        html.Button('Reset', id='reset-button', n_clicks=0, style={'margin': '20px 0'})
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    html.Div([
        # Самі графіки
        dcc.Graph(id='harmonic-graph', style={'display': 'none'}),
        dcc.Graph(id='noise-graph', style={'display': 'none'}),
        dcc.Graph(id='filtered-graph', style={'display': 'none'}),
    ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'})
])

@app.callback(
    Output('harmonic-graph', 'figure'),
    Output('harmonic-graph', 'style'),
    Output('noise-graph', 'figure'),
    Output('noise-graph', 'style'),
    Output('filtered-graph', 'figure'),
    Output('filtered-graph', 'style'),
    Output('amplitude-slider', 'value'),
    Output('frequency-slider', 'value'),
    Output('phase-slider', 'value'),
    Output('noise-mean-slider', 'value'),
    Output('noise-cov-slider', 'value'),
    Output('signal-dropdown', 'value'),
    Input('amplitude-slider', 'value'),
    Input('frequency-slider', 'value'),
    Input('phase-slider', 'value'),
    Input('noise-mean-slider', 'value'),
    Input('noise-cov-slider', 'value'),
    Input('signal-dropdown', 'value'),
    Input('reset-button', 'n_clicks')
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_cov, selected_signals, n_clicks):
    ctx = dash.callback_context
    
    # Скинути значення якщо натиснути ресет
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'reset-button.n_clicks':
        amplitude = 1
        frequency = 1
        phase = 0
        noise_mean = 0
        noise_cov = 0.1
        selected_signals = ['harmonic', 'noise', 'filtered']
    
    t, signal_with_noise, harmonic_signal = harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_cov, 'noise' in selected_signals)
    filtered_signal = moving_average_filter(signal_with_noise, 10) if 'noise' in selected_signals else None
    
    fig_harmonic = go.Figure()
    fig_noise = go.Figure()
    fig_filtered = go.Figure()
    
    if 'harmonic' in selected_signals:
        fig_harmonic.add_trace(go.Scatter(x=t, y=harmonic_signal, mode='lines', name='Harmonic Signal'))
    if 'noise' in selected_signals:
        fig_noise.add_trace(go.Scatter(x=t, y=signal_with_noise, mode='lines', name='Signal with Noise'))
    if 'filtered' in selected_signals:
        fig_filtered.add_trace(go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal'))
    
    fig_harmonic.update_layout(title='Harmonic Signal', xaxis_title='Time', yaxis_title='Amplitude')
    fig_noise.update_layout(title='Signal with Noise', xaxis_title='Time', yaxis_title='Amplitude')
    fig_filtered.update_layout(title='Filtered Signal', xaxis_title='Time', yaxis_title='Amplitude')
    
    # Встановлення стилю відображення для кожного графіка
    style_harmonic = {'display': 'block'} if 'harmonic' in selected_signals else {'display': 'none'}
    style_noise = {'display': 'block'} if 'noise' in selected_signals else {'display': 'none'}
    style_filtered = {'display': 'block'} if 'filtered' in selected_signals else {'display': 'none'}
    
    return (fig_harmonic, style_harmonic,
            fig_noise, style_noise,
            fig_filtered, style_filtered,
            amplitude, frequency, phase, noise_mean, noise_cov, selected_signals)

if __name__ == '__main__':
    app.run_server(debug=True)
