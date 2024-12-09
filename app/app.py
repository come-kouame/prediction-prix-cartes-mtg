from dash import Dash, dcc, html, Input, Output, callback, State, ALL
import dash
from dash.exceptions import PreventUpdate
import json

with open("data/AllPricesSorted.json", 'r',errors="ignore") as f:
    file = json.load(f)

def rechercheParId(input):
    for card_id in file:
        if "uuid" in file[card_id]:
            if file[card_id]["uuid"] == input:
                return [f"{file[card_id]["name"]} ({file[card_id]["setCode"]})"]
    else:
        return [f'Carte non trouvée.']

def rechercheParNom(input):
    found_ids=[]
    for card_id in file:
        if "name" in file[card_id]:
            if file[card_id]["name"] == input:
                found_ids.append(f"{file[card_id]["name"]} ({file[card_id]["setCode"]})")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

def rechercheParSetCode(input):
    found_ids=[]
    for card_id in file:
        if "setCode" in file[card_id]:
            if file[card_id]["setCode"] == input:
                found_ids.append(f"{file[card_id]["name"]} ({file[card_id]["setCode"]})")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

def rechercheParArtiste(input):
    found_ids = []
    for card_id in file:
        if "artist" in file[card_id]:
            if file[card_id]["artist"] == input:
                found_ids.append(f"{file[card_id]["name"]} ({file[card_id]["setCode"]})")
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
            resultat,
            id={'type': 'result-item', 'index': i},
            className="column",
            style={'cursor': 'pointer'}
        )
        blocs.append(bloc)
    return html.Div(className="row", children=blocs)

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

#Fonction pour récupérer les derniers prix d'une carte selon le type de carte
def extraireDernierPrix(prices):
    prix_textes = []

    if not prices:
        return ["Prix non disponible"]
    
    for card_type in prices:
        valeurs = prices[card_type]
        if valeurs and isinstance(valeurs, dict):
            derniere_date = sorted(valeurs.keys())[-1]  # Pour avoir la dernière date
            prix = valeurs[derniere_date]
            prix_textes.append(f"{card_type.capitalize()} : {prix} (le {derniere_date})")

    return prix_textes if prix_textes else ["Aucun prix disponible"]



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

    if 'retour-btn.n_clicks' in ctx.triggered_id:
        return afficheResultats(input_value, dropdown_value), {'display': 'none'}

    if result_clicks and any(result_clicks):
        clicked_index = next((i for i, nc in enumerate(result_clicks) if nc), None)
        if clicked_index is not None and clicked_index < len(result_texts):
            card_name = result_texts[clicked_index]
            details = next(
                (card for card_id, card in file.items() 
                 if f"{card['name']} ({card['setCode']})" == card_name),
                None
            )
            if details:
                name = details.get("name", "N/A")
                set_name = details.get("setName", "N/A")
                set_code = details.get("setCode", "N/A")
                artist = details.get("artist", "N/A")
                rarity = details.get("rarity", "N/A")
                prices_textes = extraireDernierPrix(details.get("prices", {}))

                return html.Div(className="details-carte", children=[
                    html.H2(f"Détails de la carte : {name}"),
                    html.P(f"Set : {set_name} ({set_code})"),
                    html.P(f"Artiste : {artist}"),
                    html.P(f"Rareté : {rarity}"),
                    html.Div([html.P(prix) for prix in prices_textes]),
                ]), {'display': 'block'}

    return afficheResultats(input_value, dropdown_value), {'display': 'none'}

if __name__ == '__main__':
    app.run(debug=True)