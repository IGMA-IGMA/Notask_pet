from contextlib import contextmanager
from typing import Any

import psycopg2

import hash_pwd
from queries import Queries


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
                port=self.port,
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

    def create_tables(self):
        with self.get_db_cur() as cursor:
            cursor.execute(self.query_create_table_users)
            cursor.execute(self.query_create_table_notes_users)

    def drop_table_users(self):
        with self.get_db_cur() as cursor:
            cursor.execute(self.query_drop_table_notes_users)

    def create_user(self, username: str, pwd: str):
        with self.get_db_cur() as cursor:
            cursor.execute(
                self.query_create_user, (username, hash_pwd.hash_password(pwd))
            )

    def read_user(self, username: str) -> list[tuple[Any, ...]]:
        with self.get_db_cur() as cursor:
            cursor.execute(self.query_read_user, username)
            result = cursor.fetchall()
        return result

    def update_user_username(self, username, pwd):
        with self.get_db_cur() as cursor:
            cursor.execute(
                self.query_update_user_username,
                (username, username, hash_pwd.hash_password(pwd)),
            )

    def delete_user_username(self, username, pwd):
        with self.get_db_cur() as cursor:
            cursor.execute(
                self.query_delete_user, (username, hash_pwd.hash_password(pwd))
            )
