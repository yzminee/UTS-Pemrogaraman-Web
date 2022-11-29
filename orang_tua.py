from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection

orang_tua_bp = Blueprint('orang_tua_bp', __name__,)


@orang_tua_bp.route('/show_orang_tua')
def show_orang_tua():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT * FROM orang_tua"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('orang_tua.html', data=output_json)


@orang_tua_bp.route('/create_orang_tua', methods=['GET', 'POST'])
def create_orang_tua():
    if request.method == 'POST':
        db = get_mysql_connection()

        nama = request.form['nama']
        alamat = request.form['alamat']
        telp = request.form['telp']
        pekerja = request.form['pekerjaan']
        agama = request.form['agama']
        status = request.form['status']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO orang_tua (nama, alamat, telp, pekerjaan, agama, status) VALUES('{nama}', '{alamat}', '{telp}', '{pekerja}', '{agama}', '{status}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('index'))
    return render_template('form_orang_tua.html')


@orang_tua_bp.route('/update_orang_tua/<int:kd_ortu>', methods=['GET', 'POST'])
def update_orang_tua(kd_ortu):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM orang_tua where kd_ortu = {kd_ortu}"
        cur.execute(sqlstr)
        print('sukses')
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'GET':
        return render_template('update_form_orang_tua.html', data=old_data)
    else:
        nama = request.form['nama']
        telpon = request.form['telpon']
        alamat = request.form['alamat']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        status = request.form['status']

        if len(nama) == 0:
            nama = old_data[0][1]
        if len(alamat) == 0:
            alamat = old_data[0][2]
        if len(telpon) == 0:
            telpon = old_data[0][3]
        if len(pekerjaan) == 0:
            pekerjaan = old_data[0][4]
        if len(agama) == 0:
            agama = old_data[0][5]
        if len(status) == 0:
            status = old_data[0][6]

        try:
            cur = db.cursor()
            sqlstr = f"update orang_tua set nama='{nama}', alamat='{alamat}', telp='{telpon}', pekerjaan='{pekerjaan}', agama='{agama}', status='{status}' where kd_ortu={kd_ortu}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('orang_tua_bp.show_orang_tua'))


@orang_tua_bp.route('/delete_orang_tua/<int:kd_ortu>', methods=['GET', 'POST'])
def delete_orang_tua(kd_ortu):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM orang_tua where kd_ortu={kd_ortu}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('orang_tua_bp.show_orang_tua'))
