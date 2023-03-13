import mysql.connector


class DatabaseConnector:
    '''Classe para conectar ao banco de dados.'''
    def __init__(self,  db_path, login, psw):
        self.db_path = db_path
        self.login = login
        self.psw = psw

    def conecta_db(self):
        '''Conecta ao banco com o caminho mysql na azure'''
        self.conn = mysql.connector.connect(
                user=self.login,
                password=self.psw,
                host="mrn-mysql-database.mysql.database.azure.com",
                port=3306,
                database=self.db_path,
                ssl_disabled=True)
        self.cur = self.conn.cursor()

    def desconecta_db(self):
        '''Encerra a conecção com o banco de dados'''
        self.conn.close()
        self.conn = None
        self.cur = None

class DatabaseTable(DatabaseConnector):
    '''Classe filha da DatabaseConnector.
    --- Possui como métodos criar a tabela no BD caso não exista e
        inserir registros na tabela.
    '''

    def insere_registro(self, table_name, data_tuple):
        '''Recebe o nome da tabela e cria registro nela'''
        if table_name == "bd_oc":
            sql_query = "INSERT INTO " + table_name +  " VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        elif table_name == "bd_diesel_s10":
            sql_query = "INSERT INTO " + table_name +  " VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        self.cur.execute(sql_query, data_tuple)
        self.conn.commit()
