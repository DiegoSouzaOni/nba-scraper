import requests
import pandas as pd
import numpy as np
import difflib
import json
import os
import argparse
import pprint
from datetime import datetime, timedelta
from tabulate import tabulate
from unidecode import unidecode
import logging
import cloudscraper

SEASON_DEFAULT = "2024-25"
SEASON_TYPE_DEFAULT = "Regular Season"
SEASON_TYPE_PLAYOFFS = "Playoffs"
SEASON_TYPE_PRESEASON = "Pre Season"
SEASON_TYPE_ALLSTAR = "All Star"
SEASON_TYPE_SUMMER = "Summer League"

PER_MODE_DEFAULT = "Totals"
PER_MODE_PER_100 = "Per100Possessions"
PER_MODE_PER_36 = "Per36"
PER_MODE_PER_GAME = "PerGame"

BASE_URL = "https://stats.nba.com/stats/"
BASE_URL_CLOUDSCRAPER = "https://cdn.nba.com/stats/"
