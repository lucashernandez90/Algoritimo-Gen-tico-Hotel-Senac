import random

# Definição dos funcionários e suas habilidades
funcionarios = {
    'João': ['Recepção', 'Limpeza de Quartos'],
    'Maria': ['Cozinha', 'Serviço de Quarto', 'Bar'],
    'Ana': ['Recepção', 'Lavanderia'],
    'Carlos': ['Limpeza de Quartos', 'Manutenção'],
    'Bruno': ['Cozinha', 'Serviço de Quarto'],
    'Paula': ['Recepção', 'Limpeza de Quartos', 'Bar'],
    'Pedro': ['Manutenção', 'Limpeza de Quartos'],
    'Luiza': ['Lavanderia', 'Limpeza de Quartos'],
    'Thiago': ['Cozinha', 'Bar'],
    'Fernanda': ['Recepção', 'Lavanderia', 'Serviço de Quarto'],
    'Rafael': ['Cozinha', 'Serviço de Quarto', 'Bar'],
    'Juliana': ['Recepção', 'Limpeza de Quartos'],
    'Caio': ['Manutenção', 'Limpeza de Quartos'],
    'Beatriz': ['Recepção', 'Limpeza de Quartos', 'Serviço de Quarto'],
    'Lucas': ['Manutenção', 'Limpeza de Quartos', 'Bar'],
    'Bruna': ['Cozinha', 'Serviço de Quarto'],
    'Marcelo': ['Recepção', 'Limpeza de Quartos', 'Lavanderia'],
    'Vanessa': ['Cozinha', 'Bar'],
    'Danilo': ['Manutenção', 'Limpeza de Quartos'],
    'Renata': ['Recepção', 'Serviço de Quarto', 'Bar']
}

# Duração total em horas
duracao_total = 24

# Duração de cada turno em horas
duracao_turno = 8

# Número de turnos
num_turnos = duracao_total // duracao_turno

# Turnos de trabalho
turnos = [f"Turno {i}" for i in range(1, num_turnos + 1)]

# Função de fitness
def fitness(individuo):
    # Pontuação inicial
    pontuacao = 0

    # Verifica se cada habilidade é atendida em cada turno
    for turno in turnos:
        habilidades_necessarias = set()  # Habilidades necessárias para este turno
        for funcionario, habilidades in individuo.items():
            if turno in habilidades:
                habilidades_necessarias |= set(habilidades)
        if len(habilidades_necessarias) == 0:
            pontuacao -= 1  # Penaliza turnos sem funcionários com habilidades necessárias
        else:
            pontuacao += len(habilidades_necessarias)  # Adiciona pontuação por cada habilidade atendida

    return pontuacao

# Função de criação de indivíduos aleatórios
def criar_individuo():
    individuo = {}
    habilidades_disponiveis = list(funcionarios.values())
    turnos_habilidades = {turno: random.choice(habilidades_disponiveis) for turno in turnos}

    for turno, habilidades in turnos_habilidades.items():
        funcionarios_disponiveis = [funcionario for funcionario, habilidades_funcionario in funcionarios.items() if any(habilidade in habilidades_funcionario for habilidade in habilidades)]
        num_funcionarios_necessarios = max(1, len(habilidades))  # Pelo menos uma pessoa, mas mais se necessário
        funcionarios_selecionados = random.sample(funcionarios_disponiveis, num_funcionarios_necessarios)
        individuo[turno] = funcionarios_selecionados

    return individuo

# Função para garantir que cada turno tenha pelo menos um funcionário alocado
def garantir_funcionario(turno, individuo):
    if not individuo[turno]:
        individuo[turno] = [random.choice(list(funcionarios.keys()))]

# Função para garantir que cada funcionário não trabalhe em mais de dois turnos consecutivos
def garantir_descanso(individuo):
    for i in range(len(turnos) - 2):
        funcionarios_turno_atual = set(individuo[turnos[i]])
        funcionarios_proximo_turno = set(individuo[turnos[i + 1]])
        funcionarios_proximo_proximo_turno = set(individuo[turnos[i + 2]])

        funcionarios_consecutivos = funcionarios_turno_atual.intersection(funcionarios_proximo_turno, funcionarios_proximo_proximo_turno)

        for funcionario in funcionarios_consecutivos:
            funcionarios_disponiveis = set(funcionarios.keys()) - funcionarios_proximo_turno - funcionarios_proximo_proximo_turno

            # Remove o funcionário atual da lista de disponíveis para evitar repetições excessivas
            funcionarios_disponiveis.discard(funcionario)

            if funcionarios_disponiveis:
                novo_funcionario = random.choice(list(funcionarios_disponiveis))
                # Se o novo funcionário já estiver nos próximos dois turnos, selecionamos outro
                while any(novo_funcionario in individuo[turno] for turno in turnos[i+1:i+3]):
                    novo_funcionario = random.choice(list(funcionarios_disponiveis))
                individuo[turnos[i + 1]].remove(funcionario)
                individuo[turnos[i + 1]].append(novo_funcionario)
                break
            else:
                # Se não houver funcionários disponíveis, tentamos remover um dos funcionários do próximo turno
                funcionario_a_remover = random.choice(list(funcionarios_proximo_turno))
                individuo[turnos[i + 1]].remove(funcionario_a_remover)
                break  # Sai do loop após realizar a troca

# Função de seleção de pais
def selecionar_pais(populacao):
    return random.choices(populacao, weights=[fitness(individuo) for individuo in populacao], k=2)

# Função de crossover
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(turnos) - 1)
    filho = {}
    for i, turno in enumerate(turnos):
        if i < ponto_corte:
            filho[turno] = pai1[turno]
        else:
            filho[turno] = pai2[turno]
    return filho

# Função de mutação
def mutacao(individuo):
    for turno in turnos:
        if random.random() < 0.1:  # Probabilidade de mutação de 10%
            individuo[turno] = random.sample(funcionarios.keys(), random.randint(1, len(funcionarios)))
    return individuo

# Algoritmo genético
def algoritmo_genetico(tamanho_populacao, taxa_mutacao, num_geracoes):
    populacao = [criar_individuo() for _ in range(tamanho_populacao)]

    for geracao in range(num_geracoes):
        nova_populacao = []

        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = selecionar_pais(populacao)
            filho = crossover(pai1, pai2)
            if random.random() < taxa_mutacao:
                filho = mutacao(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao

    melhor_individuo = max(populacao, key=fitness)
    return melhor_individuo

# Definição dos parâmetros do algoritmo genético
tamanho_populacao = 50
taxa_mutacao = 0.1
taxa_crossover = 0.8  # Taxa de cross-over inicial
num_geracoes = 100

melhor_individuo = algoritmo_genetico(tamanho_populacao, taxa_mutacao, num_geracoes)

if num_geracoes >= 1000:
    # Ajuste a taxa de cross-over após 1000 gerações
    taxa_crossover = 0.7  # Nova taxa de cross-over após 1000 gerações
    melhor_individuo = algoritmo_genetico(tamanho_populacao, taxa_mutacao, num_geracoes)

# Impressão da alocação de funcionários
print("Melhor alocação de funcionários encontrada:")
for turno, funcionarios in melhor_individuo.items():
    print(f"{turno}: {funcionarios}")
