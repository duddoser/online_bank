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
                                     expiry_m VARCHAR(2),
                                     expiry_y VARCHAR(2),
                                     name VARCHAR(50),
                                     safe_number VARCHAR(3),
                                     money INTEGER
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, password_hash, card_number, expiry_m, expiry_y, name, safe_number, money):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, card_number, expiry_m, expiry_y, name, safe_number, money) 
                          VALUES (?,?,?,?,?,?,?,?)''', (login, password_hash, card_number, expiry_m, expiry_y, name,
                                                        safe_number, money))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_id(self, card_number):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE card_number = ?", (str(card_number),))
        row = cursor.fetchone()
        return row

    def get_money(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT money FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def update_money(self, card_number, money):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET money = ? WHERE card_number = ?", (str(money), str(card_number),))
        cursor.fetchone()

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

    def exists(self, user_name, password_hash=None):
        cursor = self.connection.cursor()
        if password_hash is not None:
            cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                           (user_name, password_hash))
        else:
            cursor.execute("SELECT * FROM users WHERE user_name = ?", (str(user_name),))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)
