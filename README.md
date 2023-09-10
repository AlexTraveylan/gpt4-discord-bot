# MonApplicationPythonTemplate

Ce dépôt est un modèle de base pour construire une application Python dans VSCode, préconfiguré pour l'utilisation avec l'intégration continue (CI) sur [Railway.app](https://railway.app/). Il contient des exemples de configuration pour plusieurs outils couramment utilisés dans le développement Python.

## Contenu du dépôt

1. **Github Actions** : un fichier de configuration pour les Github Actions se trouve dans le dossier `.github/workflows`.
2. **VSCode Config** : le dossier `/.vscode` contient des configurations spécifiques pour VSCode, notamment pour l'utilisation de [Black](https://black.readthedocs.io/en/stable/) comme formatteur de code et la définition de `pythonPath` à la racine.
3. **Singleton Logger** : une implémentation exemple d'un logger singleton se trouve dans le fichier `logger.py`.
4. **.env Exemple** : un fichier `.env` est fourni pour montrer comment configurer les variables d'environnement.
5. **.gitignore Exemple** : un fichier `.gitignore` est fourni comme modèle pour ignorer les fichiers non nécessaires.
6. **.pytest.ini Exemple** : un fichier `.pytest.ini` est fourni comme modèle pour configurer PyTest.
7. **Dockerfile Exemple** : un `Dockerfile` est fourni comme un modèle pour construire des images Docker.

## Utilisation

Pour utiliser ce modèle, suivez ces étapes:

1. Clonez le dépôt, renommer le, et placez vous dedans `cd votre-dossier`
2. Renommez `.env.exemple` en supprimant l'extension `.exemple`, et modifiez-les en fonction de vos besoins.
3. Créer un environnement virtuel avec :
```bash
python -m venv env
```
4. Activer votre environnement virtuel :
 ```bash 
 windows : env\Script\activate
 linux : source env/bin/activate
 ```
5. Installez les dépendances en exécutant :
```bash
pip install -r requirements.txt
```
6. Lancez votre application Python.

## Contribution

Les contributions à ce dépôt sont les bienvenues. Si vous avez des suggestions pour améliorer ce modèle, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est [Open source](LICENSE).
