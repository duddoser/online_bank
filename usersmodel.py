class UsersModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             login VARCHAR(50),
                             password_hash VARCHAR(128),
                             card_number VARCHAR(16),
                             expiry_date VARCHAR(8),
                             name VARCHAR(50),
                             safe_number(3),
                             money(30) 
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, password_hash, card_number, expiry_date, name, safe_number):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (login, password_hash, card_number, expiry_date, name, safe_number, money) 
                          VALUES (?,?,?,?,?,?,?)''', (login, password_hash, card_number,
                                                      expiry_date, name, safe_number))
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
