from contextlib import closing
from utils.db import get_db_connection

def criar_tabelas():
    with closing(get_db_connection()) as db:
        cursor = db.cursor()
        
        # Criação da tabela usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            senha_hash VARCHAR(255) NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        # Criação da tabela servicos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        # Criação da tabela filas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS filas (
            id INT PRIMARY KEY AUTO_INCREMENT,
            servico_id INT,
            usuario_id INT,
            status VARCHAR(50) DEFAULT 'espera',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (servico_id) REFERENCES servicos(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """)

        # Criação da tabela atendimentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fila_id INT,
            atendente_id INT,
            iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            finalizado_em TIMESTAMP NULL,
            FOREIGN KEY (fila_id) REFERENCES filas(id),
            FOREIGN KEY (atendente_id) REFERENCES usuarios(id)
        );
        """)
        
        db.commit()
        print("Tabelas criadas com sucesso!")

# Executa a criação das tabelas se o arquivo for executado diretamente
if __name__ == "__main__":
    criar_tabelas()