import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading

class AplicacaoLembrete:
    def __init__(self, root):
        self.root = root
        self.root.title("Notify App")
        self.root.geometry("400x200")

        self.label_hora = tk.Label(root, text="Escolha o horário do lembrete:")
        self.label_hora.pack(pady=10)

        # Widget para escolha de hora
        self.combobox_hora = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(24)], state="readonly")
        self.combobox_hora.set("00")
        self.combobox_hora.pack(pady=5)

        # Widget para escolha de minutos
        self.combobox_minutos = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(60)], state="readonly")
        self.combobox_minutos.set("00")
        self.combobox_minutos.pack(pady=5)

        # Widget para inserção do nome do lembrete
        self.label_nome_lembrete = tk.Label(root, text="Nome do lembrete:")
        self.label_nome_lembrete.pack(pady=5)

        self.entry_nome_lembrete = tk.Entry(root)
        self.entry_nome_lembrete.pack(pady=5)

        self.button_definir = tk.Button(root, text="Definir Lembrete", command=self.definir_lembrete)
        self.button_definir.pack(pady=10)

        self.lembrete_thread = None

    def definir_lembrete(self):
        hora_selecionada = self.combobox_hora.get()
        minutos_selecionados = self.combobox_minutos.get()
        nome_lembrete = self.entry_nome_lembrete.get()

        try:
            horario_lembrete = datetime.datetime.strptime(f"{hora_selecionada}:{minutos_selecionados}", "%H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Formato de horário inválido. Use HH:MM.")
            return

        agora = datetime.datetime.now()
        horario_lembrete = horario_lembrete.replace(year=agora.year, month=agora.month, day=agora.day)

        if horario_lembrete < agora:
            horario_lembrete += datetime.timedelta(days=1)

        segundos_para_lembrete = (horario_lembrete - agora).total_seconds()

        if self.lembrete_thread:
            self.lembrete_thread.cancel()

        self.lembrete_thread = threading.Timer(segundos_para_lembrete, self.mostrar_lembrete, args=(nome_lembrete,))
        self.lembrete_thread.start()

        messagebox.showinfo("Sucesso", "Lembrete definido com sucesso.")

    def mostrar_lembrete(self, nome_lembrete):
        mensagem = f"Lembrete! Não se esqueça: '{nome_lembrete}'!"

        # Cria uma nova janela (top) para a mensagem
        top = tk.Toplevel(self.root)
        top.title("Lembrete")

        # Calcula as coordenadas para centralizar a janela de lembrete
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width - top.winfo_reqwidth()) / 2
        y = (screen_height - top.winfo_reqheight()) / 2

        # Define as coordenadas e exibe a nova janela
        top.geometry("+%d+%d" % (x, y))
        tk.Label(top, text=mensagem).pack()

        # Configura a nova janela (top) para ficar sempre no topo
        top.attributes('-topmost', 1)

        # Exibe a nova janela
        top.focus_force()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoLembrete(root)
    root.mainloop()
