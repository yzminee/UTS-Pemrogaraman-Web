from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection

kelas_bp = Blueprint('kelas_bp', __name__,)


@kelas_bp.route('/show_kelas')
def show_kelas():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT * FROM kelas"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('kelas.html', data=output_json)


@kelas_bp.route('/create_kelas', methods=['GET', 'POST'])
def create_kelas():
    db = get_mysql_connection()
    if request.method == 'POST':

        kelas = request.form['kelas']
        nip = request.form['nip']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO kelas (kelas, nip) VALUES('{kelas}', {nip})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('kelas_bp.show_kelas'))
    try:
        cur = db.cursor()
        sqlstr = f"select nip from guru"
        cur.execute(sqlstr)
        print('sukses')
        nip = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('form_kelas.html', data=nip)


@kelas_bp.route('/update_kelas/<int:id_kelas>', methods=['GET', 'POST'])
def update_kelas(id_kelas):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM kelas where id_kelas = {id_kelas}"
        cur.execute(sqlstr)
        print('sukses')
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        cur = db.cursor()
        sqlstr = f"SELECT nip FROM guru"
        cur.execute(sqlstr)
        print('sukses')
        nip = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'GET':
        return render_template('update_form_kelas.html', data=old_data, nip=nip)
    else:
        kelas = request.form['kelas']
        nip = request.form['nip']

        if len(kelas) == 0:
            kelas = old_data[0][1]
        if len(nip) == 0:
            nip = old_data[0][2]

        try:
            cur = db.cursor()
            sqlstr = f"update kelas set kelas='{kelas}', nip={nip} where id_kelas={id_kelas}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('kelas_bp.show_kelas'))


@kelas_bp.route('/delete_kelas/<int:id_kelas>', methods=['GET', 'POST'])
def delete_kelas(id_kelas):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM kelas where id_kelas={id_kelas}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('kelas_bp.show_kelas'))
