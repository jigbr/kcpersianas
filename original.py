import os
import tkinter as tk
import tkinter.messagebox as messagebox
import psycopg2

DB_HOST = os.environ.get("DB_HOST", "167.114.17.72")
DB_PORT = os.environ.get("DB_PORT", "25793")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "c7tu55vvxjwp")

class DatabaseConnection:
    def __init__(self, username=None):
        self.db_name = None
        self.username = username
        self.connection = None

    def create_new_database_connection(self):
        # Cria uma conexão com o banco de dados "postgres"
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Verifica se a base de dados com o nome do usuário já existe
        cursor.execute("SELECT COUNT(*) FROM pg_database WHERE datname = %s", (self.username,))
        if cursor.fetchone()[0] == 0:
            # Cria a nova base de dados com o nome do usuário
            cursor.execute(f"CREATE DATABASE {self.username}")

        cursor.close()

        # Conecta-se à nova base de dados com o nome do usuário
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=self.username
        )
        self.db_name = self.username
        self.connection = connection
        return connection

    def __enter__(self):
        self.connection = self.create_new_database_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_connection = None


        self.title("DataVault")

        # Adiciona os widgets de login e senha
        self.username_label = tk.Label(self, text="Nome de usuário")
        self.username_entry = tk.Entry(self)
        
        self.password_label = tk.Label(self, text="Senha")
        self.password_entry = tk.Entry(self, show="*")
        
        self.login_button = tk.Button(
            self,
            text="Entrar",
            command=self.login,
        )

        self.username_label.pack(side=tk.TOP, padx=10, pady=10)
        self.username_entry.pack(side=tk.TOP, padx=10, pady=10)
        self.password_label.pack(side=tk.TOP, padx=10, pady=10)
        self.password_entry.pack(side=tk.TOP, padx=10, pady=10)
        self.login_button.pack(side=tk.TOP, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            with DatabaseConnection(username) as connection:
                cursor = connection.cursor()
                query = """
                    SELECT * FROM users
                    WHERE username = %s AND password = %s
                """
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                if user:
                    # Criar a instância de DatabaseConnection e armazená-la no atributo db_connection da classe Application
                    app.db_connection = DatabaseConnection(username)

                    # Verificar se a tabela de clientes existe e, se não existir, criá-la
                    with app.db_connection.cursor() as cursor:
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS clientes (
                                id SERIAL PRIMARY KEY,
                                nome VARCHAR(255) NOT NULL,
                                cpf VARCHAR(15) NOT NULL,
                                telefone VARCHAR(15) NOT NULL,
                                email VARCHAR(255) NOT NULL,
                                endereco VARCHAR(255) NOT NULL,
                                observacoes VARCHAR(255)
                            );
                        """)

                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS vendas (
                                id SERIAL PRIMARY KEY,
                                cliente_id INTEGER NOT NULL,
                                telefone VARCHAR(15) NOT NULL,
                                email VARCHAR(255) NOT NULL,
                                endereco VARCHAR(255) NOT NULL,
                                material VARCHAR(20) NOT NULL,
                                tipo VARCHAR(20) NOT NULL,
                                linha VARCHAR(20) NOT NULL,
                                largura FLOAT NOT NULL,
                                altura FLOAT NOT NULL,
                                valor FLOAT NOT NULL,
                                data_venda VARCHAR(10) NOT NULL,
                                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                            );
                        """)

                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS valores (
                                material VARCHAR(20) NOT NULL,
                                tipo VARCHAR(20) NOT NULL,
                                linha VARCHAR(20) NOT NULL,
                                valor FLOAT NOT NULL,
                                PRIMARY KEY (material, tipo, linha)
                            );
                        """)

                        query = """
                            INSERT INTO valores (material, tipo, linha, valor)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (material, tipo, linha) DO UPDATE
                            SET valor = EXCLUDED.valor
                        """
                        values = [
                            ('translucida', 'vertical', 'estoque', 95),
                            ('translucida', 'vertical', 'alfa', 138),
                            ('translucida', 'vertical', 'cedro', 158),
                            ('translucida', 'vertical', 'europa', 145),
                            ('translucida', 'vertical', 'juta', 158),
                            ('translucida', 'vertical', 'letter', 172),
                            ('translucida', 'vertical', 'linho', 148),
                            ('translucida', 'vertical', 'marajo', 156),
                            ('translucida', 'vertical', 'metalizada', 222),
                            ('translucida', 'vertical', 'monaco', 145),
                            ('translucida', 'vertical', 'natural', 148),
                            ('translucida', 'vertical', 'natura', 138),
                            ('translucida', 'vertical', 'new', 188),
                            ('translucida', 'vertical', 'nuance', 118),
                            ('translucida', 'vertical', 'prestige', 152),
                            ('translucida', 'vertical', 'shangai', 118),
                            ('translucida', 'vertical', 'shantung', 138),
                            ('translucida', 'vertical', 'strip', 172),
                            ('translucida', 'vertical', 'semi', 138),
                            ('translucida', 'vertical', 'screen', 228),
                            ('translucida', 'vertical', 'strip', 172),
                            ('translucida', 'vertical', 'tradicional', 168),
                            ('translucida', 'vertical', 'tropical', 186),
                            ('translucida', 'rolo', 'napoles', 244),
                            ('translucida', 'rolo', 'prestige', 246),
                            ('translucida', 'rolo', 'ilusion', 246),
                            ('translucida', 'rolo', 'nilo', 248),
                            ('translucida', 'rolo', 'lugano', 248),
                            ('translucida', 'rolo', 'polonia', 259),
                            ('translucida', 'rolo', 'viena', 259),
                            ('translucida', 'rolo', 'lousiana', 269),
                            ('translucida', 'rolo', 'carina', 259),
                            ('translucida', 'rolo', 'screenstar', 405),
                            ('translucida', 'rolo', 'screen1', 398),
                            ('translucida', 'rolo', 'screen3', 282),
                            ('translucida', 'rolo', 'screen5', 268),
                            ('translucida', 'romana', 'napoles', 268),
                            ('translucida', 'romana', 'prestige', 258),
                            ('translucida', 'romana', 'ilusion', 258),
                            ('translucida', 'romana', 'nilo', 280),
                            ('translucida', 'romana', 'lugano', 298),
                            ('translucida', 'romana', 'polonia', 284),
                            ('translucida', 'romana', 'viena', 330),
                            ('translucida', 'romana', 'lousiana', 284),
                            ('translucida', 'romana', 'carina', 356),
                            ('translucida', 'romana', 'screenstar', 485),
                            ('translucida', 'romana', 'screen1', 485),
                            ('translucida', 'romana', 'screen3', 308),
                            ('translucida', 'romana', 'screen5', 296),
                            ('translucida', 'painel', 'napoles', 291),
                            ('translucida', 'painel', 'prestige', 295),
                            ('translucida', 'painel', 'ilusion', 306),
                            ('translucida', 'painel', 'nilo', 256),
                            ('translucida', 'painel', 'lugano', 280),
                            ('translucida', 'painel', 'polonia', 323),
                            ('translucida', 'painel', 'viena', 302),
                            ('translucida', 'painel', 'lousiana', 295),
                            ('translucida', 'painel', 'carina', 326),
                            ('translucida', 'painel', 'screenstar', 445),
                            ('translucida', 'painel', 'screen1', 491),
                            ('translucida', 'painel', 'screen3', 371),
                            ('translucida', 'painel', 'screen5', 326),
                            ('blackout', 'vertical', 'estoque', 120),
                            ('blackout', 'vertical', 'alfa', 218),
                            ('blackout', 'vertical', 'ardanza', 218),
                            ('blackout', 'vertical', 'cedro', 198),
                            ('blackout', 'vertical', 'europa', 184),
                            ('blackout', 'vertical', 'linho', 198),
                            ('blackout', 'vertical', 'linen', 184),
                            ('blackout', 'vertical', 'maresia', 184),
                            ('blackout', 'vertical', 'marajo', 218),
                            ('blackout', 'vertical', 'monaco', 184),
                            ('blackout', 'vertical', 'mosaico', 184),
                            ('blackout', 'vertical', 'new', 218),
                            ('blackout', 'vertical', 'prestige', 184),
                            ('blackout', 'vertical', 'rami', 184),
                            ('blackout', 'vertical', 'sp', 184),
                            ('blackout', 'vertical', 'shantung', 184),
                            ('blackout', 'vertical', 'soleil', 184),
                            ('blackout', 'vertical', 'suica', 196),
                            ('blackout', 'vertical', 'toquio', 184),
                            ('blackout', 'vertical', 'tresse', 198),
                            ('blackout', 'vertical', 'tropical', 218),
                            ('blackout', 'rolo', 'napoles', 282),
                            ('blackout', 'rolo', 'prestige', 298),
                            ('blackout', 'rolo', 'miami', 283),
                            ('blackout', 'rolo', 'polonia', 312),
                            ('blackout', 'rolo', 'libia', 305),
                            ('blackout', 'rolo', 'shantung', 344),
                            ('blackout', 'rolo', 'metropolitan', 398),
                            ('blackout', 'rolo', 'udine', 328),
                            ('blackout', 'rolo', 'asia', 328),
                            ('blackout', 'rolo', 'viena', 298),
                            ('blackout', 'rolo', 'lugano', 328),
                            ('blackout', 'rolo', 'polonia', 312),
                            ('blackout', 'rolo', 'pinpointe', 298),
                            ('blackout', 'rolo', 'pinpointe+', 448),
                            ('blackout', 'romana', 'napoles', 308),
                            ('blackout', 'romana', 'prestige', 330),
                            ('blackout', 'romana', 'miami', 308),
                            ('blackout', 'romana', 'polonia', 328),
                            ('blackout', 'romana', 'libia', 366),
                            ('blackout', 'romana', 'shantung', 398),
                            ('blackout', 'romana', 'metropolitan', 485),
                            ('blackout', 'romana', 'udine', 394),
                            ('blackout', 'romana', 'asia', 394),
                            ('blackout', 'romana', 'viena', 330),
                            ('blackout', 'romana', 'lugano', 394),
                            ('blackout', 'romana', 'polonia', 328),
                            ('blackout', 'romana', 'pinpointe', 356),
                            ('blackout', 'romana', 'pinpointe+', 541),
                            ('blackout', 'painel', 'napoles', 362),
                            ('blackout', 'painel', 'prestige', 398),
                            ('blackout', 'painel', 'polonia', 345),
                            ('blackout', 'painel', 'libia', 335),
                            ('blackout', 'painel', 'shantung', 378),
                            ('blackout', 'painel', 'metropolitan', 485),
                            ('blackout', 'painel', 'udine', 394),
                            ('blackout', 'painel', 'asia', 394),
                            ('blackout', 'painel', 'viena', 330),
                            ('blackout', 'painel', 'lugano', 394),
                            ('blackout', 'painel', 'polonia', 328),
                            ('blackout', 'painel', 'pinpointe', 356),
                            ('blackout', 'painel', 'pinpointe+', 541)
                        ]
                        cursor.executemany(query, values)

                        connection.commit()
                        cursor.close()
                        connection.close()

                        # Se tudo estiver certo, abrir a janela principal do aplicativo
                        self.withdraw()  # Ocultar a janela de login
                        self.destroy()  # Destruir a janela de login
                        app = Application()
                        app.atualizar_vendas()
                        app.mainloop()
                else:
                    messagebox.showerror(
                        "Erro",
                        "Credenciais inválidas. Por favor, tente novamente."
                    )
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao tentar fazer login: {str(e)}"
            )

# Funções relacionadas a clientes
def cadastrar_cliente(connection, nome, cpf, telefone, email, endereco):
    cursor = connection.cursor()

    query = """
        SELECT id
        FROM clientes
        WHERE telefone = %s;
    """
    cursor.execute(query, (telefone,))
    resultado = cursor.fetchone()
    if resultado:
        raise ValueError("Já existe um cliente cadastrado com este número de telefone.")

    query = """
        INSERT INTO clientes (nome, cpf, telefone, email, endereco, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    cursor.execute(query, (nome, cpf, telefone, email, endereco, None))
    cliente_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return cliente_id

def atualizar_cliente(connection, cliente_id, nome, telefone, endereco, observacoes, email):
    cursor = connection.cursor()
    query = """
        UPDATE clientes
        SET nome = %s, telefone = %s, endereco = %s, observacoes = %s, email = %s
        WHERE id = %s;
    """
    cursor.execute(query, (nome, telefone, endereco, observacoes, email, cliente_id))
    connection.commit()
    cursor.close()

def consultar_cliente_especifico(connection, telefone):
    cursor = connection.cursor()
    query = """
        SELECT id, nome, cpf, email, endereco
        FROM clientes
        WHERE telefone = %s;
    """
    cursor.execute(query, (telefone,))
    cliente = cursor.fetchone()
    cursor.close()
    return cliente

def pesquisar_clientes(connection, termo_pesquisa):
    cursor = connection.cursor()
    query = """
        SELECT id, nome, cpf, telefone, email, endereco, observacoes
        FROM clientes
        WHERE nome LIKE %s OR telefone LIKE %s OR cpf LIKE %s;
    """
    cursor.execute(query, (f"%{termo_pesquisa}%", f"%{termo_pesquisa}%", f"%{termo_pesquisa}%"))
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

# Funções relacionadas a vendas
def cadastrar_venda(connection, telefone, material, tipo, linha, largura, altura, endereco, data_venda, callback):
    cursor = connection.cursor()

    cliente = consultar_cliente_especifico(connection, telefone)
    if not cliente:
        messagebox.showerror(
            "Erro",
            "Cliente não encontrado. Por favor, cadastre o cliente antes de registrar a venda.",
        )
        return

    cliente_id, nome, cpf, email, endereco_cliente = cliente

    # calcular o valor da venda
    query = """
        SELECT valor
        FROM valores
        WHERE material = %s AND tipo = %s AND linha = %s;
    """
    cursor.execute(query, (material, tipo, linha))
    valor = cursor.fetchone()[0]
    valor_venda = largura * altura * valor

    query = """
        INSERT INTO vendas (cliente_id, telefone, email, endereco, material, tipo, linha, largura, altura, valor, data_venda)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (cliente_id, telefone, email, endereco, material, tipo, linha, largura, altura, valor_venda, data_venda))
    connection.commit()
    cursor.close()

    messagebox.showinfo(
        "Cadastro de vendas",
        "Venda cadastrada com sucesso!",
    )

def consultar_vendas(connection):
    cursor = connection.cursor()
    query = """
        SELECT id, cliente_id, telefone, email, endereco, material, tipo, linha, largura, altura, valor, data_venda
        FROM vendas
    """
    cursor.execute(query)
    vendas = cursor.fetchall()
    cursor.close()
    return vendas

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("DataVault")
        self.geometry("800x600")

        self.nome_label = tk.Label(self, text="Nome")
        self.nome_entry = tk.Entry(self)
        
        self.cpf_label = tk.Label(self, text="CPF")
        self.cpf_entry = tk.Entry(self)

        self.telefone_label = tk.Label(self, text="Telefone")
        self.telefone_entry = tk.Entry(self)

        self.email_label = tk.Label(self, text="E-mail")
        self.email_entry = tk.Entry(self)

        self.endereco_label = tk.Label(self, text="Endereço")
        self.endereco_entry = tk.Entry(self)


        self.cadastrar_cliente_button = tk.Button(
            self,
            text="Cadastrar cliente",
            command=self.cadastrar_cliente,
        )

        self.telefone_label2 = tk.Label(self, text="Telefone")
        self.telefone_entry2 = tk.Entry(self)

        self.endereco_label2 = tk.Label(self, text="Endereço")
        self.endereco_entry2 = tk.Entry(self)

        self.material_label = tk.Label(self, text="Material")
        self.material_entry = tk.Entry(self)

        self.tipo_label = tk.Label(self, text="Tipo")
        self.tipo_entry = tk.Entry(self)

        self.linha_label = tk.Label(self, text="Linha")
        self.linha_entry = tk.Entry(self)

        self.largura_label = tk.Label(self, text="Largura")
        self.largura_entry = tk.Entry(self)

        self.altura_label = tk.Label(self, text="Altura")
        self.altura_entry = tk.Entry(self)

        self.data_venda_label = tk.Label(self, text="Data da venda")
        self.data_venda_entry = tk.Entry(self)

        self.resultados_text = tk.Text(self, height=10, width=50)

        self.vendas_text = tk.Text(self, height=10, width=50)

        self.cadastrar_venda_button = tk.Button(
            self,
            text="Cadastrar venda",
            command=self.cadastrar_venda,
        )

        self.pesquisa_cliente_label = tk.Label(self, text="Pesquisar cliente")
        self.pesquisa_cliente_entry = tk.Entry(self)

        self.pesquisa_button = tk.Button(
            self,
            text="Pesquisar cliente",
            command=self.exibir_resultados
        )

        self.nome_label.grid(row=0, column=0, sticky=tk.E)
        self.nome_entry.grid(row=0, column=1, columnspan=2)
        self.cpf_label.grid(row=1, column=0, sticky=tk.E)
        self.cpf_entry.grid(row=1, column=1, columnspan=2)
        self.telefone_label.grid(row=2, column=0, sticky=tk.E)
        self.telefone_entry.grid(row=2, column=1, columnspan=2)
        self.email_label.grid(row=3, column=0, sticky=tk.E)
        self.email_entry.grid(row=3, column=1, columnspan=2)
        self.endereco_label.grid(row=4, column=0, sticky=tk.E)
        self.endereco_entry.grid(row=4, column=1, columnspan=2)
        self.cadastrar_cliente_button.grid(row=5, column=1)

        self.telefone_label2.grid(row=6, column=0, sticky=tk.E)
        self.telefone_entry2.grid(row=6, column=1, columnspan=2)
        self.endereco_label2.grid(row=7, column=0, sticky=tk.E)
        self.endereco_entry2.grid(row=7, column=1, columnspan=2)
        self.material_label.grid(row=8, column=0, sticky=tk.E)
        self.material_entry.grid(row=8, column=1, columnspan=2)
        self.tipo_label.grid(row=9, column=0, sticky=tk.E)
        self.tipo_entry.grid(row=9, column=1, columnspan=2)
        self.linha_label.grid(row=10, column=0, sticky=tk.E)
        self.linha_entry.grid(row=10, column=1, columnspan=2)
        self.largura_label.grid(row=11, column=0, sticky=tk.E)
        self.largura_entry.grid(row=11, column=1, columnspan=2)
        self.altura_label.grid(row=12, column=0, sticky=tk.E)
        self.altura_entry.grid(row=12, column=1, columnspan=2)
        self.data_venda_label.grid(row=13, column=0, sticky=tk.E)
        self.data_venda_entry.grid(row=13, column=1, columnspan=2)
        self.cadastrar_venda_button.grid(row=14, column=1)

        self.pesquisa_cliente_label.grid(row=15, column=0, sticky=tk.E)
        self.pesquisa_cliente_entry.grid(row=15, column=1, columnspan=2)
        self.pesquisa_button.grid(row=16, column=1)
        self.resultados_text.grid(row=17, column=0, columnspan=3)

        self.vendas_text.grid(row=18, column=1, padx=10, pady=10, sticky="nsew")

    def atualizar_vendas(self):
        self.vendas_text.delete(1.0, tk.END)  # limpa o conteúdo do widget
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM vendas")
            vendas_count = cursor.fetchone()[0]
            if vendas_count > 0:
                vendas = consultar_vendas(connection)  # busca todas as vendas no banco de dados
                # adiciona as informações de cada venda no widget
                for venda in vendas:
                    linha = f"{venda[0]} - {venda[1]} - {venda[2]} - {venda[3]} - {venda[4]} - {venda[5]} - {venda[6]} - {venda[7]} - {venda[8]} - {venda[9]} - {venda[10]} - {venda[11]}\n"
                    self.vendas_text.insert(tk.END, linha)
                self.vendas_text.config(state=tk.DISABLED)
            else:
                self.vendas_text.insert(tk.END, "Nenhuma venda registrada.\n")
                self.vendas_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao tentar atualizar as vendas: {str(e)}"
            )

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        endereco = self.endereco_entry.get()
        try:
            connection = self.db_connection.get_connection()
            cadastrar_cliente(connection, nome, cpf, telefone, email, endereco)
            messagebox.showinfo(
                "Cadastro de clientes",
                "Cliente cadastrado com sucesso!",
            )
        except ValueError as error:
            messagebox.showerror(
                "Erro",
                str(error),
            )
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao tentar cadastrar o cliente: {str(e)}"
            )

    def cadastrar_venda(self):
        telefone = self.telefone_entry2.get()
        material = self.material_entry.get()
        tipo = self.tipo_entry.get()
        linha = self.linha_entry.get()
        largura = float(self.largura_entry.get())
        altura = float(self.altura_entry.get())
        endereco = self.endereco_entry2.get()
        data_venda = self.data_venda_entry.get()
        try:
            connection = self.db_connection.get_connection()
            cadastrar_venda(connection, telefone, material, tipo, linha, largura, altura, endereco, data_venda, self.atualizar_vendas)
            messagebox.showinfo("Cadastro de vendas", "Venda cadastrada com sucesso!")
        except ValueError as error:
            messagebox.showerror(
                "Erro",
                str(error),
            )
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao tentar cadastrar a venda: {str(e)}"
            )
            
def exibir_resultados(self):
    termo_pesquisa = self.pesquisa_cliente_entry.get()
    try:
        connection = self.db_connection.get_connection()
        clientes = pesquisar_clientes(connection, termo_pesquisa)
        self.resultados_text.delete("1.0", tk.END)
        for cliente in clientes:
            self.resultados_text.insert(
                tk.END,
                f"{cliente[0]} - {cliente[1]} - {cliente[2]} - {cliente[3]}\n"
            )
    except Exception as e:
        messagebox.showerror(
            "Erro",
            f"Ocorreu um erro ao tentar exibir os resultados: {str(e)}"
        )


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()