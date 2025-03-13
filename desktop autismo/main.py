import tkinter as tk
from telas.login import TelaLogin

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de Apoio ao Autismo")
        self.root.geometry("500x500")  # Tamanho inicial da janela
        self.root.minsize(500, 500)  # Tamanho mínimo da janela
        self.root.configure(bg="#f0f0f0")  # Fundo cinza claro

        # Inicia a tela de login
        self.abrir_tela_login()

    def abrir_tela_login(self):
        # Limpa a tela atual (se houver widgets)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Carrega a tela de login
        self.tela_login = TelaLogin(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()