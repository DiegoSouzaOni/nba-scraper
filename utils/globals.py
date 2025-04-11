import requests
import pandas as pd
import numpy as np
import difflib
import json
import os
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
