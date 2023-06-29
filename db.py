from settings import IMG_FLAGS_PATH, IMG_COMPETITIONS_PATH, NAME_DB
from logging_utils import log_message
import sqlite3


class ConnectionDB:
    
    def __init__(self, database_file: str = NAME_DB) -> None:
        
        try:
            # Connect to the SQLite database
            self.database_file = database_file
            self.connection = sqlite3.connect(database_file)
            self.cursor = self.connection.cursor()
            log_message('INFO', f"Connect to database: {database_file}")
            
        except sqlite3.Error as e:
            log_message('INFO', f"Error connecting to the database: {database_file}")
            

    def get_countries_broadcast(self, lang='en') -> list:
        
        query = f'SELECT name FROM countries WHERE lang = (SELECT id FROM languages WHERE code = "{lang}")'
        
        try:
            # Execute the query
            self.cursor.execute(query)

            # Fetch all the records returned by the query
            records = self.cursor.fetchall()
            
            # Convert the records from tuples to lists
            records = [row[0] for row in records]

            # Return the query results
            return records
        
        except sqlite3.Error as e:
            print(f"Error: {e}")
    
    
    def get_competition_by_continent(self, continent, lang='en') -> list:
        
        query = f"""SELECT name FROM competitions 
                    WHERE lang = (SELECT id FROM languages WHERE code = '{lang}'
                    AND continent = (SELECT id FROM continents WHERE name = '{continent}')
                    AND active = 1)
                """
        
        try:
            # Execute the query
            self.cursor.execute(query)

            # Fetch all the records returned by the query
            records = self.cursor.fetchall()
            
            # Convert the records from tuples to lists
            records = [row[0] for row in records]

            # Return the query results
            return records
        
        except sqlite3.Error as e:
            print(f"Error: {e}")
            
            
    def get_competitions(self, lang='en') -> list:
        
        query = f"""SELECT name FROM competitions 
                    WHERE lang = (SELECT id FROM languages WHERE code = '{lang}'
                    AND active = 1)
                """
        
        try:
            # Execute the query
            self.cursor.execute(query)

            # Fetch all the records returned by the query
            records = self.cursor.fetchall()
            
            # Convert the records from tuples to lists
            records = [row[0] for row in records]

            # Return the query results
            return records
        
        except sqlite3.Error as e:
            print(f"Error: {e}")
            
            
    def get_path_image_flag(self, country: str) -> str:
        query = f'SELECT image_path FROM countries WHERE name = "{country}"'
        
        try:
            # Execute the query
            self.cursor.execute(query)

            # Fetch all the records returned by the query
            record = self.cursor.fetchone()

            if record is not None:
                # Return the query result
                return record[0]
            else:
                return ' '
        
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def get_path_image_competition(self, competition: str) -> str:
        query = f'SELECT image_path FROM competitions WHERE name = "{competition}"'
        
        try:
            # Execute the query
            self.cursor.execute(query)

            # Fetch all the records returned by the query
            record = self.cursor.fetchone()

            if record is not None:
                # Return the query result
                return record[0]
            else:
                return ' '
        
        except sqlite3.Error as e:
            print(f"Error: {e}")
    
    
    def close(self) -> None:
        # Close the cursor and the database connection
        self.cursor.close()
        self.connection.close()
        log_message('INFO', f"Close connection to database: {self.database_file}")


def db_init():

    # database
    conn = sqlite3.connect(NAME_DB)
    log_message('INFO', f"Database {NAME_DB} created successfully.")
    cursor = conn.cursor()
    
    # delete tables if exists
    cursor.execute("DROP TABLE IF EXISTS competitions")
    cursor.execute("DROP TABLE IF EXISTS countries")
    cursor.execute("DROP TABLE IF EXISTS continents")
    cursor.execute("DROP TABLE IF EXISTS languages")
    
    # create tables
    cursor.execute("""CREATE TABLE languages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                code TEXT)
                """)
    log_message('INFO', "Table languages created successfully.")

    cursor.execute("""CREATE TABLE continents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT)
                """)
    log_message('INFO', f"Table continents created successfully.")

    cursor.execute("""CREATE TABLE countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                image_path TEXT,
                lang INT,
                FOREIGN KEY (lang) REFERENCES languages(id))
                """)
    log_message('INFO', f"Table countries created successfully.")

    cursor.execute("""CREATE TABLE competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                continent INT,
                lang INT,
                image_path TEXT,
                active BOOL,
                FOREIGN KEY (continent) REFERENCES continents(id),
                FOREIGN KEY (lang) REFERENCES languages(id))
                """)
    log_message('INFO', f"Table competitions created successfully.")


    # rows
    r_languages = [('English', 'en'), ('Spanish', 'es')]
    r_continents = [('Europe',), ('South America',), ('North America',), ('Asia',), ('Africa',), ('International',)]
    r_countries = [('México', 'es', f'{IMG_FLAGS_PATH}Mexico.png'), 
            ('Estados Unidos', 'es', f'{IMG_FLAGS_PATH}United States.png'), 
            ('Mexico', 'en', f'{IMG_FLAGS_PATH}Mexico.png'), 
            ('United States', 'en', f'{IMG_FLAGS_PATH}United States.png')]
    r_competitions = [('England - Premier League', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}England - Premier League.png'),
                ('Spain - La Liga', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Spain - La Liga.png'),
                ('Italy - Serie A', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Italy - Serie A.png'),
                ('Germany - Bundesliga', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Germany - Bundesliga.png'),
                ('France - Ligue 1', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}France - Ligue 1.png'),
                ('Netherlands - Eredivisie', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Netherlands - Eredivisie.png'),
                ('Portugal - Primeira Liga', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Portugal - Primeira Liga.png'),
                ('Europe - UEFA Champions League', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Champions League.png'),
                ('Europe - UEFA Europa League', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Europa League.png'),
                ('England - FA Cup', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}England - FA Cup.png'),
                ('Spain - Copa del Rey', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Spain - Copa del Rey.png'),
                ('Italy - Coppa Italia', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Italy - Coppa Italia.png'),
                ('Germany - DFB Pokal', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Germany - DFB Pokal.png'),
                ('France - Coupe de France', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}France - Coupe de France.png'),
                ('Netherlands - KNVB Beker', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Netherlands - KNVB Beker.png'),
                ('Portugal - Taça de Portugal', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Portugal - Taça de Portugal.png'),
                ('Europe - UEFA Super Cup', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Super Cup.png'),
                ('Europe - UEFA Europa Conference League', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Europa Conference League.png'),
                ('Europe - UEFA Nations League', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Nations League.png'),
                ('Europe - UEFA Euro', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Euro.png'),
                ('Europe - UEFA Euro Qualifying', 'Europe', 'en', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Euro Qualifying.png'),
                ('Argentina - Primera División', 'South America', 'en', f'{IMG_COMPETITIONS_PATH}Argentina - Primera División.png'),
                ('Brazil - Brasileirão', 'South America', 'en', f'{IMG_COMPETITIONS_PATH}Brazil - Brasileirão.png'),
                ('South America - Copa Libertadores', 'South America', 'en', f'{IMG_COMPETITIONS_PATH}South America - Copa Libertadores.png'),
                ('South America - Copa América', 'South America', 'en', f'{IMG_COMPETITIONS_PATH}South America - Copa América.png'),
                ('Mexico - Liga MX', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}Mexico - Liga MX.png'),
                ('Mexico - Liga MX Femenil', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}Mexico - Liga MX Femenil.png'),
                ('Mexico - Copa MX', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}Mexico - Copa MX.png'),
                ('Mexico - Liga de Expansión MX', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}Mexico - Liga de Expansión MX.png'),
                ('Mexico - Campeon de Campeones', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}Mexico - Campeon de Campeones.png'),
                ('USA/Canada - Major League Soccer', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}USACanada - Major League Soccer.png'),
                ('North America - CONCACAF Champions League', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Champions League.png'),
                ('North America - CONCACAF Nations League', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Nations League.png'),
                ('North America - CONCACAF Gold Cup', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Gold Cup.png'),
                ('North America - CONCACAF Gold Cup Qualification', 'North America', 'en', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Gold Cup Qualification.png'),
                ('Friendly', 'International', 'en', f'{IMG_COMPETITIONS_PATH}Friendly.png'),
                ('FIFA U-20 World Cup', 'International', 'en', f'{IMG_COMPETITIONS_PATH}FIFA U-20 World Cup.png'),
                ('South America - Copa Sudamericana', 'South America', 'en', f'{IMG_COMPETITIONS_PATH}South America - Copa Sudamericana'),
                # ---------------------------------------------------------------------------------------------------------------------------#
                ('Inglaterra - Premier League', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}England - Premier League.png'),
                ('España - La Liga', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Spain - La Liga.png'),
                ('Italia - Serie A', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Italy - Serie A.png'),
                ('Alemania - Bundesliga', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Germany - Bundesliga.png'),
                ('Francia - Ligue 1', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}France - Ligue 1.png'),
                ('Países Bajos - Eredivisie', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Netherlands - Eredivisie.png'),
                ('Portugal - Primeira Liga', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Portugal - Primeira Liga.png'),
                ('Europa - Liga de Campeones de la UEFA', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Champions League.png'),
                ('Europa - UEFA Europa League', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Europa League.png'),
                ('Inglaterra - FA Cup', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}England - FA Cup.png'),
                ('España - Copa del Rey', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Spain - Copa del Rey.png'),
                ('Italia - Copa Italiana', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Italy - Coppa Italia.png'),
                ('Alemania - Copa de Alemania', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Germany - DFB Pokal.png'),
                ('Francia - Copa de Francia', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}France - Coupe de France.png'),
                ('Países Bajos - Copa de Futbol Holanda', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Netherlands - KNVB Beker.png'),
                ('Portugal - Copa de Portugal', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Portugal - Taça de Portugal.png'),
                ('Europa - Super Copa de Europa', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Super Cup.png'),
                ('Europa - Liga de Conferencia de la UEFA', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Europa Conference League.png'),
                ('Europa - Liga de las Naciones de la UEFA', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Nations League.png'),
                ('Europa - Eurocopa', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Euro.png'),
                ('Europa - Eliminatorias para la Euro', 'Europe', 'es', f'{IMG_COMPETITIONS_PATH}Europe - UEFA Euro Qualifying.png'),
                ('Argentina - Superliga Argentina', 'South America', 'es', f'{IMG_COMPETITIONS_PATH}Argentina - Primera División.png'),
                ('Brasil - Brasileirão', 'South America', 'es', f'{IMG_COMPETITIONS_PATH}Brazil - Brasileirão.png'),
                ('Sudamérica - Copa Libertadores', 'South America', 'es', f'{IMG_COMPETITIONS_PATH}South America - Copa Libertadores.png'),
                ('Sudamérica - Copa América', 'South America', 'es', f'{IMG_COMPETITIONS_PATH}South America - Copa América.png'),
                ('México - Liga MX', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}Mexico - Liga MX.png'),
                ('México - Liga MX Femenil', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}Mexico - Liga MX Femenil.png'),
                ('México - Copa MX', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}Mexico - Copa MX.png'),
                ('México - Ascenso MX', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}Mexico - Liga de Expansión MX.png'),
                ('México - Campeon de Campeones', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}Mexico - Campeon de Campeones.png'),
                ('EE. UU./Canadá - Major League Soccer', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}USACanada - Major League Soccer.png'),
                ('Norteamérica - Liga Campeones CONCACAF', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Champions League.png'),
                ('Norteamérica - Liga de Naciones CONCACAF', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Nations League.png'),
                ('Norteamérica - Copa Oro', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Gold Cup.png'),
                ('Norteamérica - CONCACAF Gold Cup Qualification', 'North America', 'es', f'{IMG_COMPETITIONS_PATH}North America - CONCACAF Gold Cup Qualification.png'),
                ('Amistoso', 'International', 'es', f'{IMG_COMPETITIONS_PATH}Friendly.png'),
                ('Copa Mundial Sub-20 de la FIFA', 'International', 'es', f'{IMG_COMPETITIONS_PATH}FIFA U-20 World Cup.png'),
                ('Sudamérica - Copa Sudamericana', 'South America', 'es', f'{IMG_COMPETITIONS_PATH}South America - Copa Sudamericana'),]


    cursor.executemany("INSERT INTO languages (name, code) VALUES (?, ?)", r_languages)
    cursor.executemany("INSERT INTO continents (name) VALUES (?)", r_continents)
    cursor.executemany("INSERT INTO countries (name, lang, image_path) VALUES (?, (SELECT id FROM languages WHERE code = ?), ?)", r_countries)
    cursor.executemany("INSERT INTO competitions (name, continent, lang, active, image_path) VALUES (?, (SELECT id FROM continents WHERE name = ?), (SELECT id FROM languages WHERE code = ?), true, ?);", r_competitions)
    
    log_message('INFO', f"Rows inserted successfully.")

    conn.commit()
    conn.close()