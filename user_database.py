import hashlib
import sqlite3


class UserDB:
    def __init__(self):
        self.con = sqlite3.connect("data.db")  # data will be stored in the data.db
        self.cur = self.con.cursor()

    @staticmethod
    def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_hashes(self, password, hashed_text):
        if self.make_hashes(password) == hashed_text:
            return hashed_text
        return False

    def create_usertable(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS userstable(id integer primary key autoincrement, username TEXT, password TEXT, userheight INTEGER, userweight INTEGER)"
        )

    def create_recordtable(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS recordtable(id INTEGER, date DATETIME, comsumed_calories INTEGER, running_distance INTEGER)"
        )

    def add_userdata(self, user_name, password, user_height, user_weight):
        self.cur.execute(
            "INSERT INTO userstable(username, password, userheight, userweight) VALUES (?,?,?,?)",
            (user_name, password, user_height, user_weight),
        )
        self.con.commit()

    def modify_userdata(self, user_height, user_weight, password, user_id):
        self.cur.execute(
            "UPDATE userstable SET userheight=?, userweight=?, password=? Where id=?",
            (user_height, user_weight, password, user_id),
        )
        self.con.commit()

    def login_user(self, user_name, password):
        self.cur.execute(
            "SELECT DISTINCT * FROM userstable WHERE username =? AND password = ?",
            (user_name, password),
        )
        data = self.cur.fetchall()
        return data

    def get_user_record(self, user_id):
        self.cur.execute("SELECT DISTINCT * FROM recordtable WHERE id =?", (user_id,))
        data = self.cur.fetchall()
        return data

    # def add_user_record(self, user_id, date, comsumed_calories, running_distance):
    #       self.cur.execute('INSERT INTO userstable(username, password, userheight, userweight) VALUES (?,?,?,?)',(user_id, date, comsumed_calories, running_distance))
    #       self.con.commit()

    def add_user_record(self, user_record):
        user_record.to_sql("recordtable", self.con, if_exists="append")

    def view_all_users(self):
        self.cur.execute("SELECT * FROM userstable")
        data = self.cur.fetchall()
        return data

    def view_all_records(self):
        self.cur.execute("SELECT * FROM recordtable")
        data = self.cur.fetchall()
        return data
