import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk  # Importando a biblioteca para temas
import csv
import os
import subprocess

# Caminho do arquivo CSV onde os dados dos usuários serão armazenados
USER_DATA_FILE = 'usuarios.csv'

# Função para verificar se o arquivo de usuários existe e criar um caso contrário
def inicializar_dados_usuarios():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nome", "Email", "Senha"])  # Cabeçalhos

# Função para cadastrar novos usuários
def cadastrar_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()

    if not nome or not email or not senha:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        return

    # Verifica se o email já está cadastrado
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            if row[1] == email:
                messagebox.showerror("Erro", "E-mail já cadastrado!")
                return

    # Cadastra o novo usuário
    with open(USER_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nome, email, senha])

    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    limpar_campos()

# Função para fazer login
def login_usuario():
    email = entry_login_email.get()
    senha = entry_login_senha.get()

    if not email or not senha:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        return

    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            if row[1] == email and row[2] == senha:
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                return acessar_acervo()

    messagebox.showerror("Erro", "E-mail ou senha incorretos!")

# Função para acessar o acervo de livros
def acessar_acervo():
    # Fecha a janela de login
    root.destroy()
    
    # Abre o sistema de biblioteca
    subprocess.run(["python", "biblioteca.py"])

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

# Inicializa o arquivo de dados de usuários
inicializar_dados_usuarios()

# Janela principal com tema
root = ThemedTk(theme="arc")  # Escolha um tema do ttkthemes, ex: "arc", "breeze", "clam", etc.
root.title("Sistema de Biblioteca - Login e Cadastro")

# --- Aba de Cadastro ---
frame_cadastro = ttk.LabelFrame(root, text="Cadastro de Usuário", padding=(10, 10))
frame_cadastro.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
entry_nome = ttk.Entry(frame_cadastro, width=30)
entry_nome.grid(row=0, column=1, pady=5)

ttk.Label(frame_cadastro, text="E-mail:").grid(row=1, column=0, sticky="w", pady=5)
entry_email = ttk.Entry(frame_cadastro, width=30)
entry_email.grid(row=1, column=1, pady=5)

ttk.Label(frame_cadastro, text="Senha:").grid(row=2, column=0, sticky="w", pady=5)
entry_senha = ttk.Entry(frame_cadastro, show="*", width=30)
entry_senha.grid(row=2, column=1, pady=5)

btn_cadastrar = ttk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_usuario)
btn_cadastrar.grid(row=3, column=1, pady=10, sticky="e")

# --- Aba de Login ---
frame_login = ttk.LabelFrame(root, text="Login", padding=(10, 10))
frame_login.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_login, text="E-mail:").grid(row=0, column=0, sticky="w", pady=5)
entry_login_email = ttk.Entry(frame_login, width=30)
entry_login_email.grid(row=0, column=1, pady=5)

ttk.Label(frame_login, text="Senha:").grid(row=1, column=0, sticky="w", pady=5)
entry_login_senha = ttk.Entry(frame_login, show="*", width=30)
entry_login_senha.grid(row=1, column=1, pady=5)

btn_login = ttk.Button(frame_login, text="Login", command=login_usuario)
btn_login.grid(row=2, column=1, pady=10, sticky="e")

# Executa a janela principal
root.mainloop()
