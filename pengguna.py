from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages, session
from database import get_mysql_connection


pengguna_bp = Blueprint('pengguna_bp', __name__,)


@pengguna_bp.route('/show_pengguna')
def show_pengguna():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT * FROM pengguna"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('pengguna.html', data=output_json)


@pengguna_bp.route('/create_pengguna', methods=['GET', 'POST'])
def create_pengguna():
    db = get_mysql_connection()
    if request.method == 'POST':

        nama = request.form['nama']
        password = request.form['password']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO pengguna (kata_kunci, nama_pengguna) VALUES('{password}', '{nama}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('pengguna_bp.show_pengguna'))
    return render_template('from_pengguna.html')


@pengguna_bp.route('/update_pengguna/<int:id_pengguna>', methods=['GET', 'POST'])
def update_pengguna(id_pengguna):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM pengguna where id_pengguna = {id_pengguna}"
        cur.execute(sqlstr)
        print('sukses')
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'GET':
        return render_template('update_form_pengguna.html', data=old_data)
    else:
        nama = request.form['nama']
        password = request.form['password']

        if len(nama) == 0:
            nama = old_data[0][2]
        if len(password) == 0:
            password = old_data[0][1]

        try:
            cur = db.cursor()
            sqlstr = f"update pengguna set kata_kunci='{password}', nama_pengguna='{nama}' where id_pengguna={id_pengguna}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('pengguna_bp.show_pengguna'))


@pengguna_bp.route('/delete_pengguna/<int:id_pengguna>', methods=['GET', 'POST'])
def delete_pengguna(id_pengguna):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM pengguna where id_pengguna={id_pengguna}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('pengguna_bp.show_pengguna'))


@pengguna_bp.route('/login', methods=['GET', 'POST'])
def login():
    db = get_mysql_connection()

    if request.method == 'POST':
        username = request.form['nama_pengguna']
        password = request.form['password']
        cur = db.cursor()
        sqlstr = f"select * from pengguna where nama_pengguna='{username}'"
        cur.execute(sqlstr)
        account = cur.fetchone()
        print(account)
        if account:
            if (account[1] == password):
                flash('login sukses', category='success')
                session['logged_in'] = True
                session['id'] = account[0]
                session['username'] = account[2]
                print('berhasil login')
                return redirect(url_for('dashboard'))
            else:
                flash('password salah', category='danger')
                return redirect(url_for('pengguna_bp.login'))
        else:
            flash('email salah', category='danger')
            return redirect(url_for('pengguna_bp.login'))
    return render_template('login_form.html')


@pengguna_bp.route('/logout/')
def logout():
    session.pop('username', None)
    print('berhasil logout')
    return redirect(url_for('index'))
