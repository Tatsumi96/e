# Projet ETL et Dashboard

Ce projet contient un pipeline ETL (Extract, Transform, Load) qui traite des données depuis un fichier Excel, les charge dans une base de données SQLite, et un tableau de bord pour visualiser ces données.

## Prérequis

- Python 3.8 ou supérieur
- `pip` (le gestionnaire de paquets Python)

## Lancement Rapide

Des scripts ont été préparés pour automatiser le lancement sur différents systèmes d'exploitation. Ces scripts s'occupent de tout : création de l'environnement virtuel, installation des dépendances, exécution du pipeline ETL et lancement du tableau de bord.

-   **Sur Windows** :
    Double-cliquez sur le fichier `run_dashboard.bat`.

-   **Sur macOS ou Linux** :
    Ouvrez un terminal et exécutez la commande suivante :
    ```bash
    sh run_dashboard.sh
    ```

Le terminal affichera l'avancement et le tableau de bord se lancera à la fin du processus.

## Installation et Lancement Manuel

Si vous préférez lancer l'application manuellement, suivez les étapes ci-dessous.

1.  **Créer un environnement virtuel**
    Ouvrez un terminal dans le répertoire du projet et exécutez :
    ```bash
    python -m venv venv
    ```

2.  **Activer l'environnement virtuel**
    -   Sur Windows :
        ```cmd
        .\venv\Scripts\activate
        ```
    -   Sur macOS et Linux :
        ```bash
        source venv/bin/activate
        ```

3.  **Installer les dépendances**
    Assurez-vous que votre environnement virtuel est activé, puis installez les paquets nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Exécuter le pipeline ETL**
    Cette commande va peupler ou mettre à jour la base de données `database.db`.
    ```bash
    python main.py
    ```

5.  **Lancer le tableau de bord**
    Une fois l'ETL terminé, lancez le tableau de bord :
    ```bash
    python dashboard.py
    ```
