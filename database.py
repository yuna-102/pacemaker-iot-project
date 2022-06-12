import hashlib
import sqlite3


class UserDB:
    """
    유저 데이터를 저장하는 데이터베이스
        -   usertable: 유저 로그인 정보를 저장하는 테이블. 유저 id, 유저 이름, 유저 비밀번호, 키, 몸무게 데이터 저장
        -   recordtable: 유저 페이스메이커 사용 기록 저장하는 테이블. 유저 id, 시간, 소모 칼로리, 주행 거리 데이터 저장
    """

    def __init__(self):
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

    # 비밀번호 암호화
    @staticmethod
    def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    # 암호화된 비밀번호와 인자로 받은 비밀번호가 일치하는지 확인
    def check_hashes(self, password, hashed_text):
        if self.make_hashes(password) == hashed_text:
            return hashed_text
        return False

    # usertable이 존재하지 않는 경우 생성
    def create_usertable(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS userstable(id integer primary key autoincrement, username TEXT, password TEXT, userheight INTEGER, userweight INTEGER)"
        )

    # recordtable이 존재하지 않는 경우 생성
    def create_recordtable(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS recordtable(id INTEGER, date DATETIME, comsumed_calories INTEGER, running_distance INTEGER)"
        )

    # usertable에 데이터 추가
    def add_userdata(self, user_name, password, user_height, user_weight):
        self.cur.execute(
            "INSERT INTO userstable(username, password, userheight, userweight) VALUES (?,?,?,?)",
            (user_name, password, user_height, user_weight),
        )
        self.con.commit()

    # usertable의 데이터 수정
    def modify_userdata(self, user_height, user_weight, password, user_id):
        self.cur.execute(
            "UPDATE userstable SET userheight=?, userweight=?, password=? Where id=?",
            (user_height, user_weight, password, user_id),
        )
        self.con.commit()

    # recordtable에 데이터 추가
    def add_user_record(self, user_record):
        user_record.to_sql("recordtable", self.con, if_exists="append")

    # 인자로 받은 유저 이름과 비밀번호가 usertable에 존재하는지 찾고 이를 리턴
    def login_user(self, user_name, password):
        self.cur.execute(
            "SELECT DISTINCT * FROM userstable WHERE username =? AND password = ?",
            (user_name, password),
        )
        data = self.cur.fetchall()
        return data

    # 인자로 받은 유저 이름이 이미 존재하는지 확인
    def check_if_username_exits(self, user_name):
        self.cur.execute(
            "SELECT DISTINCT * FROM userstable WHERE username =?",
            (user_name,),
        )
        data = self.cur.fetchall()
        return data

    # 인자로 받은 유저 id가 recordtable에 존재하는지 찾고 이를 리턴
    def get_user_record(self, user_id):
        self.cur.execute("SELECT DISTINCT * FROM recordtable WHERE id =?", (user_id,))
        data = self.cur.fetchall()
        return data

    # usertable의 모든 데이터 정보 열람
    def view_all_users(self):
        self.cur.execute("SELECT * FROM userstable")
        data = self.cur.fetchall()
        return data

    # recordtable의 모든 데이터 정보 열람
    def view_all_records(self):
        self.cur.execute("SELECT * FROM recordtable")
        data = self.cur.fetchall()
        return data
