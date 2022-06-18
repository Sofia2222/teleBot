from mysql.connector import connect
from DataBase.helper.read_config_Methods import read_config

class DB:
    config = None
    conn = None

    def __init__(self):
        self.config = read_config()
        self.conn = None

    def DBConnect(self):
        try:
            self.conn = connect(
                user=self.config['DBSettings']['dbuser'],
                password=self.config['DBSettings']['dbpassword'],
                host=self.config['DBSettings']['dbhost'],
                port=self.config['DBSettings']['dbport'],
                database=self.config['DBSettings']['dbdatabase'],
                ssl_ca=self.config['DBSettings']['dbssl_ca'],
            )
        except NameError:
            print(NameError.name)

    def SELECT(self, query):
        self.DBConnect()
        print(query)
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except NameError:
            print(NameError.name)
        finally:
            if(cursor != None):
                cursor.close()
            if(self != None):
                self.conn.close()

    def INSERT(self, query):
        self.DBConnect()
        if self.conn != None:
            cursor = None
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                self.conn.commit()
            except NameError:
                print(NameError.name)
            finally:
                cursor.close()
                self.conn.close()

    def DELETE(self, query):
        self.DBConnect()
        Product = list()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def UPDATE(self, query):
        self.DBConnect()
        Product = list()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()
