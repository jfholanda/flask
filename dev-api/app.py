from flask import Flask, jsonify, request
import json

app = Flask(__name__)

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

# devolve um desenvolvedor pelo id, altera e deleta um desenvolvedor
@app.route('/dev/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def desenvolvedor(id):
    if request.method == 'GET':
        try:
            response = desenvolvedores[id]
        except IndexError:
            message = f'Desenvolvedor de ID {id} não existe'
            response = {'status': 'erro', 'mensagem': message}
        except Exception:
            message = 'Erro desconhecido. Procure o administrador da API'
            response = {'status': 'erro', 'mensagem': message}
        
        return jsonify(response)
    
    elif request.method == 'PUT':
        dados = json.loads(request.data)
        desenvolvedores[id] = dados
        return jsonify(dados)
    
    elif request.method == 'DELETE':
        desenvolvedores.pop(id)
        return jsonify({"status": "Deletado com sucesso"})

# devolve todos os desenvolvedores e adiciona um novo desenvolvedor
@app.route('/dev/', methods=['GET', 'POST'])  
def lista_desenvolvedores():
    if request.method == 'POST':
        dados = json.loads(request.data)
        posicao = len(desenvolvedores)
        dados['id'] = posicao
        desenvolvedores.append(dados)
        return jsonify(desenvolvedores[posicao])
    elif request.method == 'GET':
        return jsonify(desenvolvedores)

if __name__ == '__main__':
    app.run(debug=True)