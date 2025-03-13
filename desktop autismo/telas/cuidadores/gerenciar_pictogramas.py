import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import sqlite3

class GerenciarPictogramas:
    def __init__(self, root, id_cuidador, voltar_menu_callback, abrir_rotinas_callback, abrir_habilidades_callback):
        self.root = root
        self.id_cuidador = id_cuidador
        self.voltar_menu_callback = voltar_menu_callback
        self.abrir_rotinas_callback = abrir_rotinas_callback
        self.abrir_habilidades_callback = abrir_habilidades_callback

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

        btn_habilidades = ctk.CTkButton(self.sidebar, text="Ir para Habilidades", font=("Arial", 14), fg_color="#34495E", hover_color="#1ABC9C", command=self.abrir_habilidades_callback)
        btn_habilidades.pack(pady=10, padx=10, fill="x")

        # Frame do conteúdo
        self.content_frame = ctk.CTkFrame(self.frame, fg_color="#FFFFFF", corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Título
        ctk.CTkLabel(self.content_frame, text="Gerenciar Pictogramas", font=("Arial", 20), text_color="#2C3E50").pack(pady=20)

        # Lista de autistas
        ctk.CTkLabel(self.content_frame, text="Autista:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.autistas = self.carregar_autistas()
        self.combo_autistas = ctk.CTkComboBox(self.content_frame, values=self.autistas, font=("Arial", 14), dropdown_font=("Arial", 14))
        self.combo_autistas.pack(pady=5, padx=20, fill="x")

        # Campo de nome do pictograma
        ctk.CTkLabel(self.content_frame, text="Nome do Pictograma:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.entry_nome = ctk.CTkEntry(self.content_frame, font=("Arial", 14))
        self.entry_nome.pack(pady=5, padx=20, fill="x")

        # Campo de imagem do pictograma
        ctk.CTkLabel(self.content_frame, text="Imagem do Pictograma:", font=("Arial", 14), text_color="#2C3E50").pack(pady=5)
        self.entry_imagem = ctk.CTkEntry(self.content_frame, font=("Arial", 14))
        self.entry_imagem.pack(pady=5, padx=20, fill="x")
        btn_procurar_imagem = ctk.CTkButton(self.content_frame, text="Procurar", font=("Arial", 14), fg_color="#1ABC9C", hover_color="#16A085", command=self.selecionar_imagem)
        btn_procurar_imagem.pack(pady=5, padx=20, fill="x")

        # Botão de adicionar pictograma
        btn_adicionar = ctk.CTkButton(self.content_frame, text="Adicionar", font=("Arial", 14), fg_color="#1ABC9C", hover_color="#16A085", command=self.adicionar_pictograma)
        btn_adicionar.pack(pady=20, padx=20, fill="x")

        # Tabela de pictogramas
        self.tree = ttk.Treeview(self.content_frame, columns=("ID", "Autista", "Nome", "Imagem"), show="headings", style="mystyle.Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Autista", text="Autista")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Imagem", text="Imagem")
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)

        # Estilo da tabela
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 12), rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=("Arial", 14, "bold"))  # Aplica negrito aos cabeçalhos

        # Botões de editar e excluir
        btn_editar = ctk.CTkButton(self.content_frame, text="Editar", font=("Arial", 14), fg_color="#3498DB", hover_color="#2980B9", command=self.editar_pictograma)
        btn_editar.pack(pady=10, padx=20, side="left", fill="x", expand=True)

        btn_excluir = ctk.CTkButton(self.content_frame, text="Excluir", font=("Arial", 14), fg_color="#E74C3C", hover_color="#C0392B", command=self.excluir_pictograma)
        btn_excluir.pack(pady=10, padx=20, side="right", fill="x", expand=True)

        # Carregar pictogramas ao iniciar
        self.carregar_pictogramas()

    def carregar_autistas(self):
        """Carrega a lista de autistas do banco de dados."""
        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM Usuarios WHERE tipo = "autista"')
        autistas = cursor.fetchall()
        conn.close()
        return [f"{nome} (ID: {id})" for id, nome in autistas]

    def selecionar_imagem(self):
        """Abre uma janela para selecionar um arquivo de imagem."""
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho_imagem:
            self.entry_imagem.delete(0, ctk.END)
            self.entry_imagem.insert(0, caminho_imagem)

    def carregar_pictogramas(self):
        """Carrega os pictogramas do banco de dados e exibe na tabela."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, u.nome, p.nome, p.imagem
            FROM Pictogramas p
            JOIN Usuarios u ON p.id_autista = u.id
            WHERE p.id_cuidador = ?
        ''', (self.id_cuidador,))
        pictogramas = cursor.fetchall()
        conn.close()

        for picto in pictogramas:
            self.tree.insert("", "end", values=picto)

    def adicionar_pictograma(self):
        """Adiciona um novo pictograma ao banco de dados."""
        autista_selecionado = self.combo_autistas.get()
        nome = self.entry_nome.get()
        imagem = self.entry_imagem.get()

        if not autista_selecionado or not nome or not imagem:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        id_autista = int(autista_selecionado.split("(ID: ")[1].replace(")", ""))

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Pictogramas (id_cuidador, id_autista, nome, imagem)
            VALUES (?, ?, ?, ?)
        ''', (self.id_cuidador, id_autista, nome, imagem))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pictograma adicionado!")
        self.carregar_pictogramas()

    def editar_pictograma(self):
        """Edita o pictograma selecionado."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum pictograma selecionado!")
            return

        id_pictograma = self.tree.item(selecionado, "values")[0]
        novo_nome = self.entry_nome.get()
        nova_imagem = self.entry_imagem.get()

        if not novo_nome or not nova_imagem:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Pictogramas SET nome = ?, imagem = ? WHERE id = ?', (novo_nome, nova_imagem, id_pictograma))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pictograma atualizado!")
        self.carregar_pictogramas()

    def excluir_pictograma(self):
        """Exclui o pictograma selecionado."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum pictograma selecionado!")
            return

        id_pictograma = self.tree.item(selecionado, "values")[0]

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Pictogramas WHERE id = ?', (id_pictograma,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pictograma excluído!")
        self.carregar_pictogramas()