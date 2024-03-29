import random
import string

# Definição da senha secreta
senha_secreta = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(512))

# Função de fitness
def fitness(individuo):
    return sum(c1 == c2 for c1, c2 in zip(individuo, senha_secreta))

# Função de criação de indivíduos aleatórios
def criar_individuo():
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(512))

# Função de seleção de pais por torneio
def selecionar_pais(populacao, tamanho_torneio):
    torneio = random.sample(populacao, tamanho_torneio)
    return max(torneio, key=fitness)

# Função de crossover de um ponto
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, 511)
    filho = pai1[:ponto_corte] + pai2[ponto_corte:]
    return filho

# Função de mutação
def mutacao(individuo, taxa_mutacao):
    return ''.join(c if random.random() > taxa_mutacao else random.choice(string.ascii_letters + string.digits + string.punctuation) for c in individuo)

# Algoritmo genético
def algoritmo_genetico(tamanho_populacao, tamanho_torneio, taxa_mutacao, num_geracoes):
    populacao = [criar_individuo() for _ in range(tamanho_populacao)]

    for geracao in range(num_geracoes):
        nova_populacao = []

        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecionar_pais(populacao, tamanho_torneio)
            pai2 = selecionar_pais(populacao, tamanho_torneio)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao

        melhor_individuo = max(populacao, key=fitness)
        melhor_fitness = fitness(melhor_individuo)

        print(f"Geração {geracao + 1}: {melhor_individuo} (Fitness: {melhor_fitness})")

    return melhor_individuo

# Definição dos parâmetros do algoritmo genético
tamanho_populacao = 100
tamanho_torneio = 3
taxa_mutacao = 0.01
num_geracoes = 100

# Execução do algoritmo genético
melhor_senha = algoritmo_genetico(tamanho_populacao, tamanho_torneio, taxa_mutacao, num_geracoes)

print("\nSenha secreta:", senha_secreta)
print("Melhor senha encontrada:", melhor_senha)
