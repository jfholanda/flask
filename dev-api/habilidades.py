from flask_restful import Resource, request
import json

lista_habilidades = ['Python', 'Java', 'Flask', 'PHP']
class Habilidades(Resource):
    def get(self, id):
        try:
            response = lista_habilidades[id]
        except IndexError:
            message = f'Habilidade de ID {id} não existe'
            response = {'status': 'erro', 'mensagem': message}
        
        return response

    def put(self, id):
        dados = json.loads(request.data)
        try:
            lista_habilidades[id] = dados['habilidades']
        except KeyError:
            message = f"O campo 'habilidades' não foi informado"
            response = {'status': 'erro', 'mensagem': message}
            return response
        
        return dados

    def delete(self, id):
        try:
            del lista_habilidades[id]
        except IndexError:
            message = f'Habilidade de ID {id} não existe'
            response = {'status': 'erro', 'mensagem': message}
            return response

        return {"status": "Sucesso", "mensagem": f"Desenvolvedor de ID {id} deletado com sucesso!"}

class ListaHabilidades(Resource):
    def get(self):
        return lista_habilidades
    
    def post(self):
        dados = json.loads(request.data)
        check_habilidades = [habilidade for habilidade in dados['habilidades'] if habilidade in lista_habilidades]
        if check_habilidades:    
            lista_habilidades.append(dados)
            return dados
        else:
            return {"status": "erro", "mensagem": "Há habilidades não existentes no nosso banco de dados. Cheque as habilidades existentes."}