from dash import dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input,Output

df = pd.read_excel('promedio_Tienda_Ropa.xlsx')

external_stylesheets = ['style.css']

app = dash.Dash(__name__)

constantes = {
	'clics_totales' : df['CLICKS'].sum(),
	'promedio_general_precios' : round(df['PRECIO US'].sum()/df['PRECIO US'].count(), 2),
	'categorias' : df['CATEGORÍA'].unique(),
	'paises' : df['CIUDAD'].unique(),
	'meses' : df['MES'].unique()
}

mes_plus = list(constantes['meses'])
mes_plus.insert(0, 'Todos')

pais_plus = list(constantes['paises'])
pais_plus.insert(0, 'Todos')

app.layout = html.Div([
	html.Header([
		html.Img(src="assets/venta-online.png", alt="Ropa iconos creados por adriansyah - Flaticon"),
		html.Nav([
			html.H1("Dashboard tienda de ropa")
			])
		]),
	#Tablero 1
	html.Div([
		html.Label('Clics Vs Precios', className='titulo'), 
		html.Div([
			html.Div([
				html.Label('Clics totales: ', className='descripcion'),
				html.Label(constantes['clics_totales'])
				], className='envoltura'),
			html.Div([
				html.Label('Promedio general precios: ', className='descripcion'),
				html.Label(constantes['promedio_general_precios'])
				], className='envoltura')
			], className='fila_tablero'), 
		html.Div([
			html.Div([
				html.Label('Categoría:', className='descripcion'),
				dcc.Dropdown(constantes['categorias'], constantes['categorias'][0], id='categoria-dropdown')
				], className='envoltura'),
			html.Div([
				html.Label('País:', className='descripcion'),
				dcc.Dropdown(constantes['paises'], constantes['paises'][0], id='pais-dropdown'),
				], className='envoltura'),
			html.Div([
				html.Label('Mes:', className='descripcion'),
				dcc.Dropdown(constantes['meses'], constantes['meses'][0], id='mes-dropdown')
				], className='envoltura')
			], className='fila_tablero'), 
		html.Div([
			html.Div([
				html.Div([
					html.Div([
					html.Label('Clics pulsados:', className='descripcion'),
					html.Label(id='clics_pulsados')
					], className='envoltura')
					], className='fila_media_tablero'),
				html.Div([
					html.Div([
					html.Label('Promedio precios:', className='descripcion'),
					html.Label(id='promedio_precios')
					], className='envoltura')
					], className='fila_media_tablero')
				], className='fila_m_tablero'),
			html.Div([
				dcc.Graph(id='graph_clics_vs_precios'),
				html.Label(id='filtros_constantes')
				])
			], id='preciovsclics')
		], className='tablero'),
	#Tablero 2
		html.Div([
		html.Label('Categorías más visitadas', className='titulo'), 
		html.Div([
			dcc.RadioItems(id = 'estado-precios', 
				labelStyle = {'display': 'inline-block'},
				options = [
				{'label' : 'Todos', 'value' : 'todos'}, 
				{'label' : 'Precios normales', 'value' : 'normal'},
				{'label' : 'Precios elevados', 'value' : 'alto'}
				], value = 'todos'
				)], className='fila_tablero'), 
		html.Div([
			html.Div([
				html.Label('País:', className='descripcion'),
				dcc.Dropdown(pais_plus, 'Todos', id='pais-dropdown-3')
				], className='envoltura'),
			html.Div([
				html.Label('Mes:', className='descripcion'),
				dcc.Dropdown(mes_plus, 'Todos', id='mes-dropdown-3')
				], className='envoltura')
			], className='fila_tablero'), 
		html.Div([
			html.Div([
				dcc.Graph(id='categorias_mas_visitadas')
				])
			])
		], className='tablero'),
	#tablero 3
	html.Div([
		html.Label('Países que más visitan la tienda', className='titulo'), 
		html.Div([
			html.Div([
				html.Label('Mes:', className='descripcion'),
				dcc.Dropdown(mes_plus, 'Todos', id='mes-dropdown-2')
				], className='envoltura')
			], className='fila_tablero'), 
		html.Div([
			dcc.Graph(id='paises_mas_visitan')
			]),
		html.Button(id='submit-val', n_clicks=1)
		], className='tablero'),
	#tablero 4
	html.Div([
		html.Label('Historial visitas de la tienda', className='titulo'), 
		html.Div([
			html.Div([
				html.Label('Mes:', className='descripcion'),
				dcc.Dropdown(mes_plus, 'Todos', id='mes-dropdown-4')
				], className='envoltura')
			], className='fila_tablero'), 
		html.Div([
			dcc.Graph(id='historial_visitas')
			])
		], className='tablero')
], id='container')

#callback primer tablero
@app.callback(
	[Output('clics_pulsados', 'children'),
	Output('promedio_precios', 'children'),
	Output('graph_clics_vs_precios', 'figure'),
	Output('filtros_constantes', 'children')],
	[Input('categoria-dropdown', 'value'),
	Input('pais-dropdown', 'value'),
	Input('mes-dropdown', 'value')]
)
def update_output(categoria_value, pais_value, mes_value):
	filtro = df[df['CATEGORÍA'].isin([categoria_value]) & df['CIUDAD'].isin([pais_value]) & df['MES'].isin([mes_value])]
	clics_pull = filtro['CLICKS'].sum()
	promedio_precio = str(round(filtro['PRECIO US'].sum()/filtro['PRECIO US'].count(), 2)) + ' US'
	fig = px.bar(
			data_frame= filtro,
			x = 'CLICKS',
			y = 'PRECIO US')
	filtros= str(categoria_value+' - '+pais_value+' - '+mes_value)

	return clics_pull, promedio_precio, fig, filtros

#callback segundo tablero
@app.callback(
	Output('categorias_mas_visitadas', 'figure'),
	[Input('estado-precios', 'value'),
	Input('pais-dropdown-3', 'value'),
	Input('mes-dropdown-3', 'value')]
	)
def update_output_tablero3(estado_precio, pais_value, mes_value):
	filtro = df

	if estado_precio == 'normal':
		filtro = filtro[filtro['PRECIO ELEVADO'].isin([0])]
	elif estado_precio == 'alto':
		filtro = filtro[filtro['PRECIO ELEVADO'].isin([1])]


	if not pais_value == 'Todos':
		filtro = filtro[filtro['CIUDAD'].isin([pais_value])]


	if not mes_value == 'Todos':
		filtro = filtro[filtro['MES'].isin([mes_value])]

	visitas_categoria = (filtro.groupby("CATEGORÍA").agg(visitas=("CATEGORÍA", "count")).reset_index())

	fig3 = px.pie(data_frame= visitas_categoria, values='visitas', names='CATEGORÍA', title='Categorias mas visitadas', hole=.3)
	
	return fig3

#callback tercer tablero
@app.callback(
	[Output('paises_mas_visitan', 'figure'),
	Output('submit-val', 'children')],
	[Input('mes-dropdown-2', 'value'),
	Input('submit-val', 'n_clicks')]
)
def update_output_tablero2(mes_value, n_clicks):
	filtro=df[~ df['ID SESIÓN'].duplicated()]
	if not mes_value == 'Todos':
		filtro = filtro[filtro['MES'].isin([mes_value])]

	visitas = (filtro.groupby("CIUDAD").agg(VISITAS=("CIUDAD", "count")).reset_index())
	txt = 'ver menos'
	if not n_clicks % 2 == 0:
		filtro = visitas.iloc[:4]
		txt = 'ver todos'
	else:
		filtro = visitas

	fig2 = px.bar(
			data_frame= filtro,
			x = 'VISITAS',
			y = 'CIUDAD',
			orientation='h')
	return fig2, txt

#callback cuarto tablero
@app.callback(
	Output('historial_visitas', 'figure'),
	Input('mes-dropdown-4', 'value')
	)
def update_output_tablero4(value):
	filtro=df[~ df['ID SESIÓN'].duplicated()]
	if not value == 'Todos':
		filtro = filtro[filtro['MES'].isin([value])]
		data = (filtro.groupby("DÍA").agg(visitas=("DÍA", "count")).reset_index())
		x = 'DÍA'
	else:
		data = (filtro.groupby("MES").agg(visitas=("MES", "count")).reset_index())
		x = 'MES'
	
	fig = px.line(data_frame= data, x= x, y='visitas')
	return fig

if __name__ == ('__main__'):
	app.run_server(debug=True, port=5000)