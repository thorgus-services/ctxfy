# HISTÓRIA 1: Recebimento e Processamento Inicial de Tarefas (Versão Final com Prompt)

**Como** desenvolvedor usando uma ferramenta compatível com MCP (Claude Code, Cursor, Trae, etc.)  
**Eu quero** enviar um arquivo markdown contendo uma história do usuário ou tarefa para o MCP Server através de uma URI  
**Para que** o servidor processe o arquivo e me forneça informações necessárias para iniciar o fluxo automatizado de Context Engineering, enquanto eu mantenho o controle total sobre onde e como os arquivos são armazenados no meu ambiente local.

## Critérios de Aceitação SMART:

### Specific (Específico)
**LADO DO SERVIDOR (Tool `process_task`):**
- [ ] A tool `process_task` recebe um parâmetro `task_file_uri: str` (URI do arquivo markdown)
- [ ] O servidor lê o conteúdo do arquivo usando `ctx.read_resource(task_file_uri)`
- [ ] O servidor gera uma `task_id` única usando o formato `task_{timestamp}_{hash_curto}`, onde:
  - `timestamp`: Unix timestamp em segundos (ex: 1735432567)
  - `hash_curto`: Primeiros 6 caracteres do SHA-256 do conteúdo do arquivo
  - Exemplo resultante: `task_1735432567_a1b2c3` (mais compacto para nomes de diretório)
- [ ] O servidor retorna apenas dados estruturados:
  ```json
  {
    "task_id": 1735432567,
    "task_id_str": "task_1735432567_a1b2c3",
    "file_content": "Conteúdo completo do arquivo markdown...",
    "file_name": "original_task.md",
    "timestamp": "2025-12-29T10:30:00Z"
  }
  ```

**LADO DO SERVIDOR (Prompt `setup_context_engineering`):**
- [ ] O prompt `setup_context_engineering` recebe um parâmetro `task_file_uri: str`
- [ ] O prompt contém instruções claras para o LLM do cliente:
  ```
    You are a specialized agent in Context Engineering. Your task is to prepare 
    the local environment to process a task using the complete Context Engineering workflow.

    Steps to follow:

    1. First, use the tool 'process_task' with the file URI: {task_file_uri}

    2. With the returned result (which will include task_id_str and file_content), you must:
    - Create locally the directory structure: .ctxfy/{task_id_str}/
    - Save the file content as .ctxfy/{task_id_str}/original_task.md

    3. Important: You do not have permission to execute shell code or scripts.
    Use the following approaches (depending on your MCP client capabilities):
    
    a) If your MCP client supports native file operations:
        - Use your client's file manipulation capabilities
        - Create the directory .ctxfy/{task_id_str}/ using the available commands in your client
        - Save the file content to .ctxfy/{task_id_str}/original_task.md using your client's resources
    
    b) If your MCP client does not support automatic file operations:
        - Provide clear instructions to the user to create manually:
            "Please manually create the following directory structure in your local environment:
            .ctxfy/{task_id_str}/
            
            Then, save the following content as .ctxfy/{task_id_str}/original_task.md:
            [file content]"

    4. After creating the structure, confirm to the user that the environment is prepared and 
    inform the complete path: .ctxfy/{task_id_str}/

    5. Do not proceed to the next steps of Context Engineering yet. Only 
    prepare the initial environment and wait for additional instructions.

    Remember: Your responsibility is to organize locally, not to execute code.
    If you encounter limitations in your client's capabilities, be transparent 
    with the user and offer manual alternatives.
  ```

### Measurable (Mensurável)
**Servidor:**
- [ ] A tool `process_task` processa arquivos de até 10MB em menos de 2 segundos
- [ ] A `task_id` gerada tem no máximo 25 caracteres para compatibilidade com sistemas de arquivos
- [ ] A tool retorna erro claro quando:
  - URI é inválida ou não contém scheme
  - Arquivo não encontrado no recurso especificado
  - Permissões insuficientes para ler o recurso
- [ ] O prompt `setup_context_engineering` é registrado com sucesso no servidor MCP
- [ ] O prompt é acessível através do endpoint MCP de listagem de prompts

### Achievable (Alcançável)
**Prompt Configuration:**
- [ ] O prompt `setup_context_engineering` é registrado no servidor FastMCP
- [ ] O prompt tem uma descrição clara e parâmetros bem definidos
- [ ] O prompt funciona com diferentes clientes MCP (Claude Code, Cursor, Trae, etc.)

### Relevant (Relevante)
- [ ] A tool segue princípios de responsabilidade única: processa dados, não gerencia arquivos
- [ ] Remove dependência de operações de sistema de arquivos no servidor, melhorando portabilidade
- [ ] Permite que o cliente controle seu próprio ambiente de arquivos
- [ ] O prompt `setup_context_engineering` permite a integração agnóstica com diferentes clientes MCP
- [ ] A abordagem mantém a segurança ao não executar código no lado do cliente
- [ ] Prepara o ambiente para o fluxo completo de Context Engineering

### Time-bound (Temporizado - implícito)
- [ ] A tool no servidor responde em menos de 2 segundos
- [ ] O prompt é processado pelo LLM do cliente em menos de 5 segundos
- [ ] O fluxo completo (servidor + cliente) não deve exceder 5 segundos para tarefas típicas

## Tarefas Técnicas Detalhadas:

### Servidor (Tool `process_task`):
- [ ] Implementar validação robusta de URI antes de tentar ler recursos
- [ ] Adicionar tratamento de erros para casos de arquivo não encontrado ou permissões insuficientes
- [ ] Implementar sanitização do conteúdo para evitar problemas de encoding
- [ ] Adicionar logging detalhado usando `ctx.info()` e `ctx.error()`
- [ ] Implementar rate limiting por client_id para prevenir abuso
- [ ] Testar com diferentes tipos de URIs (file://, resource://, http://)
- [ ] Validar a geração de `task_id` com conteúdo idêntico em momentos diferentes

### Servidor (Prompt `setup_context_engineering`):
- [ ] Registrar o prompt com o nome `setup_context_engineering`
- [ ] Configurar o parâmetro `task_file_uri` como obrigatório
- [ ] Definir uma descrição clara para o prompt
- [ ] Testar o prompt com diferentes clientes MCP para garantir compatibilidade
- [ ] Validar que o prompt funciona corretamente com o fluxo completo

### Documentação:
- [ ] Documentar o formato esperado do arquivo de tarefa (markdown)
- [ ] Explicar claramente que o servidor não cria arquivos no sistema do cliente
- [ ] Documentar como usar o prompt `setup_context_engineering` com diferentes clientes

## Exemplo de Uso Esperado:

**Passo 1 - Cliente chama o prompt:**
```bash
# Usuário chama o prompt no seu cliente MCP
>>> /prompt setup_context_engineering task_file_uri="file:///home/user/minha_tarefa.md"
```

**Passo 2 - Servidor processa e retorna:**
```json
{
  "task_id": 1735432567,
  "task_id_str": "task_1735432567_a1b2c3",
  "file_content": "# Minha Tarefa\n\nDescrição completa da tarefa aqui...",
  "file_name": "original_task.md",
  "timestamp": "2025-12-29T10:30:00Z"
}
```

**Passo 3 - Cliente (LLM) processa as instruções do prompt:**
O LLM do cliente recebe as instruções do prompt e:
- Chama a tool `process_task` com a URI fornecida
- Recebe o resultado com `task_id_str` e `file_content`
- Cria a estrutura de diretórios `.ctxfy/task_1735432567_a1b2c3/` usando as capacidades nativas do cliente
- Salva o conteúdo como `.ctxfy/task_1735432567_a1b2c3/original_task.md`
- Confirma ao usuário que o ambiente está preparado