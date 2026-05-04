# Discord Channel Exporter

Télécharge tous les messages d'un salon Discord dans un fichier JSON,
en utilisant ton compte personnel (pas un bot).

---

## Prérequis

### 1. Python
Télécharge et installe Python depuis https://www.python.org/downloads/  
Coche **"Add Python to PATH"** pendant l'installation.  
Aucun module supplémentaire à installer (`pip install` inutile).

### 2. DiscordChatExporter CLI
1. Va sur https://github.com/Tyrrrz/DiscordChatExporter/releases
2. Télécharge **`DiscordChatExporter.Cli.zip`** (Windows x64)
3. Extrais le zip où tu veux (ex: `C:\Tools\DCE\`)
4. Note le chemin vers `DiscordChatExporter.Cli.exe`

---

## Lancer l'outil

Double-clique sur `discord_channel_exporter.py`  
ou lance dans un terminal :
```
python discord_channel_exporter.py
```

---

## Utilisation

### Remplir les champs

**DiscordChatExporter.Cli.exe**  
Clique sur `…` et sélectionne le fichier `DiscordChatExporter.Cli.exe` téléchargé.

**Token Discord (compte perso)**  
Ton token d'authentification personnel — voir section ci-dessous pour le récupérer.

**Channel ID**  
L'identifiant numérique du salon à exporter — voir section ci-dessous.

---

## Récupérer ton token Discord

> ⚠️ Ne partage jamais ton token. Il donne un accès complet à ton compte.

1. Ouvre Discord dans ton **navigateur web** (pas l'appli) : https://discord.com/app
2. Appuie sur **F12** pour ouvrir les outils développeur
3. Va dans l'onglet **Network**
4. Dans le filtre, tape `messages`
5. Clique sur n'importe quel salon Discord
6. Une requête apparaît dans la liste → clique dessus
7. Va dans **Headers** → cherche le header **`Authorization`**
8. Copie la valeur (commence par `MTk…` ou similaire) — c'est ton token

---

## Récupérer un Channel ID

1. Dans Discord (appli ou navigateur), va dans **Paramètres → Avancés**
2. Active **"Mode développeur"**
3. Fais un clic droit sur le salon souhaité
4. Clique **"Copier l'identifiant"**

---

## Télécharger

Une fois les 3 champs remplis, clique **Télécharger**.  
Les logs s'affichent en temps réel dans la console noire.  
Le fichier JSON est sauvegardé dans le dossier `exports/` (créé automatiquement à côté du script).

### Bouton Stop
Arrête le téléchargement en cours et sauvegarde ce qui a déjà été récupéré.

### Bouton Quitter
Ferme l'application immédiatement (coupe aussi le téléchargement en cours).

---

## Fichier de sortie

Format : `exports/NomDuSalon [ChannelID].json`  
Contenu : tous les messages du salon avec auteur, date, contenu, pièces jointes.

---

## Structure du projet

```
discord_channel_exporter.py   ← script principal (seul fichier nécessaire)
exports/                      ← dossier créé automatiquement à l'export
README.md                     ← ce fichier
```
