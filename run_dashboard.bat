@echo off
REM Script pour configurer l'environnement et lancer le dashboard sur Windows

echo =================================================
echo Lancement du script de configuration et de lancement
echo =================================================

REM S'assurer que Python est disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez l'installer et l'ajouter au PATH pour continuer.
    pause
    exit /b 1
)

REM Nom du dossier de l'environnement virtuel
set VENV_DIR=venv

REM 1. Création de l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
    echo --- Création de l'environnement virtuel (%VENV_DIR%)...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo ERREUR: La création de l'environnement virtuel a échoué.
        pause
        exit /b 1
    )
) else (
    echo --- L'environnement virtuel existe déjà.
)

REM 2. Activation de l'environnement virtuel
echo --- Activation de l'environnement virtuel...
call "%VENV_DIR%\Scripts\activate.bat"

REM 3. Installation des dépendances
echo --- Installation des dépendances depuis requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERREUR: L'installation des dépendances a échoué.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    pause
    exit /b 1
)

REM 4. Exécution du script ETL principal (main.py)
echo --- Exécution du pipeline ETL (main.py) pour mettre à jour la base de données...
python main.py
if %errorlevel% neq 0 (
    echo ERREUR: L'exécution du script ETL a échoué.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    pause
    exit /b 1
)

REM 5. Lancement du dashboard
echo --- Lancement du tableau de bord (dashboard.py)...
python dashboard.py

REM Désactivation de l'environnement virtuel
call "%VENV_DIR%\Scripts\deactivate.bat"

echo =================================================
echo Script terminé.
echo =================================================
pause
