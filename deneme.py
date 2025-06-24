import sqlite3
import pandas as pd
from datetime import datetime

def excel_to_database(file_name):
    try:
        df = pd.read_excel(file_name)
        conn = sqlite3.connect('kitaplar.db')



