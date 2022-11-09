from flask import render_template, redirect, request, session, flash
from login_register import app
from login_register.models.recipe import Recipe
from login_register.models.log_reg import User


@app.route('/crear_receta')
def formulario_receta():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/crear_receta', methods=['POST'])
def crear_receta():
    if not Recipe.validation(request.form):
        return render_template('new_recipe.html')
    receta_id = Recipe.crear_receta(request.form)
    return redirect("/dashboard")

@app.route('/recipe/edit/<int:receta_id>')
def editar_receta(receta_id):
    data ={ 
        "id": receta_id
    }
    receta=Recipe.get_one(data)
    return render_template('edit_recipe.html',receta=receta)

@app.route('/recipe/edit/<int:receta_id>',methods=['POST'])
def update(receta_id):
    if not Recipe.validate_edit(request.form):
        data ={ 
        "id": receta_id
    }
        receta=Recipe.get_one(data)
        return render_template('edit_recipe.html', receta=receta)
    data ={ 
        'id': 'receta_id'
    }
    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/recipe/destroy/<int:id>')
def delete(id):
    if 'usuario_id' not in session:
        return redirect('/')
    data ={
        'id': id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')

@app.route('/recipe/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    data_userid = {
        "id":session['usuario_id']
    }
    user_in = User.get_user(data_userid)
    receta_con_usuario = Recipe.receta_de_un_usuario(data)
    return render_template("show_recipe.html",receta=Recipe.get_one(data), receta_con_usuario=receta_con_usuario, user_in=user_in)

