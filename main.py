from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import Contato
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@app.route('/')
def home():
    try:
        contatos = db.session.query(Contato).all()
        return render_template('home.html', contatos=contatos)
    except Exception as e:
        db.session.rollback()
        return f'Erro ao carregar a página incial {e}', 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['NomeForm']
        telefone = request.form['TelefoneForm']

    try:
        novo_contato = Contato(nome=nome, telefone=telefone)
        db.session.add(novo_contato)
        db.session.commit()

        return redirect(url_for('home'))
    
    except SQLAlchemyError as e:
        db.session.rollback() 
        return f"Erro de banco de dados no Commit: {str(e)}", 500
    except Exception as e:
        return f"Outro erro ocorreu: {str(e)}", 500


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit(id):
    try:
        contato = db.session.query(Contato).filter_by(id=id).first()
        if request.method == 'GET':
            return render_template('edit.html', contato=contato)
        elif request.method == 'POST':
            nome = request.form['NomeForm']
            telefone = request.form['TelefoneForm']

            contato.nome = nome
            contato.telefone = telefone
            db.session.commit()
            return redirect(url_for('home'))

    except Exception as e:
        db.session.rollback()
        return f"Erro de banco de dados no Commit: {str(e)}", 500


@app.route("/deletar/<int:id>")
def delete(id):
    try:
        contato = db.session.query(Contato).filter_by(id=id).first()
        db.session.delete(contato)
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        return f"Erro de banco de dados no Commit: {str(e)}", 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
 
    app.run(debug=True)