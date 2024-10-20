import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# Caminho dos arquivos CSV onde os dados dos livros e reservas serão armazenados
BOOK_DATA_FILE = 'livros.csv'
RESERVA_DATA_FILE = 'reservas.csv'

# Função para verificar se o arquivo de livros e reservas existe e criar caso contrário
def inicializar_dados():
    if not os.path.exists(BOOK_DATA_FILE):
        with open(BOOK_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Título", "Autor", "Ano", "Disponível"])  # Cabeçalhos
    
    if not os.path.exists(RESERVA_DATA_FILE):
        with open(RESERVA_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Título", "Usuário"])  # Cabeçalhos para reservas

# Função para carregar livros do arquivo CSV
def carregar_livros():
    livros = []
    with open(BOOK_DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            livros.append(row)
    return livros

# Função para carregar reservas do arquivo CSV
def carregar_reservas():
    reservas = []
    with open(RESERVA_DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            reservas.append(row)
    return reservas

# Função para cadastrar novos livros
def cadastrar_livro():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    ano = entry_ano.get()

    if not titulo or not autor or not ano:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        return

    with open(BOOK_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([titulo, autor, ano, "Sim"])  # Livro está disponível por padrão

    messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
    limpar_campos()
    atualizar_tabela()

# Função para limpar os campos de entrada
def limpar_campos():
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_ano.delete(0, tk.END)

# Função para atualizar a tabela de livros
def atualizar_tabela(livros=None):
    for row in tree.get_children():
        tree.delete(row)
    
    if livros is None:
        livros = carregar_livros()

    for livro in livros:
        tree.insert("", tk.END, values=livro)

# Função para pesquisar livros em tempo real
def pesquisar_livros(event=None):
    termo = entry_pesquisa.get().lower()
    livros = carregar_livros()
    
    resultados = []
    for livro in livros:
        if termo in livro[0].lower():
            resultados.append(livro)

    atualizar_tabela(resultados)

# Função para reservar um livro
def reservar_livro():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um livro para reservar!")
        return

    valores = tree.item(selecionado, 'values')
    titulo = valores[0]
    disponivel = valores[3]

    if disponivel == "Não":
        messagebox.showwarning("Indisponível", f"O livro '{titulo}' já está reservado!")
        return

    # Reservar o livro
    with open(RESERVA_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([titulo, "Usuário Exemplo"])  # Aqui pode usar o nome do usuário logado

    # Atualizar disponibilidade do livro no CSV de livros
    atualizar_disponibilidade_livro(titulo, False)
    exibir_notificacao(f"O livro '{titulo}' foi reservado com sucesso!")
    atualizar_tabela()

# Função para remover a reserva de um livro
def remover_reserva():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um livro para remover a reserva!")
        return

    valores = tree.item(selecionado, 'values')
    titulo = valores[0]

    # Verificar se o livro está reservado
    reservas = carregar_reservas()
    reservas_atualizadas = [reserva for reserva in reservas if reserva[0] != titulo]
    
    if len(reservas) == len(reservas_atualizadas):
        messagebox.showwarning("Não Encontrado", f"O livro '{titulo}' não está reservado!")
        return

    with open(RESERVA_DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Usuário"])
        writer.writerows(reservas_atualizadas)

    # Atualizar disponibilidade do livro no CSV de livros
    atualizar_disponibilidade_livro(titulo, True)
    exibir_notificacao(f"A reserva do livro '{titulo}' foi removida com sucesso!")
    atualizar_tabela()

# Função para atualizar a disponibilidade de um livro
def atualizar_disponibilidade_livro(titulo, disponivel):
    livros = carregar_livros()
    with open(BOOK_DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Autor", "Ano", "Disponível"])  # Cabeçalhos
        for livro in livros:
            if livro[0] == titulo:
                livro[3] = "Sim" if disponivel else "Não"
            writer.writerow(livro)

# Função para exibir notificações
def exibir_notificacao(mensagem):
    messagebox.showinfo("Notificação", mensagem)

# Inicializa o arquivo de dados de livros e reservas
inicializar_dados()

# Janela principal
root = tk.Tk()
root.title("Sistema de Biblioteca")

# --- Área de Cadastro de Livros ---
frame_cadastro = tk.LabelFrame(root, text="Cadastro de Livros", padx=10, pady=10)
frame_cadastro.pack(padx=10, pady=10, fill="x")

tk.Label(frame_cadastro, text="Título:").grid(row=0, column=0)
entry_titulo = tk.Entry(frame_cadastro, width=30)
entry_titulo.grid(row=0, column=1)

tk.Label(frame_cadastro, text="Autor:").grid(row=1, column=0)
entry_autor = tk.Entry(frame_cadastro, width=30)
entry_autor.grid(row=1, column=1)

tk.Label(frame_cadastro, text="Ano:").grid(row=2, column=0)
entry_ano = tk.Entry(frame_cadastro, width=30)
entry_ano.grid(row=2, column=1)

btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar Livro", command=cadastrar_livro)
btn_cadastrar.grid(row=3, column=1, pady=10)

# --- Área de Pesquisa ---
frame_pesquisa = tk.LabelFrame(root, text="Pesquisar Livros", padx=10, pady=10)
frame_pesquisa.pack(padx=10, pady=10, fill="x")

tk.Label(frame_pesquisa, text="Pesquisar por Título:").grid(row=0, column=0)
entry_pesquisa = tk.Entry(frame_pesquisa, width=30)
entry_pesquisa.grid(row=0, column=1)
entry_pesquisa.bind("<KeyRelease>", pesquisar_livros)  # Pesquisa em tempo real

# --- Área de Visualização de Livros ---
frame_visualizacao = tk.LabelFrame(root, text="Livros Disponíveis", padx=10, pady=10)
frame_visualizacao.pack(padx=10, pady=10, fill="both", expand=True)

# Configuração da tabela de livros
colunas = ("Título", "Autor", "Ano", "Disponível")
tree = ttk.Treeview(frame_visualizacao, columns=colunas, show="headings")
tree.heading("Título", text="Título")
tree.heading("Autor", text="Autor")
tree.heading("Ano", text="Ano")
tree.heading("Disponível", text="Disponível")

# Barra de rolagem para a tabela
scrollbar = tk.Scrollbar(frame_visualizacao, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# --- Botões ---
btn_reservar = tk.Button(root, text="Reservar Livro", command=reservar_livro)
btn_reservar.pack(side="left", padx=10, pady=10)

btn_remover_reserva = tk.Button(root, text="Remover Reserva", command=remover_reserva)
btn_remover_reserva.pack(side="right", padx=10, pady=10)

# Atualiza a tabela com os livros existentes
atualizar_tabela()

# Executa a janela principal
root.mainloop()
