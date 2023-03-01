import psycopg2
from src.main.utils.Constants import HOST, DB, USER, PASSWORD
from src.main.config.SQL import SQL
from abc import ABC
from src.main.config.Logger import Logger


class Postgres(SQL, ABC):
    def __init__(self):
        super().__init__()
        logger = Logger('______main______')
        self.logger = logger
        try:
            self.conn = psycopg2.connect(
                host=HOST,
                database=DB,
                user=USER,
                password=PASSWORD
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            self.logger.info(f'Error connecting to database: {e}')

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def create_profile_table(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "CREATE TABLE profile (id_profile varchar(255) PRIMARY KEY);"
            )
            cur.close()
            self.conn.commit()
        except Exception as e:
            self.logger.info(f'error to create profile table: {e}')

    def create_src_table(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "CREATE TABLE src ("
                "id_src varchar(255) PRIMARY KEY, "
                "id_profile varchar(255), "
                "CONSTRAINT fk_profile "
                "FOREIGN KEY (id_profile) "
                "REFERENCES profile(id_profile) ON DELETE CASCADE);"
            )
            cur.close()
            self.conn.commit()
        except Exception as e:
            self.logger.info(f'error to create src table: {e}')

    def insert_src(self, id_profile, id_src):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO src (id_src, id_profile) "
                "VALUES (%s, %s)",
                (id_src, id_profile)
            )
            cur.close()
            self.conn.commit()
        except Exception as e:
            self.logger.info(f'error to insert src: {e}')

    def check_src_exists(self, id_src):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id_src FROM src WHERE id_src = %s;", (id_src,))
            result = cur.fetchone()
            cur.close()
            if result is None:
                return False
            else:
                return True
        except Exception as e:
            self.logger.info(f'error to execute select in src table: {e}')
            return False

    def insert_profile(self, id_profile):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO profile (id_profile) VALUES (%s);", (id_profile,))
            cur.close()
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.info(f'error to insert data in profile table: {e}')
            return False

    def check_profile_exists(self, id_profile):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id_profile FROM profile WHERE id_profile = %s;", (id_profile,))
            result = cur.fetchone()
            cur.close()
            if result is None:
                return False
            else:
                return True
        except Exception as e:
            self.logger.info(f'error to execute select in profile table: {e}')
            return False
