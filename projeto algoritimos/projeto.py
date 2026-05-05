# Programa simples para gerenciar usuários e vídeos
# Usamos arquivos de texto para armazenar dados

# Nomes dos arquivos (assumindo que estão na mesma pasta do programa)
CAMINHO_USUARIOS = 'usuarios.txt'
CAMINHO_VIDEOS = 'videos.txt'

# Função para carregar usuários do arquivo.
# Formato salvo: usuario:senha|curtidas|favoritos
def carregar_usuarios():
    usuario = [] # Lista de nomes de usuários
    senha = [] # Lista de senhas
    curtidas = [] # Lista de curtidas (lista de listas)
    favoritos = [] # Lista de favoritos (lista de listas)
    
    try:
        arquivo = open(CAMINHO_USUARIOS, 'r')
        for linha in arquivo:
            if ':' in linha:
                linha = linha.strip() # Remove espaços extras
                
                # Divide em usuario:senha e dados
                partes = linha.split('|')
                nome_e_senha = partes[0]
                
                # Divide nome e senha
                pos = nome_e_senha.find(':')
                nome = nome_e_senha[0:pos]
                pass_word = nome_e_senha[pos+1:]
                
                usuario.append(nome)
                senha.append(pass_word)
                
                # Extrai curtidas
                curt = []
                if len(partes) > 1 and partes[1] != '':
                    curt_lista = partes[1].split(',')
                    for c in curt_lista:
                        if c != '':
                            curt.append(c)
                curtidas.append(curt)
                
                # Extrai favoritos
                fav = []
                if len(partes) > 2 and partes[2] != '':
                    fav_lista = partes[2].split(',')
                    for f in fav_lista:
                        if f != '':
                            fav.append(f)
                favoritos.append(fav)
        
        arquivo.close()
    except:
        # Se o arquivo não existe, começa vazio
        pass
    
    return usuario, senha, curtidas, favoritos

# Função para salvar usuários no arquivo.
def salvar_usuarios(usuario, senha, curtidas, favoritos):
    arquivo = open(CAMINHO_USUARIOS, 'w')
    
    i = 0
    while i < len(usuario):
        nome = usuario[i]
        pass_word = senha[i]
        
        # Junta as curtidas com vírgula
        curtidas_str = ''
        j = 0
        while j < len(curtidas[i]):
            if j > 0:
                curtidas_str = curtidas_str + ','
            curtidas_str = curtidas_str + curtidas[i][j]
            j = j + 1
        
        # Junta os favoritos com vírgula
        favoritos_str = ''
        j = 0
        while j < len(favoritos[i]):
            if j > 0:
                favoritos_str = favoritos_str + ','
            favoritos_str = favoritos_str + favoritos[i][j]
            j = j + 1
        
        # Escreve no arquivo
        linha = nome + ':' + pass_word + '|' + curtidas_str + '|' + favoritos_str + '\n'
        arquivo.write(linha)
        
        i = i + 1
    
    arquivo.close()

# Função para carregar vídeos do arquivo.
def carregar_videos():
    videos = []
    try:
        arquivo = open(CAMINHO_VIDEOS, 'r')
        for linha in arquivo:
            linha = linha.strip() # Remove espaços extras
            videos.append(linha)
        arquivo.close()
    except:
        # Se o arquivo não existe, começa vazio
        pass
    return videos

# Carregar dados iniciais.
usuario, senha, curtidas, favoritos = carregar_usuarios()
videos = carregar_videos()

# Função responsável pelo cadastro dos usuários.
def cadastro():
    print('\nCadastro de usuário')
    nome_cadastro = input('Nome do usuário: ')
    
    # Verifica se o usuário já existe
    existe = False
    for u in usuario:
        if u == nome_cadastro:
            existe = True
    
    if existe:
        print('Usuário já cadastrado.\n')
        return
    
    senha_cadastro = input('Defina sua senha: ')
    usuario.append(nome_cadastro)
    senha.append(senha_cadastro)
    curtidas.append([])
    favoritos.append([])
    salvar_usuarios(usuario, senha, curtidas, favoritos)
    print('Usuário ' + nome_cadastro + ' cadastrado com sucesso!\n')

# Função responsável pelo login dos usuários.
def login():
    print('\nLogin')
    nome_login = input('Nome do usuário: ')
    
    # Procura o usuário na lista
    indice = -1
    i = 0
    while i < len(usuario):
        if usuario[i] == nome_login:
            indice = i
        i = i + 1
    
    if indice == -1:
        print('Usuário não cadastrado.\n')
        return None
    
    senha_login = input('Senha: ')
    if senha[indice] == senha_login:
        print('Login realizado com sucesso!\n')
        return nome_login
    else:
        print('Senha inválida.\n')
    
    return None

# Função responsável por buscar os vídeos de acordo com o nome atribuido a eles.
def busca_video():
    print('\nBuscar Vídeo')
    pesquisa_video = input('Procurar: ')
    pesquisa_video = pesquisa_video.lower()
    
    encontrados = []
    for v in videos:
        v_lower = v.lower()
        if pesquisa_video in v_lower:
            encontrados.append(v)
    
    if len(encontrados) > 0:
        print('Vídeos encontrados:')
        for v in encontrados:
            print('- ' + v)
    else:
        print('Nenhum vídeo encontrado.')
    print()

# Função responsável por listar as infromações dos videos presentes no arquivo 'txt'.
def informacoes_videos():
    print('\nInformações sobre vídeos listados')
    if len(videos) > 0:
        print('Total de vídeos: ' + str(len(videos)))
        i = 1
        for v in videos:
            print(str(i) + '. ' + v)
            i = i + 1
    else:
        print('Nenhum vídeo cadastrado.')
    print()
# Função encarregada de permitir ao usuário curtir ou descurtir os videos presentes.
def curtir_video(usuario_logado):
    if usuario_logado == None:
        print('Você precisa estar logado para curtir vídeos.\n')
        return
    
    print('\nCurtir vídeo')
    informacoes_videos()
    nome_video = input('Nome do vídeo para curtir/descurtir: ')
    
    # Verifica se o vídeo existe
    video_existe = False
    nome_video_lower = nome_video.lower()
    for v in videos:
        v_lower = v.lower()
        if nome_video_lower in v_lower:
            video_existe = True
    
    if not video_existe:
        print('Vídeo não encontrado.\n')
        return
    
    # Encontra o índice do usuário logado
    indice_usuario = -1
    i = 0
    while i < len(usuario):
        if usuario[i] == usuario_logado:
            indice_usuario = i
        i = i + 1
    
    # Verifica se já foi curtido
    ja_curtiu = False
    pos = -1
    j = 0
    while j < len(curtidas[indice_usuario]):
        if curtidas[indice_usuario][j] == nome_video:
            ja_curtiu = True
            pos = j
        j = j + 1
    
    if ja_curtiu:
        # Remove a curtida
        curtidas[indice_usuario].pop(pos)
        print('Você removeu a curtida de: ' + nome_video + '\n')
    else:
        # Adiciona a curtida
        curtidas[indice_usuario].append(nome_video)
        print('Você curtiu: ' + nome_video + '\n')
    
    salvar_usuarios(usuario, senha, curtidas, favoritos)

# Função para o gerenciamento dos videos listados como favoritos pelo usuário.
def gerenciar_favoritos(usuario_logado):
    if usuario_logado == None:
        print('Você precisa estar logado para gerenciar favoritos.\n')
        return
    
    # Encontra o índice do usuário logado
    indice_usuario = -1
    i = 0
    while i < len(usuario):
        if usuario[i] == usuario_logado:
            indice_usuario = i
        i = i + 1
    
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
            nome_video = input('Nome do vídeo para adicionar aos favoritos: ')
            
            # Verifica se o vídeo existe
            video_existe = False
            nome_video_lower = nome_video.lower()
            for v in videos:
                v_lower = v.lower()
                if nome_video_lower in v_lower:
                    video_existe = True
            
            if not video_existe:
                print('Vídeo não encontrado.\n')
                continue
            
            # Verifica se já está nos favoritos
            ja_existe = False
            j = 0
            while j < len(favoritos[indice_usuario]):
                if favoritos[indice_usuario][j] == nome_video:
                    ja_existe = True
                j = j + 1
            
            if ja_existe:
                print(nome_video + ' já está nos favoritos.\n')
            else:
                favoritos[indice_usuario].append(nome_video)
                print(nome_video + ' adicionado aos favoritos!\n')
                salvar_usuarios(usuario, senha, curtidas, favoritos)
        
        # Remove o vídeo dos favoritos:
        elif opcao == '2':
            if len(favoritos[indice_usuario]) == 0:
                print('Você não tem vídeos nos favoritos.\n')
                continue
            
            print('Seus favoritos:')
            j = 1
            for v in favoritos[indice_usuario]:
                print(str(j) + '. ' + v)
                j = j + 1
            
            nome_video = input('Nome do vídeo para remover dos favoritos: ')
            
            # Procura o vídeo nos favoritos
            encontrou = False
            pos = -1
            j = 0
            while j < len(favoritos[indice_usuario]):
                if favoritos[indice_usuario][j] == nome_video:
                    encontrou = True
                    pos = j
                j = j + 1
            
            if encontrou:
                favoritos[indice_usuario].pop(pos)
                print(nome_video + ' removido dos favoritos!\n')
                salvar_usuarios(usuario, senha, curtidas, favoritos)
            else:
                print('Vídeo não encontrado nos favoritos.\n')
        
        # Mostra os videos salvos como favoritos, caso haja ao menos um:
        elif opcao == '3':
            if len(favoritos[indice_usuario]) == 0:
                print('Você não tem vídeos nos favoritos.\n')
            else:
                print('\nSeus favoritos (' + str(len(favoritos[indice_usuario])) + '):')
                j = 1
                for v in favoritos[indice_usuario]:
                    print(str(j) + '. ' + v)
                    j = j + 1
                print()
        
        # Menu principal
        elif opcao == '4':
            break
        
        else:
            print('Opção inválida.\n')

# Interface inicial do programa "FEItv".
print('FEItv')
usuario_logado = None
while True:
    # Tenta executar o programa da forma correta
    try:
        mensagem = '1- Cadastrar novo usuário\n2- Login de usuário\n3- Buscar vídeo por nome\n4- Informações sobre vídeos listados\n5- Curtir e descurtir vídeos\n6- Gerenciar favoritos\n7- Sair do programa\n----------------------------------------\nEscolha uma funcionalidade: '
        escolha = int(input(mensagem))
        
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
    
    # Caso um erro de valor ocorra:
    except ValueError:
        print('Entrada inválida. Por favor, digite um número.\n')