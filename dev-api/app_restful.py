from flask import Flask, request
from flask_restful import Resource, Api
from habilidades import Habilidades, ListaHabilidades, lista_habilidades
import json

app = Flask(__name__)
api = Api(app)

desenvolvedores = [
    {
     'id': 0,
     'nome': 'Jota',
     'habilidades': ['Python', 'Data Science']
    },
    {
    'id': 1,
     'nome': 'Matheus',
     'habilidades': ['Javascript', 'React']
    }
]

class Desenvolvedor(Resource):
    def get(self, id):
        try:
            response = desenvolvedores[id]
        except IndexError:
            message = f'Desenvolvedor de ID {id} não existe'
            response = {'status': 'erro', 'mensagem': message}
        except Exception:
            message = 'Erro desconhecido. Procure o administrador da API'
            response = {'status': 'erro', 'mensagem': message}
        
        return response

    def put(self, id):
        dados = json.loads(request.data)
        desenvolvedores[id] = dados
        return dados
    
    def delete(self, id):
        try:
            desenvolvedores.pop(id)
        except IndexError:
            message = f'Desenvolvedor de ID {id} não existe'
            response = {'status': 'erro', 'mensagem': message}
            return response
        except Exception:
            message = 'Erro desconhecido. Procure o administrador da API'
            response = {'status': 'erro', 'mensagem': message}
            return response
        
        return {"status": "Sucesso", "mensagem": f"Desenvolvedor de ID {id} deletado com sucesso!"}

class ListaDesenvolvedores(Resource):
    def get(self):
        return desenvolvedores
    
    def post(self):
        dados = json.loads(request.data)
        check_habilidades = [habilidade for habilidade in dados['habilidades'] if habilidade in lista_habilidades]
        if check_habilidades:    
            posicao = len(desenvolvedores)
            dados['id'] = posicao
            desenvolvedores.append(dados)
            return desenvolvedores[posicao]
        else:
            return {"status": "erro", "mensagem": "Há habilidades não existentes no nosso banco de dados. Cheque as habilidades existentes."}

api.add_resource(Desenvolvedor, '/dev/<int:id>/')
api.add_resource(ListaDesenvolvedores, '/dev/')
api.add_resource(Habilidades, '/habilidades/<int:id>')
api.add_resource(ListaHabilidades, '/habilidades/')

if __name__ == '__main__':
    app.run(debug=True)