import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3

class VisualizarPictogramas:
    def __init__(self, root, id_autista, voltar_menu_callback, abrir_habilidades_callback, abrir_agenda_callback):
        self.root = root
        self.id_autista = id_autista
        self.voltar_menu_callback = voltar_menu_callback
        self.abrir_habilidades_callback = abrir_habilidades_callback
        self.abrir_agenda_callback = abrir_agenda_callback

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
            text="Meus Pictogramas", 
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
            text="Ir para Habilidades", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.abrir_habilidades_callback
        )
        btn_habilidades.pack(side="left", padx=5, fill="x", expand=True)

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

        # Frame para exibir as imagens
        self.imagens_frame = ctk.CTkFrame(self.frame, fg_color=self.cor_fundo, corner_radius=10)
        self.imagens_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame para os botões de ação
        botoes_acao_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        botoes_acao_frame.pack(pady=10, padx=10, fill="x")

        # Botão de adicionar pictograma
        btn_adicionar = ctk.CTkButton(
            botoes_acao_frame, 
            text="Adicionar Pictograma", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.adicionar_pictograma
        )
        btn_adicionar.pack(side="left", padx=5, fill="x", expand=True)

        # Botão de remover pictograma
        btn_remover = ctk.CTkButton(
            botoes_acao_frame, 
            text="Remover Pictograma", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao_voltar, 
            hover_color=self.cor_botao_voltar_hover, 
            corner_radius=8,
            command=self.remover_pictograma
        )
        btn_remover.pack(side="left", padx=5, fill="x", expand=True)

        # Botão de atualizar
        btn_atualizar = ctk.CTkButton(
            botoes_acao_frame, 
            text="Atualizar", 
            font=("Helvetica", 14), 
            fg_color=self.cor_botao, 
            hover_color=self.cor_botao_hover, 
            corner_radius=8,
            command=self.carregar_pictogramas
        )
        btn_atualizar.pack(side="left", padx=5, fill="x", expand=True)

        # Carregar pictogramas ao iniciar
        self.carregar_pictogramas()

    def carregar_pictogramas(self):
        """Carrega os pictogramas do banco de dados e exibe no frame."""
        # Limpar o frame de imagens
        for widget in self.imagens_frame.winfo_children():
            widget.destroy()

        # Buscar pictogramas no banco de dados
        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, imagem FROM Pictogramas WHERE id_autista = ?', (self.id_autista,))
        pictogramas = cursor.fetchall()
        conn.close()

        # Exibir as imagens
        for i, (id_pictograma, nome, caminho_imagem) in enumerate(pictogramas):
            try:
                imagem = Image.open(caminho_imagem)
                imagem = imagem.resize((100, 100))  # Redimensionar a imagem
                foto = ImageTk.PhotoImage(imagem)

                # Criar um label para exibir a imagem
                label_imagem = ctk.CTkLabel(self.imagens_frame, image=foto, text="")
                label_imagem.image = foto  # Manter uma referência para evitar garbage collection
                label_imagem.grid(row=i // 4, column=i % 4, padx=10, pady=10)

                # Adicionar o nome do pictograma abaixo da imagem
                label_nome = ctk.CTkLabel(self.imagens_frame, text=nome, font=("Helvetica", 10))
                label_nome.grid(row=i // 4 + 1, column=i % 4, padx=10, pady=5)

                # Adicionar evento de clique para ampliar a imagem
                label_imagem.bind("<Button-1>", lambda e, img=caminho_imagem: self.ampliar_imagem(img))
            except Exception as e:
                print(f"Erro ao carregar a imagem {caminho_imagem}: {e}")

    def ampliar_imagem(self, caminho_imagem):
        """Exibe a imagem ampliada em uma nova janela."""
        janela_ampliada = ctk.CTkToplevel(self.root)
        janela_ampliada.title("Imagem Ampliada")
        janela_ampliada.geometry("400x400")

        try:
            imagem = Image.open(caminho_imagem)
            imagem = imagem.resize((300, 300))  # Redimensionar a imagem
            foto = ImageTk.PhotoImage(imagem)

            label_imagem = ctk.CTkLabel(janela_ampliada, image=foto, text="")
            label_imagem.image = foto  # Manter uma referência
            label_imagem.pack(pady=20, padx=20)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}")

    def adicionar_pictograma(self):
        """Adiciona um novo pictograma ao banco de dados."""
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho_imagem:
            nome = caminho_imagem.split("/")[-1]  # Pega o nome do arquivo
            conn = sqlite3.connect('autismo_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Pictogramas (id_autista, nome, imagem) VALUES (?, ?, ?)', (self.id_autista, nome, caminho_imagem))
            conn.commit()
            conn.close()
            self.carregar_pictogramas()

    def remover_pictograma(self):
        """Remove o último pictograma adicionado."""
        selecionado = messagebox.askquestion("Remover Pictograma", "Tem certeza que deseja remover o pictograma selecionado?")
        if selecionado != "yes":
            return

        conn = sqlite3.connect('autismo_app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Pictogramas WHERE id_autista = ? ORDER BY id DESC LIMIT 1', (self.id_autista,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pictograma removido!")
        self.carregar_pictogramas()