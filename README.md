# P9 Développez une application Web en utilisant Django

### Site de partage de ticket, critique sur des livres

#### version de python 3.10.4

### Instalation
Pour créer l'environnement virtuel, placez-vous dans le dossier source du projet, puis exécutez la commande suivante :
```
python -m venv env
```

Activé le ensuite en executant la commande suivante sous windows :
powershell :
```
env\Scripts\activate
```
Bash :
```
source env\Scripts\activate
```

Mac\Linux :
```
source env/bin/activate
```

Installer les dépendances :
```
pip install -r requirements.txt
```
### Lancement
démaré ensuite le site en utilisant la commande suivante :
```
python manage.py runserver
```
vous pouvez ensuite ouvrir le lien suivant depuis votre navigateur :

http://127.0.0.1:8000/

Vous pouver ensuite vous inscrire pour avoir acces au site

L'onglet Flux vous affichera vos post et review ainsi que ceux de vos abonnements.

L'onglet Posts vous affichera vos post et review afin de pouvoir les modifier et les supprimer.

L'onglet Abonnements vous permettra de vous abonner au post et review d'un autre membre et de vous en désabonner.