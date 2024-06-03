import sqlite3

class Connection:
    def __init__(self):
        self.con = sqlite3.connect('bankdata.db')  # Connect to SQLite database
        self.cursor = self.con.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                emailid TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS account (
                emailid TEXT NOT NULL,
                acno INTEGER PRIMARY KEY,
                balance REAL NOT NULL,
                FOREIGN KEY(emailid) REFERENCES users(emailid)
            )
        ''')
        self.con.commit()

    def storeUser(self, email, pass1):
        sql = "INSERT INTO users (emailid, password) VALUES (?, ?)"
        try:
            self.cursor.execute(sql, (email, pass1))
            self.con.commit()
            self.status = True
        except sqlite3.IntegrityError:  # Handle unique constraint violation
            self.con.rollback()
            self.status = False
        return self.status

    def checkUser(self, email, pass1):
        sql = "SELECT * FROM users WHERE emailid = ? AND password = ?"
        self.cursor.execute(sql, (email, pass1))
        if self.cursor.fetchone():
            self.status = True
        else:
            self.status = False
        return self.status

    def storeAccount(self, email, acno, amt):
        sql = "INSERT INTO account (emailid, acno, balance) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(sql, (email, acno, amt))
            self.con.commit()
            self.status = True
        except sqlite3.IntegrityError:  # Handle unique constraint violation
            self.con.rollback()
            self.status = False
        return self.status

    def checkAccount(self, email, acno):
        sql = "SELECT * FROM account WHERE emailid = ? AND acno = ?"
        self.cursor.execute(sql, (email, acno))
        data = self.cursor.fetchone()
        if data:
            balance = data[2]
        else:
            balance = -1
        return balance

    def storeTrans(self, email, acno, amt, type):
        if type == 'Deposit':
            sql = "UPDATE account SET balance = balance + ? WHERE emailid = ? AND acno = ?"
        else:
            sql = "UPDATE account SET balance = balance - ? WHERE emailid = ? AND acno = ?"
        try:
            self.cursor.execute(sql, (amt, email, acno))
            self.con.commit()
            self.status = True
        except sqlite3.Error:
            self.con.rollback()
            self.status = False
        return self.status

    def storeRecharge(self, email, acno, amt, type):
        sql = "UPDATE account SET balance = balance - ? WHERE emailid = ? AND acno = ?"
        try:
            self.cursor.execute(sql, (amt, email, acno))
            self.con.commit()
            self.status = True
        except sqlite3.Error:
            self.con.rollback()
            self.status = False
        return self.status

    def storeFundTransfer(self, email, acno1, acno2, amt):
        try:
            self.con.execute("BEGIN")  # Start a transaction
            sql = "UPDATE account SET balance = balance - ? WHERE emailid = ? AND acno = ?"
            self.cursor.execute(sql, (amt, email, acno1))
            sql = "UPDATE account SET balance = balance + ? WHERE emailid = ? AND acno = ?"
            self.cursor.execute(sql, (amt, email, acno2))
            self.con.commit()
            self.status = True
        except sqlite3.Error:
            self.con.rollback()
            self.status = False
        return self.status

    def checkPassword(self, email, pass1):
        sql = "SELECT * FROM users WHERE emailid = ? AND password = ?"
        self.cursor.execute(sql, (email, pass1))
        if self.cursor.fetchone():
            status = True
        else:
            status = False
        return status

    def updatePassword(self, email, oldp, newp):
        sql = "UPDATE users SET password = ? WHERE emailid = ? AND password = ?"
        try:
            self.cursor.execute(sql, (newp, email, oldp))
            self.con.commit()
            self.status = True
        except sqlite3.Error:
            self.con.rollback()
            self.status = False
        return self.status
