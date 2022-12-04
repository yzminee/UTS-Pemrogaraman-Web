from flask import Blueprint, jsonify, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
from database import get_mysql_connection


api = Blueprint('api', __name__,)


@api.route('/api/v1/guru/')
def api_guru():
    db = get_mysql_connection()
    result = {}
    result['results'] = []
    try:
        cur = db.cursor()
        sqlstr = "SELECT guru.id_guru, guru.nip, guru.nama, guru.alamat, guru.tmp_lahir, guru.tgl_lahir, guru.gender,guru.agama, guru.telp, guru.pendidikan, mapel.mapel FROM guru INNER JOIN relasi_mapel_guru ON relasi_mapel_guru.nip=guru.nip INNER JOIN mapel on mapel.id_mapel=relasi_mapel_guru.id_mapel"
        cur.execute(sqlstr)
        print('sukses')
        output_json = cur.fetchall()
        print(output_json)
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    for i in output_json:
        result['results'].append(
            {
                'id_guru': i[0],
                'nip': i[1],
                'nama': i[2],
                'alamat': i[3],
                'tmp_lahir': i[4],
                'tgl_lahir': i[5],
                'gender': i[6],
                'agama': i[7],
                'telp': i[8],
                'pendidikan': i[9],
                'status': i[10]
            }
        )
    return jsonify(result)
