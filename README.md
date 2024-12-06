# lifprojet



# Objectifs

Le but de ce projet est d'analyser les variations de prix des cartes du jeu Magic The Gathering, célèbre jeu de cartes à jouer et collectionner.
Nous avons utilisé l'algorithme de calcul Apriori afin d'établir une méthode pour prédire les prix des cartes selon les variations de prix des autres cartes de la base de donnée.
Nous avons la possibilité de simuler un évenement (tournoi) -> cet évenement va augmenter le prix de certaines cartes qui sont beaucoup joués (cartes méta) ce qui va provoqué des variations de prix sur d'autres cartes associées.
Nous avons également réalisé une application web permettant de visualisé la prédiction de prix des cartes Magic.

# Installation

( Optionnel )
Apres téléchargement vous pouvez remplacer les fichiers json dans data par les plus récents fournis par MTGJSON : https://mtgjson.com/downloads/all-files/ 
Exécuter simplement le fichier buildMTGFiles.py, il va merge les 2 fichiers afin de créer des fichiers moins lourds que nous utiliserons pour l'application et l'algorithme apriori

### dossier app
Là où se trouve l'application web
### dossier data
Là où se trouve et sont créé les fichiers json (base de donnée)
### dossier PricesDataSorter
Là où se trouve les fonctions de triage des donnée ainsi que l'algorithme Apriori
### dossier Test_Python
Tests réalisés sur la base que nous avons réaliser au début pour nous familiarisé avec (plusieurs ne donnerons rien car ils utilisent des fichiers json qui ne sont plus présent dans le projet)