import sqlite3
import pandas as pd
import requests
import re
import os
import flet as ft
import urllib.parse
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def exportar_para_excel(tabela, nome_arquivo):
    conn = sqlite3.connect('pizzaria.db')
    query = f"SELECT * FROM {tabela}"
    df = pd.read_sql(query, conn)
    conn.close()
    caminho_arquivo = f"{nome_arquivo}.xlsx"
    df.to_excel(caminho_arquivo, index=False)
    return f"Dados exportados com sucesso para {caminho_arquivo}"

def criar_textfield(label, hint_text, prefix_icon, max_length=None, telefone=False, cpf=False, cep=False, somente_numeros=False, somente_texto=False, icon_color=False):
    def atualizar_contador(e):
        texto = e.control.value
        if max_length:
            e.control.counter_text = f"{len(texto)}/{max_length}"
        if telefone:
            e.control.value = formatar_telefone(texto)
        if cpf:
            e.control.value = formatar_cpf(texto)
        if cep:
            e.control.value = formatar_cep(texto)
        e.control.update()

    if somente_numeros:
        input_filter = ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string="")
    elif somente_texto:
        input_filter = ft.InputFilter(allow=True, regex_string=r"[a-zA-Z\s]", replacement_string="")
    else:
        input_filter = None

    return ft.TextField(
        label=label,
        hint_text=hint_text,
        border_radius=ft.border_radius.all(5),
        content_padding=20,
        width="90%",
        text_style=ft.TextStyle(size=18),
        height=50,
        prefix_icon=ft.Icon(prefix_icon, color=icon_color) if icon_color else prefix_icon,
        capitalization=ft.TextCapitalization.CHARACTERS,
        counter_text=f"0/{max_length}" if max_length else "",
        input_filter=input_filter,
        on_change=atualizar_contador,
        max_length=max_length,
        keyboard_type=ft.KeyboardType.TEXT,
    )

def formatar_telefone(numero):
    numero = re.sub(r'\D', '', numero)
    if len(numero) > 11:
        numero = numero[:11]
    if len(numero) > 7:
        numero = f"({numero[:2]}) {numero[2]} {numero[3:7]}-{numero[7:]}"
    elif len(numero) > 2:
        numero = f"({numero[:2]}) {numero[2:]}"
    return numero

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) > 11:
        cpf = cpf[:11]
    if len(cpf) > 9:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    elif len(cpf) > 6:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
    elif len(cpf) > 3:
        cpf = f"{cpf[:3]}.{cpf[3:]}"
    return cpf

def formatar_cep(cep):
    cep = re.sub(r'\D', '', cep)
    if len(cep) > 8:
        cep = cep[:8]
    if len(cep) > 5:
        cep = f"{cep[:5]}-{cep[5:]}"
    return cep

def buscar_endereco_por_cep(cep):
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    if response.status_code == 200:
        dados = response.json()
        if "erro" not in dados:
            return dados
    return None

def preencher_endereco(page, cep_field, endereco_field, bairro_field, cidade_field, uf_field):
    cep = cep_field.value.strip()
    if cep:
        dados = buscar_endereco_por_cep(cep)
        if dados:
            endereco_field.value = dados.get('logradouro', '')
            bairro_field.value = dados.get('bairro', '')
            cidade_field.value = dados.get('localidade', '')
            uf_field.value = dados.get('uf', '')
            page.update()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("CEP não encontrado."), bgcolor=ft.colors.RED))

def mensagem_salvar_pedido(nome_cliente, codigo_pedido, quantidade, nome_pizza, valor_total):
    return (f"Olá {nome_cliente}, tudo bem?\n"
            f"O código do seu pedido é {codigo_pedido}.\n"
            f"Você pediu {quantidade} pizza(s) do sabor {nome_pizza}.\n"
            f"O tempo estimado de entrega é de 40 a 60 minutos.\n"
            f"O valor do seu pedido é R${valor_total:.2f}.")

def mensagem_enviar_pedido(nome_cliente):
    return (f"Olá {nome_cliente}, está com fome aí?\n"
            f"O seu pedido acaba de sair do estabelecimento para entrega.")

def mensagem_concluir_pedido(nome_cliente):
    return (f"Olá {nome_cliente}, como estava a(s) pizza(s)?\n"
            f"Dê um feedback para que possamos sempre melhorar.")

def mensagem_cancelar_pedido(nome_cliente, codigo_pedido):
    return (f"Olá {nome_cliente}!\n"
            f"O seu pedido de código {codigo_pedido} acaba de ser cancelado.")

def enviar_mensagem_whatsapp(numero, mensagem):
    options = webdriver.FirefoxOptions()
    options.profile = r"C:\Users\kauantavares\AppData\Roaming\Mozilla\Firefox\Profiles\oxbcyzri.default-release"  # Certifique-se de que este é o caminho correto
    navegador = webdriver.Firefox(options=options)
    navegador.get("https://web.whatsapp.com/")
    wait = WebDriverWait(navegador, 60)
    
    texto = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span')))
    elemento = navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span')
    navegador.execute_script("arguments[0].click();", elemento)
    time.sleep(2)
    navegador.quit()

def enviar_mensagem_pedido(nome_cliente, codigo_pedido, quantidade, nome_pizza, valor_total, numero_cliente, status="salvar"):
    if status == "salvar":
        mensagem = mensagem_salvar_pedido(nome_cliente, codigo_pedido, quantidade, nome_pizza, valor_total)
    elif status == "enviar":
        mensagem = mensagem_enviar_pedido(nome_cliente)
    elif status == "concluir":
        mensagem = mensagem_concluir_pedido(nome_cliente)
    elif status == "cancelar":
        mensagem = mensagem_cancelar_pedido(nome_cliente, codigo_pedido)

    enviar_mensagem_whatsapp(numero_cliente, mensagem)