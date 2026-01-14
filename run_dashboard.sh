#!/bin/bash

# Script pour configurer l'environnement et lancer le dashboard

echo "================================================="
echo "Lancement du script de configuration et de lancement"
echo "================================================="

# S'assurer que Python 3 est disponible
if ! command -v python3 &> /dev/null
then
    echo "ERREUR: Python 3 n'est pas installé. Veuillez l'installer pour continuer."
    exit 1
fi

# Nom du dossier de l'environnement virtuel
VENV_DIR="venv"

# 1. Création de l'environnement virtuel s'il n'existe pas
if [ ! -d "$VENV_DIR" ]; then
    echo "--- Création de l'environnement virtuel ($VENV_DIR)..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "ERREUR: La création de l'environnement virtuel a échoué."
        exit 1
    fi
else
    echo "--- L'environnement virtuel existe déjà."
fi

# 2. Activation de l'environnement virtuel
echo "--- Activation de l'environnement virtuel..."
source $VENV_DIR/bin/activate

# 3. Installation des dépendances
echo "--- Installation des dépendances depuis requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERREUR: L'installation des dépendances a échoué."
    deactivate
    exit 1
fi

# 4. Exécution du script ETL principal (main.py)
echo "--- Exécution du pipeline ETL (main.py) pour mettre à jour la base de données..."
python main.py
if [ $? -ne 0 ]; then
    echo "ERREUR: L'exécution du script ETL a échoué."
    deactivate
    exit 1
fi

# 5. Lancement du dashboard
echo "--- Lancement du tableau de bord (dashboard.py)..."
python dashboard.py

# Désactivation de l'environnement virtuel à la fermeture
deactivate

echo "================================================="
echo "Script terminé."
echo "================================================="
