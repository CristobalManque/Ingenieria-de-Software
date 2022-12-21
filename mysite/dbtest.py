import unittest
import sqlite3
from unittest.mock import patch

from flask import Flask

from db import get_db, init_db, close_db, init_db_command, read_db_row, read_db_col


class TestDB(unittest.TestCase):
    def setUp(self):
        # Creamos una aplicación de Flask de prueba
        self.app = Flask(__name__)
        # Establecemos la configuración de la base de datos en una base de datos en memoria
        self.app.config['DATABASE'] = ':memory:'
        # Inicializamos la base de datos
        init_db(self.app)
    
    def tearDown(self):
        # Cerramos la conexión de la base de datos
        close_db()
    
    def test_get_db(self):
        # Comprobamos que se devuelve una conexión a la base de datos
        with self.app.app_context():
            db = get_db()
            self.assertIsInstance(db, sqlite3.Connection)
    
    def test_init_db(self):
        # Creamos una conexión a la base de datos en memoria y comprobamos que se ha creado la tabla "test"
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_close_db(self):
        # Comprobamos que se cierra la conexión de la base de datos
        with self.app.app_context():
            db = get_db()
            close_db()
            self.assertIsNone(g.get('db'))
    
    @patch('tu_modulo.click.echo')
    def test_init_db_command(self, mock_echo):
        # Creamos una conexión a la base de datos en memoria y ejecutamos el comando "init-db"
        with self.app.app_context():
            init_db_command()
            # Comprobamos que se ha llamado a click.echo con el mensaje "Initialized the database."
            mock_echo.assert_called_with('Initialized the database.')
    
        def test_read_db_row(self):
        # Insertamos una fila en la tabla "test" y comprobamos que se devuelve al leer la tabla completa
            with self.app.app_context():
                db = get_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO test (col1, col2) VALUES (?, ?)", ("val1", "val2"))
                db.commit()

                data = read_db_row("test")
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["col1"], "val1")
                self.assertEqual(data[0]["col2"], "val2")
    
    def test_read_db_col(self):
        # Insertamos una fila en la tabla "test" y comprobamos que se devuelve al leer una columna específica
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO test (col1, col2) VALUES (?, ?)", ("val1", "val2"))
            db.commit()

            data = read_db_col("test", "col1")
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["col1"], "val1")
