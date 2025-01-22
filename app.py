import random

class Caixa:
    def __init__(self, id, altura, peso):
        self.id = id
        self.altura = altura
        self.peso = peso

# Caixas a serem empilhadas no Pallet
caixas = [
    Caixa(id=1, altura=8, peso=15),
    Caixa(id=2, altura=6, peso=10),
    Caixa(id=3, altura=9, peso=5),
    Caixa(id=4, altura=3, peso=22),
    Caixa(id=5, altura=10, peso=12),
    Caixa(id=6, altura=10, peso=3),
    Caixa(id=7, altura=8, peso=7),
    Caixa(id=8, altura=5, peso=5),
    Caixa(id=9, altura=5, peso=23),
    Caixa(id=10, altura=7, peso=7)
]

# Parâmetros
limite_peso = 45
populacao_tamanho = 20  
numero_geracoes = 50
taxa_mutacao = 0.02

def calcular_altura(caixas):
    return sum(caixa.altura for caixa in caixas)

def calcular_peso(caixas):
    return sum(caixa.peso for caixa in caixas)

# Função de aptidão
def funcao_fitness(individuo):
    altura = calcular_altura(individuo)
    peso_total = calcular_peso(individuo)
    return (1 / altura) + peso_total

# Criando um individuo válido na População inicial
def criar_individuo(caixas):
    individuo_aleatorio = caixas[:]
    individuo = []
    random.shuffle(individuo_aleatorio)
    peso_total = 0
    for caixa in individuo_aleatorio:
        peso_total += caixa.peso
        if avalia_caixa(caixa, peso_total) :
           individuo.append(caixa)
    return individuo

def avalia_caixa(caixa, peso_total):
    if peso_total <= limite_peso :
        return True
    else:
        return False

def criar_populacao(tamanho, caixas):
    return [criar_individuo(caixas) for _ in range(tamanho)]

# Selecionar dois individuos para cruzamento de forma aleatoria: Roleta
def selecionar_pais(populacao, fitnesses):
    total_fitness = sum(fitnesses)
    probabilidades = [f / total_fitness for f in fitnesses]
    pais = random.choices(populacao, probabilidades, k=2)
    return pais

#O cruzamento deve ser efetuado de forma a resultar um individuo válido, isto é, o empilhamento deve respeitar o limite do Pallet
def cruzar(pais):
    ponto_cruzamento = random.randint(1, len(pais[0]) - 1)
    filho1_aleatorio = pais[0][:ponto_cruzamento] + [caixa for caixa in pais[1] if caixa not in pais[0][:ponto_cruzamento]]
    filho2_aleatorio = pais[1][:ponto_cruzamento] + [caixa for caixa in pais[0] if caixa not in pais[1][:ponto_cruzamento]]
    filho1 = []
    filho2 = []
    peso_total = 0
    for caixa in filho1_aleatorio:
        peso_total += caixa.peso
        if avalia_caixa(caixa, peso_total) :
           filho1.append(caixa)
    
    peso_total = 0
    for caixa in filho2_aleatorio:
        peso_total += caixa.peso
        if avalia_caixa(caixa, peso_total) :
           filho2.append(caixa)

    return [filho1, filho2]

def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]

# Processamento do Algoritmo Genético
def algoritmo_genetico(caixas, limite_peso, populacao_tamanho, numero_geracoes, taxa_mutacao):
    populacao = criar_populacao(populacao_tamanho, caixas)

    for geracao in range(numero_geracoes):
        fitnesses = [funcao_fitness(individuo) for individuo in populacao]
        nova_populacao = []
        
        while len(nova_populacao) < populacao_tamanho:
            pais = selecionar_pais(populacao, fitnesses)
            filhos = cruzar(pais)
            for filho in filhos:
                mutacao(filho, taxa_mutacao)
                nova_populacao.append(filho)
        
        populacao = nova_populacao[:populacao_tamanho]

    melhor_individuo = max(populacao, key=lambda individuo: funcao_fitness(individuo))
    return melhor_individuo

# Executando o algoritmo 
melhor_solucao = algoritmo_genetico(caixas, limite_peso, populacao_tamanho, numero_geracoes, taxa_mutacao)
print("Melhor solução encontrada:")
for caixa in melhor_solucao:
    print(f"Caixa {caixa.id}: Altura {caixa.altura}, Peso {caixa.peso}")

altura_final = calcular_altura(melhor_solucao)
peso_total_final = calcular_peso(melhor_solucao)
print(f"Altura total: {altura_final}")
print(f"Peso total: {peso_total_final}")
