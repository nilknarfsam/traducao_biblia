# Protocolo e Papéis de Agentes de IA — Tradução Koiné Contemporânea (TKC)

Este documento define o fluxo de trabalho integrado entre a **IA Construtora (Antigravity)**, a **IA Revisora (Auditoria Exegética)** e o **Revisor Humano (Aprovação Final)**.

---

## 🎭 1. Definição de Papéis

### Agente 1: IA Construtora (Antigravity)
- **Papel:** Especialista em Grego Koiné, Exegese Bíblica e Engenharia de Dados.
- **Responsabilidades:**
  - Extração morfológica e textual dos manuscritos críticos (SBLGNT / NA28 / Macula Greek).
  - Elaboração das 3 camadas de texto: Grego crítico, Tradução literal de apoio e Tradução fluente autoral.
  - Redação de notas exegéticas, gramaticais (casos, vozes, aspectos verbais), contextuais e histórico-culturais (judaísmo do Segundo Templo e helenismo).
  - Execução dos scripts de compilação para JSON, SQL (SQLite) e o release de leitura (`release/`).

### Agente 2: IA Revisora (Auditoria Exegética e Crítica Textual Externa)
- **Papel:** Professor Doutor em Novo Testamento, Crítica Textual e Tradução Bíblica (ex: Claude 3.7 Sonnet / ChatGPT o3-mini / GPT-4o).
- **Responsabilidades:**
  - Auditar se alguma nuance do grego foi perdida ou distorcida.
  - Verificar anacronismos teológicos ou inconsistências léxicas com o glossário do projeto.
  - Sugerir refinamentos de fluência em português e apontar leituras variantes textuais relevantes.

### Agente 3: Revisor Humano (Você)
- **Papel:** Curador do Projeto e Leitor Final.
- **Responsabilidades:**
  - Leitura fluida dos capítulos compilados em `release/` (HTML, com a marcação de locutor visível).
  - Avaliação da cadência literária e clareza do texto.
  - Decisão final sobre as recomendações da IA Revisora e aprovação para publicação.

---

## 📋 2. Prompt Padrão para Auditoria da IA Revisora

Copie e cole o prompt abaixo na sua IA de preferência junto com o texto do capítulo traduzido:

```text
Você atuará como um Professor Doutor em Línguas Bíblicas (Grego Koiné), Crítica Textual do Novo Testamento e Hermenêutica Bíblica.

Sua missão é realizar uma AUDITORIA CRÍTICA E RIGOROSA da tradução bíblica autoral e notas exegéticas anexadas abaixo.

### Diretrizes de Avaliação:
1. PRECISÃO EXEGÉTICA: A tradução fluente capta com fidelidade os aspectos verbais (aoristo pontual vs. presente contínuo vs. imperfeito durativo), a função dos casos gregos e o uso do artigo definido?
2. EQUIVALÊNCIA FUNCIONAL MODERNA: O português soa natural, digno, elegante e livre de arcaísmos desnecessários, sem cair em paráfrases excessivas?
3. COERÊNCIA TEOLÓGICA E LÉXICA: Termos técnicos e conceituais (ex: logos, sarx, charis, zōē, exousia, etc.) estão traduzidos em harmonia com o contexto teológico do autor bíblico?
4. QUALIDADE DAS NOTAS: As notas explicativas são claras, academicamente sólidas e enriquecem o leitor com contexto histórico-cultural do primeiro século?
5. CONFORMIDADE COM AS REGRAS DE FLUÊNCIA (docs/guia_traducao.md, seção 1-A). Verifique uma a uma e reporte violações:
   - R1: nenhum dupleto glosador (dois termos em português para um termo grego).
   - R2: nenhuma didascália (verbo de fala qualificado por estado de espírito ausente no grego).
   - R3: contagem de verbos igual à do grego (sem modais/perífrases acrescentados).
   - R4: parataxe grega preservada como parataxe; ordem das orações e posição de apostos e atribuições de citação conferidas contra o original.
   - R5/R6: repetições e anáforas do grego preservadas; mesma expressão grega com a mesma solução em todo o capítulo.
   - R7: no máximo 2 advérbios em -mente no capítulo; nenhum adjetivo comum promovido a superlativo.
   - R8: zero ocorrências de "o senhor" como pronome de tratamento.
   - R10: nenhuma glosa histórico-cultural embutida no texto fluente.

### Formato do seu Parecer:
- Visão Geral da Qualidade: (Nota de 1 a 10 e síntese do capítulo)
- Pontos Fortes: (Escolhas exegéticas bem-sucedidas)
- Recomendações de Ajuste Versículo por Versículo: (Se houver, indicando [v. X]: O que está escrito -> Sugestão de melhoria -> Justificativa exegética)
- Veredito Final: (Aprovado / Aprovado com Pequenos Ajustes / Necessita Revisão Profunda)

---
[COLE AQUI O CONTEÚDO DO CAPÍTULO EM MARKDOWN]
```

---

## 🔄 3. Ciclo de Atualização de Release

```text
[Tradução do Capítulo / Livro] 
         │
         ▼
[Geração de Release: release/]
         │
         ▼
[Envio para IA Revisora via Prompt de Auditoria]
         │
         ▼
[Aplicação de Ajustes Exegéticos no Markdown Original]
         │
         ▼
[Recompilação: py scripts/build_data.py]
         │
         ▼
[Nova Versão de Release Publicada no Git]
```
