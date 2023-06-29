import json
import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class EuromonitorAPI:
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = 'https://api.euromonitor.com/authentication/connect/token'
        headers = {
            'Ocp-Apim-Subscription-Key': os.getenv('TOKEN'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = os.getenv('BODY')
        response = requests.post(url, headers=headers, data=body)
        json_response = response.json()
        access_token = json_response.get('access_token')
        return access_token

    def make_request(self, url):
        headers = {
            'Ocp-Apim-Subscription-Key': os.getenv('TOKEN'),
            'Accept': 'application/json; api-version=1.0',
            'Authorization': "Bearer "+self.token
        }
        response = requests.get(url, headers=headers)
        return response.content

    def get_categories(self):
        url = 'https://api.euromonitor.com/catalog/category'
        json_response = self.make_request(url)
        data_entries = json.loads(json_response)
        return data_entries

    def get_countries(self):
        url = 'https://api.euromonitor.com/catalog/geography'
        json_response = self.make_request(url)
        data_entries = json.loads(json_response)
        return data_entries
    
    def get_dataslices_by_industry_code(self, industry_code):
        url = f"https://api.euromonitor.com/catalog/dataslices?IndustryCodes={industry_code}"
        json_response = self.make_request(url)
        data_slices = json.loads(json_response)
        return data_slices
    
    def get_datatypes_by_industry_code(self, industry_code):
        url = f"https://api.euromonitor.com/catalog/MarketSize/datatype?IndustryCodes={industry_code}"
        json_response = self.make_request(url)
        data_slices = json.loads(json_response)
        return data_slices

class EuromonitorDB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()

    def create_em_categories_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS em_categories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                parentId INTEGER,
                parentName TEXT,
                level INTEGER,
                industryCode TEXT,
                industryName TEXT,
                industryOrder INTEGER
            )
        ''')
        self.conn.commit()

    def create_em_countries_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS em_countries (
                id INTEGER PRIMARY KEY,
                name TEXT,
                parentId INTEGER,
                parentName TEXT,
                isoAlpha2Code TEXT,
                FOREIGN KEY (parentId) REFERENCES countries (id)
            )
        ''')
        self.conn.commit()

    def create_countries_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY,
                name TEXT,
                alpha_2 TEXT,
                alpha_3 TEXT,
                country_code TEXT,
                iso_3166_2 TEXT,
                region TEXT,
                sub_region TEXT,
                intermediate_region TEXT,
                region_code TEXT,
                sub_region_code TEXT,
                intermediate_region_code TEXT
            )
        ''')
        self.conn.commit()

    def insert_em_categories(self, categories_data):
        # Create a connection to the SQLite database
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()

        # Create em_categories table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS em_categories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                parentId INTEGER,
                parentName TEXT,
                level INTEGER,
                industryCode TEXT,
                industryName TEXT,
                industryOrder INTEGER
            )
        ''')

        # Insert data entries into the em_categories table
        for data_entry in categories_data:
            cursor.execute('''
                INSERT OR IGNORE INTO em_categories (
                    id, name, parentId, parentName,
                    level, industryCode, industryName, industryOrder
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data_entry['id'], data_entry['name'], data_entry['parentId'], data_entry['parentName'],
                data_entry['level'], data_entry['industryCode'], data_entry['industryName'], data_entry['industryOrder']
            ))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def insert_em_countries(self, countries):
        for country in countries:
            self.cursor.execute('''
                INSERT INTO em_countries (id, name, parentId, parentName, isoAlpha2Code)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                country['id'], country['name'], country['parentId'],
                country['parentName'], country['isoAlpha2Code']
            ))
        self.conn.commit()

    def get_em_categories(self):
        self.cursor.execute('''
            SELECT id, name, parentId, parentName, level, industryCode, industryName, industryOrder
            FROM em_categories
        ''')
        categories = self.cursor.fetchall()
        category_dicts = []
        for category in categories:
            category_dict = {
                'id': category[0],
                'name': category[1],
                'parentId': category[2],
                'parentName': category[3],
                'level': category[4],
                'industryCode': category[5],
                'industryName': category[6],
                'industryOrder': category[7]
            }
            category_dicts.append(category_dict)
        return category_dicts

    def get_em_countries(self):
        self.cursor.execute('''
            SELECT id, name, isoAlpha2Code
            FROM em_countries
            WHERE isoAlpha2Code <> ''
        ''')
        countries = self.cursor.fetchall()
        country_dicts = []
        for country in countries:
            country_dict = {
                'id': country[0],
                'name': country[1],
                'iso_code': country[2]
            }
            country_dicts.append(country_dict)
        return country_dicts

    def close_connection(self):
        self.conn.close()
        
    def get_categories(self, level=None, parentId=None, industryCode=None):
        query = "SELECT name, id, parentId, industryCode FROM em_categories WHERE 1=1"
        conditions = []
        parameters = []

        if level is not None:
            conditions.append("level = ?")
            parameters.append(level)

        if parentId is not None:
            conditions.append("parentId = ?")
            parameters.append(parentId)

        if industryCode is not None:
            conditions.append("industryCode = ?")
            parameters.append(industryCode)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        self.cursor.execute(query, tuple(parameters))
        results = self.cursor.fetchall()

        categories = [
            {
                'name': row[0],
                'id': row[1],
                'parentId': row[2],
                'industryCode': row[3]
            }
            for row in results
        ]

        return categories



# Example usage
#api = EuromonitorAPI()
#categories_data = api.get_categories()
#countries_data = api.get_countries()

#db = EuromonitorDB()
#db.create_em_categories_table()
#db.create_em_countries_table()
#db.create_countries_table()
#db.insert_em_categories(categories_data)
#db.insert_em_countries(countries_data)
#db.close_connection()
