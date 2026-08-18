# Tradução Koiné Contemporânea (TKC)

Tradução autoral do Novo Testamento a partir dos textos críticos em Grego Koiné
(SBLGNT / Nestle-Aland / Macula Greek), em português contemporâneo, com notas
exegéticas e culturais versículo a versículo.

O projeto persegue duas coisas ao mesmo tempo: **leitura fluida** — um texto ao
qual o leitor se apegue — e **fidelidade verificável** — cada escolha justificada
pelo grego e exposta em três camadas.

## 📖 [→ LER A TRADUÇÃO](https://nilknarfsam.github.io/traducao_biblia/release/)

**https://nilknarfsam.github.io/traducao_biblia/release/**

Abre em qualquer navegador, no celular ou no computador, e atualiza sozinho a
cada push. Guarde na tela de início do celular para acesso em um toque.

---

## 📐 O princípio

> **Explicitação é adição, e adição é infidelidade.**

A tradução fluente não faz o trabalho das outras camadas. Se um termo grego é
ambíguo, o texto escolhe a leitura primária e a nuance vai para a nota; se João
repete uma palavra, o português repete; se o grego coordena, o português não
subordina. As regras operacionais estão em
[`docs/guia_traducao.md`](docs/guia_traducao.md), seção 1-A (R1 a R11), com
checklist de aceite por capítulo.

## 📚 As camadas

Cada versículo é registrado em quatro níveis:

1. **Grego Koiné** — texto crítico com acentuação e pontuação.
2. **Tradução Literal de Apoio** — palavra por palavra, expondo a sintaxe grega.
3. **Tradução Fluente Autoral** — a versão de leitura.
4. **Notas Exegéticas e Culturais** — morfologia, lemas, judaísmo do Segundo
   Templo, contexto helenístico.

## 🎨 Marcação de locutor

O discurso direto é marcado por **quem fala**, nunca por cor — cor é decisão de
renderização e precisa ser desativável pelo leitor.

| Marcador | Locutor | Renderização padrão |
|---|---|---|
| `[[J]]` | Jesus | vermelho |
| `[[D]]` | Deus / YHWH, inclusive no NT | azul |
| `[[E]]` | Citação do Antigo Testamento | versalete, sem cor |

No banco, `verses.translation_text` fica **limpo** e os trechos viram offsets de
caractere em `verse_speech_spans`. Assim o app escolhe entre cor, itálico, barra
lateral ou nada — cerca de 8% dos homens têm deficiência de visão de cores, e
vermelho sobre branco é a pior combinação para leitura longa.

## 🗂️ Estrutura

```text
├── docs/
│   ├── guia_traducao.md     # Filosofia, regras R1-R11, glossário, schema
│   ├── agents.md            # Papéis das IAs e prompt de auditoria
│   └── roadmap.md           # Fases e fluxo de revisão
├── content/                 # 🔒 Fonte da verdade + insumo do app
│   ├── markdown/nt/         # Arquivos primários de trabalho (4 camadas)
│   ├── json/nt/             # Capítulos estruturados, carga sob demanda
│   └── sql/                 # schema_and_seed.sql + biblia.db (SQLite offline)
├── release/                 # 📖 Somente leitura humana — gerado, não editado
│   ├── index.html           # Índice de livros
│   └── nt/04_joao.html      # Livro com menu de capítulos e notas
└── scripts/
    └── build_data.py        # markdown → json → sql/sqlite → release
```

**`content/` é a fonte da verdade.** Toda correção se faz no Markdown de
`content/markdown/` e se propaga pelo build. Nada em `release/` deve ser editado
à mão — é sobrescrito a cada execução.

## 📱 Como ler

**Publicado em:** <https://nilknarfsam.github.io/traducao_biblia/release/>

Servido por GitHub Pages a partir de `main` / `(root)`, então cada push
republica automaticamente. Alternativa offline: clonar o repositório e abrir
`release/index.html` no navegador.

Uma ressalva que vale saber: **abrir o `.html` pelo app do GitHub não funciona** —
o GitHub descarta estilo inline e mostra o código-fonte. O release é HTML
justamente porque a marcação de locutor por cor não sobrevive ao Markdown. Use
sempre o endereço acima, nunca o arquivo pela interface do repositório.

## ⚡ Pipeline

```bash
python scripts/build_data.py
```

Lê `content/markdown/`, valida a marcação de locutor (falha se houver marcador
sem par) e regenera JSON, SQL, SQLite e o release HTML.

## 📄 Licença

O projeto tem **duas licenças**, deliberadamente separadas:

| O quê | Licença |
|---|---|
| Tradução, notas, glossário, docs, dados derivados | [CC BY-SA 4.0](LICENSE-TEXTO.md) |
| Código (`scripts/`) | [MIT](LICENSE) |

A maioria das traduções bíblicas modernas em português é fechada. A TKC é aberta
de propósito: livre para copiar, adaptar e usar — inclusive comercialmente —
desde que **atribuída** e mantida sob a **mesma licença**, para que ninguém possa
fechar o que nasceu aberto.

O texto grego base (SBLGNT, Nestle-Aland) permanece sob os termos de seus
detentores; a TKC licencia apenas o que é criação própria deste projeto.

> Tradução Koiné Contemporânea (TKC), © 2026 Franklin Carvalho, licenciada sob
> CC BY-SA 4.0.
