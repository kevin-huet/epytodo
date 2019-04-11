from flask import Flask, session, render_template, request, redirect, url_for
import pymysql
import sys
from app import app
from app import models, views

db = models.Database()
db.init_database()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)