import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3

class HabilidadesAutista:
    def __init__(self, root, id_autista, voltar_menu_callback, abrir_agenda_callback, abrir_pictogramas_callback):
        self.root = root
        self.id_autista = id_autista
        self.voltar_menu_callback = voltar_menu_callback
        self.abrir_agenda_callback = abrir_agenda_callback
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
            text="Minhas Habilidades", 
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

        # Botão para agenda
        btn_agenda = ctk.CTkButton(
            botoes_navegacao_frame, 
            text="Ir para Agenda", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.abrir_agenda_callback
        )
        btn_agenda.pack(side="left", padx=5, fill="x", expand=True)

        # Botão para pictogramas
        btn_pictogramas = ctk.CTkButton(
            botoes_navegacao_frame, 
            text="Ir para Pictogramas", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.abrir_pictogramas_callback
        )
        btn_pictogramas.pack(side="left", padx=5, fill="x", expand=True)

        # Tabela de habilidades
        self.tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "Categoria", "Habilidade", "Data de Início", "Progresso"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Habilidade", text="Habilidade")
        self.tree.heading("Data de Início", text="Data de Início")
        self.tree.heading("Progresso", text="Progresso")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Estilo da tabela
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background=self.cor_tabela_cabecalho, foreground="white")
        estilo.configure("Treeview", font=("Helvetica", 12), background=self.cor_tabela_linhas, fieldbackground=self.cor_tabela_linhas)
        estilo.map("Treeview", background=[("selected", self.cor_botao)])

        # Frame para os botões de ação
        botoes_acao_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        botoes_acao_frame.pack(pady=10, padx=10, fill="x")

        # Botão de editar progresso
        btn_editar = ctk.CTkButton(
            botoes_acao_frame, 
            text="Editar Progresso", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.editar_progresso
        )
        btn_editar.pack(side="left", padx=5, fill="x", expand=True)

        # Botão de excluir habilidade
        btn_excluir = ctk.CTkButton(
            botoes_acao_frame, 
            text="Excluir", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao_voltar, 
            hover_color=self.cor_botao_voltar_hover, 
            corner_radius=8,
            command=self.excluir_habilidade
        )
        btn_excluir.pack(side="right", padx=5, fill="x", expand=True)

        # Carregar habilidades ao iniciar
        self.carregar_habilidades()

    def carregar_habilidades(self):
        """Carrega as habilidades do banco de dados e exibe na tabela."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, categoria, habilidade, data_inicio, progresso
            FROM Habilidades
            WHERE id_autista = ?
        ''', (self.id_autista,))
        habilidades = cursor.fetchall()
        conn.close()

        for hab in habilidades:
            self.tree.insert("", "end", values=hab)

    def editar_progresso(self):
        """Edita o progresso da habilidade selecionada."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma habilidade selecionada!")
            return

        id_habilidade = self.tree.item(selecionado, "values")[0]
        novo_progresso = self.obter_novo_progresso()

        if novo_progresso:
            conn = sqlite3.connect('autismo_app.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE Habilidades SET progresso = ? WHERE id = ?', (novo_progresso, id_habilidade))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Progresso atualizado!")
            self.carregar_habilidades()

    def obter_novo_progresso(self):
        """Janela para selecionar o novo progresso."""
        dialog = ctk.CTkInputDialog(text="Selecione o novo progresso:", title="Editar Progresso")
        novo_progresso = dialog.get_input()
        return novo_progresso

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