import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk

class TelaCadastro:
    def __init__(self, root, abrir_tela_login):
        self.root = root
        self.abrir_tela_login = abrir_tela_login
        self.root.title("Cadastro")
        self.root.geometry("600x700")
        self.root.minsize(600, 700)

        self.caminho_foto = None

        # Configuração do tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Cores personalizadas (tons discretos e profissionais)
        self.cor_fundo = "#F5F5F5"  # Fundo claro
        self.cor_primaria = "#607D8B"  # Azul acinzentado
        self.cor_secundaria = "#78909C"  # Azul acinzentado mais claro
        self.cor_texto = "#37474F"  # Texto escuro
        self.cor_borda = "#CFD8DC"  # Bordas claras
        self.cor_botao = "#607D8B"  # Botões com cor primária
        self.cor_botao_hover = "#78909C"  # Efeito hover suave
        self.cor_botao_voltar = "#B0BEC5"  # Cinza para botão de voltar
        self.cor_botao_voltar_hover = "#90A4AE"  # Cinza mais escuro para hover

        # Frame principal
        main_frame = ctk.CTkFrame(root, fg_color=self.cor_fundo, corner_radius=15)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        titulo = ctk.CTkLabel(main_frame, text="Cadastro", font=("Helvetica", 28, "bold"), text_color=self.cor_primaria)
        titulo.pack(pady=10)

        # Frame para os campos de entrada
        campos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        campos_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Configuração do grid para responsividade
        campos_frame.grid_columnconfigure(0, weight=1)
        campos_frame.grid_columnconfigure(1, weight=3)

        # Função para criar campos de entrada
        def criar_campo(frame, texto, row, placeholder, show=None):
            label = ctk.CTkLabel(frame, text=texto, font=("Helvetica", 14), text_color=self.cor_texto)
            label.grid(row=row, column=0, pady=5, padx=10, sticky="w")
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=300, corner_radius=8, border_color=self.cor_borda, show=show)
            entry.grid(row=row, column=1, pady=5, padx=10, sticky="ew")
            return entry

        # Campos de entrada
        self.entry_nome = criar_campo(campos_frame, "Nome:", 0, "Digite seu nome")
        self.entry_email = criar_campo(campos_frame, "Email:", 1, "Digite seu email")
        self.entry_telefone = criar_campo(campos_frame, "Telefone:", 2, "Digite seu telefone")
        self.entry_endereco = criar_campo(campos_frame, "Endereço:", 3, "Digite seu endereço")

        # Seleção do tipo de usuário
        label_tipo = ctk.CTkLabel(campos_frame, text="Tipo de Usuário:", font=("Helvetica", 14), text_color=self.cor_texto)
        label_tipo.grid(row=4, column=0, pady=5, padx=10, sticky="w")
        self.tipo_usuario = ctk.StringVar(value="autista")
        radio_autista = ctk.CTkRadioButton(campos_frame, text="Autista", variable=self.tipo_usuario, value="autista", command=self.toggle_campos_autista, font=("Helvetica", 14))
        radio_autista.grid(row=4, column=1, pady=5, padx=10, sticky="w")
        radio_cuidador = ctk.CTkRadioButton(campos_frame, text="Cuidador", variable=self.tipo_usuario, value="cuidador", command=self.toggle_campos_autista, font=("Helvetica", 14))
        radio_cuidador.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        # Campo de nível de apoio (apenas para autistas)
        self.label_nivel_apoio = ctk.CTkLabel(campos_frame, text="Nível de Apoio:", font=("Helvetica", 14), text_color=self.cor_texto)
        self.combo_nivel_apoio = ctk.CTkComboBox(campos_frame, values=["Nível 1: Necessidade de pouco apoio", "Nível 2: Necessidade moderada de apoio", "Nível 3: Necessidade de muito apoio"], width=300, corner_radius=8, border_color=self.cor_borda)
        self.combo_nivel_apoio.set("Nível 1: Necessidade de pouco apoio")

        # Campo de idade (apenas para autistas)
        self.label_idade = ctk.CTkLabel(campos_frame, text="Idade:", font=("Helvetica", 14), text_color=self.cor_texto)
        self.entry_idade = ctk.CTkEntry(campos_frame, placeholder_text="Digite sua idade", width=300, corner_radius=8, border_color=self.cor_borda)

        # Campo de escolaridade (apenas para autistas)
        self.label_escolaridade = ctk.CTkLabel(campos_frame, text="Escolaridade:", font=("Helvetica", 14), text_color=self.cor_texto)
        self.entry_escolaridade = ctk.CTkEntry(campos_frame, placeholder_text="Digite sua escolaridade", width=300, corner_radius=8, border_color=self.cor_borda)

        # Campo de senha
        self.entry_senha = criar_campo(campos_frame, "Senha:", 6, "Digite sua senha", show="*")

        # Campo de foto de perfil
        label_foto = ctk.CTkLabel(campos_frame, text="Foto de Perfil:", font=("Helvetica", 14), text_color=self.cor_texto)
        label_foto.grid(row=7, column=0, pady=5, padx=10, sticky="w")
        self.btn_selecionar_foto = ctk.CTkButton(campos_frame, text="Selecionar Foto", command=self.selecionar_foto, width=300, fg_color=self.cor_primaria, hover_color=self.cor_secundaria, corner_radius=8)
        self.btn_selecionar_foto.grid(row=7, column=1, pady=5, padx=10, sticky="ew")

        # Frame para os botões (centralizado)
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.pack(pady=10, fill="x", expand=False)

        # Botão de cadastro
        btn_cadastrar = ctk.CTkButton(botoes_frame, text="Cadastrar", command=self.cadastrar_usuario, width=300, fg_color=self.cor_botao, hover_color=self.cor_botao_hover, corner_radius=8)
        btn_cadastrar.pack(pady=5)

        # Botão de voltar
        btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", command=self.abrir_tela_login, width=300, fg_color=self.cor_botao_voltar, hover_color=self.cor_botao_voltar_hover, corner_radius=8)
        btn_voltar.pack(pady=5)

        # Inicialmente, esconder campos específicos de autista
        self.toggle_campos_autista()

    def toggle_campos_autista(self):
        if self.tipo_usuario.get() == "autista":
            self.label_nivel_apoio.grid(row=8, column=0, pady=5, padx=10, sticky="w")
            self.combo_nivel_apoio.grid(row=8, column=1, pady=5, padx=10, sticky="ew")
            self.label_idade.grid(row=9, column=0, pady=5, padx=10, sticky="w")
            self.entry_idade.grid(row=9, column=1, pady=5, padx=10, sticky="ew")
            self.label_escolaridade.grid(row=10, column=0, pady=5, padx=10, sticky="w")
            self.entry_escolaridade.grid(row=10, column=1, pady=5, padx=10, sticky="ew")
        else:
            self.label_nivel_apoio.grid_forget()
            self.combo_nivel_apoio.grid_forget()
            self.label_idade.grid_forget()
            self.entry_idade.grid_forget()
            self.label_escolaridade.grid_forget()
            self.entry_escolaridade.grid_forget()

    def selecionar_foto(self):
        self.caminho_foto = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if self.caminho_foto:
            messagebox.showinfo("Sucesso", "Foto selecionada com sucesso!")

    def cadastrar_usuario(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        telefone = self.entry_telefone.get()
        endereco = self.entry_endereco.get()
        tipo = self.tipo_usuario.get()
        nivel_apoio = self.combo_nivel_apoio.get() if tipo == "autista" else None
        idade = self.entry_idade.get() if tipo == "autista" else None
        escolaridade = self.entry_escolaridade.get() if tipo == "autista" else None
        senha = self.entry_senha.get()
        foto = self.caminho_foto

        # Validação dos campos obrigatórios
        if not nome or not email or not telefone or not endereco or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        # Validação da idade (deve ser um número)
        if tipo == "autista" and (not idade or not idade.isdigit()):
            messagebox.showerror("Erro", "Idade deve ser um número válido!")
            return

        # Conexão com o banco de dados
        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO Usuarios (nome, email, telefone, endereco, tipo, senha, nivel_apoio, idade, escolaridade, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, telefone, endereco, tipo, senha, nivel_apoio, idade, escolaridade, foto))
            conn.commit()

            # Se for cuidador, relacionar com autistas
            if tipo == "cuidador":
                id_cuidador = cursor.lastrowid
                autistas = self.carregar_autistas()
                for autista in autistas:
                    id_autista = autista[0]
                    cursor.execute('''
                        INSERT INTO Relacionamentos (id_cuidador, id_autista)
                        VALUES (?, ?)
                    ''', (id_cuidador, id_autista))
                conn.commit()

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.abrir_tela_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado!")
        finally:
            conn.close()

    def carregar_autistas(self):
        """Carrega a lista de autistas do banco de dados."""
        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM Usuarios WHERE tipo = "autista"')
        autistas = cursor.fetchall()
        conn.close()
        return autistas