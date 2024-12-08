from dash import Dash, dcc, html, Input, Output, callback, State, ALL
import dash
from dash.exceptions import PreventUpdate
import json

with open("data/AllPricesSorted.json", 'r',errors="ignore") as f:
    file = json.load(f)

def rechercheParId(input):
    for card_id, card_data in file.items():
        if card_data.get("uuid") == input:
            return [f"{card_data.get('name')} ({card_data.get('setCode')})"]
    else:
        return [f'Carte non trouvée.']
    
def rechercheParNom(input):
    found_ids=[]
    for card_id,card_data in file.items():
        if card_data.get("name") == input:
            found_ids.append(f"{card_data.get('name')} ({card_data.get('setCode')})")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

def rechercheParSetCode(input):
    found_ids=[]
    for card_id,card_data in file.items():
        if card_data.get("setCode") == input:
            found_ids.append(f"{card_data.get('name')} ({card_data.get('setCode')})")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

def rechercheParArtiste(input):
    found_ids = []
    for card_id, card_data in file.items():
        if card_data.get("artist") and card_data.get("artist") == input:
            found_ids.append(f"{card_data.get('name')} ({card_data.get('setCode')})")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

app = Dash(__name__, suppress_callback_exceptions=True)
    
def afficheResultats(input, parametres_dropdown):
    match parametres_dropdown:
        case '... par id':
            resultats = rechercheParId(input)
        case '... par nom':
            resultats = rechercheParNom(input)
        case '... par code de set':
            resultats = rechercheParSetCode(input)
        case '... par artiste':
            resultats = rechercheParArtiste(input)
        case _:
            resultats = []
    blocs = []
    for i, resultat in enumerate(resultats):
        bloc = html.Div(
            f"{resultat}",
            id={'type': 'result-item', 'index': i},
            className="column",
            style={'cursor': 'pointer'}
        )
        blocs.append(bloc)

    return html.Div(
        className="row",
        children=blocs
    )

app.layout = html.Div([
    dcc.Store(id='app-state', data='results'),
    html.Div(
        className="header",
        children=[
            html.Div('Prédiction de prix de cartes Magic The Gathering', className="titre-header")
        ]
    ),
    html.Div(
        className="main",
        children=[
            html.Div(
                className="colonne-recherche colle",
                children=[
                    "Recherche",
                    dcc.Input(id='input',
                              type='text',
                              placeholder="Recherche..."),
                    dcc.Dropdown(['','... par id','... par nom','... par code de set','... par artiste'],
                                 '',
                                 id='parametres-dropdown',
                                 searchable=False),
                    html.Div(id='resultatRecherche'),
                ]
            ),
            html.Div(
                className="resultats",
                id='bloc-resultats'
            ),
            html.Button("Retour", id="retour-btn", style={'display': 'none'})
        ]
    )
])

@app.callback(
    [Output('bloc-resultats', 'children'),
     Output('retour-btn', 'style')],
    [Input('input', 'value'),
     Input('parametres-dropdown', 'value'),
     Input({'type': 'result-item', 'index': ALL}, 'n_clicks'),
     Input('retour-btn', 'n_clicks')],
    [State({'type': 'result-item', 'index': ALL}, 'children')]
)
def navigationEntreEtats(input_value, dropdown_value, result_clicks, retour_click, result_texts):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    # Vérifie si le bouton de retour a été cliqué
    if 'retour-btn.n_clicks' in ctx.triggered_id:
        # Réinitialise l'affichage à la page de recherche principale
        return afficheResultats(input_value, dropdown_value), {'display': 'none'}

    # Gère la logique de clic sur les résultats
    if result_clicks and any(nc for nc in result_clicks):
        clicked_index = next((i for i, nc in enumerate(result_clicks) if nc), None)
        if clicked_index is not None:
            resultat = result_texts[clicked_index]
            infos_carte = {
                'Nom': resultat,
                'Prix': '10€',
                'Extension': 'Magic Set',
                'Artiste': 'John Doe'
            }
            return html.Div(
                className="details-carte",
                children=[
                    html.H2(f"Détails de la carte : {infos_carte['Nom']}"),
                    html.P(f"Prix : {infos_carte['Prix']}"),
                    html.P(f"Extension : {infos_carte['Extension']}"),
                    html.P(f"Artiste : {infos_carte['Artiste']}"),
                ]
            ), {'display': 'block'}

    # Sinon, renvoie les résultats principaux
    return afficheResultats(input_value, dropdown_value), {'display': 'none'}

if __name__ == '__main__':
    app.run(debug=True)

