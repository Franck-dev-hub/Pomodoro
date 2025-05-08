@echo off
:: Active l'environnement virtuel s'il existe
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)

:: Lance le script Python
python main.py

pause
