# HISTÓRIA 1: Recebimento e Processamento Inicial de Tarefas

**Como** desenvolvedor usando uma ferramenta compatível com MCP (Claude Code, Cursor, Trae, etc.)  
**Eu quero** enviar o caminho de um arquivo markdown contendo uma história do usuário ou tarefa para o MCP Server  
**Para que** o servidor processe o arquivo, organize a estrutura de diretórios e inicie o fluxo automatizado de Context Engineering, mantendo todos os arquivos gerados centralizados em um workspace gerenciado pelo servidor.

## Critérios de Aceitação SMART:

### Specific (Específico)
**LADO DO SERVIDOR (Tool `process_task`):**
- [ ] A tool `process_task` recebe um parâmetro `task_file_path: str` (caminho do arquivo markdown)
- [ ] O servidor lê o conteúdo do arquivo usando funções nativas do Python (`open()`, `read()`)
- [ ] O servidor gera uma `task_id` única usando o formato `task_{timestamp}_{hash_curto}`, onde:
  - `timestamp`: Unix timestamp em segundos (ex: 1735432567)
  - `hash_curto`: Primeiros 6 caracteres do SHA-256 do conteúdo do arquivo
  - Exemplo resultante: `task_1735432567_a1b2c3`
- [ ] O servidor determina o workspace baseado no ambiente de execução:
  - Se executado via Docker: `/workspace`
  - Se executado via STDIO: diretório atual do processo (`${PWD}`)
- [ ] O servidor cria a estrutura de diretórios `.ctxfy/tasks/{task_id_str}/` no workspace
- [ ] O servidor salva o arquivo original como `.ctxfy/tasks/{task_id_str}/original-task.md`
- [ ] O servidor retorna dados estruturados com informações sobre o processamento:
  ```json
  {
    "task_id": 1735432567,
    "task_id_str": "task_1735432567_a1b2c3",
    "file_path": ".ctxfy/tasks/task_1735432567_a1b2c3/original-task.md",
    "workspace_path": "/workspace/.ctxfy/tasks/task_1735432567_a1b2c3/",
    "timestamp": "2025-12-29T10:30:00Z"
  }
  ```

**LADO DO SERVIDOR (Prompt `setup_context_engineering`):**
- [ ] O prompt `setup_context_engineering` recebe um parâmetro `task_file_path: str`
- [ ] O prompt contém instruções claras e simplificadas para o LLM do cliente:
  ```
  You are a specialized agent in Context Engineering. Your task is to initiate 
  the Context Engineering workflow by providing the path to a task file.
  
  Steps to follow:
  
  1. Ask the user for the path to the markdown file containing the task or user story.
  
  2. Use the tool 'process_task' with the file path provided by the user.
  
  3. Wait for the server to process the file and create the necessary directory structure.
  
  4. Confirm to the user that the task has been processed successfully and provide the task ID.
  
  Important: Do not attempt to create directories or save files manually. The server handles all file operations automatically.
  ```

### Measurable (Mensurável)
**Servidor:**
- [ ] A tool `process_task` processa arquivos de até 10MB em menos de 2 segundos
- [ ] A `task_id` gerada tem no máximo 25 caracteres para compatibilidade com sistemas de arquivos
- [ ] A tool retorna erro claro quando:
  - Caminho do arquivo é inválido ou não existe
  - Permissões insuficientes para ler o arquivo
  - Erro ao criar diretórios ou salvar arquivos
- [ ] O prompt `setup_context_engineering` é registrado com sucesso no servidor MCP
- [ ] O prompt é acessível através do endpoint MCP de listagem de prompts
- [ ] A estrutura de diretórios `.ctxfy/tasks/` é criada automaticamente se não existir

### Achievable (Alcançável)
**Configuração do Servidor:**
- [ ] O servidor detecta automaticamente se está executando em ambiente Docker ou STDIO
- [ ] O workspace é configurado corretamente baseado no ambiente de execução
- [ ] O prompt `setup_context_engineering` é registrado no servidor FastMCP
- [ ] O prompt tem uma descrição clara e parâmetros bem definidos
- [ ] A tool `process_task` utiliza funções nativas do Python para operações de arquivo

### Relevant (Relevante)
- [ ] Centraliza o gerenciamento de arquivos no servidor, simplificando a experiência do cliente
- [ ] Mantém a consistência da estrutura de diretórios independentemente do ambiente de execução
- [ ] Elimina a necessidade de o cliente gerenciar operações de arquivo manualmente
- [ ] Prepara o ambiente organizado para as próximas etapas do fluxo de Context Engineering
- [ ] Suporta execução tanto em containers Docker quanto em ambiente local via STDIO
- [ ] Mantém a segurança ao controlar todas as operações de arquivo no servidor

### Time-bound (Temporizado - implícito)
- [ ] A tool no servidor responde em menos de 2 segundos
- [ ] O prompt é processado pelo LLM do cliente em menos de 3 segundos
- [ ] O fluxo completo (servidor + cliente) não deve exceder 4 segundos para tarefas típicas

## Tarefas Técnicas Detalhadas:

### Servidor (Tool `process_task`):
- [ ] Implementar detecção automática do ambiente de execução (Docker vs STDIO)
- [ ] Criar variável `workspace_dir` que aponta para `/workspace` (Docker) ou diretório atual (STDIO)
- [ ] Implementar validação robusta do caminho do arquivo antes de tentar ler
- [ ] Adicionar tratamento de erros para casos de arquivo não encontrado ou permissões insuficientes
- [ ] Implementar criação recursiva de diretórios com `os.makedirs(..., exist_ok=True)`
- [ ] Implementar sanitização de paths para evitar directory traversal attacks
- [ ] Adicionar logging detalhado usando `ctx.info()` e `ctx.error()`
- [ ] Validar a geração de `task_id` com conteúdo idêntico em momentos diferentes

### Servidor (Prompt `setup_context_engineering`):
- [ ] Registrar o prompt com o nome `setup_context_engineering`
- [ ] Configurar o parâmetro `task_file_path` como obrigatório
- [ ] Definir uma descrição clara e concisa para o prompt
- [ ] Testar o prompt com diferentes clientes MCP para garantir compatibilidade
- [ ] Remover qualquer referência a operações de arquivo do lado do cliente

### Documentação:
- [ ] Documentar o formato esperado do arquivo de tarefa (markdown)
- [ ] Explicar como o workspace é determinado (Docker vs STDIO)

## Exemplo de Uso Esperado:

**Passo 1 - Cliente chama o prompt:**
```bash
# Usuário chama o prompt no seu cliente MCP
>>> /prompt setup_context_engineering task_file_path="/home/user/minha_tarefa.md"
```

**Passo 2 - Servidor processa e retorna:**
```json
{
  "task_id": 1735432567,
  "task_id_str": "task_1735432567_a1b2c3",
  "file_path": ".ctxfy/tasks/task_1735432567_a1b2c3/original-task.md",
  "workspace_path": "/workspace/.ctxfy/tasks/task_1735432567_a1b2c3/",
  "timestamp": "2025-12-29T10:30:00Z"
}
```

**Passo 3 - Cliente (LLM) processa as instruções do prompt:**
O LLM do cliente recebe as instruções do prompt e:
- Solicita ao usuário o caminho do arquivo markdown
- Chama a tool `process_task` com o caminho fornecido
- Recebe a confirmação de processamento bem-sucedido do servidor
- Informa ao usuário o ID da tarefa e onde os arquivos foram armazenados
- Aguarda instruções para as próximas etapas do Context Engineering