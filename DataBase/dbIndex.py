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
            str_query = f"INSERT INTO Customers (id,Name,Surname,Mail) " \
                        f"VALUES (" \
                        f"'{cust['userID']}', " \
                        f"'{cust['userName']}', " \
                        f"'{cust['userSurname'] if cust['userSurname'] != None else cust['userUsername']}', " \
                        f"'{cust['Mail']}'" \
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

    def get_customers_mail(self, id):
        self.DBConnect()
        str_query = f"SELECT Mail FROM Customers" \
                    f" WHERE id = '{id}'"
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            category_prod = list()
            for item in cursor.fetchall():
                listCategory = list(item)
                print(listCategory)
                category_prod.append({'mail': listCategory[0]})
            return category_prod
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

    def get_CategoryProd(self, id):
        self.DBConnect()
        str_query = f"SELECT distinct cp.id, cp.Name, idGlobalCategory " \
                    f"FROM CategoryProd cp, GlobalCategory gc " \
                    f"WHERE cp.idGlobalCategory = {int(id)} "
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

    def get_Product(self, id):
        self.DBConnect()
        str_query = f"SELECT DISTINCT p.id,p.NamePhoto, p.Name, p.CategoryId, p.Description, p.Price, p.isSale, p.percentSale, p.countProd " \
                    f"FROM Products p " \
                    f"WHERE p.CategoryId = {int(id)}; "
        Product = list()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            for item in cursor.fetchall():
                listProduct = list(item)
                Product.append({'id': listProduct[0], 'NamePhoto': listProduct[1], 'Name': listProduct[2], 'CategoryId': listProduct[3], 'Description': listProduct[4], 'Price': listProduct[5],
                                'isSale': listProduct[6], 'percentSale': listProduct[7], 'countProd': listProduct[8]})
            Product.reverse()
            return Product
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def delete_Basket_by_idCust(self, idCust):
        self.DBConnect()
        str_query = f"DELETE " \
                    f"FROM Basket " \
                    f"WHERE idCust = {int(idCust)}; "
        Product = list()
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

    def get_Product_by_id(self,id):
            self.DBConnect()
            str_query = f"SELECT id, NamePhoto, Name, CategoryId, Description, Price, isSale, percentSale, countProd " \
                        f"FROM Products " \
                        f"WHERE id = {int(id)}; "
            Product = list()
            cursor = None
            try:
                cursor = self.conn.cursor()
                cursor.execute(str_query)
                for item in cursor.fetchall():
                    listProduct = list(item)
                    Product.append({'id': listProduct[0], 'NamePhoto': listProduct[1], 'Name': listProduct[2],
                                    'CategoryId': listProduct[3], 'Description': listProduct[4],
                                    'Price': listProduct[5],
                                    'isSale': listProduct[6], 'percentSale': listProduct[7],
                                    'countProd': listProduct[8]})
                return Product
            except NameError:
                print(NameError.name)
            finally:
                cursor.close()
                self.conn.close()

    def get_Product_by_all_id(self,id):
            self.DBConnect()
            str_query = f"SELECT id, NamePhoto, Name, CategoryId, Description, Price, isSale, percentSale, countProd " \
                        f"FROM Products " \
                        f"WHERE {id}; "
            Product = list()
            cursor = None
            try:
                cursor = self.conn.cursor()
                cursor.execute(str_query)
                for item in cursor.fetchall():
                    listProduct = list(item)
                    Product.append({'id': listProduct[0], 'NamePhoto': listProduct[1], 'Name': listProduct[2],
                                    'CategoryId': listProduct[3], 'Description': listProduct[4],
                                    'Price': listProduct[5],
                                    'isSale': listProduct[6], 'percentSale': listProduct[7],
                                    'countProd': listProduct[8]})
                return Product
            except NameError:
                print(NameError.name)
            finally:
                cursor.close()
                self.conn.close()


    def insert_Basket(self, basket):
        self.DBConnect()
        print('s')
        if self.conn != None:
            str_query = f"INSERT INTO Basket (idCust, idsProd, SumOrder, countsProd) " \
                        f"VALUES (" \
                        f"'{basket['idCust']}', " \
                        f"'{basket['idsProd']}', " \
                        f"'{basket['SumOrder']}'," \
                        f"'{basket['countsProd']}');"
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

    def get_basket(self, idCust):
        self.DBConnect()
        str_query = f"SELECT id, idCust, idsProd, SumOrder, countsProd " \
                    f"FROM Basket " \
                    f"WHERE idCust = '{idCust}' "
        Product = list()
        cursor = None
        try:

            cursor = self.conn.cursor()
            cursor.execute(str_query)
            for item in cursor.fetchall():
                print(item)
                prodOfBasket = list(item)
                Product.append({'id': prodOfBasket[0], 'idCust': prodOfBasket[1], 'idsProd': prodOfBasket[2],
                                'SumOrder': prodOfBasket[3], 'countsProd': prodOfBasket[4]})
            Product.reverse()
            print(Product)
            return Product
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def update_basket(self, idCust, basket):
        self.DBConnect()
        str_query = f"UPDATE Basket SET idsProd = '{basket['idsProd']}' ,SumOrder = {basket['SumOrder']} ,CountsProd= '{basket['countsProd']}' " \
                    f"WHERE idCust = '{idCust}'"
        Product = list()
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

    def get_Sale_Product(self):
        self.DBConnect()
        str_query = f"SELECT id, NamePhoto, Name, CategoryId, Description, Price, isSale, percentSale, countProd " \
                    f"FROM Products " \
                    f"WHERE isSale = TRUE "
        Product = list()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(str_query)
            for item in cursor.fetchall():
                listProduct = list(item)
                Product.append({'id': listProduct[0], 'NamePhoto': listProduct[1], 'Name': listProduct[2],
                                'CategoryId': listProduct[3], 'Description': listProduct[4],
                                'Price': listProduct[5],
                                'isSale': listProduct[6], 'percentSale': listProduct[7],
                                'countProd': listProduct[8]})
            return Product
        except NameError:
            print(NameError.name)
        finally:
            cursor.close()
            self.conn.close()

    def insert_orders(self, order):
        self.DBConnect()
        if self.conn != None:
            str_query = f"INSERT INTO Orders(idCust, idsProd, countProd, City, AdressNP, SumOrder, Phone) " \
                        f"VALUES (" \
                        f" '{order['idCust']}' , " \
                        f" '{order['idsProd']}' , " \
                        f" '{order['countProd']}' ," \
                        f" '{order['City']}' ," \
                        f" '{order['AdressNP']}' ," \
                        f" {float(order['SumOrder'])} ," \
                        f"'{order['Phone']}');"
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