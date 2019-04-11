import pymysql
import init_sql
import config
import warnings

class Database:
    def __init__(self):
        db_info = config.db_init()
        self.con = pymysql.connect(host=db_info["host"],
                    user=db_info["user"], password=db_info["password"],
                    db=db_info["db"], 
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    
    def init_database(self):
        stmts = init_sql.parse_sql('epytodo.sql')
        warnings.filterwarnings('ignore')
        with self.con.cursor() as self.cur:
            for stmt in stmts:
                self.cur.execute(stmt)
            self.con.commit()

    def list_users(self):
        self.cur.execute("SELECT * FROM user LIMIT 50")
        result = self.cur.fetchall()
        return (result)

    def list_task(self, id):
        self.cur.execute("SELECT * FROM task WHERE userid = %s LIMIT 50", (id,))
        result = self.cur.fetchall()
        return (result)
    
    def user_has_task(self):
        self.cur.execute("SELECT * FROM user_has_task LIMIT 50")
        result = self.cur.fetchall()
        return (result)
    
    def check_login(self, username, password):
        self.cur.execute("SELECT id FROM user WHERE username = %s AND password = %s", (username, password,))
        result = self.cur.fetchone()
        if result == None:
            return (result, 0)
        return (result, len(result))

    def remove_task(self, user_id, task_id):
        self.cur.execute("DELETE FROM task WHERE id = %s AND userid = %s", (task_id, user_id,))
        result = self.cur.fetchone()
        self.con.commit()
        return (result)

    def add_user(self, username, password):
        add_new_user = ("INSERT INTO user (id, username, password) VALUES (NULL, %s, %s)")
        data_user = (username, password)
        self.cur.execute(add_new_user, data_user)
        result = self.cur.fetchall()
        self.con.commit()
        return (result)

    def add_users_task(self, user_id, task_id):
        add_new_user_task = ("INSERT INTO user_has_task (id, username, password) VALUES (%d, %d)")
        data_user = (user_id, task_id)
        self.cur.execute(add_new_user_task, data_user)
        result = self.cur.fetchall()
        self.con.commit()
        return (result)
    
    def add_task(self, user_id, title, begin, end, status):
        add_new_task = ("INSERT INTO task (id, title, userid, begin, end, status) VALUES (NULL, %s, %s, %s, %s, %s)")
        data = (title, user_id, begin, end, status)
        result = self.cur.execute(add_new_task, data)
        self.cur.fetchall()
        self.con.commit()
        return (result)
    
    def edit_task(self, user_id, task_id, status, title, begin, end):
        self.cur.execute("UPDATE task SET status=%s, title=%s, begin=%s, end=%s WHERE userid=%s AND id=%s", (status, title, begin, end, user_id, task_id,))
        self.con.commit()