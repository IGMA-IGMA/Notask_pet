from contextlib import contextmanager

import psycopg2

import hash_pwd


class Queries:
    def __init__(self):
        self.query_create_tables = """
            DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users(
            	id SERIAL PRIMARY KEY,
            	username VARCHAR(255) UNIQUE NOT NULL,
            	hash_pwd TEXT  NOT NULL,
            	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            CREATE INDEX IF NOT EXISTS idx_users_create_at ON users(create_at);
        """
        self.query_create_user = """
            INSERT INTO users (username, hash_pwd)
            VALUES (%s, %s)
        """
        self.query_read_user = """
            SELECT username, hash_pwd FROM users WHERE username=%s;
        """
        self.query_update_user_username = """
            UPDATE users SET username=%s WHERE username=%s AND hash_pwd=%s;
        """
        self.query_update_user_pwd = """
            UPDATE users SET username=%s WHERE username=%s AND hash_pwd=%s;
        """


class DB_MANAGER(Queries):
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        super().__init__()
        self.dbname: str = dbname
        self.user: str = user
        self.password: str = password
        self.host: str = host
        self.port: str = port
        self.conn = None

    def _get_db_conn(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        return self.conn

    @contextmanager
    def get_db_cur(self):
        conn = self._get_db_conn()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def create_table(self):
        with self.get_db_cur() as cursor:
            cursor.execute(self.query_create_tables)

    def create_user(self, username: str, pwd: str):
        with self.get_db_cur() as cursor:
            cursor.execute(
                self.query_create_user,
                (username,
                 hash_pwd.hash_password(pwd)))
