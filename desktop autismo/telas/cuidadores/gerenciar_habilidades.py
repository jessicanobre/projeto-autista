import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk  # Para carregar ícones

class GerenciarHabilidades:
    def __init__(self, root, id_cuidador, voltar_menu_callback, abrir_rotinas_callback, abrir_pictogramas_callback):
        self.root = root
        self.id_cuidador = id_cuidador
        self.voltar_menu_callback = voltar_menu_callback
        self.abrir_rotinas_callback = abrir_rotinas_callback
        self.abrir_pictogramas_callback = abrir_pictogramas_callback

        # Configuração do tema
        ctk.set_appearance_mode("light")  # Modo claro
        ctk.set_default_color_theme("blue")  # Tema azul

        # Frame principal
        self.frame = ctk.CTkFrame(root, fg_color="#FFFFFF", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        # Barra lateral
        self.sidebar = ctk.CTkFrame(self.frame, fg_color="#2C3E50", corner_radius=0, width=200)
        self.sidebar.pack(side="left", fill="y")

        # Botões de navegação na barra lateral
        btn_voltar = ctk.CTkButton(self.sidebar, text="Voltar ao Menu", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.voltar_menu_callback)
        btn_voltar.pack(pady=10, padx=10, fill="x")

        btn_rotinas = ctk.CTkButton(self.sidebar, text="Ir para Rotinas", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.abrir_rotinas_callback)
        btn_rotinas.pack(pady=10, padx=10, fill="x")

        btn_pictogramas = ctk.CTkButton(self.sidebar, text="Ir para Pictogramas", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.abrir_pictogramas_callback)
        btn_pictogramas.pack(pady=10, padx=10, fill="x")

        # Frame do conteúdo
        self.content_frame = ctk.CTkFrame(self.frame, fg_color="#FFFFFF", corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Título
        ctk.CTkLabel(self.content_frame, text="Gerenciar Habilidades", font=("Arial", 20), text_color="#2C3E50").pack(pady=20)

        # Lista de autistas
        ctk.CTkLabel(self.content_frame, text="Autista:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.autistas = self.carregar_autistas()
        self.combo_autistas = ctk.CTkComboBox(self.content_frame, values=self.autistas, font=("Arial", 14), dropdown_font=("Arial", 14))
        self.combo_autistas.pack(pady=5, padx=20, fill="x")

        # Formulário para adicionar habilidades
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(pady=10, padx=10, fill="x")

        # Campo de categoria
        ctk.CTkLabel(form_frame, text="Categoria:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.entry_categoria = ctk.CTkEntry(form_frame, font=("Arial", 14), corner_radius=8)
        self.entry_categoria.pack(pady=5, padx=10, fill="x")

        # Campo de habilidade
        ctk.CTkLabel(form_frame, text="Habilidade:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.entry_habilidade = ctk.CTkEntry(form_frame, font=("Arial", 14), corner_radius=8)
        self.entry_habilidade.pack(pady=5, padx=10, fill="x")

        # Campo de progresso
        ctk.CTkLabel(form_frame, text="Progresso:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.combo_progresso = ctk.CTkComboBox(form_frame, values=["em desenvolvimento", "desenvolvida", "não desenvolvida"], font=("Arial", 14), dropdown_font=("Arial", 14))
        self.combo_progresso.pack(pady=5, padx=10, fill="x")

        # Botão de adicionar habilidade
        btn_adicionar = ctk.CTkButton(form_frame, text="Adicionar Habilidade", font=("Arial", 14), fg_color="#1ABC9C", hover_color="#16A085", corner_radius=8, command=self.adicionar_habilidade)
        btn_adicionar.pack(pady=10, padx=10, fill="x")

        # Tabela de habilidades
        self.tree = ttk.Treeview(self.content_frame, columns=("ID", "Categoria", "Habilidade", "Progresso"), show="headings", style="mystyle.Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Habilidade", text="Habilidade")
        self.tree.heading("Progresso", text="Progresso")
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)

        # Estilo da tabela
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 12), rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=("Arial", 14))

        # Botões de editar e excluir
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="#F5F5F5")
        btn_frame.pack(pady=10, padx=10, fill="x")

        btn_editar = ctk.CTkButton(btn_frame, text="Editar Progresso", font=("Arial", 14), fg_color="#3498DB", hover_color="#2980B9", corner_radius=8, command=self.editar_progresso)
        btn_editar.pack(side="left", padx=5, fill="x", expand=True)

        btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 14), fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, command=self.excluir_habilidade)
        btn_excluir.pack(side="right", padx=5, fill="x", expand=True)

        # Carregar habilidades ao iniciar
        self.carregar_habilidades()

    def carregar_autistas(self):
        """Carrega a lista de autistas do banco de dados."""
        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM Usuarios WHERE tipo = "autista"')
        autistas = cursor.fetchall()
        conn.close()
        return [f"{nome} (ID: {id})" for id, nome in autistas]

    def carregar_habilidades(self):
        """Carrega as habilidades do banco de dados e exibe na tabela."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, categoria, habilidade, progresso
            FROM Habilidades
            WHERE id_cuidador = ?
        ''', (self.id_cuidador,))
        habilidades = cursor.fetchall()
        conn.close()

        for hab in habilidades:
            self.tree.insert("", "end", values=hab)

    def adicionar_habilidade(self):
        """Adiciona uma nova habilidade ao banco de dados."""
        categoria = self.entry_categoria.get()
        habilidade = self.entry_habilidade.get()
        progresso = self.combo_progresso.get()

        # Extrai o ID do autista selecionado
        autista_selecionado = self.combo_autistas.get()
        if not autista_selecionado:
            messagebox.showerror("Erro", "Selecione um autista!")
            return
        id_autista = int(autista_selecionado.split("(ID: ")[1].replace(")", ""))

        if not categoria or not habilidade or not progresso:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        # Obtém a data atual no formato YYYY-MM-DD
        data_inicio = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Habilidades (id_autista, id_cuidador, categoria, habilidade, data_inicio, progresso)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id_autista, self.id_cuidador, categoria, habilidade, data_inicio, progresso))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Habilidade adicionada!")
        self.carregar_habilidades()

        # Limpa os campos do formulário
        self.entry_categoria.delete(0, ctk.END)
        self.entry_habilidade.delete(0, ctk.END)
        self.combo_progresso.set("")

    def editar_progresso(self):
        """Edita o progresso da habilidade selecionada."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma habilidade selecionada!")
            return

        id_habilidade = self.tree.item(selecionado, "values")[0]
        progresso_atual = self.tree.item(selecionado, "values")[3]

        dialog = ctk.CTkInputDialog(text=f"Editar Progresso:\nProgresso Atual: {progresso_atual}", title="Editar Progresso")
        novo_progresso = dialog.get_input()

        if novo_progresso:
            conn = sqlite3.connect('autismo_app.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE Habilidades SET progresso = ? WHERE id = ?', (novo_progresso, id_habilidade))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Progresso atualizado!")
            self.carregar_habilidades()

    def excluir_habilidade(self):
        """Exclui a habilidade selecionada."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma habilidade selecionada!")
            return

        id_habilidade = self.tree.item(selecionado, "values")[0]

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Habilidades WHERE id = ?', (id_habilidade,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Habilidade excluída!")
        self.carregar_habilidades()