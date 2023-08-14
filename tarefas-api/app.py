from flask import Flask, jsonify, request
import json

app = Flask(__name__)

tarefas = [
    {
        'id': 0,
        'responsável': 'Jota',
        'tarefa': 'Criar API de Gerenciamento de Tarefas',
        'status': 'Em andamento'
    },
    {
        'id': 1,
        'responsável': 'Jota',
        'tarefa': 'Criar o método de exclusão de tarefas na API',
        'status': 'Pendente'
    }
]

campos_tarefa = ['responsável', 'tarefa', 'status']

@app.route('/tarefa/', methods=['GET', 'POST'])
def create_and_list():
    if request.method == 'GET':
        return jsonify(tarefas)
    
    elif request.method == 'POST':
        dados = json.loads(request.data)
        campos_ausentes = [campo for campo in campos_tarefa if campo not in dados]

        if not campos_ausentes:
            posicao = len(tarefas)
            dados['id'] = posicao
            tarefas.append(dados)
            return jsonify({'status': 'Sucesso', 'mensagem': 'Tarefa adicionada com sucesso!'})
        else:
            return jsonify({'status': 'erro', 'mensagem': f'Estão faltando os seguintes campos na tarefa: {campos_ausentes}'})
        
@app.route('/tarefa/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def view_edit_delete(id):
    if request.method == 'GET':
        try:
            response = tarefas[id]
        except IndexError:
            
            response = {'status': 'erro', 'mensagem': f'Tarefa de ID {id} não existe'}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'Erro desconhecido. Procure o administrador da API'}
        
        return jsonify(response)

    elif request.method == 'PUT':
        dados = json.loads(request.data)
        novo_status = dados['status']
        tarefas[id]['status'] = novo_status
        return jsonify({'status': 'Sucesso', 'mensagem': f'Você alterou com sucesso o status da tarefa ID {id} para {novo_status}'})

    elif request.method == 'DELETE':
        tarefas.pop(id)
        return jsonify({'status': 'Sucesso', 'mensagem': f'Você excluiu com sucesso a tarefa de ID {id}'})
    

if __name__ == '__main__':
    app.run(debug=True)




