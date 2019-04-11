import pymysql
import models

class my_controllers: 
    def db_query(self, select):
        db = models.Database()
        if select == "users_list":
            users = db.list_users()
        if select == "task_list":
            users = db.list_task()
        if select == "user_has_task":
            users = db.user_has_task()
        return (users)
