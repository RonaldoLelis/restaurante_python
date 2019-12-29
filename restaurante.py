from tkinter import *
import pymysql
from tkinter import messagebox, ttk


class AdminJanela():

    def CadastrarProdutos(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de Produtos')
        self.cadastrar['bg'] = '#848484'

        Label(self.cadastrar, text='INSERIR NOVOS PRODUTOS', bg='#848484', fg='white').grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        Label(self.cadastrar, text='Nome', bg='#848484', fg='white').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Ingredientes', bg='#848484', fg='white').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Grupo', bg='#848484', fg='white').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Preço', bg='#848484', fg='white').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        Button(self.cadastrar, text='Salvar', width=15, bg='#81F781', relief='flat', highlightbackground='#848484', command=self.CadastrarProdutoBackEnd).grid(row=7, column=4, padx=5, pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='#FE2E2E', relief='flat', highlightbackground='#848484', command=self.RemoverCadstroBackEnd).grid(row=7, column=5, padx=5, pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='#F4FA58', relief='flat', highlightbackground='#848484', command=self.MostrarProdutos).grid(row=7, column=6, padx=5, pady=5)
        #Button(self.cadastrar, text='Limpar', width=15, bg='#000000', fg='white', relief='flat', highlightbackground='#848484').grid(row=7, column=7, padx=5, pady=5)

        self.tree = ttk.Treeview(self.cadastrar, selectmode="browse", column=("column1", "column2", "column3", "column4"), show='headings')

        self.tree.column("column1", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')

        self.tree.column("column2", width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')

        self.tree.column("column3", width=150, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')

        self.tree.column("column4", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Preço')

        self.tree.grid(row=0, column=4, columnspan=4, rowspan=6, padx=10, pady=10)

        self.MostrarProdutos()
        self.cadastrar.mainloop()

    def __init__(self):
        self.root = Tk()
        self.root.title('Administrador')
        self.root.geometry('300x300')

        Button(self.root, text='Pedidos', width=20, bg='#5882FA').grid(row=0, column=0, padx=10, pady=10)
        Button(self.root, text='Cadastrar', width=20, bg='#FE9A2E', command=self.CadastrarProdutos).grid(row=1, column=0, padx=10, pady=10)

        self.root.mainloop()

    def CadastrarProdutoBackEnd(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar no banco')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('INSERT INTO produtos(nome, ingredientes, grupo, preco) VALUES (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
                conexao.commit()
        except:
            print('erro ao inserir produto')

        self.MostrarProdutos()

    def MostrarProdutos(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar no banco')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM produtos')
                resultado = cursor.fetchall()
        except:
            print('erro ao fazer a consulta')

        self.tree.delete(*self.tree.get_children())
        linhaP = []

        for linha in resultado:
            #linhaV.append(linha['id'])
            linhaP.append(linha['nome'])
            linhaP.append(linha['ingredientes'])
            linhaP.append(linha['grupo'])
            linhaP.append(linha['preco'])
            self.tree.insert("", END, values=linhaP, iid=linha['id'], tag='1')
            linhaP.clear()

    def RemoverCadstroBackEnd(self):
        idDeletar = int(self.tree.selection()[0])

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

        except:
            print('erro ao conectar no banco')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('DELETE FROM produtos WHERE id = {}'.format(idDeletar))
                conexao.commit()
        except:
            print('erro ao tentar excluir')

        self.MostrarProdutos()



class JanelaLogin():

    def VerificaLogin(self):
        autenticado = False
        usuarioMaster = False

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

        except:
            print('erro ao conectar no banco')

        usuario = self.login.get()
        senha = self.senha.get()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM cadastros')
                resultado = cursor.fetchall()
        except:
            print('erro ao fazer a consulta')

        for linha in resultado:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            messagebox.showinfo('Tela de Login', 'Email ou senha inválidos')

        if autenticado:
            self.root.destroy()
            if usuarioMaster:
                AdminJanela()

    def CadastroBackEnd(self):
        codigoPadrao = '123'

        if self.codigoSeguranca.get() == codigoPadrao:
            if len(self.login.get()) <=20:
                if len(self.senha.get()) <=50:
                    nome = self.login.get()
                    senha = self.senha.get()

                    try:
                        conexao = pymysql.connect(
                            host='localhost',
                            user='root',
                            password='',
                            db='erp',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )

                    except:
                        print('erro ao conectar no banco')

                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute('INSERT INTO cadastros (nome, senha, nivel) VALUES (%s, %s, %s)', (nome, senha, 1))
                            conexao.commit()
                        messagebox.showinfo('Cadastro', 'Usuário cadastrado com sucesso!')
                        self.root.destroy()
                    except:
                        print('erro ao inserir dados')
                else:
                    messagebox.showinfo('ERRO', 'Senha deve ter no máximo 50 caracteres')
            else:
                messagebox.showinfo('ERRO', 'Nome deve ter no máximo 20 caracteres')
        else:
            messagebox.showinfo('ERRO', 'Código de segurança inválido')

    def Cadastro(self):
        Label(self.root, text='Chave de Segurança').grid(row=3, column=0, padx=5, pady=5)
        self.codigoSeguranca = Entry(self.root, show='*')
        self.codigoSeguranca.grid(row=3, column=1, padx=10, pady=5)
        Button(self.root, text='Confirmar Cadastro', width=15, bg='blue1', command=self.CadastroBackEnd).grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    def UpdateBackEnd(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar no banco')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM cadastros')
                resultado = cursor.fetchall()
        except:
            print('erro ao fazer a consulta')

        self.tree.delete(*self.tree.get_children())
        linhaV = []

        for linha in resultado:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')
            linhaV.clear()

    def VisualizarCadastros(self):
        self.vc = Toplevel()
        self.vc.resizable(False, False)
        self.vc.title('Visualizar cadastros')

        self.tree = ttk.Treeview(self.vc, selectmode="browse", column=("column1", "column2", "column3", "column4"), show='headings')

        self.tree.column("column1", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column("column2", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuário')

        self.tree.column("column3", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')

        self.tree.column("column4", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.UpdateBackEnd()
        self.vc.mainloop()

    def __init__(self):
        self.root = Tk()
        self.root.title('LOGIN')
        #self.root.geometry('200x200')
        Label(self.root, text='Restaurante Lélis').grid(row=0, column=0, columnspan=2,  padx=5, pady=5)

        Label(self.root, text='Usuário: ').grid(row=1, column=0)
        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=5, pady=5)

        Label(self.root, text='Senha: ').grid(row=2, column=0)
        self.senha = Entry(self.root)
        self.senha.grid(row=2, column=1,  padx=5, pady=5)

        Button(self.root, text='Entrar', bg='green3', width=10, command=self.VerificaLogin).grid(row=5, column=1,  padx=10, pady=5)
        Button(self.root, text='Cadastrar', bg='orange3', width=10, command=self.Cadastro).grid(row=5, column=0, padx=2, pady=5)
        Button(self.root, text='Visualizar Cadastros', bg='white', command=self.VisualizarCadastros).grid(row=6, column=0, columnspan=2, padx=2, pady=5)

        self.root.mainloop()

JanelaLogin()
