import sqlalchemy
from sqlalchemy import *
from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec
from models import *

app = Flask(__name__)
spec = FlaskPydanticSpec(app)


@app.route('/cadastrar_livro', methods=['POST'])
def cadastrar_livro():
    """
       API para cadastrar livro.

       ## Endpoint:
        /cadastrar_livro

       ## Respostas (JSON):
       ```json

       {
            "titulo":
            "autor",
            "isbn":,
            "resumo",
        }

       ## Erros possíveis (JSON):
        "O livro já está cadastrado", rertorna erro ***400
        Bad Request***:
            ```json
       """
    db_session = session_local()
    dados_livro = request.get_json()
    try:
        if (not "titulo" in dados_livro or not "autor" in dados_livro
                or not "isbn" in dados_livro or not "resumo" in dados_livro):
            return jsonify({
                "erro": "É obrigatório ter os campos: Título, autor, isbn, resumo"
            }), 400

        if (dados_livro["titulo"] == "" or dados_livro["autor"] == ""
                or dados_livro["isbn"] == "" or dados_livro["resumo"] == ""):
            return jsonify({
                "erro": "Preencher os campos em branco!!"
            }), 400


        titulo = dados_livro["titulo"]
        autor = dados_livro["autor"]
        isbn = dados_livro["isbn"]
        resumo = dados_livro["resumo"]

        titulo_existe = db_session.execute(select(Livro).where(Livro.titulo == titulo)).scalar()
        isbn_existe = db_session.execute(select(Livro).where(Livro.isbn == isbn)).scalar()

        if titulo_existe:
            return jsonify({
                "erro": "Já existe um livro com esse titulo!"
            }),400

        if isbn_existe:
            return jsonify({
                "erro": "Já existe um livro com esse ISBN!"
            }),400

        form_criar = Livro(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            resumo=resumo
        )

        form_criar.save(db_session)
        # db_session.close()

        return jsonify({
            "titulo": dados_livro["titulo"],
            "autor": dados_livro["autor"],
            "isbn": dados_livro["isbn"],
            "resumo": dados_livro["resumo"]
        })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Esse livro já está cadastrado!"
        }), 400

    except Exception as e:
        return jsonify({"erro": str(e)})
    finally:
        db_session.close()


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
           API para cadastrar usuário.

           ## Endpoint:
            /cadastrar_usuario

           ## Respostas (JSON):
           ```json

           {
                "id":
                "nome",
                "cpf":,
                "endereco",
            }

           ## Erros possíveis (JSON):
            "O usuário já está cadastrado", rertorna erro ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()
    dados_usuario = request.get_json()
    try:
        if (not "nome" in dados_usuario or not "cpf" in dados_usuario or not "endereco" in dados_usuario):
            return jsonify({
                "erro": "É obrigatório ter os campos: Nome, CPF, Endereco"
            }), 400

        if (dados_usuario["nome"] == "" or dados_usuario["cpf"] == "" or dados_usuario["endereco"] ==""):
            return jsonify({
                "erro": "Preencher os campos em branco!!"
            }), 400

        nome = dados_usuario["nome"]
        cpf = dados_usuario["cpf"]
        endereco = dados_usuario["endereco"]

        cpf_existe = db_session.execute(select(Usuario).where(Usuario.cpf == cpf)).scalar()

        if cpf_existe:
            return jsonify({
                "erro": "Este CPF já existe!"
            }), 400

        form_criar = Usuario(
            nome=nome,
            cpf=cpf,
            endereco=endereco
        )

        form_criar.save(db_session)
        # db_session.close()

        return jsonify({
            "id": form_criar.id,
            "nome": dados_usuario["nome"],
            "cpf": dados_usuario["cpf"],
            "endereco": dados_usuario["endereco"]
        }), 201

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Este usuário já está cadastrado!"
        }), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 404

    finally:
        db_session.close()


@app.route('/cadastrar_emprestimo', methods=['POST'])
def cadastrar_emprestimo():
    """
           API para cadastrar emprestimo.

           ## Endpoint:
            /cadastrar_emprestimo

           ## Respostas (JSON):
           ```json

           {
                "data_devolucao":
                "data_emprestimo",
                "livro":,
                "usuario":,
            }

           ## Erros possíveis (JSON):
            "Emprestimo já cadastrado", rertorna erro ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()
    dados_emprestimo = request.get_json()
    print(dados_emprestimo)
    # print(dados_emprestimo["livro_id"])
    try:
        if (not "livro_id" in dados_emprestimo or not "usuario_id" in dados_emprestimo
                or not "data_devolucao_prevista" in dados_emprestimo or not "data_emprestimo" in dados_emprestimo):
            return jsonify({
                "erro": "É obrigatório ter os campos: Livro, usuário, data_devolucao e data_emprestimo"
            }), 400

        if dados_emprestimo["livro_id"] == "" or dados_emprestimo["usuario_id"] == ""\
                or dados_emprestimo["data_devolucao_prevista"] == "" or dados_emprestimo["data_emprestimo"] == "":
            return jsonify({
                "erro": "Preencher os campos em branco!!"
            }), 400

        data_devolucao = dados_emprestimo["data_devolucao_prevista"]
        data_emprestimo = dados_emprestimo["data_emprestimo"]
        livro = dados_emprestimo["livro_id"]
        usuario = dados_emprestimo["usuario_id"]

        form_criar = Emprestimo(
            data_emprestimo=data_emprestimo,
            data_devolucao_prevista=data_devolucao,
            livro_id=int(livro),
            usuario_id=int(usuario)
        )


        form_criar.save(db_session)
        # db_session.close()

        return jsonify({
            "data_devolucao_prevista": dados_emprestimo["data_devolucao_prevista"],
            "data_emprestimo": dados_emprestimo["data_emprestimo"],
            "livro_id": dados_emprestimo["livro_id"],
            "usuario_id": dados_emprestimo["usuario_id"],
        }), 200

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Empréstimo já cadastrado!"
        }), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 404
    finally:
        db_session.close()


@app.route('/editar_livro/<int:id>', methods=['POST'])
def editar_livro(id):
    """
           API para editar informações do livro.

           ## Endpoint:
            /editar_livro/<int:id>

            ## Parâmetro:
            "id" **Id do livro**

           ## Respostas (JSON):
           ```json

           {
                "titulo":
                "autor",
                "isbn":,
                "resumo",
            }

           ## Erros possíveis (JSON):
            "O titulo deste livro já está cadastrado", rertorna erro ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()
    dados_editar_livro = request.get_json()
    try:
        livro_atualizado = db_session.execute(select(Livro).where(Livro.id == id)).scalar()

        if not livro_atualizado:
            return jsonify({
                "erro": "Livro não encontrado!"
            }), 404

        if (not "titulo" in dados_editar_livro or not "autor" in dados_editar_livro
                or not "isbn" in dados_editar_livro or not "resumo" in dados_editar_livro):
            return jsonify({
                "erro": "É obrigatório ter os campos: Título, autor, isbn, resumo"
            }), 400

        if (dados_editar_livro["titulo"] == "" or dados_editar_livro["autor"] == ""
                or dados_editar_livro["isbn"] == "" or dados_editar_livro["resumo"] == ""):
            return jsonify({
                "erro": "Preencher os campos em branco!!"
            }), 400

            livro_atualizado.titulo = dados_editar_livro["titulo"]
            livro_atualizado.autor = dados_editar_livro["autor"]
            livro_atualizado.isbn = dados_editar_livro["isbn"]
            livro_atualizado.resumo = dados_editar_livro["resumo"]

            livro_atualizado.save()
            # db_session.commit()

            return jsonify({
                "titulo": livro_atualizado.titulo,
                "autor": livro_atualizado.autor,
                "isbn": livro_atualizado.isbn,
                "resumo": livro_atualizado.resumo
            }), 201

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O título deste livro já está cadastrado!"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 404

    finally:
        db_session.close()



@app.route('/editar_usuario/<int:id>', methods=['POST'])
def editar_usuario(id):
    """
           API para editar dados do usuario.

           ## Endpoint:
            /editar_usuario/<int:id>

            ##Parâmetros:
            "id" **Id do usuario**

           ## Respostas (JSON):
           ```json

           {
                "nome":
                "cpf",
                "endereco":,
            }

           ## Erros possíveis (JSON):
            "O CPF deste usuário já está cadastrado", rertorna erro ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()
    dados_editar_usuario = request.get_json()
    try:
        usuario_atualizado = db_session.execute(select(Usuario).where(Usuario.id == id)).scalar()

        if not usuario_atualizado:
            return jsonify({
                "erro": "Usuário não encontrado!"
            })

        if (not "nome" in dados_editar_usuario or not "cpf" in dados_editar_usuario
                or not "endereco" in dados_editar_usuario):
            return jsonify({
                "erro": "É obrigatório ter os campos: Título, autor, isbn, resumo"
            }), 400

        if (dados_editar_usuario["nome"] == "" or dados_editar_usuario["cpf"] == ""
                or dados_editar_usuario["endereco"] == ""):
            return jsonify({
                "erro": "Preencher os campos em branco!!"
            }), 400

        cpf = dados_editar_usuario["cpf"].strip()
        if usuario_atualizado.cpf != cpf:
            cpf_existe = db_session.execute(select(Usuario).where(Usuario.cpf == cpf)).scalar()

            if cpf_existe:
                return jsonify({
                    "erro": "Este CPF já existe!"
                }), 400

        usuario_atualizado.nome = dados_editar_usuario["nome"]
        usuario_atualizado.cpf = dados_editar_usuario["cpf"].strip()
        usuario_atualizado.endereco = dados_editar_usuario["endereco"]

        usuario_atualizado.save()
        # db_session.commit()

        return jsonify({
            "nome": usuario_atualizado.nome,
            "cpf": usuario_atualizado.cpf,
            "endereco": usuario_atualizado.endereco,
        }), 201

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O CPF deste usuário já está cadastrado!"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()



@app.route('/get_usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    """
           API para buscar um usuário.

           ## Endpoint:
            /get_usuario/<int:id>

            ##Parâmetros:
            "id" **Id do usuario**

           ## Respostas (JSON):
           ```json

           {
                "id":
                "nome",
                "cpf":,
                "endereco",
            }

           ## Erros possíveis (JSON):
            "Usuário não encontrado ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()
    try:
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
    except ValueError:
        return jsonify({
            "error": "Não foi possível listar os dados!"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()


@app.route('/usuarios', methods=['GET'])
def usuarios():


    """
           API para listar usuários.

           ## Endpoint:
            /usuarios

           ## Respostas (JSON):
           ```json

           {
                "usuarios": lista_usuarios
            }

    """
    db_session = session_local()

    try:
        sql_usuarios = select(Usuario)
        resultado_usuarios = db_session.execute(sql_usuarios).scalars()
        lista_usuarios = []
        for usuario in resultado_usuarios:
            lista_usuarios.append(usuario.serialize_user())
        return jsonify({
            "usuarios": lista_usuarios
        })
    except ValueError:
        return jsonify({
            "error": "Não foi possível listar os usuários"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()


@app.route('/livros', methods=['GET'])
def livros():
    """
           API listar livros.

           ## Endpoint:
            /livros

           ## Respostas (JSON):
           ```json

        {
            "livros": lista_livros"
        }

        ## Erros possíveis (JSON):
        "Não foi possível listar os livros ***400
        Bad Request***:
            ```json
           """
    db_session = session_local()

    try:
        sql_livros = select(Livro)
        resultado_livros = db_session.execute(sql_livros).scalars()
        lista_livros = []
        for livro in resultado_livros:
            lista_livros.append(livro.serialize_user())
        return jsonify({
            "livros": lista_livros
        })
    except ValueError:
        return jsonify({
            "error": "Não foi possível listar os livros"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()

@app.route('/get_livro/<int:id>', methods=['GET'])
def get_livro(id):
    """
           API para verificar um livro.

           ## Endpoint:
            /get_livro/<int:id>

            ##Parâmetros:
            "id" **Id do livro**

           ## Respostas (JSON):
           ```json

        {
            "id":,
            "titulo":
            "autor",
            "isbn":,
            "resumo",
        }

        ## Erros possíveis (JSON):
            "Não foi possível listar os dados do livro ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()

    try:
        livro = db_session.execute(select(Livro).where(Livro.id == id)).scalar()

        if not livro:
            return jsonify({
                "error": "Livro não encontrado!"
            }), 400

        else:
            return jsonify({
                "id": livro.id,
                "titulo": livro.titulo,
                "autor": livro.autor,
                "isbn": livro.isbn,
                "resumo": livro.resumo
            }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possívl listar os dados do livro"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()

@app.route('/emprestimos_usuario/<id>', methods=['GET'])
def emprestimos_usuario(id):
    """
           API para listar emprestimos por usuários.

           ## Endpoint:
            /emprestimos_usuario/<int:id>

            ##Parâmetros:
            "id" **Id do usuário**

           ## Respostas (JSON):
           ```json

            {
                "usuario":
                "emprestimo",

            }

            ## Erros possíveis (JSON):
            "Não foi possível listar os dados deste emprestimo ***400
            Bad Request***:
                ```json
           """
    db_session = session_local()

    try:
        id_usuario = int(id)
        emprestimos_user = db_session.execute(select(Emprestimo).where(Emprestimo.usuario_id == id_usuario)).scalars().all()

        if not emprestimos_user:
            return jsonify({
                "error": "Este usuário não fez emprestimo!"
            }), 400

        else:
            emprestimos_livros = []
            for emprestimo in emprestimos_user:
                emprestimos_livros.append(emprestimo.serialize_user())
            #     livro = db_session.execute(select(Livro).where(Livro.id == emprestimo.livro_id)).scalars().all()
            #     emprestimos_livros.append(livro)
            return jsonify({
                'usuario': int(id_usuario),
                'emprestimos': emprestimos_livros,
            }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possível listar os dados do emprestimo"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()

@app.route('/status_livro', methods=['GET'])
def status_livro():
    """
           API para mostrar status de livro.

           ## Endpoint:
            /status_livro

           ## Respostas (JSON):
           ```json

           {
                "livros emprestados":
                "livros disponiveis",
            }

            ## Erros possíveis (JSON):
            "Não foi possível mostrar o status dos livros ***400
            Bad Request***:
                ```json
            """
    db_session = session_local()

    try:
        livro_emprestado = db_session.execute(
            select(Livro).where(Livro.id == Emprestimo.livro_id).distinct(Livro.isbn)).scalars()
        id_livro_emprestado = db_session.execute(
            select(Livro.id).where(Livro.id == Emprestimo.livro_id).distinct(Livro.isbn)).scalars()
        print("livro Emprestado",livro_emprestado)
        livros = db_session.execute(select(Livro)).scalars()

        print("Livros todos", livros)

        lista_emprestados = []
        lista_disponiveis = []
        for livro in livro_emprestado:
            lista_emprestados.append(livro.serialize_user())

        for book in livros:
            if book.id not in id_livro_emprestado:
                lista_disponiveis.append(book.serialize_user())

        print("resultados lista", lista_emprestados)
        print("resultados disponibiliza", lista_disponiveis)


        return jsonify({
            "livros emprestados": lista_emprestados,
            "livros disponiveis": lista_disponiveis

        }), 200

    except ValueError:
        return jsonify({
            "error": "não foi possível mostrar o status do livro"
        }), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()


spec.register(app)

if __name__ == '__main__':
    app.run(debug=True)
