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



    def insert_customer(self, cust):
        self.DBConnect()
        if self.conn != None:
            str_query = f"INSERT INTO Customers (id,Name,Surname,Phone) " \
                        f"VALUES (" \
                        f"'{cust['userID']}', " \
                        f"'{cust['userName']}', " \
                        f"'{cust['userSurname'] if cust['userSurname'] != None else cust['userUsername']}', " \
                        f"'{cust['userPhone']}'" \
                        f");"
            cursor = None
            try:
                cursor = self.conn.cursor()
                cursor.execute(str_query)
                self.conn.commit()
            except NameError:
                print(NameError.name)
            finally:
                cursor.close()
                self.conn.close()

    def get_customers_by_id(self, id):
        self.DBConnect()
        str_query = f"SELECT * FROM Customers" \
                    f" WHERE id = '{id}'"
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            if len(cursor.fetchall()) != 0:
                return True
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def get_category(self):
        self.DBConnect()
        str_query = f"SELECT id, Name, idGlobalCategory " \
                    f"FROM CategoryProd"
        cursor = None
        category_prod = list()
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            c = 0
            for item in cursor.fetchall():
                c = c + 1
                listCategory = list(item)
                category_prod.append({'id': listCategory[0], 'name': listCategory[1]})
            category_prod.reverse()
            return category_prod
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def get_Global_Category(self):
        self.DBConnect()
        str_query = f"SELECT id, Name " \
                    f"FROM GlobalCategory"
        cursor = None
        global_prod_category = list()
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            for item in cursor.fetchall():
                listCategory = list(item)
                global_prod_category.append({'id': listCategory[0], 'name': listCategory[1]})
            global_prod_category.reverse()
            return global_prod_category
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def get_CategoryProd(self, call_str):
        self.DBConnect()
        str_query = f"SELECT distinct cp.id, cp.Name, idGlobalCategory " \
                    f"FROM CategoryProd cp, GlobalCategory gc " \
                    f"WHERE cp.idGlobalCategory = (SELECT id FROM GlobalCategory gc1 WHERE gc1.Name = '{call_str}') "
        categoryProd = list()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            for item in cursor.fetchall():
                listCategoryProd = list(item)
                categoryProd.append({'id': listCategoryProd[0], 'name': listCategoryProd[1]})

            categoryProd.reverse()
            return categoryProd
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()