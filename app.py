from flask import Flask, url_for, render_template, redirect
from orang_tua import orang_tua_bp
from guru import guru_bp
from kelas import kelas_bp
from siswa import siswa_bp
from mapel import mapel_bp
from mengajar import mengajar_bp
from pengguna import pengguna_bp

app = Flask(__name__)
app.register_blueprint(orang_tua_bp)
app.register_blueprint(guru_bp)
app.register_blueprint(kelas_bp)
app.register_blueprint(siswa_bp)
app.register_blueprint(mapel_bp)
app.register_blueprint(mengajar_bp)
app.register_blueprint(pengguna_bp)

app.secret_key = 'utsmimin'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login_form.html')


@app.route('/dashboard')
def dashboard():
    return redirect(url_for('guru_bp.show_guru'))


if __name__ == '__main__':
    app.run(debug=True)
