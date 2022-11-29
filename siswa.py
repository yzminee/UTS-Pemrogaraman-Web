from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection

siswa_bp = Blueprint('siswa_bp', __name__,)


@siswa_bp.route('/show_siswa')
def show_siswa():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT * FROM siswa"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('siswa.html', data=output_json)


@siswa_bp.route('/create_siswa', methods=['GET', 'POST'])
def create_siswa():
    db = get_mysql_connection()
    if request.method == 'POST':

        nama = request.form['nama']
        alamat = request.form['alamat']
        tmp_lahir = request.form['tmp_lahir']
        tgl_lahir = request.form['tgl_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        id_kelas = request.form['id_kelas']
        kd_ortu = request.form['kd_ortu']
        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO siswa (nama, alamat, tmp_lahir, tgl_lahir, gender, agama, id_kelas, kd_ortu) VALUES('{nama}', '{alamat}', '{tmp_lahir}', '{tgl_lahir}', '{gender}', '{agama}', {id_kelas}, {kd_ortu})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('siswa_bp.show_siswa'))
    try:
        cur = db.cursor()
        sqlstr = f"select id_kelas from kelas"
        cur.execute(sqlstr)
        print('sukses')
        kelas = cur.fetchall()

        sqlstr = f"select kd_ortu from orang_tua"
        cur.execute(sqlstr)
        print('sukses')
        ortu = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('form_siswa.html', kelas=kelas, ortu=ortu)


@siswa_bp.route('/update_siswa/<int:nis>', methods=['GET', 'POST'])
def update_siswa(nis):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM siswa where nis = {nis}"
        cur.execute(sqlstr)
        print('sukses')
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        cur = db.cursor()
        sqlstr = f"SELECT id_kelas FROM kelas"
        cur.execute(sqlstr)
        print('sukses')
        kelas = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'GET':
        return render_template('update_form_siswa.html', data=old_data, kelas=kelas)
    else:
        nama = request.form['nama']
        alamat = request.form['alamat']
        tmp_lahir = request.form['tmp_lahir']
        tgl_lahir = request.form['tgl_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        id_kelas = request.form['id_kelas']

        if len(nama) == 0:
            nama = old_data[0][1]
        if len(alamat) == 0:
            alamat = old_data[0][2]
        if len(tmp_lahir) == 0:
            tmp_lahir = old_data[0][3]
        if len(tgl_lahir) == 0:
            tgl_lahir = old_data[0][4]
        if len(gender) == 0:
            gener = old_data[0][5]
        if len(agama) == 0:
            agama = old_data[0][6]
        if len(id_kelas) == 0:
            id_kelas = old_data[0][7]
        

        try:
            cur = db.cursor()
            sqlstr = f"update siswa set nama='{nama}', alamat='{alamat}', tmp_lahir='{tmp_lahir}', tgl_lahir='{tgl_lahir}', gender='{gender}', agama='{agama}', id_kelas={id_kelas} where nis={nis}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('siswa_bp.show_siswa'))


@siswa_bp.route('/delete_siswa/<int:nis>', methods=['GET', 'POST'])
def delete_siswa(nis):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM siswa where nis={nis}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('siswa_bp.show_siswa'))
