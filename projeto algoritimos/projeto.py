usuario = []
senha = []

#Função responsável pelo cadastro dos usuários.
def cadastro():
    print('\nCadastro de usuário')
    nome_cadastro = str(input('Nome do usuário: '))
    senha_cadastro = str(input('Defina sua senha: '))
    usuario.append(nome_cadastro)
    senha.append(senha_cadastro)
    print(f'Usuário {nome_cadastro} cadastrado com sucesso!\n')

#Função responsável pelo login dos usuários. Note que para que o login seja efetuado com sucesso, obviamente, deve haver um usuário válido, já registrado, tal como sua senha.
def login():
    print('\nLogin')
    nome_login = str(input('Nome do usuário: '))
    if nome_login not in usuario:
        print('Usuário não cadastrado.\n')
    else:
        senha_login = str(input('Senha: '))

        indice = usuario.index(nome_login)
        if senha[indice] == senha_login:
            print('Login realizado com sucesso!\n')
        else:
            print('Senha inválida.\n')


#Interface inicial do programa "FEItv".
print('FEItv')
while True:
    escolha = int(input('1- Cadastrar novo usuário\n2- Login de usuário\n3- Buscar vídeo por nome\n4- Listar informações de vídeos listados\n5- Curtir e descurtir vídeos\n6- Gerenciar favoritos\n7- Sair do programa\n----------------------------------------\nEscolha uma funcionalidade: '))
    if escolha == 1:
        cadastro()
    elif escolha == 2:
        login()