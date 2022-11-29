from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection

mapel_bp = Blueprint('mapel_bp', __name__,)


@mapel_bp.route('/show_mapel')
def show_mapel():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT * FROM mapel"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('mapel.html', data=output_json)


@mapel_bp.route('/create_mapel', methods=['GET', 'POST'])
def create_mapel():
    db = get_mysql_connection()
    if request.method == 'POST':

        mapel = request.form['mapel']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO mapel (mapel) VALUES('{mapel}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('mapel_bp.show_mapel'))
    return render_template('form_mapel.html')


@mapel_bp.route('/update_mapel/<int:id_mapel>', methods=['GET', 'POST'])
def update_mapel(id_mapel):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM mapel where id_mapel = {id_mapel}"
        cur.execute(sqlstr)
        print('sukses')
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'GET':
        return render_template('update_form_mapel.html', data=old_data)
    else:
        mapel = request.form['mapel']

        if len(mapel) == 0:
            mapel = old_data[0][1]

        try:
            cur = db.cursor()
            sqlstr = f"update mapel set mapel='{mapel}' where id_mapel={id_mapel}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('mapel_bp.show_mapel'))


@mapel_bp.route('/delete_mapel/<int:id_mapel>', methods=['GET', 'POST'])
def delete_mapel(id_mapel):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM mapel where id_mapel={id_mapel}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('mapel_bp.show_mapel'))
