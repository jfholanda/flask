from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Pessoas, Atividades, Usuarios


auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verificacao_login(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }

        return response
    

    def put(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json
            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome, 
                'idade': pessoa.idade
            }
        except Exception:
            response = {
                'status': 'error',
                'mensagem': 'Erro durante a requisição'
            }
        return response
    

    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            response = {
                    'status': 'sucesso',
                    'mensagem': f'Pessoa {nome} deletada com sucesso'
                }
        except AttributeError:
            response = {
                    'status': 'error',
                    'mensagem': f'Pessoa {nome} não existe'
                }
        return response
    

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': pessoa.id, 'nome': pessoa.nome, 'idade': pessoa.idade} for pessoa in pessoas]
        return response
    
    def post(self):
        dados = request.json
        try:
            pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
        except KeyError:
            response = {
                    'status': 'error',
                    'mensagem': 'Estão faltando campos necessários'
                }
        return response


class Atividade(Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            atividades = Atividades.query.filter_by(pessoa_id=pessoa.id)
            response = [{'id': atividade.id, 'nome': atividade.nome, 'pessoa': atividade.pessoa.nome} for atividade in atividades]
        except AttributeError:
            response = {
                    'status': 'error',
                    'mensagem': f'Pessoa {nome} não existe'
                }
        return response
    

class StatusAtividade(Resource):
    def put(self, id):
        dados = request.json
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            if 'status' in dados:
                atividade.status = dados['status']
                atividade.save()
            else:
                response = {
                    'status': 'erro', 'mensagem': 'Não há o campo status na requisição'
                }
        except AttributeError:
            response = {
                    'status': 'erro', 'mensagem': f'Atividade com ID {id} não existe'
                }
        return response
    
    def delete(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.delete()
            response = {
                    'status': 'sucesso', 'mensagem': f'Atividade de ID {id} deletada com sucesso'
                }
        except AttributeError:
            response = {
                    'status': 'erro', 'mensagem': f'Atividade com ID {id} não existe'
                }
        return response


class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'descricao': i.descricao, 'pessoa':i.pessoa.nome}  for i in atividades]
        return response


    def post(self):
        dados = request.json
        try:
            nome_pessoa = dados['pessoa']
            nome = dados['nome']
            descricao = dados['descricao']
            status = dados['status']
        except KeyError:
            response = {
                'status': 'error',
                'mensagem': 'Estão faltando campos necessários'
            }
        try:
            pessoa = Pessoas.query.filter_by(nome=nome_pessoa).first()
            atividade = Atividades(nome=nome, descricao=descricao, pessoa=pessoa, status=status)
            atividade.save()
            response = {
                'pessoa':atividade.pessoa.nome,
                'nome':atividade.nome,
                'descricao':atividade.descricao,
                'id':atividade.id
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': f'Pessoa com nome {nome_pessoa} não existe, portanto não é possível atrelar à atividade'
            }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(Atividade, '/atividades/<string:nome>')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(StatusAtividade, '/atividades/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)