import tkinter as tk
from tkinter import ttk
import webbrowser
import urllib.parse
import sqlite3  # Biblioteca nativa para Banco de Dados

class AppSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro, DB SQLite e WhatsApp")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        # Configurar banco de dados antes de iniciar a interface
        self.inicializar_banco_dados()

        # Configuração de estilo básico
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configuração do layout principal (Abas)
        self.tab_control = ttk.Notebook(root)
        
        self.tab_formulario = ttk.Frame(self.tab_control)
        self.tab_whatsapp = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_formulario, text=" Formulário e Banco de Dados ")
        self.tab_control.add(self.tab_whatsapp, text=" Integração WhatsApp API ")
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Inicializar os componentes de cada aba
        self.criar_aba_formulario()
        self.criar_aba_whatsapp()

    def inicializar_banco_dados(self):
        # Conecta ao arquivo de banco de dados (se não existir, ele cria na hora)
        conexao = sqlite3.connect("sistema_escola.db")
        cursor = conexao.cursor()
        
        # Criação da tabela com tipos de dados SQL padrão
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL
            )
        """)
        conexao.commit()
        conexao.close()

    def criar_aba_formulario(self):
        frame_central = ttk.LabelFrame(self.tab_formulario, text=" Dados do Novo Usuário ", padding=15)
        frame_central.pack(padx=20, pady=10, fill="x")

        # Campo Nome
        ttk.Label(frame_central, text="Nome Completo:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_central, width=40)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        # Campo CPF
        ttk.Label(frame_central, text="CPF:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_cpf = ttk.Entry(frame_central, width=40)
        self.entry_cpf.grid(row=1, column=1, padx=10, pady=5)

        # Campo Senha
        ttk.Label(frame_central, text="Senha de Acesso:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_senha = ttk.Entry(frame_central, width=40, show="*")
        self.entry_senha.grid(row=2, column=1, padx=10, pady=5)

        # Tipo de Perfil (Combobox)
        ttk.Label(frame_central, text="Nível de Acesso:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.combo_perfil = ttk.Combobox(frame_central, values=["Estudante", "Desenvolvedor", "Administrador"], width=37, state="readonly")
        self.combo_perfil.current(0)
        self.combo_perfil.grid(row=3, column=1, padx=10, pady=5)

        # Checkbox LGPD
        self.var_termos = tk.IntVar()
        self.check_termos = ttk.Checkbutton(frame_central, text="Autorizo o tratamento dos meus dados de acordo com a LGPD", variable=self.var_termos)
        self.check_termos.grid(row=4, column=0, columnspan=2, pady=10)

        # Frame para organizar botões de ação do banco
        frame_acoes = ttk.Frame(frame_central)
        frame_acoes.grid(row=5, column=0, columnspan=2, pady=5)

        self.btn_salvar = ttk.Button(frame_acoes, text="Gravar no Banco (INSERT)", command=self.salvar_no_banco)
        self.btn_salvar.grid(row=0, column=0, padx=5)

        self.btn_listar = ttk.Button(frame_acoes, text="Consultar Banco (SELECT)", command=self.listar_dados_banco)
        self.btn_listar.grid(row=0, column=1, padx=5)

        # Console de Logs e Saída de Dados SQL
        ttk.Label(self.tab_formulario, text="Console do Banco de Dados (Log de Operações SQL):").pack(anchor="w", padx=20)
        self.txt_log = tk.Text(self.tab_formulario, height=10, width=85, bg="#2b2b2b", fg="#ffffff", font=("Consolas", 10))
        self.txt_log.pack(padx=20, pady=5, fill="both", expand=True)
        self.txt_log.insert("1.0", "Console: Sistema iniciado. Banco 'sistema_escola.db' verificado/criado.\n")

    def criar_aba_whatsapp(self):
        frame_wpp = ttk.LabelFrame(self.tab_whatsapp, text=" Configurações de Mensageria (API Web) ", padding=20)
        frame_wpp.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Label(frame_wpp, text="Número do Destinatário (Com DDD apenas números):").pack(anchor="w", padx=10, pady=2)
        self.entry_wpp_num = ttk.Entry(frame_wpp, width=50)
        self.entry_wpp_num.pack(padx=10, pady=5)
        self.entry_wpp_num.insert(0, "5541") 

        ttk.Label(frame_wpp, text="Texto da Mensagem Customizada:").pack(anchor="w", padx=10, pady=2)
        self.entry_wpp_msg = ttk.Entry(frame_wpp, width=50)
        self.entry_wpp_msg.pack(padx=10, pady=5)

        self.btn_enviar_custom = ttk.Button(frame_wpp, text="Disparar Texto Customizado", command=self.enviar_wpp_customizado)
        self.btn_enviar_custom.pack(pady=10)

        ttk.Separator(frame_wpp, orient="horizontal").pack(fill="x", pady=15)
        ttk.Label(frame_wpp, text="Ações Rápidas (Simulador de Botões de API):", font=("Arial", 10, "italic")).pack(anchor="w", padx=10)

        frame_botoes_api = ttk.Frame(frame_wpp)
        frame_botoes_api.pack(pady=10)

        self.btn_suporte = ttk.Button(frame_botoes_api, text="Botão: Acionar Suporte", command=lambda: self.enviar_wpp_template("suporte"))
        self.btn_suporte.grid(row=0, column=0, padx=10)

        self.btn_financeiro = ttk.Button(frame_botoes_api, text="Botão: Segunda Via Boleto", command=lambda: self.enviar_wpp_template("financeiro"))
        self.btn_financeiro.grid(row=0, column=1, padx=10)

    # ---- LÓGICA DO BANCO DE DADOS (SQLITE3) ----

    def limpar_console(self):
        self.txt_log.delete("1.0", tk.END)

    def salvar_no_banco(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        senha = self.entry_senha.get()
        perfil = self.combo_perfil.get()
        termos = self.var_termos.get()

        self.limpar_console()

        if not nome or not cpf or not senha:
            self.txt_log.insert("1.0", "ERRO: Preencha todos os campos cadastrais antes de salvar!\n")
            return

        if termos == 0:
            self.txt_log.insert("1.0", "ERRO: Aceite os termos da LGPD para autorizar o salvamento.\n")
            return

        try:
            # Abrindo conexão para inserir o registro
            conexao = sqlite3.connect("sistema_escola.db")
            cursor = conexao.cursor()
            
            # Comando SQL usando placeholders (?) para evitar SQL Injection (ótimo conceito para passar aos alunos)
            comando_insert = "INSERT INTO usuarios (nome, cpf, senha, perfil) VALUES (?, ?, ?, ?)"
            cursor.execute(comando_insert, (nome, cpf, senha, perfil))
            
            conexao.commit()
            conexao.close()

            self.txt_log.insert("1.0", f"SUCESSO NO BANCO DE DADOS!\n")
            self.txt_log.insert("2.0", f"Comando Executado: {comando_insert}\n")
            self.txt_log.insert("3.0", f"Valores Inseridos -> Nome: {nome} | CPF: {cpf} | Perfil: {perfil}\n")
            
            # Limpa os campos da tela após o salvamento com sucesso
            self.entry_nome.delete(0, tk.END)
            self.entry_cpf.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            
        except Exception as e:
            self.txt_log.insert("1.0", f"Erro crítico ao acessar o banco de dados: {e}\n")

    def listar_dados_banco(self):
        self.limpar_console()
        
        try:
            conexao = sqlite3.connect("sistema_escola.db")
            cursor = conexao.cursor()
            
            comando_select = "SELECT id, nome, cpf, perfil FROM usuarios"
            cursor.execute(comando_select)
            linhas = cursor.fetchall()
            conexao.close()

            if not linhas:
                self.txt_log.insert("1.0", "Consulta concluída: Nenhum registro encontrado na tabela 'usuarios'.\n")
                return

            self.txt_log.insert("1.0", f"EXECUÇÃO DE COMANDO: {comando_select}\n")
            self.txt_log.insert("2.0", f"{'ID':<5} | {'NOME':<25} | {'CPF':<15} | {'PERFIL':<15}\n")
            self.txt_log.insert("3.0", "-" * 70 + "\n")
            
            for registro in linhas:
                self.txt_log.insert(tk.END, f"{registro[0]:<5} | {registro[1]:<25} | {registro[2]:<15} | {registro[3]:<15}\n")
                
        except Exception as e:
            self.txt_log.insert("1.0", f"Erro ao consultar dados: {e}\n")

    # ---- LÓGICA DO WHATSAPP ----

    def enviar_wpp_customizado(self):
        numero = self.entry_wpp_num.get()
        mensagem = self.entry_wpp_msg.get()
        numero_limpo = "".join(filter(str.isdigit, numero))

        if not numero_limpo or not mensagem:
            self.limpar_console()
            self.txt_log.insert("1.0", "ERRO WHATSAPP: Forneça o número e a mensagem customizada.\n")
            return

        texto_url = urllib.parse.quote(mensagem)
        url_final = f"https://api.whatsapp.com/send?phone={numero_limpo}&text={texto_url}"
        webbrowser.open(url_final)

    def enviar_wpp_template(self, contexto):
        numero = self.entry_wpp_num.get()
        numero_limpo = "".join(filter(str.isdigit, numero))

        if not numero_limpo:
            self.limpar_console()
            self.txt_log.insert("1.0", "ERRO WHATSAPP: O número precisa estar preenchido para usar os botões.\n")
            return

        if contexto == "suporte":
            mensagem = "Olá! Encontrei um comportamento inesperado no banco de dados do sistema de testes e preciso de auxílio."
        elif contexto == "financeiro":
            mensagem = "Olá! Registro acadêmico localizado no banco. Segue a solicitação de envio de boleto."

        texto_url = urllib.parse.quote(mensagem)
        url_final = f"https://api.whatsapp.com/send?phone={numero_limpo}&text={texto_url}"
        webbrowser.open(url_final)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSistema(root)
    root.mainloop()