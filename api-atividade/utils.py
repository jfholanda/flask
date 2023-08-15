from models import Pessoas


def insere_pessoas(nome, idade):
    pessoa = Pessoas(nome=nome, idade=idade)
    pessoa.save()


def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)


def altera_pessoas(nome, novo_nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    pessoa.nome = novo_nome
    pessoa.save()


def exclui_pessoa(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    pessoa.delete()


if __name__ == '__main__':
    # insere_pessoas('Felipe', 21)
    consulta_pessoas()
