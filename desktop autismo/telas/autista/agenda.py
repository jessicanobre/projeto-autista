import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
from PIL import Image, ImageTk  # Para carregar ícones

class AgendaAutista:
    def __init__(self, root, id_autista, voltar_menu_callback, abrir_habilidades_callback, abrir_pictogramas_callback):
        self.root = root
        self.id_autista = id_autista
        self.voltar_menu_callback = voltar_menu_callback
        self.abrir_habilidades_callback = abrir_habilidades_callback
        self.abrir_pictogramas_callback = abrir_pictogramas_callback

        # Configuração do tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Paleta de cores discreta com um toque de cor
        self.cor_fundo = "#FFFFFF"  # Fundo branco
        self.cor_primaria = "#4A4A4A"  # Cinza escuro para textos e elementos principais
        self.cor_secundaria = "#757575"  # Cinza médio para hover e detalhes
        self.cor_texto = "#2C3E50"  # Texto escuro para contraste
        self.cor_borda = "#E0E0E0"  # Bordas claras
        self.cor_botao = "#64B5F6"  # Azul suave para botões principais
        self.cor_botao_hover = "#90CAF9"  # Azul mais claro para hover
        self.cor_botao_voltar = "#9E9E9E"  # Cinza para botão de voltar
        self.cor_botao_voltar_hover = "#BDBDBD"  # Cinza mais claro para hover
        self.cor_tabela_cabecalho = "#64B5F6"  # Cabeçalho da tabela com azul suave
        self.cor_tabela_linhas = "#FFFFFF"  # Linhas da tabela brancas

        # Frame principal
        self.frame = ctk.CTkFrame(root, fg_color=self.cor_fundo, corner_radius=15)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        ctk.CTkLabel(
            self.frame, 
            text="Minha Agenda", 
            font=("Helvetica", 24, "bold"), 
            text_color=self.cor_primaria
        ).pack(pady=(10, 20))

        # Frame para os botões de navegação
        botoes_navegacao_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        botoes_navegacao_frame.pack(pady=10, padx=10, fill="x")

        # Botão de voltar ao menu
        btn_voltar = ctk.CTkButton(
            botoes_navegacao_frame, 
            text="Voltar ao Menu", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao_voltar, 
            hover_color=self.cor_botao_voltar_hover, 
            corner_radius=8,
            command=self.voltar_menu_callback
        )
        btn_voltar.pack(side="left", padx=5, fill="x", expand=True)

        # Botão para habilidades
        btn_habilidades = ctk.CTkButton(
            botoes_navegacao_frame, 
            text="Habilidades", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.abrir_habilidades_callback
        )
        btn_habilidades.pack(side="left", padx=5, fill="x", expand=True)

        # Botão para pictogramas
        btn_pictogramas = ctk.CTkButton(
            botoes_navegacao_frame, 
            text="Pictogramas", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.abrir_pictogramas_callback
        )
        btn_pictogramas.pack(side="left", padx=5, fill="x", expand=True)

        # Tabela de tarefas
        self.tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "Tarefa", "Horário"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tarefa", text="Tarefa")
        self.tree.heading("Horário", text="Horário")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Estilo da tabela
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background=self.cor_tabela_cabecalho, foreground="white")
        estilo.configure("Treeview", font=("Helvetica", 12), background=self.cor_tabela_linhas, fieldbackground=self.cor_tabela_linhas)
        estilo.map("Treeview", background=[("selected", self.cor_botao)])

        # Frame para os botões de ação
        botoes_acao_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        botoes_acao_frame.pack(pady=10, padx=10, fill="x")

        # Botão de adicionar tarefa
        btn_adicionar = ctk.CTkButton(
            botoes_acao_frame, 
            text="Adicionar Tarefa", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.adicionar_tarefa
        )
        btn_adicionar.pack(side="left", padx=5, fill="x", expand=True)

        # Botão de editar tarefa
        btn_editar = ctk.CTkButton(
            botoes_acao_frame, 
            text="Editar Tarefa", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.editar_tarefa
        )
        btn_editar.pack(side="left", padx=5, fill="x", expand=True)

        # Botão de excluir tarefa
        btn_excluir = ctk.CTkButton(
            botoes_acao_frame, 
            text="Excluir Tarefa", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao_voltar, 
            hover_color=self.cor_botao_voltar_hover, 
            corner_radius=8,
            command=self.excluir_tarefa
        )
        btn_excluir.pack(side="left", padx=5, fill="x", expand=True)

        # Carregar tarefas ao iniciar
        self.carregar_tarefas()

    def carregar_tarefas(self):
        """Carrega as tarefas do banco de dados e exibe na tabela."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, tarefa, horario FROM Rotinas WHERE id_autista = ?', (self.id_autista,))
        tarefas = cursor.fetchall()
        conn.close()

        for id_tarefa, tarefa, horario in tarefas:
            self.tree.insert("", "end", values=(id_tarefa, tarefa, horario))

    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa ao banco de dados."""
        dialog = ctk.CTkInputDialog(text="Digite a nova tarefa e o horário (separados por vírgula):", title="Adicionar Tarefa")
        entrada = dialog.get_input()

        if entrada:
            try:
                tarefa, horario = entrada.split(",")
                tarefa = tarefa.strip()
                horario = horario.strip()

                if not tarefa or not horario:
                    messagebox.showerror("Erro", "Tarefa e horário são obrigatórios!")
                    return

                conn = sqlite3.connect('autismo_app.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Rotinas (id_autista, tarefa, horario) VALUES (?, ?, ?)', (self.id_autista, tarefa, horario))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Tarefa adicionada!")
                self.carregar_tarefas()
            except ValueError:
                messagebox.showerror("Erro", "Formato inválido! Use: Tarefa, Horário")

    def editar_tarefa(self):
        """Edita a tarefa selecionada."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma tarefa selecionada!")
            return

        id_tarefa = self.tree.item(selecionado, "values")[0]
        tarefa_atual = self.tree.item(selecionado, "values")[1]
        horario_atual = self.tree.item(selecionado, "values")[2]

        dialog = ctk.CTkInputDialog(text=f"Editar Tarefa:\nTarefa: {tarefa_atual}\nHorário: {horario_atual}", title="Editar Tarefa")
        entrada = dialog.get_input()

        if entrada:
            try:
                nova_tarefa, novo_horario = entrada.split(",")
                nova_tarefa = nova_tarefa.strip()
                novo_horario = novo_horario.strip()

                if not nova_tarefa or not novo_horario:
                    messagebox.showerror("Erro", "Tarefa e horário são obrigatórios!")
                    return

                conn = sqlite3.connect('autismo_app.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE Rotinas SET tarefa = ?, horario = ? WHERE id = ?', (nova_tarefa, novo_horario, id_tarefa))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Tarefa atualizada!")
                self.carregar_tarefas()
            except ValueError:
                messagebox.showerror("Erro", "Formato inválido! Use: Tarefa, Horário")

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