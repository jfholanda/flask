from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades


app = Flask(__name__)
api = Api(app)


class Pessoa(Resource):
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
        atividade = Atividades.query.filter_by(id=id).first()
        if 'status' in dados:
            atividade.status = dados['status']
            atividade.save()
        else:
            response = {
                'status': 'erro', 'mensagem': 'Não há o campo status na requisição'
            }
            return response
        return atividade


class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome}  for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response
    
# class StatusAtividades(Resource)

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(Atividade, '/atividades/<string:nome>')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(StatusAtividade, '/atividades/status/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)