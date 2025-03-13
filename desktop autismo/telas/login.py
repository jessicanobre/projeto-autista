import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from telas.autista.agenda import AgendaAutista
from telas.autista.habilidades import HabilidadesAutista
from telas.autista.visualizar_pictogramas import VisualizarPictogramas
from telas.cuidadores.gerenciar_rotinas import GerenciarRotinas
from telas.cuidadores.gerenciar_habilidades import GerenciarHabilidades
from telas.cuidadores.gerenciar_pictogramas import GerenciarPictogramas
from telas.cadastro import TelaCadastro
from PIL import Image, ImageTk  # Para carregar ícones

# Configuração do tema do customtkinter
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema azul

class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Autismo")
        self.root.geometry("600x600")  # Tamanho inicial da janela
        self.root.minsize(600, 600)  # Tamanho mínimo da janela

        # Cores personalizadas
        self.cor_fundo = "#F5F5F5"
        self.cor_primaria = "#42A5F5"
        self.cor_secundaria = "#64B5F6"
        self.cor_texto = "#2C3E50"
        self.cor_borda = "#B0BEC5"

        # Frame principal
        self.frame = ctk.CTkFrame(root, fg_color=self.cor_fundo, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o frame

        # Cabeçalho com ícone
        self.cabecalho_frame = ctk.CTkFrame(self.frame, fg_color="transparent", corner_radius=15)
        self.cabecalho_frame.pack(pady=(20, 10), fill="x")

        # Ícone de quebra-cabeça (simulado com texto)
        ctk.CTkLabel(self.cabecalho_frame, text="🧩", font=("Arial", 60), text_color=self.cor_primaria).pack(pady=10)
        ctk.CTkLabel(self.cabecalho_frame, text="Login - Autismo", font=("Arial", 24, "bold"), text_color=self.cor_texto).pack(pady=5)

        # Campo de usuário
        self.usuario_frame = ctk.CTkFrame(self.frame, fg_color="transparent", corner_radius=15)
        self.usuario_frame.pack(pady=10, fill="x")

        ctk.CTkLabel(self.usuario_frame, text="Usuário:", font=("Arial", 14), text_color=self.cor_texto).pack(pady=5)
        self.entry_usuario = ctk.CTkEntry(
            self.usuario_frame, 
            font=("Arial", 14), 
            placeholder_text="Digite seu usuário", 
            width=300, 
            corner_radius=8,
            border_color=self.cor_borda,
            fg_color="#FFFFFF"
        )
        self.entry_usuario.pack(pady=5)

        # Campo de senha
        self.senha_frame = ctk.CTkFrame(self.frame, fg_color="transparent", corner_radius=15)
        self.senha_frame.pack(pady=10, fill="x")

        ctk.CTkLabel(self.senha_frame, text="Senha:", font=("Arial", 14), text_color=self.cor_texto).pack(pady=5)
        self.entry_senha = ctk.CTkEntry(
            self.senha_frame, 
            show="*", 
            font=("Arial", 14), 
            placeholder_text="Digite sua senha", 
            width=300, 
            corner_radius=8,
            border_color=self.cor_borda,
            fg_color="#FFFFFF"
        )
        self.entry_senha.pack(pady=5)

        # Botão de login
        self.btn_login = ctk.CTkButton(
            self.frame, 
            text="Login", 
            font=("Arial", 16, "bold"), 
            fg_color=self.cor_primaria, 
            hover_color=self.cor_secundaria, 
            command=self.verificar_login, 
            width=300, 
            corner_radius=8,
            border_color=self.cor_borda,
            border_width=1
        )
        self.btn_login.pack(pady=20)

        # Botão de cadastro
        self.btn_cadastro = ctk.CTkButton(
            self.frame, 
            text="Cadastrar", 
            font=("Arial", 14), 
            fg_color="transparent", 
            hover_color=self.cor_secundaria, 
            text_color=self.cor_primaria, 
            command=self.abrir_tela_cadastro, 
            width=300, 
            corner_radius=8,
            border_color=self.cor_primaria,
            border_width=1
        )
        self.btn_cadastro.pack(pady=5)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # Validação de campos vazios
        if not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, tipo FROM Usuarios WHERE nome = ? AND senha = ?', (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            id_usuario, tipo_usuario = resultado
            self.abrir_interface_correta(id_usuario, tipo_usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def abrir_interface_correta(self, id_usuario, tipo_usuario):
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()

        if tipo_usuario == "cuidador":
            # Menu para cuidadores
            menu_frame = ctk.CTkFrame(self.root, fg_color=self.cor_fundo, corner_radius=15)
            menu_frame.pack(pady=20, padx=50, fill="both", expand=True)

            # Callback para abrir a tela de rotinas
            def abrir_rotinas():
                for widget in self.root.winfo_children():
                    widget.destroy()
                GerenciarRotinas(
                    self.root, 
                    id_usuario, 
                    lambda: self.abrir_interface_correta(id_usuario, tipo_usuario), 
                    lambda: abrir_habilidades(), 
                    lambda: abrir_pictogramas()
                )

            # Callback para abrir a tela de habilidades
            def abrir_habilidades():
                for widget in self.root.winfo_children():
                    widget.destroy()
                GerenciarHabilidades(
                    self.root, 
                    id_usuario, 
                    lambda: self.abrir_interface_correta(id_usuario, tipo_usuario), 
                    lambda: abrir_rotinas(), 
                    lambda: abrir_pictogramas()
                )

            # Callback para abrir a tela de pictogramas
            def abrir_pictogramas():
                for widget in self.root.winfo_children():
                    widget.destroy()
                GerenciarPictogramas(
                    self.root, 
                    id_usuario, 
                    lambda: self.abrir_interface_correta(id_usuario, tipo_usuario), 
                    lambda: abrir_rotinas(), 
                    lambda: abrir_habilidades()
                )

            # Botões do menu
            btn_rotinas = ctk.CTkButton(menu_frame, text="Gerenciar Rotinas", font=("Arial", 16, "bold"), fg_color=self.cor_primaria, hover_color=self.cor_secundaria, command=abrir_rotinas)
            btn_rotinas.pack(pady=10, padx=50, fill="x")

            btn_habilidades = ctk.CTkButton(menu_frame, text="Gerenciar Habilidades", font=("Arial", 16, "bold"), fg_color=self.cor_primaria, hover_color=self.cor_secundaria, command=abrir_habilidades)
            btn_habilidades.pack(pady=10, padx=50, fill="x")

            btn_pictogramas = ctk.CTkButton(menu_frame, text="Gerenciar Pictogramas", font=("Arial", 16, "bold"), fg_color=self.cor_primaria, hover_color=self.cor_secundaria, command=abrir_pictogramas)
            btn_pictogramas.pack(pady=10, padx=50, fill="x")

        elif tipo_usuario == "autista":
            # Menu para autistas
            menu_frame = ctk.CTkFrame(self.root, fg_color=self.cor_fundo, corner_radius=15)
            menu_frame.pack(pady=20, padx=50, fill="both", expand=True)

            # Callback para abrir a tela de agenda
            def abrir_agenda():
                for widget in self.root.winfo_children():
                    widget.destroy()
                AgendaAutista(
                    self.root, 
                    id_usuario, 
                    lambda: self.abrir_interface_correta(id_usuario, tipo_usuario), 
                    lambda: abrir_habilidades(), 
                    lambda: abrir_pictogramas()
                )

            # Callback para abrir a tela de habilidades
            def abrir_habilidades():
                for widget in self.root.winfo_children():
                    widget.destroy()
                HabilidadesAutista(
                    self.root, 
                    id_usuario, 
                    lambda: self.abrir_interface_correta(id_usuario, tipo_usuario), 
                    lambda: abrir_agenda(), 
                    lambda: abrir_pictogramas()
                )

            # Callback para abrir a tela de pictogramas
            def abrir_pictogramas():
                for widget in self.root.winfo_children():
                    widget.destroy()
                VisualizarPictogramas(
                    self.root, 
                    id_usuario, 
                    lambda: self.abrir_interface_correta(id_usuario, tipo_usuario), 
                    lambda: abrir_habilidades(), 
                    lambda: abrir_agenda()
                )

            # Botões do menu
            btn_agenda = ctk.CTkButton(menu_frame, text="Agenda", font=("Arial", 16, "bold"), fg_color=self.cor_primaria, hover_color=self.cor_secundaria, command=abrir_agenda)
            btn_agenda.pack(pady=10, padx=50, fill="x")

            btn_habilidades = ctk.CTkButton(menu_frame, text="Habilidades", font=("Arial", 16, "bold"), fg_color=self.cor_primaria, hover_color=self.cor_secundaria, command=abrir_habilidades)
            btn_habilidades.pack(pady=10, padx=50, fill="x")

            btn_pictogramas = ctk.CTkButton(menu_frame, text="Pictogramas", font=("Arial", 16, "bold"), fg_color=self.cor_primaria, hover_color=self.cor_secundaria, command=abrir_pictogramas)
            btn_pictogramas.pack(pady=10, padx=50, fill="x")

    def abrir_tela_cadastro(self):
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Abre a tela de cadastro
        TelaCadastro(self.root, self.voltar_login)

    def voltar_login(self):
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Volta para a tela de login
        TelaLogin(self.root)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TelaLogin(root)
    root.mainloop()