from flask import render_template, redirect, request, session, flash
from login_register import app
from flask_bcrypt import Bcrypt
from login_register.models.log_reg import User
from login_register.models.recipe import Recipe

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('log_reg.html')

@app.route('/user_register', methods=['POST'])
def register():
    if not User.validation(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age'],
        'email': request.form['email'],
        'password':pw_hash
    }
    usuario_id = User.entry(data)
    # guardar id del usuario registrado en la sesion para hacerle seguimiento
    session ['usuario_id'] = usuario_id
    return redirect ('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    logged_user = User.validate_login(request.form)
    if not logged_user[0]:
        return redirect("/")
    session['usuario_id'] = logged_user[1].id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect("/")

    data = {
        'id':session['usuario_id']
    }
    user_in = User.get_user(data)
    todas_recetas_con_usuarios = Recipe.recetas_con_usuarios()
    return render_template('dashboard.html', user_in=user_in, todas_recetas_con_usuarios=todas_recetas_con_usuarios)

@app.route('/logout')
def clear_session():
    session.clear()
    return redirect('/')