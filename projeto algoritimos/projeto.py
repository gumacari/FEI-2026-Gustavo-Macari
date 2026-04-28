# Importa o módulo 'os', permitindo que o código interaja com o sistema operacional, verificando a existência dos arquivos txt responsaveis para o funcionamento ideal do código.
import os # OS = Operational System (Sistema Operacional)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_USUARIOS = os.path.join(BASE_DIR, 'usuarios.txt')
CAMINHO_VIDEOS = os.path.join(BASE_DIR, 'videos.txt')

# Função para carregar usuários do arquivo.
# Formato: usuario:senha|curtidas(separadas por vírgula)|favoritos(separados por vírgula)
def carregar_usuarios():
    usuario = []
    senha = []
    dados_usuario = {}  # Dict para guardar curtidas e favoritos
    if os.path.exists(CAMINHO_USUARIOS):
        with open(CAMINHO_USUARIOS, 'r') as f:
            for line in f:
                if ':' in line:
                    partes = line.strip().split('|')
                    u, s = partes[0].split(':', 1)
                    usuario.append(u) # Adiciona um novo usuário
                    senha.append(s) # Adiciona a senha referente ao usuário
                    
                    # Extrai curtidas e favoritos se existirem
                    curtidas_lista = partes[1].split(',') if len(partes) > 1 and partes[1] else []
                    favoritos_lista = partes[2].split(',') if len(partes) > 2 and partes[2] else []
                    dados_usuario[u] = {
                        'curtidas': [c for c in curtidas_lista if c],
                        'favoritos': [f for f in favoritos_lista if f]
                    }
    return usuario, senha, dados_usuario

# Função para salvar usuários no arquivo.
def salvar_usuarios(usuario, senha, dados_usuario):
    with open(CAMINHO_USUARIOS, 'w') as f:
        for u, s in zip(usuario, senha):
            curtidas = ','.join(dados_usuario.get(u, {}).get('curtidas', []))
            favoritos = ','.join(dados_usuario.get(u, {}).get('favoritos', []))
            f.write(f'{u}:{s}|{curtidas}|{favoritos}\n')

# Função para carregar vídeos do arquivo.
def carregar_videos():
    videos = []
    if os.path.exists(CAMINHO_VIDEOS):
        with open(CAMINHO_VIDEOS, 'r') as f:
            videos = [line.strip() for line in f]
    return videos

# Carregar dados iniciais.
usuario, senha, dados_usuario = carregar_usuarios()
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
    dados_usuario[nome_cadastro] = {'curtidas': [], 'favoritos': []}
    salvar_usuarios(usuario, senha, dados_usuario)
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

# Função responsável por listar as infromações dos videos presentes no arquivo 'txt'.
def informacoes_videos():
    print('\nInformações sobre vídeos listados')
    if videos:
        print(f'Total de vídeos: {len(videos)}')
        for i, v in enumerate(videos, 1):
            print(f'{i}. {v}')
    else:
        print('Nenhum vídeo cadastrado.')
    print()
# Função encarregada de permitir ao usuário curtir ou descurtir os videos presentes.
def curtir_video(usuario_logado):
    if not usuario_logado:
        print('Você precisa estar logado para curtir vídeos.\n')
        return
    
    print('\nCurtir vídeo')
    informacoes_videos()
    nome_video = str(input('Nome do vídeo para curtir/descurtir: '))
    
    # Verifica se o vídeo existe
    video_existe = any(nome_video.lower() in v.lower() for v in videos)
    
    if not video_existe:
        print('Vídeo não encontrado.\n')
        return
    
    # Verifica se já foi curtido
    if nome_video in dados_usuario[usuario_logado]['curtidas']:
        dados_usuario[usuario_logado]['curtidas'].remove(nome_video)
        print(f'Você removeu a curtida de: {nome_video}\n')
    else:
        dados_usuario[usuario_logado]['curtidas'].append(nome_video)
        print(f'Você curtiu: {nome_video}\n')
    
    salvar_usuarios(usuario, senha, dados_usuario)

# Função para o gerenciamento dos videos listados como favoritos pelo usuário.
def gerenciar_favoritos(usuario_logado):
    if not usuario_logado:
        print('Você precisa estar logado para gerenciar favoritos.\n')
        return
    
    print('\nGerenciar favoritos')
    
    while True:
        print('\n1- Adicionar vídeo aos favoritos')
        print('2- Remover vídeo dos favoritos')
        print('3- Visualizar favoritos')
        print('4- Voltar ao menu principal')
        opcao = input('Escolha uma opção: ')
        
        # Adiciona o vídeo aos favoritos:
        if opcao == '1':
            informacoes_videos()
            nome_video = str(input('Nome do vídeo para adicionar aos favoritos: '))
            
            video_existe = any(nome_video.lower() in v.lower() for v in videos)
            
            if not video_existe:
                print('Vídeo não encontrado.\n')
                continue
            
            if nome_video in dados_usuario[usuario_logado]['favoritos']:
                print(f'{nome_video} já está nos favoritos.\n')
            else:
                dados_usuario[usuario_logado]['favoritos'].append(nome_video)
                print(f'{nome_video} adicionado aos favoritos!\n')
                salvar_usuarios(usuario, senha, dados_usuario)
        
        # Remove o vídeo dos favoritos:
        elif opcao == '2':
            if not dados_usuario[usuario_logado]['favoritos']:
                print('Você não tem vídeos nos favoritos.\n')
                continue
            
            print('Seus favoritos:')
            for i, v in enumerate(dados_usuario[usuario_logado]['favoritos'], 1):
                print(f'{i}. {v}')
            
            nome_video = str(input('Nome do vídeo para remover dos favoritos: '))
            
            if nome_video in dados_usuario[usuario_logado]['favoritos']:
                dados_usuario[usuario_logado]['favoritos'].remove(nome_video)
                print(f'{nome_video} removido dos favoritos!\n')
                salvar_usuarios(usuario, senha, dados_usuario)
            else:
                print('Vídeo não encontrado nos favoritos.\n')
        
        # Mostra os videos salvos como favoritos, caso haja ao menos um:
        elif opcao == '3':
            if not dados_usuario[usuario_logado]['favoritos']:
                print('Você não tem vídeos nos favoritos.\n')
            else:
                print(f'\nSeus favoritos ({len(dados_usuario[usuario_logado]["favoritos"])}):')
                for i, v in enumerate(dados_usuario[usuario_logado]['favoritos'], 1):
                    print(f'{i}. {v}')
                print()
        
        # Menu principal:
        elif opcao == '4':
            break
        
        else:
            print('Opção inválida.\n')

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
            curtir_video(usuario_logado)
        elif escolha == 6:
            gerenciar_favoritos(usuario_logado)
        elif escolha == 7:
            print('Saindo do programa...')
            break
        else:
            print('Opção inválida.\n')

    #Caso um erro de valor ocorra:
    except ValueError:
        print('Entrada inválida. Por favor, digite um número.\n')