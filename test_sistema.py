import unittest
from unittest.mock import patch
import tkinter as tk
import sqlite3

# Importa a classe do sistema original que está no arquivo main.py
from main import AppSistema 

class TestAppSistema(unittest.TestCase):

    def setUp(self):
        # Configuração executada antes de CADA teste
        self.root = tk.Tk()
        
        # Para evitar o loop de recursão, criamos uma conexão real em memória antes do patch
        self.conexao_memoria = sqlite3.connect(":memory:")
        
        # O patch agora intercepta a chamada e simplesmente devolve a conexão que já criamos
        self.patcher_db = patch('sqlite3.connect', return_value=self.conexao_memoria)
        self.mock_db = self.patcher_db.start()
        
        # Instancia o aplicativo na memória
        self.app = AppSistema(self.root)

    def tearDown(self):
        # Limpeza executada após a finalização de CADA teste
        self.patcher_db.stop()
        self.conexao_memoria.close()
        self.root.destroy()

    def test_cadastro_com_campos_vazios(self):
        # Garante que os campos de texto iniciam vazios
        self.app.entry_nome.insert(0, "")
        self.app.entry_cpf.insert(0, "")
        self.app.entry_senha.insert(0, "")
        self.app.var_termos.set(1) # Simula que aceitou a LGPD

        # Executa a função de salvar do código original
        self.app.salvar_no_banco()
        
        # Captura o texto que foi impresso no console escuro da tela
        conteudo_console = self.app.txt_log.get("1.0", tk.END)
        
        # Verifica se a mensagem de erro esperada está dentro do console
        self.assertIn("ERRO: Preencha todos os campos cadastrais", conteudo_console)

    def test_cadastro_sem_aceitar_lgpd(self):
        # Preenche os campos corretamente, mas deixa a LGPD desmarcada
        self.app.entry_nome.insert(0, "Aluno Teste")
        self.app.entry_cpf.insert(0, "123.456.789-00")
        self.app.entry_senha.insert(0, "senha123")
        self.app.var_termos.set(0) # 0 significa desmarcado

        self.app.salvar_no_banco()
        
        conteudo_console = self.app.txt_log.get("1.0", tk.END)
        self.assertIn("ERRO: Aceite os termos da LGPD", conteudo_console)

    def test_cadastro_com_sucesso(self):
        # Fornece todos os dados válidos e aceita a LGPD
        self.app.entry_nome.insert(0, "Geovani Eduardo")
        self.app.entry_cpf.insert(0, "11122233344")
        self.app.entry_senha.insert(0, "admin123")
        self.app.combo_perfil.set("Desenvolvedor")
        self.app.var_termos.set(1) 

        self.app.salvar_no_banco()
        
        conteudo_console = self.app.txt_log.get("1.0", tk.END)
        self.assertIn("SUCESSO NO BANCO DE DADOS!", conteudo_console)
        
        # Verifica se os campos de texto foram limpos automaticamente após o sucesso
        self.assertEqual(self.app.entry_nome.get(), "")
        self.assertEqual(self.app.entry_cpf.get(), "")

    @patch('webbrowser.open')
    def test_api_whatsapp_mensagem_customizada(self, mock_browser):
        # Preenche o número com máscara e insere uma mensagem
        self.app.entry_wpp_num.delete(0, tk.END)
        self.app.entry_wpp_num.insert(0, "(41) 99999-9999")
        self.app.entry_wpp_msg.insert(0, "Olá Professor")

        # Executa a função de disparo
        self.app.enviar_wpp_customizado()

        # Valida se o número foi limpo e se os caracteres especiais foram convertidos para URL (%20)
        url_esperada = "https://api.whatsapp.com/send?phone=41999999999&text=Ol%C3%A1%20Professor"
        mock_browser.assert_called_once_with(url_esperada)

if __name__ == "__main__":
    unittest.main()