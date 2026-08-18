# Guia de Tradução e Diretrizes Exegéticas

Este documento define os princípios metodológicos, teológicos, linguísticos e técnicos para o projeto de tradução autoral do Novo Testamento a partir do Grego Koiné.

## 0. Identidade da Versão

| Campo | Valor |
|---|---|
| **Nome** | Tradução Koiné Contemporânea |
| **Sigla** | **TKC** |
| **Idioma** | Português brasileiro contemporâneo |
| **Texto-base** | SBLGNT / Nestle-Aland / Macula Greek |
| **Licença do texto** | CC BY-SA 4.0 — ver `LICENSE-TEXTO.md` |
| **Licença do código** | MIT — ver `LICENSE` |

A sigla **TKC** é a forma de citação (`Jo 1:5 TKC`). O nome e a licença são gravados na tabela `translation_meta` do banco e exibidos no release; alterá-los se faz em um único ponto, nas constantes do topo de `scripts/build_data.py`.

A licença CC BY-SA exige que qualquer uso **atribua** a versão e **indique a licença**. O aplicativo deve exibir ambos.

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

## 1-A. Princípios de Fluência e Fidelidade (Regras Operacionais)

Estas regras são vinculantes para a **Tradução Fluente Autoral**. Elas partem de uma premissa: *explicitação é adição, e adição é infidelidade*. O texto fluente não faz o trabalho das outras duas camadas — a estrutura grega vive na Tradução Literal de Apoio, e a nuance semântica vive nas Notas Exegéticas.

### R1 — Proibido o dupleto glosador
Um termo grego recebe **uma** solução em português. Se o termo é polissêmico, escolhe-se a leitura primária e o resto vai para a nota.

- ❌ "as trevas não conseguiram extingui-la **nem prevalecer contra ela**" (dois verbos para *κατέλαβεν*)
- ✅ "e a escuridão não a venceu" — o duplo sentido de *katalambanō* fica na nota.
- ❌ "ele concedeu **o direito e a autoridade**" (dois substantivos para *ἐξουσίαν*)
- ✅ "ele deu o direito"

### R2 — Proibida a didascália
O narrador de João não descreve estados de espírito. O tradutor tampouco.

- ❌ "Natanael perguntou-lhe **com ceticismo**", "disse-lhe **com autoridade**", "acrescentou **solenemente**"
- ✅ "Natanael lhe disse", "lhe disse", "E disse-lhe" — o grego traz apenas *λέγει* / *εἶπεν*.

### R3 — Um verbo grego, um verbo português
Sem verbos auxiliares, modais ou perífrases que o grego não tem. `οὐ κατέλαβεν` (aoristo simples) não vira "não **conseguiram** extinguir".

### R4 — Preservar a ordem e o tipo das orações
Parataxe grega permanece parataxe. Não converter coordenação (`καί ... καί`) em subordinação.

- ❌ "**embora** o mundo tenha sido criado por meio dele, o mundo não o reconheceu"
- ✅ "e o mundo veio a existir por meio dele, e o mundo não o reconheceu"

Aposto final permanece no fim (Jo 1:12: `τοῖς πιστεύουσιν`); atribuição de citação permanece onde está (Jo 1:23: `καθὼς εἶπεν Ἡσαΐας` fecha o versículo).

### R5 — Anáfora e repetição do original são intocáveis
Se João repete uma palavra, o português repete. Se João repete uma estrutura, o português repete.

- ❌ "nem do **impulso** da carne, nem da **deliberação da vontade** humana" (*θελήματος* nas duas)
- ✅ "nem da **vontade** da carne, nem da **vontade** de homem"
- ❌ Jo 1:20 "confessou abertamente, sem nada ocultar, declarando com franqueza"
- ✅ "Ele confessou e não negou; confessou"

### R6 — Consistência léxica intracapitular obrigatória
A mesma expressão grega recebe a mesma solução em todas as ocorrências do capítulo, salvo justificativa registrada em nota.

- `πρὸς τὸν θεόν` (1:1 e 1:2) → "face a face com Deus" nas duas.
- `ἔμπροσθέν μου γέγονεν, ὅτι πρῶτός μου ἦν` (1:15 e 1:30) → "passou à minha frente, porque existia antes de mim" nas duas.
- `κἀγὼ οὐκ ᾔδειν αὐτόν` (1:31 e 1:33) → "Eu não o conhecia" nas duas.

### R7 — Registro adjetival e adverbial contido
Não promover adjetivo comum a superlativo (`πλήρης` = "cheio", não "transbordante"). Advérbios em -mente só quando traduzem um advérbio grego. Alvo: no máximo 2 por capítulo.

### R8 — Tratamento: "você" universal
O koiné não possui distinção T–V: `σύ`/`ὑμεῖς` são a mesma forma para todos os falantes. Usar "o senhor" cria uma hierarquia ausente do original.

- Todos os personagens usam **você / vocês**, inclusive discípulos dirigindo-se a Jesus.
- A deferência vem do **vocativo**, como no grego: *Ῥαββί* → "Rabi", *διδάσκαλε* → "Mestre", *Κύριε* → "Senhor" (vocativo, substantivo — não é pronome de tratamento e permanece).

### R9 — Logos
`ὁ λόγος` → **"a Palavra"** (substantivo feminino), com **pronomes e concordância no masculino** *ad sensum*, por o referente ser pessoal: "sem **ele** nada veio a existir". Decisão deliberada, priorizando familiaridade e recepção sobre a reprodução do suspense gramatical do grego. Não usar "o Verbo" (calque latino da Vulgata, opaco ao leitor-alvo).

### R10 — Sem glosa cultural embutida
Explicações histórico-culturais vão para a nota, nunca para o texto.

- ❌ "Betsaida, a mesma cidade **costeira**", "não o conhecia **em sua identidade messiânica**"
- ✅ "Betsaida, a cidade de André e de Pedro", "Eu não o conhecia"

**Exceção única:** conversão de unidades de tempo opacas (`ὥρα δεκάτη` → "por volta das quatro da tarde"), sempre acompanhada de nota.

### R11 — Marcação de locutor
Na Tradução Fluente Autoral, trechos de fala atribuída recebem marcadores. **Marca-se o locutor, nunca a cor** — cor é decisão da camada de apresentação.

| Marcador | Locutor | Renderização padrão |
|---|---|---|
| `[[J]]…[[/J]]` | Jesus | vermelho |
| `[[D]]…[[/D]]` | Deus / YHWH — inclusive **dentro do NT** (ex.: Jo 1:33) | azul |
| `[[E]]…[[/E]]` | Citação do Antigo Testamento (ex.: Jo 1:23 = Is 40:3) | versalete, **sem cor** |

Marca-se **apenas o discurso direto**, sem incluir os verbos dicendi nem as aspas. Falas de outros personagens (João Batista, os discípulos, as autoridades) não recebem marcação.

**Fronteiras ambíguas.** Onde termina a fala de Jesus é decisão editorial, não dado do manuscrito — o grego não tem aspas. Os casos disputados em João (3:16-21 e 3:31-36, onde não há consenso se falam Jesus ou o evangelista) devem ser decididos a partir do próprio texto e **registrados em nota exegética**, jamais copiados de outra versão.

**Acessibilidade (vinculante).** Cor não pode ser o único portador de sentido: cerca de 8% dos homens têm deficiência de visão de cores, e vermelho sobre branco é a pior combinação para leitura longa. O app deve oferecer alternativas (cor / itálico / barra lateral / desligado) e permitir desativar a marcação por completo.

**Direitos autorais.** A convenção da letra vermelha (Louis Klopsch, 1899) é domínio público, e convenção tipográfica não é obra protegível (Lei 9.610/98, art. 8º). Livre para uso — desde que as decisões de fronteira sejam próprias, conforme acima.

### Checklist de aceite por capítulo
1. Nenhum dupleto glosador (R1).
2. Nenhum verbo de fala qualificado por advérbio/adjunto ausente no grego (R2).
3. Contagem de verbos por versículo igual à do grego (R3).
4. Ordem das orações conferida contra o grego (R4).
5. Repetições do original mapeadas e preservadas (R5, R6).
6. Advérbios em -mente ≤ 2 (R7).
7. Zero ocorrências de "o senhor" como pronome de tratamento (R8).
8. Todo discurso direto de Jesus, de Deus e toda citação do AT marcados (R11); marcadores balanceados — o `build_data.py` falha se houver marcador sem par.

---

## 2. Glossário Inicial de Termos Teológicos e Exegéticos (Koiné -> Português)

A coluna **Tradução Padrão** admite uma única solução por termo (regra R1). As leituras alternativas pertencem à coluna de nuances e às notas do versículo, nunca ao texto fluente.

| Termo Grego (Transliteração) | Lema / Classe | Tradução Padrão no Contexto | Nuances Exegéticas e Justificativa |
|---|---|---|---|
| **λόγος** (*logos*) | ὁ λόγος (s.m.) | **a Palavra** | Expressa tanto o *Dabar/Memra* do AT (a Palavra criadora e reveladora de Yahweh) quanto a razão cósmica divina (*logos* helenístico). Em João 1, usa-se maiúscula ('a Palavra') para designar a Pessoa do Filho. |
| **πρὸς τὸν θεόν** (*pros ton theon*) | πρός + acusativo | **face a face com Deus** | *Prós* com acusativo expressa orientação relacional direta, proximidade ativa e comunhão contínua, mais expressivo que um estático 'com'. |
| **θεός** (*theos*) [sem artigo] | θεός (s.m. predicativo) | **Deus** | Em João 1:1c (*theos en ho logos*), *theos* é predicativo do sujeito pré-posto sem artigo (Regra de Colwell / nuance qualitativa de Harner), qualificando a natureza do *Logos* sem confundi-lo com a pessoa do Pai (*ton theon*). |
| **ζωή** (*zōē*) | ἡ ζωή (s.f.) | **vida** | Diferente de *bios* (vida biológica/física), *zōē* no corpus joanino refere-se à vida não criada, eterna e divina, participada aos que creem. |
| **φῶς** (*phōs*) | τὸ φῶς (s.n.) | **luz** | Símbolo primário da revelação, verdade moral e salvação divina em contraste com a escuridão (*skotia*). |
| **σκοτία / σκότος** (*skotia / skotos*) | ἡ σκοτία (s.f.) | **escuridão** | A realidade do mundo caído alienado de Deus, incapacitado de sobrepujar (*katelaben*) a revelação divina. |
| **καταλαμβάνω** (*katalambanō*) | καταλαμβάνω (v.) | **vencer** | Verbo de duplo sentido intencional em João 1:5: o mundo nem 'compreendeu' intelectualmente a Luz, nem as trevas conseguiram 'vencê-la/apagá-la' fisicamente. |
| **σάρξ** (*sarx*) | ἡ σάρξ (s.f.) | **carne** | Em João 1:14 (*ho logos sarx egeneto*), denota a encarnação real, plena e vulnerável da divindade na humanidade histórica, refutando qualquer docetismo. |
| **σκηνόω** (*skēnoō*) | σκηνόω (v.) | **armar a tenda** | Alusão direta à *Shekinah* do tabernáculo no deserto (Êxodo 25:8; 40:34), onde a presença manifesta de Deus residia visivelmente entre Seu povo. |
| **δόξα** (*doxa*) | ἡ δόξα (s.f.) | **glória** | Equivalente ao hebraico *Kavod* (peso/glória intrínseca de Deus). |
| **μονογενής** (*monogenēs*) | μονογενής (adj.) | **Filho único** | Etimologicamente derivado de *monos* (único) + *genos* (espécie/tipo), e não de *gennao* (gerar). Expressa a singularidade única e incomparável de Jesus como revelador supremo do Pai. |
| **χάρις** (*charis*) | ἡ χάρις (s.f.) | **graça** | Equivalente ao hebraico *Hesed* (amor pactual constante e leal) quando combinado com *aletheia* (*Hesed ve-Emet* em Êxodo 34:6). |
| **ἀλήθεια** (*alētheia*) | ἡ ἀλήθεια (s.f.) | **verdade** | A realidade divina genuína e fidedigna revelada em Cristo. |
| **ἐξηγέομαι** (*exēgeomai*) | ἐξηγέομαι (v.) | **revelou** | Raiz de 'exegese'. O Filho é o exegeta definitivo do Pai invisível (João 1:18). |

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
- `verse_speech_spans`: id (INTEGER, PK AUTOINCREMENT), verse_id (TEXT, FK), speaker (TEXT: JESUS | DEUS | ESCRITURA), start_offset (INT), end_offset (INT), order_index (INT). Offsets de caractere sobre `verses.translation_text`, que é sempre armazenado **limpo**, sem marcadores. Ver R11.

**Saída de leitura:** `release/` — HTML com índice de livros, menu de capítulos e a marcação de locutor visível. É o único formato de leitura: o Markdown foi descontinuado porque o GitHub descarta estilo inline. `release/` é gerado, nunca editado à mão.
