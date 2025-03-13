import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3

class GerenciarRotinas:
    def __init__(self, root, id_cuidador, voltar_menu_callback, abrir_habilidades_callback, abrir_pictogramas_callback):
        self.root = root
        self.id_cuidador = id_cuidador
        self.voltar_menu_callback = voltar_menu_callback
        self.abrir_habilidades_callback = abrir_habilidades_callback
        self.abrir_pictogramas_callback = abrir_pictogramas_callback

        # Configuração do tema
        ctk.set_appearance_mode("light")  # Modo claro
        ctk.set_default_color_theme("blue")  # Tema azul

        # Frame principal
        self.frame = ctk.CTkFrame(root, fg_color="#FFFFFF", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        # Barra lateral (inicialmente visível)
        self.sidebar_visible = True
        self.sidebar = ctk.CTkFrame(self.frame, fg_color="#2C3E50", corner_radius=0, width=200)
        self.sidebar.pack(side="left", fill="y")

        # Botão para alternar a visibilidade da barra lateral (fora da barra lateral)
        self.btn_toggle_sidebar = ctk.CTkButton(
            self.frame, 
            text="◀",  # Símbolo para esconder a barra
            font=("Arial", 14), 
            fg_color="#34495E", 
            hover_color="#1ABC9C", 
            corner_radius=8,
            width=30,
            command=self.toggle_sidebar
        )
        self.btn_toggle_sidebar.place(x=205, y=10)  # Posiciona o botão ao lado da barra lateral

        # Botões de navegação na barra lateral
        btn_voltar = ctk.CTkButton(self.sidebar, text="Voltar ao Menu", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.voltar_menu_callback)
        btn_voltar.pack(pady=10, padx=10, fill="x")

        btn_habilidades = ctk.CTkButton(self.sidebar, text="Ir para Habilidades", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.abrir_habilidades_callback)
        btn_habilidades.pack(pady=10, padx=10, fill="x")

        btn_pictogramas = ctk.CTkButton(self.sidebar, text="Ir para Pictogramas", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.abrir_pictogramas_callback)
        btn_pictogramas.pack(pady=10, padx=10, fill="x")

        # Frame do conteúdo
        self.content_frame = ctk.CTkFrame(self.frame, fg_color="#FFFFFF", corner_radius=0)
        self.content_frame.pack(side="left", fill="both", expand=True, pady=10, padx=10)

        # Título
        ctk.CTkLabel(self.content_frame, text="Gerenciar Rotinas", font=("Arial", 20, "bold"), text_color="#2C3E50").pack(pady=20)

        # Lista de autistas
        ctk.CTkLabel(self.content_frame, text="Autista:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.autistas = self.carregar_autistas()
        self.combo_autistas = ctk.CTkComboBox(self.content_frame, values=self.autistas, font=("Arial", 14), dropdown_font=("Arial", 14))
        self.combo_autistas.pack(pady=5, padx=20, fill="x")

        # Formulário para adicionar tarefas
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(pady=10, padx=10, fill="x")

        # Campo de tarefa
        ctk.CTkLabel(form_frame, text="Tarefa:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.entry_tarefa = ctk.CTkEntry(form_frame, font=("Arial", 14), corner_radius=8)
        self.entry_tarefa.pack(pady=5, padx=10, fill="x")

        # Campo de horário
        ctk.CTkLabel(form_frame, text="Horário:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.entry_horario = ctk.CTkEntry(form_frame, font=("Arial", 14), corner_radius=8)
        self.entry_horario.pack(pady=5, padx=10, fill="x")

        # Botão de adicionar tarefa
        btn_adicionar = ctk.CTkButton(form_frame, text="Adicionar Tarefa", font=("Arial", 14, "bold"), fg_color="#1ABC9C", hover_color="#16A085", corner_radius=8, command=self.adicionar_tarefa)
        btn_adicionar.pack(pady=10, padx=10, fill="x")

        # Tabela de tarefas
        self.tree = ttk.Treeview(self.content_frame, columns=("ID", "Autista", "Tarefa", "Horário"), show="headings", style="mystyle.Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Autista", text="Autista")
        self.tree.heading("Tarefa", text="Tarefa")
        self.tree.heading("Horário", text="Horário")
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)

        # Estilo da tabela
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 12), rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=("Arial", 14, "bold"))

        # Botões de editar e excluir
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="#F5F5F5")
        btn_frame.pack(pady=10, padx=10, fill="x")

        btn_editar = ctk.CTkButton(btn_frame, text="Editar", font=("Arial", 14, "bold"), fg_color="#3498DB", hover_color="#2980B9", corner_radius=8, command=self.editar_tarefa)
        btn_editar.pack(side="left", padx=5, fill="x", expand=True)

        btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 14, "bold"), fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, command=self.excluir_tarefa)
        btn_excluir.pack(side="right", padx=5, fill="x", expand=True)

        # Carregar tarefas ao iniciar
        self.carregar_tarefas()

    def toggle_sidebar(self):
        """Alterna a visibilidade da barra lateral."""
        if self.sidebar_visible:
            self.sidebar.pack_forget()  # Esconde a barra lateral
            self.btn_toggle_sidebar.configure(text="▶")  # Altera o símbolo para "mostrar"
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y")  # Mostra a barra lateral
            self.btn_toggle_sidebar.configure(text="◀")  # Altera o símbolo para "esconder"
            self.sidebar_visible = True

    def carregar_autistas(self):
        """Carrega a lista de autistas do banco de dados."""
        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM Usuarios WHERE tipo = "autista"')
        autistas = cursor.fetchall()
        conn.close()
        return [f"{nome} (ID: {id})" for id, nome in autistas]

    def carregar_tarefas(self):
        """Carrega as tarefas do banco de dados e exibe na tabela."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, u.nome, r.tarefa, r.horario
            FROM Rotinas r
            JOIN Usuarios u ON r.id_autista = u.id
            WHERE r.id_cuidador = ?
        ''', (self.id_cuidador,))
        tarefas = cursor.fetchall()
        conn.close()

        for tarefa in tarefas:
            self.tree.insert("", "end", values=tarefa)

    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa ao banco de dados."""
        autista_selecionado = self.combo_autistas.get()
        tarefa = self.entry_tarefa.get()
        horario = self.entry_horario.get()

        if not autista_selecionado or not tarefa or not horario:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        id_autista = int(autista_selecionado.split("(ID: ")[1].replace(")", ""))

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Rotinas (id_cuidador, id_autista, tarefa, horario)
            VALUES (?, ?, ?, ?)
        ''', (self.id_cuidador, id_autista, tarefa, horario))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
        self.carregar_tarefas()

    def editar_tarefa(self):
        """Edita a tarefa selecionada."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma tarefa selecionada!")
            return

        id_tarefa = self.tree.item(selecionado, "values")[0]
        nova_tarefa = self.entry_tarefa.get()
        novo_horario = self.entry_horario.get()

        if not nova_tarefa or not novo_horario:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Rotinas SET tarefa = ?, horario = ? WHERE id = ?', (nova_tarefa, novo_horario, id_tarefa))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Tarefa atualizada!")
        self.carregar_tarefas()

    def excluir_tarefa(self):
        """Exclui a tarefa selecionada."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma tarefa selecionada!")
            return

        id_tarefa = self.tree.item(selecionado, "values")[0]

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Rotinas WHERE id = ?', (id_tarefa,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Tarefa excluída!")
        self.carregar_tarefas()