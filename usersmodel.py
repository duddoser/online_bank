class UsersModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     user_name VARCHAR(50),
                                     password_hash VARCHAR(128),
                                     card_number VARCHAR(16),
                                     expiry_date VARCHAR(11),
                                     name VARCHAR(50),
                                     safe_number VARCHAR(3),
                                     money INTEGER
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, password_hash, card_number, expiry_date, name, safe_number, money):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, card_number, expiry_date, name, safe_number, money) 
                          VALUES (?,?,?,?,?,?,?)''', (login, password_hash, card_number, expiry_date, name,
                                                      safe_number, money))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_money(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT money FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_id(self, card_number):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE card_number = ?", (str(card_number),))
        row = cursor.fetchone()
        return row

    def get_card_number(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT card_number FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def exist_card_number(self, card):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE card_number = ?",
                       (str(card),))
        row = cursor.fetchone()
        return (True,) if row else (False,)

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def get_card_number(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT card_number FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)
