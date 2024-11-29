from dash import Dash, dcc, html, Input, Output, callback
import json

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

app = Dash()

app.layout = html.Div([
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
                    dcc.Input(id='input', type='text', placeholder="Id de la carte"),
                    dcc.Dropdown(['','Recherche par id','Recherche par nom','Recherche par artiste'],'Recherche par id',id='parametres-dropdown',searchable=False),
                    html.Div(id='resultatRecherche'),
                ]
            ),
            html.Div(
                className="resultats",
                id='bloc-resultats'
            )
        ]
    )
])
        
@callback(
    Output(component_id='bloc-resultats', component_property='children'),
    Input(component_id='input', component_property='value'),
    Input(component_id='parametres-dropdown', component_property='value')
)
def afficheResultats(input, parametres_dropdown):
    match parametres_dropdown:
        case 'Recherche par id':
            resultats = rechercheParId(input)
        case 'Recherche par nom':
            resultats = rechercheParNom(input)
        case 'Recherche par artiste':
            resultats = rechercheParArtiste(input)
        case _:
            resultats = []
    bloc_resultats = [
        html.Div(
            className="row",
            children=[
                html.Div(f"{resultat}", className="column")
                for resultat in resultats
            ]
        )
    ]

    return bloc_resultats

def rechercheParId(input):
    for set_id in file["data"]:                                         
        if "cards" in file["data"][set_id]:
            for card in file["data"][set_id]["cards"]:
                if card["uuid"] == input:
                    return [f'{card["name"]}']
            else:
                continue
    else:
        return [f'Carte non trouvée.']

def rechercheParNom(input):
    found_ids=[]
    for set_id in file["data"]:                                     
        if "cards" in file["data"][set_id]:                         # Vérification si le set contient des cartes
            for card in file["data"][set_id]["cards"]:              # Parcours de chaque carte dans le set
                if "name" in card and card["name"] == input:                      # Accéder à la carte courante
                    found_ids.append(card["uuid"])
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

def rechercheParArtiste(input):
    found_ids=[]
    for set_id in file["data"]:
        if "cards" in file["data"][set_id]:
            for card in file["data"][set_id]["cards"]:
                if "artist" in card and card["artist"] == input:
                    found_ids.append(card["uuid"])
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

if __name__ == '__main__':
    app.run(debug=True)