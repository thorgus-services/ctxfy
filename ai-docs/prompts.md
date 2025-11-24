1. Extraia trechos exatos das rules do projeto que são relevantes para esta História do Usuário. Se não encontrar trecho relevantes, diga "Nenhum trecho relevante encontrado."
2. Use os trechos para analisar a conformidade com as seções das rules do projeto, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.

1. Acesse e extraia trechos exatos da documentação do FastMCP, https://gofastmcp.com/llms.txt, que são relevantes para esta História do Usuário. Se não encontrar trecho relevantes, diga "Nenhum trecho relevante encontrado."
2. Use os trechos para analisar a conformidade da História do Usuário gerada com as seções da documentação do FastMCP, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.

Use apenas informações dos documentos e recursos passados no contexto, não use conhecimento genérico ou geral.



1. Revise cada trecho do PRP {{teeee}} para encontrar citações diretas dos documentos e recursos passados no contexto. Se não encontrar nenhuma citação que apoie o trecho, remova do PRP e marque como removido com colchete vazio [].
2. Extraia trechos exatos das rules do projeto {{rules}} que são relevantes para a História do Usuário {{historia}}. Se não encontrar trecho relevante, diga "Nenhum trecho relevante encontrado."
3. Use os trechos extraídos da rules para determinar o percentual de conformidade com o PRP {{prp}} gerado, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.


---

Gere o context stack para implementar a especificação técnica {{spec}}, baseado no template {{template}}
Output com o arquivo gerado deve ser colocado no diretório {{context/}}

Use as rules do projeto {{rules/}}
Use a documentação oficial do FastMCP, https://gofastmcp.com/llms.txt, acesse apenas as URLs da documentação

1. Extraia trechos exatos das rules do projeto que são relevantes para esta especificação. Se não encontrar trecho relevantes, diga "Nenhum trecho relevante das rules encontrado."
2. Acesse e extraia trechos exatos da documentação do FastMCP, https://gofastmcp.com/llms.txt, que são relevantes para esta especificação. Se não encontrar trecho relevante, diga "Nenhum trecho relevante da documentação do FastMCP encontrado."
3. Use apenas informações dos documentos e recursos passados, não use conhecimento genérico ou geral.

---

Gere um PRP para implementar as especificação técnica {{espec}}, baseado no template {{prp-template}}
Use o context stack {{context}}

Output com o arquivo gerado deve ser colocado no diretório {{prp/}}

---

1. Revise cada trecho do PRP @ai-docs/prp/mcp-server-specification-generation-prp.md para encontrar citações diretas dos documentos e recursos passados no contexto. Se não encontrar nenhuma citação que apoie o trecho, remova do PRP e marque como removido com colchete vazio [].
2. Extraia trechos exatos das rules do projeto @ai-docs/rules/ que são relevantes para a especificação @ai-docs/tasks/mcp-server-specification-generation-technical-spec.md . Se não encontrar trecho relevante, diga "Nenhum trecho relevante encontrado."
3. Use os trechos extraídos da rules para determinar o percentual de conformidade com o PRP @ai-docs/prp/mcp-server-specification-generation-prp.md gerado, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.

Use o context stack @ai-docs/context/mcp-server-specification-generation-context-stack.md
Use a especificação @ai-docs/tasks/mcp-server-specification-generation-technical-spec.md

---

1. Revise cada trecho do PRP @ai-docs/prp/mcp-server-specification-generation-prp.md para encontrar citações diretas dos documentos e recursos passados no contexto. Se não encontrar nenhuma citação que apoie o trecho, remova do PRP e marque como removido com colchete vazio [].
2. Extraia trechos exatos das rules do projeto @ai-docs/rules/ que são relevantes para a especificação @ai-docs/tasks/mcp-server-specification-generation-technical-spec.md . Se não encontrar trecho relevante, diga "Nenhum trecho relevante encontrado."
3. Use os trechos extraídos da rules para determinar o percentual de conformidade com o PRP @ai-docs/prp/mcp-server-specification-generation-prp.md gerado, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.

Use o context stack @ai-docs/context/mcp-server-specification-generation-context-stack.md
Use a especificação @ai-docs/tasks/mcp-server-specification-generation-technical-spec.md

---

1. Revise cada trecho do context stack {{context}} para encontrar citações diretas dos documentos e recursos passados. Se não encontrar nenhuma citação que apoie o trecho, remova do context stack e marque como removido com colchete vazio [].
2. Extraia trechos exatos das rules do projeto {{rules}} que são relevantes para a especificação {{spec}}. Se não encontrar trecho relevante, diga "Nenhum trecho relevante encontrado."
3. Use os trechos extraídos das rules para determinar o percentual de conformidade com o context stack {{context}} gerado, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.

Use a especificação técnica {{spec}}

Output esperado é o percentual por seção e geral de conformidade e, se for o caso, as recomendações de melhoria.
Use apenas informações dos documentos e recursos passados, não use conhecimento genérico ou geral.

---

Aplique as recomendações de melhoria e gere um novo context stack baseado no template {{context-template}}
Substitua o {{context}} existente

---

1. Revise cada trecho do código gerado para encontrar relações diretas na especificação, context stack e PRP. Se não encontrar nenhuma citação que apoie o trecho, informe qual o trecho do código e marque como ponto de revisão manual.
2. Use os trechos de código para determinar o percentual de conformidade com a especificação técnica {{spec}}, referenciando os trechos por número. Tome como base para a sua análise apenas os trechos extraídos.

Output esperado é o percentual por seção e geral de conformidade e, se for o caso, as recomendações de melhoria.
Use apenas informações dos documentos e recursos passados, não use conhecimento genérico ou geral.