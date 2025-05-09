from sqlalchemy import create_engine, Integer,Column, String, ForeignKey, Float, Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base

from dotenv import load_dotenv
import os
import configparser

load_dotenv()
url_ = os.environ.get('DATABASE_URL')
print(f'modo1:{url_}')

config = configparser.ConfigParser()
config.read('config.ini')

database_url = config['database']['url']
print(f'modo2:{database_url}')


engine = create_engine(database_url)
#db_session = scoped_session(sessionmaker(bind=engine))
session_local = sessionmaker(bind=engine)

Base = declarative_base()
#Base.query = db_session.query_property()

class Livro(Base):
    __tablename__ = 'Livros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False, index=True, unique=True)
    autor = Column(String, nullable=False, index=True)
    isbn = Column(String, nullable=False, index=True, unique=True)
    resumo = Column(String, nullable=False, index=True)

    def __repr__(self):
        return '<Livro {}>'.format(self.titulo)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize_user(self):
        dados_livro = {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'resumo': self.resumo,

        }
        return dados_livro

class Usuario(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, index=True)
    cpf = Column(String, nullable=False, index=True, unique=True)
    endereco = Column(String, nullable=False, index=True)

    def __repr__(self):
        return '<Usuario {}>'.format(self.nome)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete_user(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize_user(self):
        dados_usuario = {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'endereco': self.endereco,
        }
        return dados_usuario

class Emprestimo(Base):
    __tablename__ = 'Emprestimos'
    id = Column(Integer, primary_key=True)
    data_emprestimo = Column(String, nullable=False, index=True)
    data_devolucao_prevista = Column(String, nullable=False, index=True)

    livro_id = Column(Integer, ForeignKey('Livros.id'))
    livros = relationship('Livro')

    usuario_id = Column(Integer, ForeignKey('Usuarios.id'))
    usuarios = relationship('Usuario')

    def __repr__(self):
        return '<Emprestimo {}>'.format(self.data_emprestimo)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize_user(self):
        dados_emprestimo = {
            'id': self.id,
            'data_emprestimo': self.data_emprestimo,
            'data_devolucao': self.data_devolucao_prevista,
            'livro_id': self.livro_id,
            'usuario_id': self.usuario_id,
        }

        return dados_emprestimo

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()