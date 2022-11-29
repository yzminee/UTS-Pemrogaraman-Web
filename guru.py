from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection

guru_bp = Blueprint('guru_bp', __name__,)


@guru_bp.route('/show_guru')
def show_guru():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = "SELECT guru.nip, guru.nama, guru.alamat, guru.tmp_lahir, guru.tgl_lahir, guru.gender,guru.agama, guru.telp, guru.pendidikan, mapel.mapel FROM guru INNER JOIN relasi_mapel_guru ON relasi_mapel_guru.nip=guru.nip INNER JOIN mapel on mapel.id_mapel=relasi_mapel_guru.id_mapel"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('guru.html', data=output_json)


@guru_bp.route('/create_guru', methods=['GET', 'POST'])
def create_guru():
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * from mapel"
        cur.execute(sqlstr)
        mapel = cur.fetchall()
        cur.close()
        print('sukses')
        # output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'POST':
        nama = request.form['nama']
        nip = request.form['nip']
        alamat = request.form['alamat']
        tmp_lahir = request.form['tmp_lahir']
        tgl_lahir = request.form['tgl_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        telp = request.form['telp']
        pendidikan = request.form['pendidikan']
        status = request.form['status']
        mapel = request.form.getlist('mapel')

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO guru (nama, nip, alamat, tmp_lahir, tgl_lahir, gender, agama, telp, pendidikan, status) VALUES('{nama}', {nip}, '{alamat}', '{tmp_lahir}', '{tgl_lahir}', '{gender}', '{agama}', '{telp}', '{pendidikan}', '{status}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)

        for i in mapel:
            try:
                cur = db.cursor()
                sqlstr = f"insert into relasi_mapel_guru (id_mapel, nip) VALUES('{i}', {nip})"
                cur.execute(sqlstr)
                db.commit()
                cur.close()
                print('sukses')
                # output_json = cur.fetchall()
            except Exception as e:
                print("Error in SQL:\n", e)

        db.close()
        return redirect(url_for('guru_bp.show_guru'))
    return render_template('form_guru.html', mapel=mapel)


@guru_bp.route('/update_guru/<int:nip>', methods=['GET', 'POST'])
def update_guru(nip):
    db = get_mysql_connection()

    try:
        cur = db.cursor()
        sqlstr = f"SELECT * from mapel"
        cur.execute(sqlstr)
        mapel = cur.fetchall()
        cur.close()
        print('sukses')
        # output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    try:
        cur = db.cursor()
        sqlstr = f"SELECT id_mapel from relasi_mapel_guru where nip={nip}"
        cur.execute(sqlstr)
        relasi_mapel = cur.fetchall()
        joined_relasi_mapel = []
        cur.close()
        print('sukses')
        # output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    print(relasi_mapel)
    for i in relasi_mapel:
        joined_relasi_mapel.append(i[0])
    print(joined_relasi_mapel)
    try:
        cur = db.cursor()
        sqlstr = f"SELECT * FROM guru where nip = {nip}"
        cur.execute(sqlstr)
        print('sukses')
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'GET':
        return render_template('update_form_guru.html', data=old_data, mapels=mapel, relasi_mapels=joined_relasi_mapel)
    else:
        nama = request.form['nama']
        kd_nip = request.form['nip']
        telpon = request.form['telp']
        alamat = request.form['alamat']
        pendidikan = request.form['pendidikan']
        agama = request.form['agama']
        status = request.form['status']
        tmp_lahir = request.form['tmp_lahir']
        tgl_lahir = request.form['tgl_lahir']
        gender = request.form['gender']
        mapel = request.form.getlist('mapel')

        if len(nama) == 0:
            nama = old_data[0][2]
        if len(kd_nip) == 0:
            kd_nip = old_data[0][1]
        if len(alamat) == 0:
            alamat = old_data[0][3]
        if len(telpon) == 0:
            telpon = old_data[0][8]
        if len(pendidikan) == 0:
            pendidikan = old_data[0][9]
        if len(agama) == 0:
            agama = old_data[0][7]
        if len(status) == 0:
            status = old_data[0][10]
        if len(tmp_lahir) == 0:
            tmp_lahir = old_data[4]
        if len(tgl_lahir) == 0:
            tgl_lahir = old_data[0][5]
        if len(gender) == 0:
            gender = old_data[0][6]
        if len(mapel) == 0:
            mapel = joined_relasi_mapel

        try:
            cur = db.cursor()
            sqlstr = f"update guru set nip={kd_nip}, nama='{nama}', alamat='{alamat}', telp='{telpon}', pendidikan='{pendidikan}', agama='{agama}', status='{status}', tgl_lahir='{tgl_lahir}', tmp_lahir='{tmp_lahir}', gender='{gender}' where nip={nip}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        try:
            cur = db.cursor()
            sqlstr = f"delete from relasi_mapel_guru where nip = {nip}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        for i in mapel:
            try:
                cur = db.cursor()
                sqlstr = f"INSERT INTO relasi_mapel_guru (id_mapel, nip) VALUES({i}, {kd_nip})"
                cur.execute(sqlstr)
                db.commit()
                print('sukses')
                cur.close()
            except Exception as e:
                print("Error in SQL:\n", e)
        db.close()
        return redirect(url_for('guru_bp.show_guru'))


@guru_bp.route('/delete_guru/<int:nip>', methods=['GET', 'POST'])
def delete_guru(nip):
    db = get_mysql_connection()
    try:
        cur = db.cursor()
        sqlstr = f"delete FROM guru where nip={nip}"
        cur.execute(sqlstr)
        db.commit()
        print('sukses')
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('guru_bp.show_guru'))
