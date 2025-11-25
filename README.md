# Sistema de Mensagens de Rede Social - UFSCar

## Descrição do Projeto

Sistema de armazenamento e gerenciamento de mensagens de uma rede social universitária implementado com **DataStax Astra DB** (Cassandra as a Service) e Python.

**Aluno:** Guilherme César Athayde

## Estrutura do Projeto

```
.
├── main.py              # Script Python principal com todas as implementações
├── relatorio.pdf        # Relatório em PDF
└── README.md            # Este arquivo
```

## Requisitos

- Python 3.x
- astrapy (biblioteca Python para AstraDB)
- Conta DataStax Astra (gratuita)

## Configuração

### 1. Instalar Dependências

```bash
pip3 install astrapy
```

### 2. Configurar AstraDB

Você precisa configurar as variáveis de ambiente com suas credenciais do AstraDB:

```bash
export ASTRA_DB_API_ENDPOINT="https://seu-database-id-regiao.apps.astra.datastax.com"
export ASTRA_DB_APPLICATION_TOKEN="seu-token-aqui"
```

**Como obter as credenciais:**

1. Acesse [https://astra.datastax.com](https://astra.datastax.com)
2. Crie uma conta gratuita (se ainda não tiver)
3. Crie um novo database (free tier)
4. Gere um Application Token com permissões de Database Administrator
5. Copie o API Endpoint e o Token

### 3. Executar o Script

```bash
python3 main.py
```

## Funcionalidades Implementadas

### ✓ Tarefa 1: Criar a Coleção

- Coleção `social_messages` criada com estrutura definida
- Campos: `_id`, `user_id`, `user_age`, `topic`, `message_text`, `timestamp`

### ✓ Tarefa 2: Inserir 20+ Mensagens

- 25 mensagens inseridas
- 10 usuários diferentes (user_001 a user_010)
- 6 tópicos: política, saúde, tecnologia, educação, esportes, entretenimento
- Distribuição aleatória de mensagens ao longo de 30 dias

### ✓ Tarefa 3: Recuperar Mensagem Específica

- Implementada consulta por usuário
- Busca eficiente usando índices
- Suporte para buscar uma ou todas as mensagens de um usuário

### ✓ Tarefa 4: Índice e Frequência de Tópicos

- Índices gerenciados automaticamente pelo AstraDB
- Consulta de frequência de tópicos por usuário
- Agregação e processamento de dados

## Saída do Script

O script produz:

1. **Confirmação de conexão** com o AstraDB
2. **Criação da coleção** com feedback
3. **Inserção de mensagens** com contagem
4. **Consulta de mensagem específica** com todos os detalhes
5. **Relatório de frequência** de tópicos por usuário
6. **Estatísticas gerais** do sistema

Exemplo de saída:

```
Connected to Astra DB. Collections: []
Coleção 'social_messages' removida (se existia).
Coleção 'social_messages' criada com sucesso!

25 mensagens inseridas com sucesso!
IDs inseridos: ['msg_001', 'msg_002', 'msg_003', 'msg_004', 'msg_005']... (mostrando primeiros 5)

============================================================
TAREFA 3: Recuperar mensagem específica de um usuário
============================================================

Mensagem encontrada do usuário user_001:
  ID: msg_007
  Usuário: user_001
  Idade: 49
  Tópico: educação
  Texto: Alguém tem informações sobre o assunto? (Tema: educação)
  Data/Hora: 2025-11-15T02:22:36.617615

Total de mensagens do user_001: 1

============================================================
TAREFA 4: Criar índice e consultar frequência de tópicos por usuário
============================================================
Nota: AstraDB gerencia índices automaticamente para otimização de consultas.

Frequência de tópicos por usuário:
------------------------------------------------------------

user_001:
  - educação: 1 mensagem(ns)

user_002:
  - esportes: 2 mensagem(ns)
  - entretenimento: 1 mensagem(ns)

user_003:
  - educação: 1 mensagem(ns)
  - tecnologia: 1 mensagem(ns)

user_004:
  - educação: 1 mensagem(ns)
  - política: 1 mensagem(ns)

user_005:
  - esportes: 1 mensagem(ns)

user_006:
  - educação: 2 mensagem(ns)
  - esportes: 1 mensagem(ns)
  - saúde: 1 mensagem(ns)

user_007:
  - entretenimento: 1 mensagem(ns)
  - educação: 1 mensagem(ns)
  - esportes: 1 mensagem(ns)

user_008:
  - educação: 1 mensagem(ns)
  - entretenimento: 1 mensagem(ns)
  - saúde: 1 mensagem(ns)
  - esportes: 1 mensagem(ns)

user_009:
  - tecnologia: 1 mensagem(ns)
  - entretenimento: 1 mensagem(ns)

user_010:
  - educação: 1 mensagem(ns)
  - esportes: 1 mensagem(ns)
  - saúde: 1 mensagem(ns)

============================================================
ESTATÍSTICAS GERAIS
============================================================
Total de usuários: 10
Total de mensagens: 25
Tópicos disponíveis: educação, esportes, saúde

Distribuição de mensagens por tópico:
  - educação: 8 mensagem(ns)
  - esportes: 7 mensagem(ns)
  - entretenimento: 4 mensagem(ns)
  - saúde: 3 mensagem(ns)
  - tecnologia: 2 mensagem(ns)
  - política: 1 mensagem(ns)

============================================================
Script executado com sucesso!
============================================================
```

## Relatório

O relatório completo (`relatorio.pdf`) contém:

1. **Nome do integrante**
2. **Scripts CQL** equivalentes para Cassandra tradicional
3. **Código Python completo** com anotações
4. **Discussão detalhada** sobre:
   - Modelagem de dados (Query-First Design)
   - Escolha de chaves primárias e particionamento
   - Estratégia de indexação
   - Trade-offs de performance
   - Análise de resultados
5. **Conclusão**

## Modelagem de Dados

### Estrutura do Documento

```json
{
  "_id": "msg_001",
  "user_id": "user_001",
  "user_age": 25,
  "topic": "tecnologia",
  "message_text": "Texto da mensagem sobre tecnologia",
  "timestamp": "2025-11-15T10:30:00"
}
```

### CQL Equivalente (Cassandra Tradicional)

```sql
CREATE TABLE social_messages (
    message_id TEXT,
    user_id TEXT,
    user_age INT,
    topic TEXT,
    message_text TEXT,
    timestamp TIMESTAMP,
    PRIMARY KEY (user_id, timestamp, message_id)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

## Princípios de Design

### 1. Desnormalização

Todos os dados da mensagem em um único documento para máxima eficiência de leitura.

### 2. Query-First Design

Modelagem baseada nas consultas mais frequentes:

- Busca por usuário (partition key)
- Ordenação por data (clustering key)
- Filtro por tópico (índice secundário)

### 3. Escalabilidade

- Distribuição de dados usando `user_id` como partition key
- Suporte a crescimento horizontal natural do Cassandra
- Performance consistente independente do volume

## Performance

### Consultas Otimizadas

- **Busca por usuário**: O(1) - lookup direto na partition
- **Ordenação por timestamp**: Pré-ordenada no armazenamento
- **Busca por tópico**: Índice secundário automático

### Recomendações para Produção

- Usar TTL para mensagens antigas
- Implementar particionamento por período
- Configurar replicação (RF=3)
- Usar Materialized Views para agregações
- Monitorar latência e throughput

## Tecnologias Utilizadas

- **DataStax Astra DB**: Cassandra gerenciado na nuvem
- **Python 3**: Linguagem de programação
- **astrapy**: Cliente Python para Astra DB

## Vantagens do AstraDB

- ✓ Setup simplificado (sem infraestrutura)
- ✓ Escalabilidade automática
- ✓ Backup e recuperação gerenciados
- ✓ APIs modernas (REST, Document, GraphQL)
- ✓ Free tier generoso para desenvolvimento
