import psycopg2
import os
import sys

class Database():
    
    def __init__(self, host=os.environ['POSTGRESQL_ADDRESS'],
                            database=os.environ['POSTGRESQL_DATABASE'],
                            user=os.environ['POSTGRESQL_USERNAME'],
                            password=os.environ['POSTGRESQL_PASSWORD']):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

        self.cur = self.conn.cursor()

        self.create_tables()

    def query(self, query):
        try:
            self.cur.execute(query)
        except Exception as e:
            self.conn.rollback()
            print(e, file=sys.stderr)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def create_tables(self):
        command = """
            CREATE TABLE IF NOT EXISTS CUSTOMER (
                email VARCHAR(255) NOT NULL,
                fullName VARCHAR(255) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                cpf VARCHAR(14) NOT NULL,
                birthDate DATE NOT NULL,
                active BOOLEAN NOT NULL,
                CONSTRAINT CUSTOMER_UK UNIQUE (cpf),
                CONSTRAINT CUSTOMER_PK PRIMARY KEY (email)
            );

            CREATE TABLE IF NOT EXISTS DISC (
                discName VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                releaseYear SMALLINT NOT NULL,
                musicStyle VARCHAR(255) NOT NULL,
                availableQuantity INTEGER NOT NULL,
                unitaryValue DOUBLE PRECISION NOT NULL,
                CONSTRAINT DISC_PK PRIMARY KEY (discName, artist)
            );

            CREATE TABLE IF NOT EXISTS PURCHASE (
                purchaseId SERIAL NOT NULL,
                purchaseDateTime TIMESTAMP NOT NULL,
                totalValue DOUBLE PRECISION NOT NULL,
                email VARCHAR(255) NOT NULL,
                effective BOOLEAN NOT NULL,
                CONSTRAINT PURCHASE_PK PRIMARY KEY (purchaseId),
                CONSTRAINT PURCHASE_CUSTOMER_FK FOREIGN KEY (email) REFERENCES CUSTOMER (email) ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS has (
                purchaseId SERIAL NOT NULL,
                discName VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                quantity INTEGER NOT NULL,
                CONSTRAINT has_PURCHASE_FK FOREIGN KEY (purchaseId) REFERENCES PURCHASE (purchaseId) ON DELETE RESTRICT,
                CONSTRAINT has_DISC_FK FOREIGN KEY (discName, artist) REFERENCES DISC (discName, artist) ON DELETE RESTRICT
            );
        """
        self.query(command)
        self.commit()