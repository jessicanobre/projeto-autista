import sqlite3

def criar_banco_dados():
    conn = sqlite3.connect('autismo_app.db')
    cursor = conn.cursor()

    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL,
            tipo TEXT NOT NULL,  -- autista ou cuidador
            senha TEXT NOT NULL,
            nivel_apoio TEXT CHECK(nivel_apoio IN ('Nível 1: Necessidade de pouco apoio', 'Nível 2: Necessidade moderada de apoio', 'Nível 3: Necessidade de muito apoio')),
            idade INTEGER,
            escolaridade TEXT,
            foto TEXT
        )
    ''')

    # Tabela de Relacionamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Relacionamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuidador INTEGER,
            id_autista INTEGER,
            FOREIGN KEY (id_cuidador) REFERENCES Usuarios(id),
            FOREIGN KEY (id_autista) REFERENCES Usuarios(id)
        )
    ''')

    # Tabela de Rotinas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rotinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuidador INTEGER,
            id_autista INTEGER,
            tarefa TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT DEFAULT 'pendente',
            FOREIGN KEY (id_cuidador) REFERENCES Usuarios(id),
            FOREIGN KEY (id_autista) REFERENCES Usuarios(id)
        )
    ''')

    # Tabela de Habilidades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Habilidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_autista INTEGER,
            id_cuidador INTEGER,
            categoria TEXT NOT NULL,
            habilidade TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            progresso TEXT CHECK(progresso IN ('em desenvolvimento', 'desenvolvida', 'não desenvolvida')) DEFAULT 'em desenvolvimento',
            FOREIGN KEY (id_autista) REFERENCES Usuarios(id),
            FOREIGN KEY (id_cuidador) REFERENCES Usuarios(id)
        )
    ''')

    # Tabela de Pictogramas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pictogramas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuidador INTEGER,
            id_autista INTEGER,
            nome TEXT NOT NULL,
            imagem TEXT NOT NULL,
            FOREIGN KEY (id_cuidador) REFERENCES Usuarios(id),
            FOREIGN KEY (id_autista) REFERENCES Usuarios(id)
        )
    ''')

    # Tabela de Eventos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_autista INTEGER,
            titulo TEXT NOT NULL,
            data TEXT NOT NULL,
            descricao TEXT,
            FOREIGN KEY (id_autista) REFERENCES Usuarios(id)
        )
    ''')

    # Inserir dados iniciais para teste
    cursor.execute('''
        INSERT OR IGNORE INTO Usuarios (nome, email, telefone, endereco, tipo, senha, nivel_apoio, idade, escolaridade, foto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('João', 'joao@example.com', '123456789', 'Rua A, 123', 'autista', '123', 'Nível 1: Necessidade de pouco apoio', 10, 'Ensino Fundamental', 'joao.png'))

    cursor.execute('''
        INSERT OR IGNORE INTO Usuarios (nome, email, telefone, endereco, tipo, senha)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Maria', 'maria@example.com', '987654321', 'Rua B, 456', 'cuidador', '456'))

    cursor.execute('''
        INSERT OR IGNORE INTO Relacionamentos (id_cuidador, id_autista)
        VALUES (?, ?)
    ''', (2, 1))  # Maria (cuidador) cuida de João (autista)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco_dados()