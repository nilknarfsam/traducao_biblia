#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de automação para o projeto de Tradução Bíblica:
1. Faz o parse dos arquivos Markdown em content/markdown/
2. Gera os arquivos JSON estruturados em content/json/
3. Gera o script SQL de schema e carga em content/sql/schema_and_seed.sql
4. Cria e popula o banco de dados SQLite content/sql/biblia.db
"""

import os
import sys
import re
import json
import sqlite3
from pathlib import Path

# Garante saída UTF-8 no console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


BASE_DIR = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = BASE_DIR / "content" / "markdown"
JSON_DIR = BASE_DIR / "content" / "json"
SQL_DIR = BASE_DIR / "content" / "sql"
RELEASE_DIR = BASE_DIR / "release"

# Identidade da versão. Alterar aqui propaga para o release, o índice e o banco.
VERSION_NAME = "Tradução Koiné Contemporânea"
VERSION_ABBR = "TKC"
VERSION_LICENSE = "CC BY-SA 4.0"
VERSION_LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br"

# Quebras de parágrafo do release, por capítulo: número do último versículo de
# cada parágrafo. São decisão editorial (perícopes), não dado do manuscrito —
# o grego não tem parágrafos. Sem entrada aqui, o capítulo sai num bloco só e o
# build avisa.
PARAGRAPH_BREAKS = {
    "JHN.1": [5, 8, 13, 14, 18, 28, 34, 42, 51],
    "JHN.2": [5, 11, 12, 17, 22, 25],
    "JHN.3": [2, 8, 15, 21, 24, 30, 36],
}

# Marcadores de locutor na Tradução Fluente Autoral (ver guia_traducao.md, R11).
# O texto armazenado em translation_text é sempre limpo; os trechos ficam em
# speech_spans, para que a renderização (cor, itálico, barra) seja decisão do app.
SPEAKER_CODES = {
    "J": "JESUS",       # fala de Jesus
    "D": "DEUS",        # fala de Deus / YHWH
    "E": "ESCRITURA",   # citação do Antigo Testamento
}
SPEAKER_MARKER_RE = re.compile(r"\[\[(/?)([A-Z])\]\]")


def extract_speech_spans(text: str):
    """Remove os marcadores de locutor e devolve (texto_limpo, spans).

    Cada span traz o código do locutor e os offsets de caractere no texto limpo,
    de modo que qualquer renderizador possa reconstruir a marcação sem depender
    de HTML embutido no conteúdo.
    """
    if not text:
        return text, []

    limpo = []
    spans = []
    abertos = []
    pos = 0
    cursor = 0

    for m in SPEAKER_MARKER_RE.finditer(text):
        limpo.append(text[cursor:m.start()])
        pos += m.start() - cursor
        cursor = m.end()
        fechando, letra = m.group(1) == "/", m.group(2)
        if letra not in SPEAKER_CODES:
            raise ValueError(f"Marcador de locutor desconhecido: [[{m.group(1)}{letra}]]")
        if fechando:
            if not abertos or abertos[-1][0] != letra:
                raise ValueError(f"Marcador [[/{letra}]] sem abertura correspondente")
            _, inicio = abertos.pop()
            spans.append({
                "speaker": SPEAKER_CODES[letra],
                "start": inicio,
                "end": pos,
            })
        else:
            abertos.append((letra, pos))

    if abertos:
        raise ValueError(f"Marcador [[{abertos[-1][0]}]] não foi fechado")

    limpo.append(text[cursor:])
    spans.sort(key=lambda s: s["start"])
    return "".join(limpo), spans


def apply_spans_html(text: str, spans) -> str:
    """Envolve os trechos marcados em <span class="fala-..."> para o release HTML."""
    import html as _html

    if not spans:
        return _html.escape(text)

    pedacos = []
    cursor = 0
    for s in spans:
        pedacos.append(_html.escape(text[cursor:s["start"]]))
        classe = "fala-" + s["speaker"].lower()
        pedacos.append(f'<span class="{classe}">{_html.escape(text[s["start"]:s["end"]])}</span>')
        cursor = s["end"]
    pedacos.append(_html.escape(text[cursor:]))
    return "".join(pedacos)


BOOK_METADATA = {
    "01_mateus": {"id": "MAT", "name": "Mateus", "testament": "NT", "order": 40},
    "02_marcos": {"id": "MRK", "name": "Marcos", "testament": "NT", "order": 41},
    "03_lucas": {"id": "LUK", "name": "Lucas", "testament": "NT", "order": 42},
    "04_joao": {"id": "JHN", "name": "João", "testament": "NT", "order": 43},
    "05_atos": {"id": "ACT", "name": "Atos", "testament": "NT", "order": 44},
    "06_romanos": {"id": "ROM", "name": "Romanos", "testament": "NT", "order": 45},
    "07_1corintios": {"id": "1CO", "name": "1 Coríntios", "testament": "NT", "order": 46},
    "08_2corintios": {"id": "2CO", "name": "2 Coríntios", "testament": "NT", "order": 47},
    "09_galatas": {"id": "GAL", "name": "Gálatas", "testament": "NT", "order": 48},
    "10_efesios": {"id": "EPH", "name": "Efésios", "testament": "NT", "order": 49},
    "11_filipenses": {"id": "PHP", "name": "Filipenses", "testament": "NT", "order": 50},
    "12_colossenses": {"id": "COL", "name": "Colossenses", "testament": "NT", "order": 51},
    "13_1tessalonicenses": {"id": "1TH", "name": "1 Tessalonicenses", "testament": "NT", "order": 52},
    "14_2tessalonicenses": {"id": "2TH", "name": "2 Tessalonicenses", "testament": "NT", "order": 53},
    "15_1timoteo": {"id": "1TI", "name": "1 Timóteo", "testament": "NT", "order": 54},
    "16_2timoteo": {"id": "2TI", "name": "2 Timóteo", "testament": "NT", "order": 55},
    "17_tito": {"id": "TIT", "name": "Tito", "testament": "NT", "order": 56},
    "18_filemom": {"id": "PHM", "name": "Filemom", "testament": "NT", "order": 57},
    "19_hebreus": {"id": "HEB", "name": "Hebreus", "testament": "NT", "order": 58},
    "20_tiago": {"id": "JAS", "name": "Tiago", "testament": "NT", "order": 59},
    "21_1pedro": {"id": "1PE", "name": "1 Pedro", "testament": "NT", "order": 60},
    "22_2pedro": {"id": "2PE", "name": "2 Pedro", "testament": "NT", "order": 61},
    "23_1joao": {"id": "1JN", "name": "1 João", "testament": "NT", "order": 62},
    "24_2joao": {"id": "2JN", "name": "2 João", "testament": "NT", "order": 63},
    "25_3joao": {"id": "3JN", "name": "3 João", "testament": "NT", "order": 64},
    "26_judas": {"id": "JUD", "name": "Judas", "testament": "NT", "order": 65},
    "27_apocalipse": {"id": "REV", "name": "Apocalipse", "testament": "NT", "order": 66},
}

# Template sem <html>/<head>/<body> de propósito: o parser HTML5 supre esses
# elementos ao abrir o arquivo direto, e o mesmo arquivo serve como página
# publicável sem reescrita. O <meta charset> vem primeiro para valer nos dois casos.
HTML_TEMPLATE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · {sigla}</title>
<style>
  /* Paleta acromática de propósito: as duas únicas cores da página são as do
     próprio texto — a fala de Jesus e a fala de Deus. Nada mais compete. */
  :root {{
    --papel: #fafbfc;
    --tinta: #1a1d21;
    --ardosia: #69737f;
    --regua: #dde2e8;
    --jesus: #9e1b1b;
    --deus: #1b4f8f;
    --realce: rgba(27, 79, 143, .10);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --papel: #14171a;
      --tinta: #e6e8ea;
      --ardosia: #8b949e;
      --regua: #2a2f35;
      --jesus: #f09a92;
      --deus: #8fb6e8;
      --realce: rgba(143, 182, 232, .14);
    }}
  }}
  :root[data-theme="dark"] {{
    --papel: #14171a;
    --tinta: #e6e8ea;
    --ardosia: #8b949e;
    --regua: #2a2f35;
    --jesus: #f09a92;
    --deus: #8fb6e8;
    --realce: rgba(143, 182, 232, .14);
  }}

  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    padding: 2.5rem 1.35rem 5rem;
    background: var(--papel);
    color: var(--tinta);
    font-family: "Iowan Old Style", "Palatino Linotype", Palatino,
                 "Book Antiqua", Georgia, serif;
    font-size: 1.15rem;
    line-height: 1.8;
    -webkit-text-size-adjust: 100%;
    text-rendering: optimizeLegibility;
  }}

  main {{ max-width: 34rem; margin: 0 auto; }}

  .capa {{ display: flex; flex-direction: column; gap: .5rem; }}
  h1 {{
    font-size: 2.4rem; font-weight: 400; margin: 0;
    letter-spacing: -.015em; text-wrap: balance;
  }}
  .creditos {{
    margin: 0; color: var(--ardosia); font-size: .95rem;
    font-style: italic; line-height: 1.5; text-wrap: pretty;
  }}

  .legenda {{
    display: flex; flex-wrap: wrap; gap: .3rem 1.25rem;
    margin: 1.75rem 0 2.5rem; padding: .75rem 0;
    border-top: 1px solid var(--regua); border-bottom: 1px solid var(--regua);
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .78rem; line-height: 1.5; color: var(--ardosia);
  }}
  .legenda b {{ font-weight: 600; }}

  h2 {{
    margin: 3rem 0 1.25rem;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .74rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .16em; color: var(--ardosia);
  }}
  h2:first-of-type {{ margin-top: 2rem; }}

  p.texto {{ margin: 0 0 1.4rem; hyphens: auto; }}

  .vn {{
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .62em; font-weight: 600; vertical-align: super;
    line-height: 0; margin-right: .15em; color: var(--ardosia);
    text-decoration: none;
  }}
  a.vn:hover, a.vn:focus-visible {{ color: var(--tinta); }}

  .fala-jesus {{ color: var(--jesus); }}
  .fala-deus {{ color: var(--deus); }}
  .fala-escritura {{ font-variant: small-caps; letter-spacing: .03em; }}

  h3 {{
    margin: 3.5rem 0 1.5rem; padding-top: 1.75rem;
    border-top: 1px solid var(--regua);
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .74rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .16em; color: var(--ardosia);
  }}

  ol.notas {{
    margin: 0; padding: 0; list-style: none;
    display: flex; flex-direction: column; gap: 1.15rem;
    font-size: .95rem; line-height: 1.65; color: var(--ardosia);
  }}
  ol.notas li {{ scroll-margin-top: 1.5rem; }}
  ol.notas b {{ color: var(--tinta); font-weight: 600; }}
  ol.notas i {{ font-style: italic; }}
  .volta {{
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .72rem; font-weight: 600; text-decoration: none;
    color: var(--ardosia); border-bottom: 1px solid var(--regua);
  }}
  .volta:hover, .volta:focus-visible {{ color: var(--tinta); }}

  .selo, .indice {{
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .74rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .14em; color: var(--ardosia);
  }}
  .selo {{ margin: 0; }}
  .indice {{ display: inline-block; margin-bottom: 2rem; text-decoration: none; }}
  .indice:hover, .indice:focus-visible {{ color: var(--tinta); }}

  /* Menu de capítulos: aparece só a partir do segundo capítulo traduzido. */
  .capitulos {{
    display: flex; flex-wrap: wrap; gap: .4rem;
    margin: 1.75rem 0 0;
  }}
  .capitulos a {{
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 2.4rem; height: 2.4rem; padding: 0 .5rem;
    border: 1px solid var(--regua); border-radius: 3px;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .9rem; font-variant-numeric: tabular-nums;
    color: var(--ardosia); text-decoration: none;
  }}
  .capitulos a:hover, .capitulos a:focus-visible {{
    color: var(--tinta); border-color: var(--ardosia);
  }}

  h2 {{ scroll-margin-top: 1.5rem; }}

  :target {{ background: var(--realce); border-radius: 2px; }}
  a:focus-visible, [id]:focus-visible {{
    outline: 2px solid var(--deus); outline-offset: 3px;
  }}
</style>

<main>
{volta_indice}
<header class="capa">
  <p class="selo">{versao} · {sigla}</p>
  <h1>{titulo}</h1>
  <p class="creditos">Tradução do Grego Koiné para o português contemporâneo, a partir
  dos textos críticos (SBLGNT / Nestle-Aland).</p>
</header>
{menu}
<div class="legenda">
  <span><b class="fala-jesus">Vermelho</b> — palavras de Jesus</span>
  <span><b class="fala-deus">Azul</b> — palavras de Deus</span>
  <span><b class="fala-escritura">Versalete</b> — citação do Antigo Testamento</span>
</div>

{corpo}
</main>
"""


INDEX_TEMPLATE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{versao}</title>
<style>
  :root {{
    --papel: #fafbfc; --tinta: #1a1d21; --ardosia: #69737f;
    --regua: #dde2e8; --deus: #1b4f8f;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --papel: #14171a; --tinta: #e6e8ea; --ardosia: #8b949e;
      --regua: #2a2f35; --deus: #8fb6e8;
    }}
  }}
  :root[data-theme="dark"] {{
    --papel: #14171a; --tinta: #e6e8ea; --ardosia: #8b949e;
    --regua: #2a2f35; --deus: #8fb6e8;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 3.5rem 1.35rem 5rem;
    background: var(--papel); color: var(--tinta);
    font-family: "Iowan Old Style", "Palatino Linotype", Palatino,
                 "Book Antiqua", Georgia, serif;
    font-size: 1.1rem; line-height: 1.7;
    -webkit-text-size-adjust: 100%;
  }}
  main {{ max-width: 34rem; margin: 0 auto; }}
  .selo {{
    margin: 0 0 .5rem;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .74rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .14em; color: var(--ardosia);
  }}
  h1 {{ font-size: 2.4rem; font-weight: 400; margin: 0 0 .6rem;
       letter-spacing: -.015em; text-wrap: balance; }}
  .creditos {{ margin: 0 0 2.5rem; color: var(--ardosia); font-size: .95rem;
              font-style: italic; line-height: 1.5; text-wrap: pretty; }}
  ul {{ list-style: none; margin: 0; padding: 0;
       display: flex; flex-direction: column; }}
  li a {{
    display: flex; align-items: baseline; justify-content: space-between; gap: 1rem;
    padding: 1rem .25rem; border-bottom: 1px solid var(--regua);
    color: inherit; text-decoration: none;
  }}
  li:first-child a {{ border-top: 1px solid var(--regua); }}
  li a:hover .livro, li a:focus-visible .livro {{ color: var(--deus); }}
  .livro {{ font-size: 1.35rem; }}
  .qtd {{
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .8rem; color: var(--ardosia); white-space: nowrap;
    font-variant-numeric: tabular-nums;
  }}
  footer {{
    margin-top: 3.5rem; padding-top: 1.5rem; border-top: 1px solid var(--regua);
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    font-size: .8rem; line-height: 1.6; color: var(--ardosia);
  }}
  footer a {{ color: inherit; }}
  a:focus-visible {{ outline: 2px solid var(--deus); outline-offset: 3px; }}
</style>

<main>
<p class="selo">{sigla}</p>
<h1>{versao}</h1>
<p class="creditos">Tradução do Grego Koiné para o português contemporâneo, a partir
dos textos críticos (SBLGNT / Nestle-Aland), com notas exegéticas e culturais.</p>

<ul>
{itens}
</ul>

<footer>
Texto da tradução e notas sob licença {licenca}. Livre para copiar, adaptar e usar,
inclusive comercialmente, desde que atribuído e mantido sob a mesma licença.
</footer>
</main>
"""


def clean_blockquote(text: str) -> str:
    """Limpa marcações de citação em bloco (> ) e quebras de linha extras."""
    lines = []
    for line in text.strip().split("\n"):
        line = re.sub(r"^\s*>\s?", "", line).strip()
        if line:
            lines.append(line)
    return " ".join(lines)

def parse_markdown_chapter(file_path: Path, book_folder: str):
    """Lê um arquivo Markdown de capítulo e retorna dados estruturados."""
    meta = BOOK_METADATA.get(book_folder, {
        "id": book_folder.upper()[:3],
        "name": book_folder.replace("_", " ").title(),
        "testament": "NT" if "nt" in str(file_path).lower() else "OT",
        "order": 99
    })

    content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

    
    # Extrai o número do capítulo do cabeçalho
    chapter_match = re.search(r"#\s+.*?Capítulo\s+(\d+)", content, re.IGNORECASE)
    if not chapter_match:
        file_chapter_match = re.search(r"capitulo_(\d+)", file_path.name, re.IGNORECASE)
        chapter_num = int(file_chapter_match.group(1)) if file_chapter_match else 1
    else:
        chapter_num = int(chapter_match.group(1))

    verse_blocks = re.split(r"(?=^##\s+)", content, flags=re.MULTILINE)
    
    verses = []
    for block in verse_blocks:
        if not block.strip() or block.strip().startswith("# "):
            continue
        
        v_header_match = re.search(r"^##\s+(?:.*?\s+)?(\d+):(\d+)", block, re.MULTILINE)
        if not v_header_match:
            continue
        
        c_num = int(v_header_match.group(1))
        v_num = int(v_header_match.group(2))
        verse_id = f"{meta['id']}.{c_num}.{v_num}"

        def extract_blockquote_section(section_header: str) -> str:
            if section_header not in block:
                return ""
            part = block.split(section_header, 1)[1]
            lines = []
            for line in part.split("\n"):
                line_str = line.strip()
                if line_str.startswith(">"):
                    lines.append(line_str.lstrip(">").strip())
                elif line_str.startswith("**") or line_str.startswith("##") or line_str.startswith("-"):
                    if lines:  # se já coletou as linhas do blockquote desta seção
                        break
            return " ".join(lines)

        greek_text = extract_blockquote_section("**Grego")
        literal_text = extract_blockquote_section("**Tradução Literal")
        translation_raw = extract_blockquote_section("**Tradução Fluente")
        try:
            translation_text, speech_spans = extract_speech_spans(translation_raw)
        except ValueError as err:
            raise ValueError(f"{file_path.name} {c_num}:{v_num} — {err}") from err


        # Extrai Notas Exegéticas
        notes = []
        if "**Notas Exegéticas" in block:
            notes_part = block.split("**Notas Exegéticas", 1)[1]
            # Remove o resto do cabeçalho da linha de notas
            if "\n" in notes_part:
                notes_raw = notes_part.split("\n", 1)[1].strip()
            else:
                notes_raw = ""
            
            raw_items = re.split(r"(?=^-\s+\*\*)", notes_raw, flags=re.MULTILINE)
            for item in raw_items:
                item = item.strip()
                if not item.startswith("-"):
                    continue
                # Remove o hífen inicial
                item_content = re.sub(r"^-\s*", "", item).strip()
                bold_match = re.search(r"^\*\*(.+?)\*\*:?\s*(.*)$", item_content, re.DOTALL)
                if bold_match:
                    header = bold_match.group(1).rstrip(":")
                    explanation = bold_match.group(2).strip()
                    explanation = " ".join(line.strip() for line in explanation.split("\n") if line.strip())

                    # Separa Termo e Lema grego/transliteração
                    if "(" in header and ")" in header:
                        term_part = header[:header.find("(")].strip()
                        lemma_part = header[header.find("(") + 1:header.rfind(")")].strip()
                    else:
                        term_part = header.strip()
                        lemma_part = ""

                    notes.append({
                        "term": term_part,
                        "greek_lemma": lemma_part,
                        "explanation": explanation
                    })



        verses.append({
            "verse_id": verse_id,
            "book_id": meta["id"],
            "chapter": c_num,
            "verse": v_num,
            "greek_text": greek_text,
            "literal_text": literal_text,
            "translation_text": translation_text,
            "speech_spans": speech_spans,
            "notes": notes
        })

    return {
        "book_id": meta["id"],
        "book_name": meta["name"],
        "testament": meta["testament"],
        "order_index": meta["order"],
        "chapter": chapter_num,
        "chapter_id": f"{meta['id']}.{chapter_num}",
        "verses": verses
    }

def main():
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    SQL_DIR.mkdir(parents=True, exist_ok=True)

    all_books = {}
    all_chapters = []
    all_verses = []
    all_chapters_data = []

    print("🔍 Iniciando leitura dos arquivos Markdown...")
    for root, _, files in os.walk(MARKDOWN_DIR):
        for file in sorted(files):
            if file.endswith(".md"):
                file_path = Path(root) / file
                book_folder = file_path.parent.name
                testament_folder = file_path.parent.parent.name
                
                print(f"📖 Processando: {file_path.relative_to(BASE_DIR)}")
                data = parse_markdown_chapter(file_path, book_folder)
                
                book_id = data["book_id"]
                if book_id not in all_books:
                    all_books[book_id] = {
                        "id": book_id,
                        "name": data["book_name"],
                        "testament": data["testament"],
                        "order_index": data["order_index"]
                    }
                
                chapter_dict = {
                    "id": data["chapter_id"],
                    "book_id": book_id,
                    "chapter_number": data["chapter"]
                }
                all_chapters.append(chapter_dict)
                all_verses.extend(data["verses"])
                all_chapters_data.append((book_id, data, testament_folder, book_folder))

                # Salva arquivo JSON
                out_json_dir = JSON_DIR / testament_folder
                out_json_dir.mkdir(parents=True, exist_ok=True)
                out_json_file = out_json_dir / f"{book_folder}_{data['chapter']:02d}.json"
                with open(out_json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"   ↳ JSON gerado: {out_json_file.relative_to(BASE_DIR)}")


    # Agrupa capítulos por livro
    book_chapters_map = {}
    for (b_id, c_data, t_folder, b_folder) in all_chapters_data:
        if b_id not in book_chapters_map:
            book_chapters_map[b_id] = {
                "name": c_data["book_name"],
                "testament_folder": t_folder,
                "book_folder": b_folder,
                "order_index": c_data["order_index"],
                "chapters": []
            }
        book_chapters_map[b_id]["chapters"].append(c_data)

    # Release: HTML é o único formato de leitura. O Markdown foi descontinuado
    # porque o GitHub descarta estilo inline e a marcação de locutor (R11)
    # ficava invisível. As fontes de dados para o app seguem em content/.
    print("\n📖 Gerando release de leitura em release/...")
    import html as _html
    superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    for b_id, b_info in book_chapters_map.items():
        html_testament_dir = RELEASE_DIR / b_info["testament_folder"]
        html_testament_dir.mkdir(parents=True, exist_ok=True)
        html_book_file = html_testament_dir / f"{b_info['book_folder']}.html"

        capitulos_ord = sorted(b_info["chapters"], key=lambda x: x["chapter"])

        # Menu de capítulos: só aparece quando há mais de um capítulo traduzido.
        menu = ""
        if len(capitulos_ord) > 1:
            chips = "".join(
                f'<a href="#cap-{ch["chapter"]}">{ch["chapter"]}</a>'
                for ch in capitulos_ord
            )
            menu = f'<nav class="capitulos" aria-label="Capítulos">{chips}</nav>'

        corpo = []
        for chap in capitulos_ord:
            c = chap["chapter"]
            quebras = PARAGRAPH_BREAKS.get(f"{b_id}.{c}")
            if quebras is None:
                quebras = []
                print(f"   ⚠️  Sem quebras de parágrafo para {b_id}.{c} — "
                      f"defina PARAGRAPH_BREAKS['{b_id}.{c}'] em build_data.py")
            corpo.append(f'<h2 id="cap-{c}">Capítulo {c}</h2>')
            paragrafos, atual, notas_cap = [], [], []
            for v in chap["verses"]:
                v_num = v["verse"]
                v_sup = str(v_num).translate(superscript_digits)
                marcado = apply_spans_html(v["translation_text"], v.get("speech_spans", []))
                # O número do versículo é a âncora do aparato: quem tem nota vira
                # link para ela, e a nota devolve o leitor ao versículo.
                if v["notes"]:
                    numero = f'<a class="vn" id="v{c}-{v_num}" href="#n{c}-{v_num}">{v_sup}</a>'
                else:
                    numero = f'<span class="vn" id="v{c}-{v_num}">{v_sup}</span>'
                atual.append(f"{numero} {marcado}")
                for n in v["notes"]:
                    notas_cap.append((v_num, n))
                if v_num in quebras:
                    paragrafos.append(" ".join(atual))
                    atual = []
            if atual:
                paragrafos.append(" ".join(atual))
            corpo.extend(f'<p class="texto">{p}</p>' for p in paragrafos)

            if notas_cap:
                corpo.append(f"<h3>Notas exegéticas e culturais — capítulo {c}</h3>")
                corpo.append('<ol class="notas">')
                vistos = set()
                for v_num, n in notas_cap:
                    lemma = n["greek_lemma"].replace("*", "").strip()
                    lemma_str = f" (<i>{_html.escape(lemma)}</i>)" if lemma else ""
                    id_attr = ""
                    if v_num not in vistos:  # âncora na primeira nota de cada versículo
                        id_attr = f' id="n{c}-{v_num}"'
                        vistos.add(v_num)
                    corpo.append(
                        f"<li{id_attr}>"
                        f'<a class="volta" href="#v{c}-{v_num}">v. {v_num}</a> '
                        f'<b>{_html.escape(n["term"])}{lemma_str}:</b> '
                        f'{_html.escape(n["explanation"])}</li>'
                    )
                corpo.append("</ol>")

        pagina = HTML_TEMPLATE.format(
            titulo=_html.escape(b_info["name"]),
            versao=VERSION_NAME,
            sigla=VERSION_ABBR,
            menu=menu,
            # Com um único livro traduzido o índice não tem o que indexar, e o
            # link quebraria ao ler a página fora da árvore de arquivos.
            volta_indice=(
                '<a class="indice" href="../index.html">← todos os livros</a>'
                if len(book_chapters_map) > 1 else ""
            ),
            corpo="\n".join(corpo),
        )
        html_book_file.write_text(pagina, encoding="utf-8")
        print(f"   ↳ {html_book_file.relative_to(BASE_DIR)}")

    # Índice de livros: porta de entrada da leitura.
    livros_ord = sorted(book_chapters_map.items(), key=lambda kv: kv[1]["order_index"])
    itens = []
    for b_id, b_info in livros_ord:
        n_caps = len(b_info["chapters"])
        caps_txt = "1 capítulo" if n_caps == 1 else f"{n_caps} capítulos"
        href = f'{b_info["testament_folder"]}/{b_info["book_folder"]}.html'
        itens.append(
            f'<li><a href="{href}"><span class="livro">{_html.escape(b_info["name"])}</span>'
            f'<span class="qtd">{caps_txt}</span></a></li>'
        )
    indice_file = RELEASE_DIR / "index.html"
    indice_file.write_text(
        INDEX_TEMPLATE.format(
            versao=VERSION_NAME,
            sigla=VERSION_ABBR,
            licenca=VERSION_LICENSE,
            itens="\n".join(itens),
        ),
        encoding="utf-8",
    )
    print(f"   ↳ {indice_file.relative_to(BASE_DIR)}")

    print("\n💾 Gerando schema e sementes SQL...")
    sql_schema = """-- ==============================================================================
-- Schema para Banco de Dados da Tradução Bíblica (SQLite / PostgreSQL)
-- ==============================================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS translation_meta;
DROP TABLE IF EXISTS verse_speech_spans;
DROP TABLE IF EXISTS verse_notes;
DROP TABLE IF EXISTS verses;
DROP TABLE IF EXISTS chapters;
DROP TABLE IF EXISTS books;

-- Identidade da versão. O app deve exibir nome, sigla e licença ao usuário:
-- a CC BY-SA 4.0 exige atribuição e indicação da licença em qualquer uso.
CREATE TABLE translation_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE books (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    testament TEXT NOT NULL CHECK(testament IN ('OT', 'NT')),
    order_index INTEGER NOT NULL
);

CREATE TABLE chapters (
    id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL,
    chapter_number INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE verses (
    id TEXT PRIMARY KEY,
    chapter_id TEXT NOT NULL,
    book_id TEXT NOT NULL,
    chapter_number INTEGER NOT NULL,
    verse_number INTEGER NOT NULL,
    greek_text TEXT,
    literal_text TEXT,
    translation_text TEXT NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE verse_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id TEXT NOT NULL,
    term TEXT NOT NULL,
    greek_lemma TEXT,
    explanation TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (verse_id) REFERENCES verses(id) ON DELETE CASCADE
);

-- Trechos de fala atribuída, com offsets de caractere em verses.translation_text.
-- Guarda o LOCUTOR, não a cor: a renderização (vermelho para Jesus, azul para
-- Deus, versalete para citação do AT, ou nenhuma) é decisão da camada de
-- apresentação e deve ser desativável pelo leitor.
CREATE TABLE verse_speech_spans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id TEXT NOT NULL,
    speaker TEXT NOT NULL CHECK(speaker IN ('JESUS', 'DEUS', 'ESCRITURA')),
    start_offset INTEGER NOT NULL,
    end_offset INTEGER NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (verse_id) REFERENCES verses(id) ON DELETE CASCADE
);

CREATE INDEX idx_verses_lookup ON verses(book_id, chapter_number, verse_number);
CREATE INDEX idx_notes_verse ON verse_notes(verse_id);
CREATE INDEX idx_spans_verse ON verse_speech_spans(verse_id);

-- ==============================================================================
-- SEED DATA
-- ==============================================================================
"""

    def sql_escape(s) -> str:
        if s is None:
            return "NULL"
        return "'" + str(s).replace("'", "''") + "'"

    sql_statements = [sql_schema]

    for k, val in [
        ("name", VERSION_NAME),
        ("abbreviation", VERSION_ABBR),
        ("language", "pt-BR"),
        ("source_text", "SBLGNT / Nestle-Aland / Macula Greek"),
        ("license", VERSION_LICENSE),
        ("license_url", VERSION_LICENSE_URL),
    ]:
        sql_statements.append(
            f"INSERT INTO translation_meta (key, value) VALUES ({sql_escape(k)}, {sql_escape(val)});"
        )

    for b in all_books.values():
        stmt = f"INSERT INTO books (id, name, testament, order_index) VALUES ({sql_escape(b['id'])}, {sql_escape(b['name'])}, {sql_escape(b['testament'])}, {b['order_index']});"
        sql_statements.append(stmt)

    for c in all_chapters:
        stmt = f"INSERT INTO chapters (id, book_id, chapter_number) VALUES ({sql_escape(c['id'])}, {sql_escape(c['book_id'])}, {c['chapter_number']});"
        sql_statements.append(stmt)

    for v in all_verses:
        chapter_fk = f"{v['book_id']}.{v['chapter']}"
        stmt = (
            f"INSERT INTO verses (id, chapter_id, book_id, chapter_number, verse_number, greek_text, literal_text, translation_text) "
            f"VALUES ({sql_escape(v['verse_id'])}, {sql_escape(chapter_fk)}, {sql_escape(v['book_id'])}, {v['chapter']}, {v['verse']}, "
            f"{sql_escape(v['greek_text'])}, {sql_escape(v['literal_text'])}, {sql_escape(v['translation_text'])});"
        )
        sql_statements.append(stmt)

        for idx, s in enumerate(v.get("speech_spans", []), start=1):
            span_stmt = (
                f"INSERT INTO verse_speech_spans (verse_id, speaker, start_offset, end_offset, order_index) "
                f"VALUES ({sql_escape(v['verse_id'])}, {sql_escape(s['speaker'])}, {s['start']}, {s['end']}, {idx});"
            )
            sql_statements.append(span_stmt)

        for idx, n in enumerate(v["notes"], start=1):
            note_stmt = (
                f"INSERT INTO verse_notes (verse_id, term, greek_lemma, explanation, order_index) "
                f"VALUES ({sql_escape(v['verse_id'])}, {sql_escape(n['term'])}, {sql_escape(n['greek_lemma'])}, {sql_escape(n['explanation'])}, {idx});"
            )
            sql_statements.append(note_stmt)

    seed_sql_file = SQL_DIR / "schema_and_seed.sql"
    with open(seed_sql_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements) + "\n")
    print(f"✅ Arquivo SQL gerado: {seed_sql_file.relative_to(BASE_DIR)}")

    db_file = SQL_DIR / "biblia.db"
    if db_file.exists():
        db_file.unlink()
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executescript("\n".join(sql_statements))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM books;")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM chapters;")
    total_chapters = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM verses;")
    total_verses = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM verse_notes;")
    total_notes = cursor.fetchone()[0]
    conn.close()

    print(f"✅ Banco SQLite criado com sucesso em: {db_file.relative_to(BASE_DIR)}")
    print(f"📊 Estatísticas: {total_books} livros, {total_chapters} capítulos, {total_verses} versículos, {total_notes} notas exegéticas carregadas com sucesso!")

if __name__ == "__main__":
    main()
