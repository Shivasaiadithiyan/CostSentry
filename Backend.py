import sqlite3

class myDB:

    def __init__(self):
        self.conn = sqlite3.connect('wishlist.db')
        self.cursor = self.conn.cursor()
        self.closeConn()

    def EstbConn(self):
        self.conn = sqlite3.connect('wishlist.db')
        self.cursor = self.conn.cursor()

    def closeConn(self):
        self.conn.commit()
        self.conn.close()
    

    def createDB(self):
        self.EstbConn()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL,
                            url TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        self.closeConn()


    def viewAllData(self):
        self.EstbConn()
        self.cursor.execute("SELECT * FROM items where name = 'Antique Gold Mild Steel Contemporary Wall Light'")
        data = self.cursor.fetchall()
        for row in data:
            print(row)
        self.closeConn()


    def deleteAllData(self):
        self.EstbConn()
        self.cursor.execute("DELETE FROM items")
        self.closeConn()
