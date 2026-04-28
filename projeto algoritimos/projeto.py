#Importa o módulo 'os', permitindo que o código interaja com o sistema operacional, verificando a existência dos arquivos txt responsaveis para o funcionamento ideal do código.
import os
print("Executando em:", os.getcwd())

# Função para carregar usuários do arquivo.
def carregar_usuarios():
    usuario = []
    senha = []
    if os.path.exists('usuarios.txt'):
        with open('usuarios.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    u, s = line.strip().split(':', 1)
                    usuario.append(u)
                    senha.append(s)
    return usuario, senha

# Função para salvar usuários no arquivo. 
def salvar_usuarios(usuario, senha):
    with open('usuarios.txt', 'w') as f:
        for u, s in zip(usuario, senha):
            f.write(f'{u}:{s}\n')

# Função para carregar vídeos do arquivo.
def carregar_videos():
    videos = []
    if os.path.exists('videos.txt'):
        with open('videos.txt', 'r') as f:
            videos = [line.strip() for line in f]
    return videos

# Carregar dados iniciais.
usuario, senha = carregar_usuarios()
videos = carregar_videos()

# Função responsável pelo cadastro dos usuários.
def cadastro():
    print('\nCadastro de usuário')
    nome_cadastro = str(input('Nome do usuário: '))
    if nome_cadastro in usuario:
        print('Usuário já cadastrado.\n')
        return
    senha_cadastro = str(input('Defina sua senha: '))
    usuario.append(nome_cadastro)
    senha.append(senha_cadastro)
    salvar_usuarios(usuario, senha)
    print(f'Usuário {nome_cadastro} cadastrado com sucesso!\n')

# Função responsável pelo login dos usuários.
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
            return nome_login  # Retornar o usuário logado para progresso.
        else:
            print('Senha inválida.\n')
    return None

# Função responsável por buscar os vídeos de acordo com o nome atribuido a eles.
def busca_video():
    print('\nBuscar Vídeo')
    pesquisa_video = str(input('Procurar: '))
    encontrados = [v for v in videos if pesquisa_video.lower() in v.lower()]
    if encontrados:
        print('Vídeos encontrados:')
        for v in encontrados:
            print(f'- {v}')
    else:
        print('Nenhum vídeo encontrado.')
    print()

# Outras funções (implementações simples para salvar progresso)
def informacoes_videos():
    print('\nInformações sobre vídeos listados')
    if videos:
        print(f'Total de vídeos: {len(videos)}')
        for i, v in enumerate(videos, 1):
            print(f'{i}. {v}')
    else:
        print('Nenhum vídeo cadastrado.')
    print()

def curtir_video():
    print('\nCurtir vídeo')
    # Simples, apenas imprimir
    print('Funcionalidade não implementada ainda.\n')

def gerenciar_favoritos():
    print('\nGerenciar favoritos')
    # Simples, apenas imprimir
    print('Funcionalidade não implementada ainda.\n')

# Interface inicial do programa "FEItv".
print('FEItv')
usuario_logado = None
while True:

    #Tentara executar o programa da forma correta, como feito para ser executado.
    try:
        escolha = int(input('1- Cadastrar novo usuário\n2- Login de usuário\n3- Buscar vídeo por nome\n4- Informações sobre vídeos listados\n5- Curtir e descurtir vídeos\n6- Gerenciar favoritos\n7- Sair do programa\n----------------------------------------\nEscolha uma funcionalidade: '))
        if escolha == 1:
            cadastro()
        elif escolha == 2:
            usuario_logado = login()
        elif escolha == 3:
            busca_video()
        elif escolha == 4:
            informacoes_videos()
        elif escolha == 5:
            curtir_video()
        elif escolha == 6:
            gerenciar_favoritos()
        elif escolha == 7:
            print('Saindo do programa...')
            break
        else:
            print('Opção inválida.\n')

    #Caso um erro de valor ocorra:
    except ValueError:
        print('Entrada inválida. Por favor, digite um número.\n')
