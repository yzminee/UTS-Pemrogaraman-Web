from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection

mengajar_bp = Blueprint('mengajar_bp', __name__,)


@mengajar_bp.route('/show_mengajar')
def show_mengajar():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT * FROM mengajar"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('mengajar.html', data=output_json)


@mengajar_bp.route('/create_mengajar', methods=['GET', 'POST'])
def create_mengajar():
    db = get_mysql_connection()
    if request.method == 'POST':
        nip = request.form['nip']
        mapel = request.form['mapel']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO mengajar (nip, id_mapel) VALUES({nip}, {mapel})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('mengajar_bp.show_mengajar'))
    try:
        cur = db.cursor()
        sqlstr = f"select nip from guru"
        cur.execute(sqlstr)
        print('sukses')
        nip = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        cur = db.cursor()
        sqlstr = f"select id_mapel from mapel"
        cur.execute(sqlstr)
        print('sukses')
        mapel = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('form_mengajar.html', nip=nip, mapel=mapel)


@mengajar_bp.route('/update_mengajar/<int:id_mengajar>', methods=['GET', 'POST'])
def update_mengajar(id_mengajar):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM mengajar where id_mengajar = {id_mengajar}"
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

    try:
        cur = db.cursor()
        sqlstr = f"SELECT id_mapel FROM mapel"
        cur.execute(sqlstr)
        print('sukses')
        mapel = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'GET':
        return render_template('update_form_mengajar.html', data=old_data, nip=nip, mapel=mapel)
    else:
        mapel = request.form['mapel']
        nip = request.form['nip']
        if len(mapel) == 0:
            mapel = old_data[0][2]
        if len(nip) == 0:
            nip = old_data[0][1]

        try:
            cur = db.cursor()
            sqlstr = f"update mengajar set id_mapel={mapel}, nip={nip} where id_mengajar={id_mengajar}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('mengajar_bp.show_mengajar'))


@mengajar_bp.route('/delete_mengajar/<int:id_mengajar>', methods=['GET', 'POST'])
def delete_mengajar(id_mengajar):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM mengajar where id_mengajar={id_mengajar}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('mengajar_bp.show_mengajar'))
