from flask import Flask, request, render_template, redirect, session, flash, get_flashed_messages
import mysql.connector
import hashlib
import tkinter as tk
from tkinter import messagebox
app = Flask(__name__)
# app.secret_key = 'your-secret-key'
from flask import url_for
from flask import Flask, request, send_file
import nlp
import threading
from datetime import datetime, timedelta
import os

# 防止某些进程错误
def run_in_main_thread(route_func):
    def wrapper(*args, **kwargs):
        return route_func(*args, **kwargs)
    return wrapper
#构造/get_file网页，可以把路径里的文件以下载的形式传到网页
# @app.route('/get_file')
# def get_file():
#     return send_file(r"C:\Users\13836\PycharmProjects\exp2\exp2\wenben.txt", as_attachment=True)

# 创建数据库连接
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='jiangjing',
    database='selab'
)

@app.route('/', methods=['GET', 'POST'])
def gologin():
    return redirect('/login')

@app.route('/exit')
def exit():
    session['username'] = ''
    session['password'] = ''
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # hashedpassword = hashlib.sha256(password.encode()).hexdigest()
        print(username)
        print(password)

        cursor = connection.cursor()
        query = "SELECT * FROM userinfo WHERE username = %s"
        values = (username,)
        print(query)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            session['username'] = result[0]  # 设置会话数据
            session['password'] = result[1]
            #session['status'] = result[3]
            if session['password'] == password:
                #登陆成功
                print(result)
                return redirect('/welcome')
            else:
                session['username'] = ''  # 设置会话数据
                session['password'] = ''
                session['status'] = ''
                flash('用户名或密码错误', 'failed')
                messages = get_flashed_messages()
                print(messages)
                return render_template('login.html', message=messages)
        else:
            flash('用户名不存在', 'failed')
            messages = get_flashed_messages()
            print(messages)
            return render_template('login.html', message=messages)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']

        cursor = connection.cursor()
        query = "SELECT * FROM userinfo WHERE username = %s "
        values = (username,)
        print(query)
        cursor.execute(query, values)
        result = cursor.fetchone()
        # print(username)
        # print(password)
        # print(repassword)

        if result:
            flash('该用户名已被注册', 'failed')
            messages = get_flashed_messages()
            print(messages)
            return render_template('reg.html', message=messages)
        else:
            if password == repassword:
                # hashedpassword = hashlib.sha256(password.encode()).hexdigest()
                query = """
                                    INSERT INTO userinfo (username, password)
                                    VALUES (%s, %s)
                                """
                values = (username, password)
                cursor.execute(query, values)
                connection.commit()
                flash('注册成功', 'success')
                messages = get_flashed_messages()
                print(messages)
            else :
                flash('两次输入密码不一致！', 'failed')
                messages = get_flashed_messages()
                print(messages)
            return render_template('reg.html', message=messages)

    return render_template('reg.html')

@app.route('/welcome', methods=['GET'])
def welcome():
    if 'username' in session:  # 检查会话中的数据来判断是否登录
        username = session['username']
        return render_template('welcome.html')
    else:
        return redirect('/login')

@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        password = request.form['password']
        mypassword = '1993'
        print(password)

        if password == mypassword:
            # print('--------------')
            return redirect('/manager')

        else:
            flash('密码错误', 'failed')
            messages = get_flashed_messages()
            print(messages)
            return render_template('manager_login.html', message=messages)

    return render_template('manager_login.html')

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    # 读取wenben.txt内容
    if os.path.exists('C:\\Users\\13836\\PycharmProjects\\exp2\\exp2\\wenben.txt'):
        with open('C:\\Users\\13836\\PycharmProjects\\exp2\\exp2\\wenben.txt', 'r',encoding='utf-8') as file:
            file_content = file.read()
    else:
        file_content = ""

    # 获取数据库内容
    cursor = connection.cursor()
    cursor.execute("SELECT username, password FROM userinfo")
    userinfo = cursor.fetchall()
    cursor.close()
    if request.method == 'POST':
        if 'newtext' in request.form:
            newtext = request.form['newtext']
            with open('C:\\Users\\13836\\PycharmProjects\\exp2\\exp2\\wenben.txt', 'w',encoding='utf-8') as file:
                file.write(newtext)
        elif 'delete_username' in request.form:
            delete_username = request.form['delete_username']
            cursor = connection.cursor()
            cursor.execute("DELETE FROM userinfo WHERE username = %s", (delete_username,))
            connection.commit()
            cursor.close()



    return render_template('manager.html', file_content=file_content, userinfo=userinfo)

@app.route('/userspace',methods = ['GET', 'POST'])
def userspace():
    if 'username' in session:
        messages = ['Hello', 'Welcome to your user space.']
        username = session['username']
        if request.method == 'POST':
            email = request.form['Email']
            name = request.form['name']
            organization = request.form['organization']
            time = request.form['time']
            print("提交信息")
            print(email,name,organization,time)

            cursor = connection.cursor()
            # 查询是否有关联记录
            cursor.execute("""
                SELECT COUNT(*) FROM information_table WHERE username = %s
            """, (username,))
            count = cursor.fetchone()[0]
            if count > 0:
                # 如果已经存在记录，更新相关信息
                query = """
                    UPDATE information_table
                    SET email = %s, name = %s, organization = %s, time = %s
                    WHERE username = %s
                """
                values = (email, name, organization, time, username)
                #messagebox.showinfo("成功", "成功更新身份信息数据")
                flash('成功更新身份信息数据', 'success')
                messages = get_flashed_messages()
            else:
                # 如果不存在记录，插入新的记录
                query = """
                    INSERT INTO information_table (username, email, name, organization, time)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (username, email, name, organization, time)
                #messagebox.showinfo("成功", "成功写入身份信息数据")
                flash('成功写入身份信息数据', 'success')
                messages = get_flashed_messages()

            # 执行查询
            cursor.execute(query, values)
            connection.commit()
            cursor.close()

        return render_template('/userspace.html', username=username, messages=messages)
    else:
        return redirect('/login')

@app.route('/userspace_read', methods=['GET'])
def userspace_read():
    if 'username' in session:  # 检查会话中的数据来判断是否登录
        username = session['username']
        cursor = connection.cursor()
        # 查询是否有关联记录
        cursor.execute("SELECT username, email, name, organization, time FROM information_table WHERE username = %s",
                       (username,))
        result = cursor.fetchone()
        if result:
            username, email, name, organization, time = result
            return render_template('/userspace_read.html', username=username, email=email, name=name, organization=organization, time=time)
        else :
            flash('查询不到个人信息，请先完善！', 'success')
            messages = get_flashed_messages()
            return render_template('/welcome.html', messages=messages)
    else:
        return redirect('/login')

@app.route('/QA', methods=['GET','POST'])
def QA():
    if 'username' in session:  # 检查会话中的数据来判断是否登录
        print(session)
        username = session['username']
        message = []
        QA_info = []
        if request.method == 'POST':
            question = request.form['question']
            answer =  nlp.main(question)
            print(answer)
            message.append(answer)
            print(message)
            print(question)

            # 插入新问答记录
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = connection.cursor()
            query = """
                        INSERT INTO user_qa (username, QAtime, Q, A)
                        VALUES (%s, %s,%s,%s)
                    """
            values = (username, now, question, answer)
            cursor.execute(query, values)
            connection.commit()


            # 检查并删除最早的记录
            cursor.execute(
                "SELECT * FROM user_qa WHERE username = %s ORDER BY QAtime ASC",
                (username,)
            )
            rows = cursor.fetchall()
            print("user",username,"当前数据条数为",len(rows))
            if len(rows) > 5:
                a, b, c, d ,e= rows[0]
                print(a)
                print(b)
                print(c)
                print(d)
                delete_query = """
                                        DELETE FROM user_qa 
                                        WHERE username = %s AND QAtime = %s AND Q = %s AND A = %s
                                """
                delete_values = (a, b, c, d)
                cursor.execute(delete_query, delete_values)
                connection.commit()

                # connection.close()

            # 获取当前用户的问答记录

            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         "SELECT Q, A, QAtime FROM user_qa WHERE username = %s ORDER BY QAtime DESC",
            #         (username,)
            #     )
            # messages = cursor.fetchall()
            print("运行到此处删除大概正常")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT Q, A, QAtime FROM user_qa WHERE username = %s ORDER BY QAtime DESC",
                (username,)
            )
            QA_info = cursor.fetchall()
            print("0000000")
            print (QA_info)
            cursor.close()
        return render_template('QA.html',messages = message,QA_info=QA_info)
    else:
        return redirect('/login')

@app.route('/FB', methods=['GET','POST'])
def FB():
    print(session)
    username = session['username']
    message = []
    if 'username' in session:  # 检查会话中的数据来判断是否登录
        print(session)
        username = session['username']
        message = []
        if request.method == 'POST':
            feedback = request.form['feedback']
            message.append("感谢您的反馈")
            print(feedback)
        return render_template('Feedback.html',messages = message)
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)