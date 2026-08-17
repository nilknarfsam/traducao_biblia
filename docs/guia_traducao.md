# Guia de Tradução e Diretrizes Exegéticas

Este documento define os princípios metodológicos, teológicos, linguísticos e técnicos para o projeto de tradução autoral do Novo Testamento a partir do Grego Koiné.

---

## 1. Filosofia de Tradução

1. **Equivalência Dinâmico-Funcional com Rigor Exegético:**
   - O objetivo é comunicar o significado original do texto em Grego Koiné em um português contemporâneo, fluente, natural e de alta dignidade literária, sem cair em arcaísmos desnecessários nem em gírias passageiras.
   - Toda escolha de tradução fluente deve ser justificada por análise gramatical (morfossintaxe, caso, tempo verbal, aspecto, voz) e contexto histórico-cultural do primeiro século.

2. **Três Camadas de Texto:**
   - **Grego Koiné Base:** Texto crítico ecumênico (SBLGNT / NA28 / Macula Greek).
   - **Tradução Literal de Apoio:** Tradução palavra por palavra estruturada para fins de estudo comparativo, evidenciando a sintaxe grega original.
   - **Tradução Fluente Autoral:** A versão principal de leitura devocional e acadêmica no app móvel.

3. **Notas Exegéticas e Culturais Aprofundadas:**
   - Cada versículo recebe notas para termos-chave, nuances verbais (aspecto imperfeito vs. aoristo, particípios, etc.), jogos de palavras (paranomásias), conceitos teológicos do judaísmo do Segundo Templo e filosofia greco-romana do período helenístico.

---

## 2. Glossário Inicial de Termos Teológicos e Exegéticos (Koiné -> Português)

| Termo Grego (Transliteração) | Lema / Classe | Tradução Padrão no Contexto | Nuances Exegéticas e Justificativa |
|---|---|---|---|
| **λόγος** (*logos*) | ὁ λόγος (s.m.) | **Palavra / a Palavra** | Expressa tanto o *Dabar/Memra* do AT (a Palavra criadora e reveladora de Yahweh) quanto a razão cósmica divina (*logos* helenístico). Em João 1, usa-se maiúscula ('a Palavra') para designar a Pessoa do Filho. |
| **πρὸς τὸν θεόν** (*pros ton theon*) | πρός + acusativo | **face a face com Deus / em íntima comunhão com Deus** | *Prós* com acusativo expressa orientação relacional direta, proximidade ativa e comunhão contínua, mais expressivo que um estático 'com'. |
| **θεός** (*theos*) [sem artigo] | θεός (s.m. predicativo) | **Deus / de essência divina** | Em João 1:1c (*theos en ho logos*), *theos* é predicativo do sujeito pré-posto sem artigo (Regra de Colwell / nuance qualitativa de Harner), qualificando a natureza do *Logos* sem confundi-lo com a pessoa do Pai (*ton theon*). |
| **ζωή** (*zōē*) | ἡ ζωή (s.f.) | **vida / a verdadeira Vida** | Diferente de *bios* (vida biológica/física), *zōē* no corpus joanino refere-se à vida não criada, eterna e divina, participada aos que creem. |
| **φῶς** (*phōs*) | τὸ φῶς (s.n.) | **luz** | Símbolo primário da revelação, verdade moral e salvação divina em contraste com a escuridão (*skotia*). |
| **σκοτία / σκότος** (*skotia / skotos*) | ἡ σκοτία (s.f.) | **trevas / escuridão** | A realidade do mundo caído alienado de Deus, incapacitado de sobrepujar (*katelaben*) a revelação divina. |
| **καταλαμβάνω** (*katalambanō*) | καταλαμβάνω (v.) | **compreender / prevalecer contra / apagar** | Verbo de duplo sentido intencional em João 1:5: o mundo nem 'compreendeu' intelectualmente a Luz, nem as trevas conseguiram 'vencê-la/apagá-la' fisicamente. |
| **σάρξ** (*sarx*) | ἡ σάρξ (s.f.) | **carne / ser humano de carne e osso** | Em João 1:14 (*ho logos sarx egeneto*), denota a encarnação real, plena e vulnerável da divindade na humanidade histórica, refutando qualquer docetismo. |
| **σκηνόω** (*skēnoō*) | σκηνόω (v.) | **tabernaculou / habitou entre nós** | Alusão direta à *Shekinah* do tabernáculo no deserto (Êxodo 25:8; 40:34), onde a presença manifesta de Deus residia visivelmente entre Seu povo. |
| **δόξα** (*doxa*) | ἡ δόξα (s.f.) | **glória / majestade radiante** | Equivalente ao hebraico *Kavod* (peso/glória intrínseca de Deus). |
| **μονογενής** (*monogenēs*) | μονογενής (adj.) | **Único / Filho Único e Singular** | Etimologicamente derivado de *monos* (único) + *genos* (espécie/tipo), e não de *gennao* (gerar). Expressa a singularidade única e incomparável de Jesus como revelador supremo do Pai. |
| **χάρις** (*charis*) | ἡ χάρις (s.f.) | **graça / favor imerecido** | Equivalente ao hebraico *Hesed* (amor pactual constante e leal) quando combinado com *aletheia* (*Hesed ve-Emet* em Êxodo 34:6). |
| **ἀλήθεια** (*alētheia*) | ἡ ἀλήθεια (s.f.) | **verdade / fidelidade real** | A realidade divina genuína e fidedigna revelada em Cristo. |
| **ἐξηγέομαι** (*exēgeomai*) | ἐξηγέομαι (v.) | **revelou / deu a conhecer plenamente / explicou** | Raiz de 'exegese'. O Filho é o exegeta definitivo do Pai invisível (João 1:18). |

---

## 3. Padrão de Formatação dos Arquivos Markdown

Cada capítulo deve ser organizado estritamente na seguinte estrutura para possibilitar o parse automatizado via script:

```markdown
# [Nome do Livro] - Capítulo [N]

## [Nome do Livro] [C]:[V]

**Grego (SBLGNT / Nestle 1904):**
> [Texto em Grego com acentuação e pontuação]

**Tradução Literal de Apoio:**
> [Texto literal palavra por palavra]

**Tradução Fluente Autoral:**
> [Tradução contemporânea fluente]

**Notas Exegéticas e Culturais:**
- **[Termo em Português] ([Termo Grego] - *[Transliteração]*):** [Explicação exegética, léxica, sintática ou histórico-cultural.]
```

---

## 4. Estrutura do Banco de Dados Relacional (SQLite)

O pipeline transforma os arquivos Markdown em JSON e popula as seguintes tabelas relacionais:

- `books`: id (TEXT, PK), name (TEXT), testament (TEXT), order_index (INT).
- `chapters`: id (TEXT, PK), book_id (TEXT, FK), chapter_number (INT).
- `verses`: id (TEXT, PK), chapter_id (TEXT, FK), book_id (TEXT), chapter_number (INT), verse_number (INT), greek_text (TEXT), literal_text (TEXT), translation_text (TEXT).
- `verse_notes`: id (INTEGER, PK AUTOINCREMENT), verse_id (TEXT, FK), term (TEXT), greek_lemma (TEXT), explanation (TEXT), order_index (INT).
