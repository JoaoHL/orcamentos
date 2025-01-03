from math import *
import json

print("Olar!!!")

produtos = dict()
orcamentos = dict()

#####################################
#############  PRODUTOS #############
#####################################

def carregar_produtos():
    try:
        with open("produtos.db", "r") as file:
            for linha in file:    
                if len(linha) == 0:
                    print("Sem dados de produtos para carregar, continuando programa...\n")
                    return
                codigo, produto = linha.split(';')
                produtos[int(codigo)] = json.loads(produto)
    except FileNotFoundError:
        print("Criando banco de dados de produtos...\n")
        salvar_produtos()
        print("Banco de dados criado!\n")

def salvar_produtos():
    with open("produtos.db", "w") as file: ## zera arquivo
        for codigo,produto in produtos.items():
            file.write("{codigo};{produto}\n".format(codigo = codigo, produto = json.dumps(produto)))

def salvar_produto(codigo, produto):
    with open("produtos.db", "a") as file:    
        file.write("{codigo};{produto}\n".format(codigo = codigo, produto = json.dumps(produto)))

def lista_produtos():
    print("==============================================")
    for codigo, produto in produtos.items():
        print("Código: ", codigo)
        print("URL do produto (se houver): {url}".format(url=produto["url"]))
        print("Nome: ", produto["nome"])
        print("Quantidade: ", produto["qtd"])
        print("Preço: ", produto["preco"])
        print("==============================================")
    print()

def cria_produto():
    codigo_produto = len(produtos)
    nome_produto = input("Digite o nome do produto: ")
    url_produto = input("Digite a URL do produto, caso tenha: ")
    qtd_produto = float(input("Digite a quantidade do produto que vem por unidade comprada (ex.: m²/caixa de azulejo): ").replace(",", "."))
    preco_produto = float(input("Digite o preço do produto: ").replace(",", "."))
    
    produto = {"nome": nome_produto, "url": url_produto, "qtd": qtd_produto, "preco": preco_produto}
    produtos[codigo_produto] = produto

    print("Produto criado! Código de produto é", codigo_produto)

    salvar_produto(codigo_produto, produto)

def modifica_produto():
    codigo_produto = int(input("Digite o código do produto a ser modificado: "))
    if codigo_produto not in produtos:
        print("Não foi encontrado produto com esse código. Crie o produto antes de tentar modificá-lo.\n")
        return

    possible_name = input("Digite o novo nome do produto: ")
    possible_url = input("Digite a nova URL do produto: ")
    possible_qtd = input("Digite a nova quantidade de produto: ")
    possible_preco = input("Digite o novo preço do produto: ")

    produto = produtos[codigo_produto]
    if len(possible_name) > 0:
        produto["nome"] = possible_name
    if len(possible_url) > 0:
        produto["url"] = possible_url
    if len(possible_qtd) > 0:
        produto["qtd"] = float(possible_qtd)
    if len(possible_preco) > 0:
        produto["preco"] = float(possible_preco)

    salvar_produto(codigo_produto, produto)



#####################################
############# ORÇAMENTOS ############
#####################################

def carregar_orcamentos():
    try:
        with open("orcamentos.db", "r") as file:
            for linha in file:    
                if len(linha) == 0:
                    print("Sem dados de orçamentos para carregar, continuando programa...\n")
                    return
                codigo, orcamento = linha.split(';')
                orcamentos[int(codigo)] = json.loads(orcamento)
    except FileNotFoundError:
        print("Criando banco de dados de orçamentos...\n")
        salvar_orcamentos()
        print("Banco de dados criado!\n")

def salvar_orcamentos():
    with open("orcamentos.db", "w") as file: ## zera arquivo
        for codigo,orcamento in orcamentos.items():
            file.write("{codigo};{orcamento}\n".format(codigo = codigo, orcamento = json.dumps(orcamento)))

def salvar_orcamento(codigo):
    with open("orcamentos.db", "a") as file:    
        file.write("{codigo};{orcamento}\n".format(codigo = codigo, orcamento = json.dumps(orcamentos[codigo])))

def cria_orcamento():
    print("Para criar orçamento, serão pedidos os códigos dos produtos e as suas respectivas quantidades. Quer listar os produtos antes para verificação?")
    print("Digite '1' para confirmar a listagem de produtos")
    print("Digite '2' para seguir com o orçamento")
    option = input()

    if option == '1':
        lista_produtos()
    
    index = len(orcamentos)
    orcamentos[index] = {'estimativas': list(), 'custo_total': 0}
    while True:
        option = input("Para finalizar o orçamento, digite 'finalizar', senão apenas aperte Enter: ")
        if option.lower() == "finalizar":
            break
        else:
            codigo_produto = int(input("De qual produto você quer fazer orçamento? Digite o código: "))
            qtd_desejada = float(input("Qual a quantidade do produto que você precisa? "))
            adicional_de_seguranca = True if input("Deseja adicionar 10% a mais de produto por precauçao? Digite '1' para adicionar: ") == '1' else False
            produto = produtos[codigo_produto]
            qtd_desejada = qtd_desejada if adicional_de_seguranca is False else qtd_desejada * 1.1
            qtd_minima = ceil(qtd_desejada / produto["qtd"])
            custo = qtd_minima * produto["preco"]
            orcamentos[index]['custo_total'] += custo

            orcamentos[index]["estimativas"].append({"nome_produto": produto["nome"], "qtd_minima": qtd_minima, "custo": custo})
    
    print("-----------")
    print("Orçamento concluído. Resumo:")
    for estimativa in orcamentos[index]['estimativas']:
        print("Produto: {produto}".format(produto = estimativa['nome_produto']))
        print("Quantidade mínima necessária: {qtd}".format(qtd = estimativa['qtd_minima']))
        print("Custo: {custo}".format(custo = estimativa['custo']))
        print()
    print("Custo total do orçamento: {custo_total}".format(custo_total = orcamentos[index]['custo_total']))
    print("Código do orçamento: {codigo}".format(codigo=index))
    print("-----------")

    salvar_orcamento(index)

def lista_orcamentos():
    print("==============================================")
    for codigo, orcamento in orcamentos.items():
        print("Código: {codigo}".format(codigo=codigo))
        print("Custo total: {custo_total}".format(custo_total = orcamento['custo_total']))
        for estimativa in orcamento['estimativas']:
            print("Nome do produto: {nome_produto}".format(nome_produto = estimativa['nome_produto']))
            print("Quantidade mínima necessária: {qtd_minima}".format(qtd_minima = estimativa['qtd_minima']))
            print("Custo: {custo}".format(custo = estimativa['custo']))
            print()
        print("==============================================")
    print()
    

###################################################
################## UTILITÁRIOS ####################
###################################################

def interface():
    print("O que você gostaria de fazer?")
    print("1 - Criar um produto")
    print("2 - Modificar um produto")
    print("3 - Criar um orçamento")
    print("4 - Listar todos os produtos")
    print("5 - Listar todos os orçamentos")
    print("6 - Sair")

    option = int(input("Qual operação você quer fazer agora?\n"))
    if option == 1:
        cria_produto()
    elif option == 2:
        modifica_produto()
    elif option == 3:
        cria_orcamento()
    elif option == 4:
        lista_produtos()
    elif option == 5:
        lista_orcamentos()
    elif option == 6:
        print("Saindo...\n")
        sair()
    else:
        print("Opção inválida")


def sair():
    salvar_produtos()
    salvar_orcamentos()
    exit()






if __name__ == "__main__":
    carregar_produtos()
    carregar_orcamentos()
    while True:
        try:
            interface()
        except KeyboardInterrupt:
            print("Finalizando programa...\n")
            sair()
        except EOFError:
            print("Finalizando programa...\n")
            sair()


