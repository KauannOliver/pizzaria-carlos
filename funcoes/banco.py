import sqlite3
from datetime import datetime

def criar_tabela_clientes():
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL,
            cep TEXT NOT NULL,
            endereco TEXT NOT NULL,
            numero TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
def obter_cliente_por_id(id):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    conn.close()
    if resultado:
        return dict(zip(colunas, resultado))
    return None

def obter_pizza_por_id(id):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pizzas WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    conn.close()
    if resultado:
        return dict(zip(colunas, resultado))
    return None

def atualizar_pizza(id, nome, ingredientes):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pizzas
        SET nome = ?, ingredientes = ?
        WHERE id = ?
    """, (nome, ingredientes, id))
    conn.commit()
    conn.close()

def obter_cliente_por_nome(nome_cliente):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clientes WHERE nome = ?", (nome_cliente,))
    resultado = cursor.fetchone()
    
    colunas = [desc[0] for desc in cursor.description]
    
    conn.close()
    
    if resultado:
        return dict(zip(colunas, resultado))
    return None

def atualizar_cliente(id, nome, telefone, cpf, cep, endereco, numero):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nome = ?, telefone = ?, cpf = ?, cep = ?, endereco = ?, numero = ?
        WHERE id = ?
    """, (nome, telefone, cpf, cep, endereco, numero, id))
    conn.commit()
    conn.close()

def inserir_cliente(nome, telefone, cpf, cep, endereco, numero):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nome, telefone, cpf, cep, endereco, numero) VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, telefone, cpf, cep, endereco, numero))
    conn.commit()
    conn.close()

def obter_clientes():
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, telefone, cpf, cep, endereco, numero FROM clientes ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return rows

def deletar_cliente(id):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def criar_tabela_pizzas():
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pizzas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ingredientes TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_pizza(nome, ingredientes):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pizzas (nome, ingredientes) VALUES (?, ?)
    ''', (nome, ingredientes))
    conn.commit()
    conn.close()

def obter_pizzas():
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, ingredientes FROM pizzas ORDER BY nome')
    rows = cursor.fetchall()
    conn.close()
    return rows

def deletar_pizza(id):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pizzas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    
def criar_tabela_pedidos():
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            nome_cliente TEXT,
            nome_pizza TEXT,
            quantidade INTEGER,
            tamanho TEXT,
            forma_pagamento TEXT,
            entrega TEXT,
            valor_total REAL,
            status TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def inserir_pedido(codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, status, data_hora):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pedidos (codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, status, data_hora)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, status, data_hora))
    conn.commit()
    conn.close()

def obter_pedidos():
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, status, data_hora FROM pedidos ORDER BY data_hora DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows    
    
def atualizar_status_pedido(id, novo_status):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE pedidos SET status = ? WHERE id = ?', (novo_status, id))
    conn.commit()
    conn.close()

def deletar_pedido(id):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pedidos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def obter_pedido_por_id(id):
    conn = sqlite3.connect('pizzaria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    conn.close()
    if resultado:
        return dict(zip(colunas, resultado))
    return None

criar_tabela_clientes()
criar_tabela_pizzas()
criar_tabela_pedidos()
