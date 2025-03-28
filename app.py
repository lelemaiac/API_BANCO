import sqlalchemy
from sqlalchemy import *
from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec
from models import *

app = Flask(__name__)
spec = FlaskPydanticSpec(app)


@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastrar_livro():
    try:
        if request.method == 'POST':
            if (not request.form['form_titulo'] or not request.form['form_autor']
                    or not request.form['form_isbn'] or not request.form['form_resumo']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })
            else:
                titulo = request.form['form_titulo'].strip()
                autor = request.form['form_autor']
                isbn = request.form['form_isbn'].strip()
                resumo = request.form['form_resumo']

                titulo_existe = db_session.execute(select(Livro).where(Livro.titulo == titulo)).scalar()
                isbn_existe = db_session.execute(select(Livro).where(Livro.isbn == isbn)).scalar()

                if titulo_existe:
                    return jsonify({
                        "erro": "Já existe um livro com esse titulo!"
                    })

                if isbn_existe:
                    return jsonify({
                        "erro": "Já existe um livro com esse ISBN!"
                    })

                form_criar = Livro(
                    titulo=titulo,
                    autor=autor,
                    isbn=isbn,
                    resumo=resumo
                )

                form_criar.save()
                # db_session.close()

                return jsonify({
                    "titulo": form_criar.titulo,
                    "autor": form_criar.autor,
                    "isbn": form_criar.isbn,
                    "resumo": form_criar.resumo
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Esse livro já está cadastrado!"
        })


@app.route('/cadastrar_usuario', methods=['POST', 'GET'])
def cadastrar_usuario():
    try:
        if request.method == 'POST':
            if (not request.form['form_nome'] or not request.form['form_cpf']
                    or not request.form['form_endereco']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                nome = request.form['form_nome']
                cpf = request.form['form_cpf'].strip()
                endereco = request.form['form_endereco']

                cpf_existe = db_session.execute(select(Usuario).where(Usuario.cpf == cpf)).scalar()

                if cpf_existe:
                    return jsonify({
                        "erro": "Este CPF já existe!"
                    })

                form_criar = Usuario(
                    nome=nome,
                    cpf=cpf,
                    endereco=endereco
                )

                form_criar.save()
                # db_session.close()

                return jsonify({
                    "id": form_criar.id,
                    "nome": form_criar.nome,
                    "cpf": form_criar.cpf,
                    "endereco": form_criar.endereco
                }), 201

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Este usuário já está cadastrado!"
        }), 404


@app.route('/cadastrar_emprestimo', methods=['POST', 'GET'])
def cadastrar_emprestimo():
    try:
        if request.method == 'POST':
            if (not request.form['form_data_emprestimo'] or not request.form['form_data_devolucao']
                    or not request.form['form_livro'] or not request.form['form_usuario']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                data_devolucao = request.form['form_data_devolucao']
                data_emprestimo = request.form['form_data_emprestimo']
                livro = request.form['form_livro']
                usuario = request.form['form_usuario']

                form_criar = Emprestimo(
                    data_emprestimo=data_emprestimo,
                    data_devolucao_prevista=data_devolucao,
                    livro_id=int(livro),
                    usuario_id=int(usuario)
                )

                form_criar.save()
                # db_session.close()

                return jsonify({
                    "data_devolucao": form_criar.data_devolucao_prevista,
                    "data_emprestimo": form_criar.data_emprestimo,
                    "livro": form_criar.livro_id,
                    "usuario": form_criar.usuario_id
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Empréstimo já cadastrado!"
        })


@app.route('/editar_livro/<int:id>', methods=['POST'])
def editar_livro(id):
    try:
        livro_atualizado = db_session.execute(select(Livro).where(Livro.id == id)).scalar()

        if not livro_atualizado:
            return jsonify({
                "erro": "Livro não encontrado!"
            })

        if request.method == 'POST':
            if (not request.form['form_titulo'] and not request.form['form_autor']
                    and not request.form['form_isbn'] and not request.form['form_resumo']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                livro_atualizado.titulo = request.form['form_titulo']
                livro_atualizado.autor = request.form['form_autor']
                livro_atualizado.isbn = request.form['form_isbn']
                livro_atualizado.resumo = request.form['form_resumo']

                livro_atualizado.save()
                # db_session.commit()

                return jsonify({
                    "titulo": livro_atualizado.titulo,
                    "autor": livro_atualizado.autor,
                    "isbn": livro_atualizado.isbn,
                    "resumo": livro_atualizado.resumo
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O título deste livro já está cadastrado!"
        })


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    try:
        usuario_atualizado = db_session.execute(select(Usuario).where(Usuario.id == id)).scalar()

        if not usuario_atualizado:
            return jsonify({
                "erro": "Usuário não encontrado!"
            })

        if request.method == 'POST':
            if (not request.form['form_nome'] and not request.form['form_cpf']
                    and not request.form['form_endereco']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                cpf = request.form['form_cpf'].strip()
                if usuario_atualizado.cpf != cpf:
                    cpf_existe = db_session.execute(select(Usuario).where(Usuario.cpf == cpf)).scalar()

                    if cpf_existe:
                        return jsonify({
                            "erro": "Este CPF já existe!"
                        })

                usuario_atualizado.nome = request.form['form_nome']
                usuario_atualizado.cpf = request.form['form_cpf'].strip()
                usuario_atualizado.endereco = request.form['form_endereco']

                usuario_atualizado.save()
                # db_session.commit()

                return jsonify({
                    "nome": usuario_atualizado.nome,
                    "cpf": usuario_atualizado.cpf,
                    "endereco": usuario_atualizado.endereco,
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O CPF deste usuário já está cadastrado!"
        })


@app.route('/get_usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = db_session.execute(select(Usuario).where(Usuario.id == id)).scalar()

    if not usuario:
        return jsonify({
            "erro": "Usuário não encontrado!"
        })

    else:
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "endereco": usuario.endereco
        })


@app.route('/usuarios', methods=['GET'])
def usuarios():
    sql_usuarios = select(Usuario)
    resultado_usuarios = db_session.execute(sql_usuarios).scalars()
    lista_usuarios = []
    for usuario in resultado_usuarios:
        lista_usuarios.append(usuario.serialize_user())
    return jsonify({
        "usuarios": lista_usuarios
    })


@app.route('/livros', methods=['GET'])
def livros():
    sql_livros = select(Livro)
    resultado_livros = db_session.execute(sql_livros).scalars()
    lista_livros = []
    for livro in resultado_livros:
        lista_livros.append(livro.serialize_user())
    return jsonify({
        "livros": lista_livros
    })

@app.route('/get_livro/<int:id>', methods=['GET'])
def get_livro(id):
    livro = db_session.execute(select(Livro).where(Livro.id == id)).scalar()

    if not livro:
        return jsonify({
            "error": "Livro não encontrado!"
        })

    else:
        return jsonify({
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "isbn": livro.isbn,
            "resumo": livro.resumo
        })
@app.route('/emprestimos_usuario/<id>', methods=['GET'])
def emprestimos_usuario(id):
    id_usuario = int(id)
    emprestimos_user = db_session.execute(select(Emprestimo).where(Emprestimo.usuario_id == id_usuario)).scalars().all()

    if not emprestimos_user:
        return jsonify({
            "error": "Este usuário não fez emprestimo!"
        })

    else:
        emprestimos_livros = []
        for emprestimo in emprestimos_user:
            emprestimos_livros.append(emprestimo.serialize_user())
        #     livro = db_session.execute(select(Livro).where(Livro.id == emprestimo.livro_id)).scalars().all()
        #     emprestimos_livros.append(livro)
        return jsonify({
            'usuario': int(id_usuario),
            'emprestimos': emprestimos_livros,
        })

@app.route('/status_livro/<id>', methods=['GET'])
def status_livro(id):
    id_livro = int(id)
    resultado_emprestimos = db_session.execute(select(Emprestimo).where(Emprestimo.livro_id == id_livro)).fetchall()
    print("resultado", resultado_emprestimos)

    livro = db_session.execute(select(Livro).where(Livro.id == Emprestimo.livro_id)).scalars().all()
    print("resultadoss", livro)

    lista_livros = []
    for x in livro:
        lista_livros.append(x.serialize_user())

    if id_livro not in resultado_emprestimos:
        return jsonify({
            "status": "Este livro está disponível",
        })

    else:
        return jsonify({
            "livros emprestados": resultado_emprestimos
        })


spec.register(app)

if __name__ == '__main__':
    app.run(debug=True)
