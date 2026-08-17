# Projeto de Tradução Bíblica Autoral (Novo Testamento)

Tradução 100% autoral do Novo Testamento a partir dos textos críticos originais em Grego Koiné (SBLGNT / Nestle-Aland / Macula Greek), com foco em **equivalência dinâmico-funcional moderna**, **rigor exegético-histórico** e **notas explicativas aprofundadas**.

---

## 🎯 Estrutura do Projeto

```text
├── docs/
│   └── guia_traducao.md         # Filosofia de tradução, metodologia e glossário exegético
├── content/
│   ├── markdown/                # Arquivos primários de leitura, exegese e tradução
│   │   └── nt/
│   │       └── 04_joao/
│   │           └── capitulo_01.md  # João 1:1-18 (O Prólogo de João)
│   ├── json/                    # Dados estruturados para consumo por APIs e apps
│   │   └── nt/
│   │       └── 04_joao_01.json
│   └── sql/                     # DDL e DML para SQLite / PostgreSQL
│       └── schema_and_seed.sql
└── scripts/
    └── build_data.py            # Automação de extração e conversão (MD -> JSON -> SQL)
```

---

## 📖 As 3 Camadas de Tradução

Cada versículo é estruturado em três níveis:
1. **Grego Koiné:** Texto original com acentuação e pontuação crítica.
2. **Tradução Literal de Apoio:** Tradução interlinear funcional palavra por palavra para análise da sintaxe grega.
3. **Tradução Fluente Autoral:** Versão contemporânea, fluente e fiel ao sentido original.
4. **Notas Exegéticas e Culturais:** Detalhamento léxico (morfologia, lemas, transliterações), contexto judaico do Segundo Templo e nuances histórico-filosóficas.

---

## ⚡ Como Rodar o Pipeline

Para ler os arquivos em Markdown e regerar automaticamente os arquivos JSON e o banco SQLite:

```bash
# Executar o script de build
python scripts/build_data.py
# ou no Windows
py scripts/build_data.py
```
