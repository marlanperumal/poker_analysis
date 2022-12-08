# Poker data analysis

This repo contains python notebooks to analyse the results of a weekly poker game of a nominal nine players. Not all players are available every week. The results of the final finishing positions of each player has been recorded. It's possible for 2 or more players to be eliminated in the same round, thereby tying in position. There is also a house rule for *ghost players*. This allows players who have previously been eliminated to return to the game and either go out again or potentially even win. If a play does come back in via the ghost player rule, then each of their finishing positions is recorded.

## Requirements

- The analysis is done using jupyter notebooks so you'll need an environment that can run these such as Jupyterlab or VSCode
- Virtual Environment management is done via pipenv so this must be installed and available on the system
- Optionally, if the required version of python is not available, this can be installed and managed with pyenv. If pyenv is installed, pipenv will automatically use it

## Installation

- Clone this repo
- Setup and install packages with
```
pipenv install --dev
```
- If updated the repo, sync the notebook and python files with
```
pipenv run jupytext --sync *.ipynb
```

## Usage
- The notebook `poker_data_cleanup` is used to read in the raw data and output clean data for further analysis
- The notebook `poker_data_analysis` analyses the data and visualises the results
