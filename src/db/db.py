import sqlite3
from pathlib import Path

DB_PATH = Path("db/metadata.db")

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure ./db exists

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            title TEXT,
            hash TEXT UNIQUE,
            timestamp TEXT,
            source_type TEXT,
            embedding_model TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            document_id INTEGER,
            chunk_index INTEGER,
            content TEXT,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        )
    ''')

    conn.commit()
    return conn

def get_existing_hashes():
    conn = init_db()
    cur = conn.cursor()
    cur.execute("SELECT hash FROM documents")
    return set(row[0] for row in cur.fetchall())


def insert_document(path, title, hash_, source_type, embedding_model):
    conn = init_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO documents (path, title, hash, timestamp, source_type, embedding_model)
        VALUES (?, ?, ?, datetime('now'), ?, ?)
    ''', (path, title, hash_, source_type, embedding_model))
    conn.commit()
    return cur.lastrowid


def insert_chunks(document_id, chunks):
    conn = init_db()
    cur = conn.cursor()
    cur.executemany('''
        INSERT INTO chunks (document_id, chunk_index, content)
        VALUES (?, ?, ?)
    ''', [(document_id, i, chunk) for i, chunk in enumerate(chunks)])
    conn.commit()


def fetch_metadata_by_content(content_substring):
    conn = init_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT d.title, d.timestamp, d.path FROM documents d
        JOIN chunks c ON c.document_id = d.id
        WHERE c.content LIKE ?
        LIMIT 1
    ''', (f"%{content_substring[:50]}%",))
    row = cur.fetchone()
    return {"title": row[0], "timestamp": row[1], "path": row[2]} if row else {}
