@echo off
:: Active lenvironnement virtuel si il existe
if exist .venv\Scripts\activate (
	call .venv\Scripts\activate
)

:: Lance le script Python
python main.py

pause