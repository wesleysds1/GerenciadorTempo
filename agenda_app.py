import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, END
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image, ImageTk
import sqlite3

class Evento:
    def __init__(self, id, titulo, hora, descricao):
        self.id = id
        self.titulo = titulo
        self.hora = hora
        self.descricao = descricao
        
class AdicionarEventoPopup:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback

        self.popup = tk.Toplevel(master)
        self.popup.title("Adicionar Evento")
        self.popup.transient(master)
        self.popup.config(bg="#dce1e6")


        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        popup_width = 280
        popup_height = 250

        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2

        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        self.titulo_label = tk.Label(self.popup, text="Título:", bg="#dce1e6")
        self.titulo_label.grid(row=0, column=0, sticky="w")

        self.titulo_entry = tk.Entry(self.popup)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)

        self.hora_label = tk.Label(self.popup, text="Hora:", bg="#dce1e6")
        self.hora_label.grid(row=1, column=0, sticky="w")

        self.hora_entry = tk.Entry(self.popup)
        self.hora_entry.grid(row=1, column=1, padx=5, pady=5)
        self.hora_entry.insert(tk.END, "")  # Valor inicial vazio
        self.hora_entry.old_value = ""  # Valor inicial vazio
        self.hora_entry.bind("<KeyRelease>", self.formatar_hora)

        self.descricao_label = tk.Label(self.popup, text="Descrição:", bg="#dce1e6")
        self.descricao_label.grid(row=2, column=0, sticky="w")

        self.descricao_entry = tk.Text(self.popup, height=5, width=20)
        self.descricao_entry.grid(row=2, column=1, padx=5, pady=5)

        self.salvar_button_img = Image.open("Salvar.png")
        self.salvar_button_img = self.salvar_button_img.resize((25, 25))
        self.salvar_button_img = ImageTk.PhotoImage(self.salvar_button_img)
        self.salvar_button = tk.Button(self.popup, text="Salvar", image=self.salvar_button_img, compound="top", command=self.salvar_evento, bg="#96a4b5")
        self.salvar_button.grid(row=3, column=0, columnspan=2, pady=10)

    def formatar_hora(self, event):
        entrada = self.hora_entry.get()
    
        # Remove caracteres não numéricos
        nova_entrada = ''.join(c for c in entrada if c.isdigit() or c == ':')

        # Limita o tamanho máximo da entrada para 5 caracteres
        nova_entrada = nova_entrada[:5]

        # Adiciona ":" após os dois primeiros caracteres, se necessário
        if len(nova_entrada) >= 2 and ':' not in nova_entrada:
            nova_entrada = nova_entrada[:2] + ":" + nova_entrada[2:]

        # Atualiza o campo de entrada
        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, nova_entrada)

    def salvar_evento(self):
        titulo = self.titulo_entry.get()
        hora = self.hora_entry.get()
        descricao = self.descricao_entry.get("1.0", "end-1c")

        if not (titulo and hora):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        # Verificar se a hora está no formato correto (HH:MM)
        try:
            horas, minutos = map(int, hora.split(':'))
            if horas < 0 or horas > 23 or minutos < 0 or minutos > 59:
                raise ValueError("Hora inválida")
        except ValueError:
            messagebox.showwarning("Aviso", "Hora inválida.")
            return

        self.callback(titulo, hora, descricao)
        self.popup.destroy()

class DetalheEventoPopup:
    def __init__(self, master, evento, voltar_callback):
        self.master = master
        self.evento = evento
        self.voltar_callback = voltar_callback

        self.popup = tk.Toplevel(master)
        self.popup.title("Evento")
        self.popup.transient(master)
        self.popup.config(bg="#dce1e6")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        popup_width = 200
        popup_height = 200

        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2

        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        self.titulo_label = tk.Label(self.popup, text="Título:", bg="#dce1e6")
        self.titulo_label.grid(row=0, column=0, sticky="w")

        self.titulo_value = tk.Label(self.popup, text=evento.titulo, bg="#dce1e6")
        self.titulo_value.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.hora_label = tk.Label(self.popup, text="Hora:", bg="#dce1e6")
        self.hora_label.grid(row=1, column=0, sticky="w")

        self.hora_value = tk.Label(self.popup, text=evento.hora, bg="#dce1e6")
        self.hora_value.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.descricao_label = tk.Label(self.popup, text="Descrição:", bg="#dce1e6")
        self.descricao_label.grid(row=2, column=0, sticky="w")

        self.descricao_value = tk.Label(self.popup, text=evento.descricao, wraplength=200, justify="left", bg="#dce1e6")
        self.descricao_value.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.voltar_button_img = Image.open("Voltar.png")  # Substitua "back_icon.png" pelo caminho do seu ícone
        self.voltar_button_img = self.voltar_button_img.resize((25, 25))
        self.voltar_button_img = ImageTk.PhotoImage(self.voltar_button_img)
        self.voltar_button = tk.Button(self.popup, text="Voltar", image=self.voltar_button_img, compound="top", command=self.voltar, bg="#96a4b5")
        self.voltar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def voltar(self):
        self.popup.destroy()
        self.voltar_callback()

class EditarEventoPopup:
    def __init__(self, master, evento, callback):
        self.master = master
        self.evento = evento
        self.callback = callback

        self.popup = tk.Toplevel(master)
        self.popup.title("Editar Evento")
        self.popup.transient(master)
        self.popup.config(bg="#dce1e6")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        popup_width = 300
        popup_height = 300

        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2

        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        self.novo_titulo_label = tk.Label(self.popup, text="Novo Título:", bg="#dce1e6")
        self.novo_titulo_label.grid(row=0, column=0, sticky="w")

        self.novo_titulo_entry = tk.Entry(self.popup)
        self.novo_titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        self.novo_titulo_entry.insert(tk.END, evento.titulo)

        self.nova_hora_label = tk.Label(self.popup, text="Nova Hora:", bg="#dce1e6")
        self.nova_hora_label.grid(row=1, column=0, sticky="w")

        self.nova_hora_entry = tk.Entry(self.popup)
        self.nova_hora_entry.grid(row=1, column=1, padx=5, pady=5)
        self.nova_hora_entry.insert(tk.END, evento.hora)

        self.nova_descricao_label = tk.Label(self.popup, text="Nova Descrição:", bg="#dce1e6")
        self.nova_descricao_label.grid(row=2, column=0, sticky="w")

        self.nova_descricao_entry = tk.Text(self.popup, height=5, width=20)
        self.nova_descricao_entry.grid(row=2, column=1, padx=5, pady=5)
        self.nova_descricao_entry.insert(tk.END, evento.descricao)

        self.salvar_button_img = Image.open("Salvar.png")  # Substitua "Salvar.png" pelo caminho do seu ícone
        self.salvar_button_img = self.salvar_button_img.resize((25, 25))  
        self.salvar_button_img = ImageTk.PhotoImage(self.salvar_button_img)
        self.salvar_button = tk.Button(self.popup, text="Salvar", image=self.salvar_button_img, compound="top", command=self.salvar_edicao, bg="#96a4b5")
        self.salvar_button.grid(row=3, column=0, columnspan=2, pady=10)

    def salvar_edicao(self):
        novo_titulo = self.novo_titulo_entry.get()
        nova_hora = self.nova_hora_entry.get()
        nova_descricao = self.nova_descricao_entry.get("1.0", "end-1c")

        if not (novo_titulo and nova_hora):  # Verifica se título e hora foram preenchidos
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        self.callback(self.evento, novo_titulo, nova_hora, nova_descricao)
        self.popup.destroy()

class AgendaApp:
    def __init__(self, master):
        self.master = master
        master.title("Agenda Pessoal")
        master.config(bg="#dce1e6")  # Defina a cor de fundo desejada
        master.geometry("440x500")

        self.conn = sqlite3.connect('agenda.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS eventos
                          (id INTEGER PRIMARY KEY, titulo TEXT, hora TEXT, descricao TEXT)''')
        self.conn.commit()


        self.agenda = {}
        self.data_selecionada = None
    
        locale = 'pt_BR.UTF-8'

        master.update_idletasks()
        self.centralizar_janela()

        self.calendario = Calendar(master, locale=locale, selectmode='day', date_pattern='dd/mm/yyyy', font="Arial 14",
                                   firstweekday='sunday')
        self.calendario.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.calendario.bind("<<CalendarSelected>>", self.on_date_select)

        self.eventos_label = tk.Label(master, text="Eventos:", bg="#dce1e6", font="Arial 12 bold")
        self.eventos_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        self.eventos_listbox = tk.Listbox(master, height=5, width=40)
        self.eventos_listbox.grid(row=2, column=0, columnspan=3, padx=10)
        self.eventos_listbox.bind("<ButtonRelease-1>", self.selecionar_evento)

        self.adicionar_button_img = Image.open("Adicionar.png")
        self.adicionar_button_img = self.adicionar_button_img.resize((25, 25))
        self.adicionar_button_img = ImageTk.PhotoImage(self.adicionar_button_img)

        self.detalhe_button_img = Image.open("Detalhar.png")
        self.detalhe_button_img = self.detalhe_button_img.resize((25, 25))
        self.detalhe_button_img = ImageTk.PhotoImage(self.detalhe_button_img)

        self.editar_button_img = Image.open("Editar.png")
        self.editar_button_img = self.editar_button_img.resize((25, 25))
        self.editar_button_img = ImageTk.PhotoImage(self.editar_button_img)

        self.excluir_button_img = Image.open("Apagar.png")
        self.excluir_button_img = self.excluir_button_img.resize((25, 25))
        self.excluir_button_img = ImageTk.PhotoImage(self.excluir_button_img)

        self.hoje_button_img = Image.open("Hoje.png")
        self.hoje_button_img = self.hoje_button_img.resize((25, 25))
        self.hoje_button_img = ImageTk.PhotoImage(self.hoje_button_img)

        self.adicionar_button = tk.Button(master, text="Adicionar", image=self.adicionar_button_img, compound="top", command=self.mostrar_pop_up, bg="#96a4b5")
        self.adicionar_button.grid(row=3, column=1, pady=(5, 10))

        self.editar_button = tk.Button(master, text="Editar", image=self.editar_button_img, compound="top", command=self.editar_evento, state=tk.DISABLED, bg="#96a4b5")  
        self.editar_button.grid(row=4, column=1)

        self.detalhe_button = tk.Button(master, text="Detalhe", image=self.detalhe_button_img, compound="top", command=self.detalhe_evento, state=tk.DISABLED, bg="#96a4b5")
        self.detalhe_button.grid(row=4, column=0)

        self.excluir_button = tk.Button(master, text="Excluir", image=self.excluir_button_img, compound="top", command=self.excluir_evento, state=tk.DISABLED, bg="#96a4b5")
        self.excluir_button.grid(row=4, column=2)

        self.hoje_button = tk.Button(master, text="Hoje", image=self.hoje_button_img, compound="top", command=self.ir_para_hoje, bg="#96a4b5")
        self.hoje_button.grid(row=0, column=3, padx=5)   

        self.configurar_data_atual()
        self.marcar_dia_atual()

        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="Sair", command=self.sair_app)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        
    def centralizar_janela(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def ir_para_hoje(self):
        self.configurar_data_atual()
        self.marcar_dia_atual()
        self.mostrar_eventos()

    def configurar_data_atual(self):
        data_atual = datetime.today().date()
        self.calendario.selection_set(data_atual)
        self.data_selecionada = data_atual
        self.mostrar_eventos()

    def marcar_dia_atual(self):
        if self.data_selecionada:
            dia_atual = self.data_selecionada.day
            self.calendario.calevent_create(self.data_selecionada, f"{dia_atual}_hoje", "hoje")

    def on_date_select(self, event):
        date = self.calendario.get_date()
        date_obj = datetime.strptime(date, '%d/%m/%Y').date()

        self.data_selecionada = date_obj
        self.mostrar_eventos()  # Atualiza os eventos ao selecionar uma nova data

    def mostrar_eventos(self):
        self.eventos_listbox.delete(0, END)

        if not self.calendario or self.data_selecionada is None:
            return

        self.calendario.calevent_remove("evento")
        self.calendario.calevent_remove("no_event")

        # Recuperando os eventos do banco de dados para a data selecionada
        data_selecionada_texto = self.data_selecionada.strftime('%Y-%m-%d')
        self.c.execute("SELECT titulo, data FROM eventos WHERE data = ?", (data_selecionada_texto,))
        eventos_do_dia = self.c.fetchall()

        if eventos_do_dia:
            for evento in eventos_do_dia:
                self.eventos_listbox.insert(tk.END, evento[0])  # Adiciona o título do evento
            # Habilitar os botões pois há eventos associados ao dia selecionado
            self.detalhe_button.config(state=tk.NORMAL)
            self.editar_button.config(state=tk.NORMAL)
            self.excluir_button.config(state=tk.NORMAL)
        else:
            # Se não houver eventos para o dia selecionado, adicionar a frase "Não há eventos para este dia"
            self.eventos_listbox.insert(tk.END, "Não há eventos para este dia")
            # Desabilitar os botões pois não há eventos associados ao dia selecionado
            self.detalhe_button.config(state=tk.DISABLED)
            self.editar_button.config(state=tk.DISABLED)
            self.excluir_button.config(state=tk.DISABLED)

        # Marcar os dias com eventos no calendário
        self.c.execute("SELECT DISTINCT data FROM eventos")
        eventos = self.c.fetchall()

        for evento in eventos:
            data_evento_obj = datetime.strptime(evento[0], '%Y-%m-%d').date()
            dia_evento = data_evento_obj.day
            self.calendario.calevent_create(data_evento_obj, f"{dia_evento}_evento", "evento")

        self.calendario.tag_config("evento", background="#f26c4f")  # Define a cor de fundo para os dias com eventos

    def on_calendar_click(self, event):
        date = self.calendario.get_date()
        date_obj = datetime.strptime(date, '%d/%m/%Y').date()

        eventos_do_dia = self.agenda.get(date_obj, [])
        if eventos_do_dia:
            eventos = "\n".join([evento.titulo for evento in eventos_do_dia])
            messagebox.showinfo("Eventos", eventos)

    def mostrar_pop_up(self):
        if not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma data no calendário.")
            return

        AdicionarEventoPopup(self.master, self.adicionar_evento)

    def adicionar_evento(self, titulo, hora, descricao):
        if self.data_selecionada is None:
            messagebox.showwarning("Aviso", "Selecione uma data no calendário.")
            return

        # Obtendo a data selecionada no formato de texto 'YYYY-MM-DD'
        data_selecionada_texto = self.data_selecionada.strftime('%Y-%m-%d')

        # Inserindo o evento no banco de dados
        self.c.execute("INSERT INTO eventos (titulo, hora, descricao, data) VALUES (?, ?, ?, ?)",
                   (titulo, hora, descricao, data_selecionada_texto))
        self.conn.commit()
        self.mostrar_eventos()

    def detalhe_evento(self):
        indice_selecionado = self.eventos_listbox.curselection()
        if indice_selecionado:
            titulo_evento = self.eventos_listbox.get(indice_selecionado[0])
            self.mostrar_detalhes_evento(titulo_evento)
        else:
            messagebox.showwarning("Aviso", "Selecione um evento para ver os detalhes.")

    def mostrar_detalhes_evento(self, titulo_evento):
        self.c.execute("SELECT id, titulo, hora, descricao FROM eventos WHERE titulo=?", (titulo_evento,))
        evento_info = self.c.fetchone()
        if evento_info:
            evento = Evento(*evento_info)
            DetalheEventoPopup(self.master, evento, self.mostrar_eventos)
        else:
            messagebox.showwarning("Aviso", "Evento não encontrado no banco de dados.")

    def editar_evento(self):
        indice_selecionado = self.eventos_listbox.curselection()
        if indice_selecionado:
            titulo_evento = self.eventos_listbox.get(indice_selecionado[0])
            evento_info = self.c.execute("SELECT id, titulo, hora, descricao FROM eventos WHERE titulo=?", (titulo_evento,)).fetchone()
            if evento_info:
                evento = Evento(*evento_info)
                self.mostrar_popup_editar(evento)
            else:
                messagebox.showwarning("Aviso", "Evento não encontrado no banco de dados.")
        else:
            messagebox.showwarning("Aviso", "Selecione um evento para editar.")
            
    def mostrar_popup_editar(self, evento):
        EditarEventoPopup(self.master, evento, self.atualizar_evento)
    
    def atualizar_evento(self, evento, novo_titulo, nova_hora, nova_descricao):
        self.c.execute("UPDATE eventos SET titulo=?, hora=?, descricao=? WHERE id=?", (novo_titulo, nova_hora, nova_descricao, evento.id))
        self.conn.commit()
        self.mostrar_eventos()
        messagebox.showinfo("Sucesso", "Evento atualizado com sucesso!")

    def excluir_evento(self):
        indice_selecionado = self.eventos_listbox.curselection()
        if indice_selecionado:
            resposta = messagebox.askokcancel("Confirmar Exclusão", "Tem certeza de que deseja excluir este evento?")
            if resposta:
                evento_selecionado = self.eventos_listbox.get(indice_selecionado[0])  # Obtém o título do evento selecionado na listbox
                self.c.execute("DELETE FROM eventos WHERE titulo=?", (evento_selecionado,))
                self.conn.commit()
                self.mostrar_eventos()
                messagebox.showinfo("Sucesso", "Evento excluído com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Selecione um evento para excluir.")

    def selecionar_evento(self, event):
        if self.eventos_listbox.curselection():
            self.detalhe_button.config(state=tk.NORMAL)
            self.editar_button.config(state=tk.NORMAL)
            self.excluir_button.config(state=tk.NORMAL)
        else:
            self.detalhe_button.config(state=tk.DISABLED)
            self.editar_button.config(state=tk.DISABLED)
            self.excluir_button.config(state=tk.DISABLED)
            
    def sair_app(self):
        self.conn.close()
        self.master.destroy()
            
root = tk.Tk()
app = AgendaApp(root)
root.mainloop()
