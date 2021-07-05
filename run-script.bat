@echo off
pip3 install pipenv > nul
pipenv sync > nul
pipenv run python -m scripts %*