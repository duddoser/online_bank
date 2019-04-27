class OperationsModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS operations
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             operation VARCHAR(128),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, operation, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO operations 
                          (operation, user_id) 
                          VALUES (?,?,?)''', (operation, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM operations WHERE user_id = ?",
                           (str(user_id),))
        rows = cursor.fetchall()
        return rows
