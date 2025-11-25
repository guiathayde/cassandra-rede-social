from astrapy import DataAPIClient
import os
from datetime import datetime, timedelta
import random

# Conexão com o AstraDB
# IMPORTANTE: Configure as variáveis de ambiente antes de executar:
# export ASTRA_DB_API_ENDPOINT="https://seu-endpoint.apps.astra.datastax.com"
# export ASTRA_DB_APPLICATION_TOKEN="seu-token"

api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
api_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

if not api_endpoint or not api_token:
    print("ERRO: Variáveis de ambiente não configuradas!")
    print("Configure antes de executar:")
    print("  export ASTRA_DB_API_ENDPOINT='https://seu-endpoint.apps.astra.datastax.com'")
    print("  export ASTRA_DB_APPLICATION_TOKEN='seu-token'")
    exit(1)

client = DataAPIClient() 
db = client.get_database(api_endpoint, token=api_token)

print(f"Connected to Astra DB. Collections: {db.list_collection_names()}")

# ============================================
# TAREFA 1: Criar a Coleção (Tabela)
# ============================================

collection_name = "social_messages"

# Dropar coleção se já existir (para testes)
try:
    db.drop_collection(collection_name)
    print(f"Coleção '{collection_name}' removida (se existia).")
except Exception as e:
    print(f"Info: {e}")

# Criar a coleção
# No AstraDB, as coleções são schemaless, mas vamos definir a estrutura dos documentos:
# {
#   "_id": "message_id",
#   "user_id": "user_xxx",
#   "user_age": 25,
#   "topic": "tecnologia",
#   "message_text": "Texto da mensagem",
#   "timestamp": "2025-11-20T10:30:00"
# }

collection = db.create_collection(collection_name)
print(f"Coleção '{collection_name}' criada com sucesso!")

# ============================================
# TAREFA 2: Inserir pelo menos 20 mensagens
# ============================================

# Definir usuários, tópicos e algumas mensagens base
users = [f"user_{str(i).zfill(3)}" for i in range(1, 11)]  # user_001 a user_010
user_ages = {user: random.randint(18, 65) for user in users}
topics = ["política", "saúde", "tecnologia", "educação", "esportes", "entretenimento"]

messages_templates = [
    "Hoje foi um dia interessante na universidade!",
    "Precisamos discutir mais sobre esse tema.",
    "Alguém tem informações sobre o assunto?",
    "Compartilhando minha opinião sobre isso.",
    "Vi uma notícia interessante hoje.",
    "O que vocês acham sobre essa questão?",
    "Evento importante acontecendo na UFSCar.",
    "Gostaria de ouvir outras perspectivas.",
    "Descobri algo novo e queria compartilhar.",
    "Reflexão do dia sobre este tópico.",
    "Atualizações importantes para todos.",
    "Debate interessante nas aulas.",
    "Projeto novo em andamento.",
    "Resultados da pesquisa foram surpreendentes.",
    "Discussão produtiva com colegas.",
    "Inovações chegando à universidade.",
    "Mudanças importantes no campus.",
    "Experiência enriquecedora hoje.",
    "Aprendizado valioso compartilhado.",
    "Perspectivas diversas sobre o tema.",
    "Análise crítica necessária aqui.",
    "Desenvolvimento contínuo da comunidade.",
]

# Gerar 25 mensagens com diferentes usuários, tópicos e datas
messages = []
base_date = datetime.now() - timedelta(days=30)

for i in range(25):
    user = random.choice(users)
    topic = random.choice(topics)
    message_text = random.choice(messages_templates)
    timestamp = base_date + timedelta(days=random.randint(0, 30), 
                                     hours=random.randint(0, 23),
                                     minutes=random.randint(0, 59))
    
    message = {
        "_id": f"msg_{str(i+1).zfill(3)}",
        "user_id": user,
        "user_age": user_ages[user],
        "topic": topic,
        "message_text": f"{message_text} (Tema: {topic})",
        "timestamp": timestamp.isoformat()
    }
    messages.append(message)

# Inserir as mensagens
result = collection.insert_many(messages)
print(f"\n{len(messages)} mensagens inseridas com sucesso!")
print(f"IDs inseridos: {result.inserted_ids[:5]}... (mostrando primeiros 5)")

# ============================================
# TAREFA 3: Recuperar mensagem específica de um usuário
# ============================================

print("\n" + "="*60)
print("TAREFA 3: Recuperar mensagem específica de um usuário")
print("="*60)

# Buscar uma mensagem do user_001
target_user = "user_001"
user_message = collection.find_one({"user_id": target_user})

if user_message:
    print(f"\nMensagem encontrada do usuário {target_user}:")
    print(f"  ID: {user_message['_id']}")
    print(f"  Usuário: {user_message['user_id']}")
    print(f"  Idade: {user_message['user_age']}")
    print(f"  Tópico: {user_message['topic']}")
    print(f"  Texto: {user_message['message_text']}")
    print(f"  Data/Hora: {user_message['timestamp']}")
else:
    print(f"Nenhuma mensagem encontrada para o usuário {target_user}")

# Buscar todas as mensagens de um usuário específico
all_user_messages = list(collection.find({"user_id": target_user}))
print(f"\nTotal de mensagens do {target_user}: {len(all_user_messages)}")

# ============================================
# TAREFA 4: Criar índice e consultar frequência por usuário
# ============================================

print("\n" + "="*60)
print("TAREFA 4: Criar índice e consultar frequência de tópicos por usuário")
print("="*60)

# Criar índice para user_id e topic (melhora performance das consultas)
# No AstraDB, índices são gerenciados automaticamente para coleções
# Mas podemos usar Vector Search Indexes ou configurações específicas se necessário
# Para este projeto, o AstraDB cria índices automaticamente nos campos consultados
print("Nota: AstraDB gerencia índices automaticamente para otimização de consultas.")

# Consulta: Para cada usuário, tipos de mensagens e frequência
# Vamos fazer isso recuperando todas as mensagens e processando em Python
all_messages = list(collection.find({}))

# Agrupar por usuário e contar frequência de tópicos
user_topic_frequency = {}

for msg in all_messages:
    user = msg['user_id']
    topic = msg['topic']
    
    if user not in user_topic_frequency:
        user_topic_frequency[user] = {}
    
    if topic not in user_topic_frequency[user]:
        user_topic_frequency[user][topic] = 0
    
    user_topic_frequency[user][topic] += 1

print("\nFrequência de tópicos por usuário:")
print("-" * 60)
for user, topics in sorted(user_topic_frequency.items()):
    print(f"\n{user}:")
    for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {topic}: {count} mensagem(ns)")

# Estatísticas gerais
print("\n" + "="*60)
print("ESTATÍSTICAS GERAIS")
print("="*60)
print(f"Total de usuários: {len(user_topic_frequency)}")
print(f"Total de mensagens: {len(all_messages)}")
print(f"Tópicos disponíveis: {', '.join(topics)}")

# Distribuição de mensagens por tópico
topic_distribution = {}
for msg in all_messages:
    topic = msg['topic']
    topic_distribution[topic] = topic_distribution.get(topic, 0) + 1

print("\nDistribuição de mensagens por tópico:")
for topic, count in sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {topic}: {count} mensagem(ns)")

print("\n" + "="*60)
print("Script executado com sucesso!")
print("="*60)
