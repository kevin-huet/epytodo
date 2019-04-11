#! /usr/bin/python

from flask import Flask, session, render_template, request, redirect, url_for
from app import app
import pymysql
import controllers
import models
import re
import hashlib

db = models.Database()
controll = controllers.my_controllers()

@app.route('/')
def main_page():
    if 'id' in session:
        return redirect('http://localhost/task')
    return render_template('index.html')

@app.route('/task')
def todo_list():
    if 'id' in session:
        data = db.list_task(session['id'])
        return render_template('list.html', data=data, id=session['id'], username=session['username'])
    else:
        return redirect('http://localhost/')

def delete(id):
    if 'id' in session:
        db.delete_task(id)
    return redirect('http://localhost/task')

@app.route('/creator')
def creator():
    return render_template('creator.html')

@app.route('/login_form')
def login_form():
    if 'id' in session:
        return redirect('http://localhost/task')
    return render_template('connexion.html')

@app.route('/register_form')
def register_form():
    if 'id' in session:
        return redirect('http://localhost/task')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_req():
    if 'id' in session:
        return redirect('http://localhost/task')
    user = request.form['username']
    password = request.form['password']
    id_user, i = db.check_login(user, hashlib.md5(password.encode('utf-8')).hexdigest())
    if user != None and password != None and user != "" and password != "" and i > 0:
        session['username'] = user
        session['id'] = int(id_user["id"])
        return redirect('http://localhost/task')
    return redirect('http://localhost/login_form')

@app.route('/register', methods=['POST'])
def register_req():
    if 'id' in session:
        return redirect('http://localhost/')
    user = request.form['username']
    password = request.form['password']
    id_user, i = db.check_login(user, hashlib.md5(password.encode('utf-8')).hexdigest())
    if user != None and password != None and user != "" and password != "" and i < 1:
        db.add_user(user, hashlib.md5(password.encode('utf-8')).hexdigest())
        return redirect('http://localhost/login_form')
    return redirect('http://localhost/register_form')

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'id' in session:
        status = request.form['status']
        title = request.form['title']
        begin = request.form['begin']
        end = request.form['end']
        db.add_task(session['id'], title, begin, end, status)
    return redirect('http://localhost/task')

@app.route('/task/<id>', methods=['GET'])
def rm_task(id):
    if 'id' in session:
        db.remove_task(session['id'], id)
    return redirect('http://localhost/task')

@app.route('/task/edit/<id>', methods=['POST', 'GET'])
def edit_task(id):
    if 'id' in session:
        status = request.form['status']
        title = request.form['title']
        begin = request.form['begin']
        end = request.form['end']
        db.edit_task(session['id'], id, status, title, begin, end)
    return redirect('http://localhost/task')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('http://localhost/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

