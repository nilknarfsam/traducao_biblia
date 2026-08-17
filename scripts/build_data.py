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
RELEASE_DIR = BASE_DIR / "release" / "markdown"


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
        translation_text = extract_blockquote_section("**Tradução Fluente")


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


    # Geração dos arquivos de Leitura Corrida (Release)
    print("\n📚 Gerando versão de leitura corrida em release/markdown/...")
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Agrupa capítulos por livro
    book_chapters_map = {}
    for (b_id, c_data, t_folder, b_folder) in all_chapters_data:
        if b_id not in book_chapters_map:
            book_chapters_map[b_id] = {
                "name": c_data["book_name"],
                "testament_folder": t_folder,
                "book_folder": b_folder,
                "chapters": []
            }
        book_chapters_map[b_id]["chapters"].append(c_data)

    for b_id, b_info in book_chapters_map.items():
        rel_testament_dir = RELEASE_DIR / b_info["testament_folder"]
        rel_testament_dir.mkdir(parents=True, exist_ok=True)
        rel_book_file = rel_testament_dir / f"{b_info['book_folder']}.md"

        lines = [
            f"# {b_info['name']}",
            f"\n> **Tradução Autoral em Português Contemporâneo**",
            f"> Baseada nos textos críticos em Grego Koiné com rigor exegético e equivalência dinâmico-funcional.\n",
            "---\n"
        ]

        # Mapeamento de números para sobrescrito
        superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

        for chap in sorted(b_info["chapters"], key=lambda x: x["chapter"]):
            lines.append(f"## Capítulo {chap['chapter']}\n")
            
            # Monta o parágrafo de texto corrido
            verse_paragraphs = []
            current_p = []
            
            # Coleta notas do capítulo para rodapé
            chapter_notes = []

            for v in chap["verses"]:
                v_num_sup = str(v["verse"]).translate(superscript_digits)
                
                # Se o versículo tem notas, anexa marcador
                note_tags = ""
                if v["notes"]:
                    for n in v["notes"]:
                        chapter_notes.append({
                            "verse": v["verse"],
                            "term": n["term"],
                            "lemma": n["greek_lemma"],
                            "explanation": n["explanation"]
                        })
                
                v_text = f"**{v_num_sup}** {v['translation_text']}"
                current_p.append(v_text)

                # Quebra de parágrafo lógica para ritmo de leitura (ex: prólogo 1-5, 6-8, 9-13, 14, 15-18)
                if v["verse"] in [5, 8, 13, 14, 18, 28, 34, 42, 51]:
                    verse_paragraphs.append(" ".join(current_p))
                    current_p = []

            if current_p:
                verse_paragraphs.append(" ".join(current_p))

            for p in verse_paragraphs:
                lines.append(p + "\n")

            # Seção de Notas Exegéticas do Capítulo
            if chapter_notes:
                lines.append("\n### 📖 Notas Exegéticas e Culturais do Capítulo\n")
                for n in chapter_notes:
                    clean_lemma = n["lemma"].replace("*", "").strip()
                    lemma_str = f" (*{clean_lemma}*)" if clean_lemma else ""
                    lines.append(f"- **v. {n['verse']} — {n['term']}{lemma_str}:** {n['explanation']}")
                lines.append("\n---\n")


        with open(rel_book_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"   ↳ Arquivo de Leitura Corrida gerado: {rel_book_file.relative_to(BASE_DIR)}")


    print("\n💾 Gerando schema e sementes SQL...")
    sql_schema = """-- ==============================================================================
-- Schema para Banco de Dados da Tradução Bíblica (SQLite / PostgreSQL)
-- ==============================================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS verse_notes;
DROP TABLE IF EXISTS verses;
DROP TABLE IF EXISTS chapters;
DROP TABLE IF EXISTS books;

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

CREATE INDEX idx_verses_lookup ON verses(book_id, chapter_number, verse_number);
CREATE INDEX idx_notes_verse ON verse_notes(verse_id);

-- ==============================================================================
-- SEED DATA
-- ==============================================================================
"""

    def sql_escape(s) -> str:
        if s is None:
            return "NULL"
        return "'" + str(s).replace("'", "''") + "'"

    sql_statements = [sql_schema]

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
