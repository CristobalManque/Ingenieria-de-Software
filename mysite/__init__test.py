import unittest
import os
from flask import Flask
import db
import auth
import views

from __init__ import create_app

class TestCreateApp(unittest.TestCase):
    def test_create_app(self):
        # Crear una instancia de la aplicación utilizando la configuración de prueba
        test_config = {
            'SECRET_KEY': 'test',
            'DATABASE': os.path.join(app.instance_path, 'test_datos.sqlite'),
        }
        app = create_app(test_config)

        # Verificar que la instancia de la aplicación es de la clase Flask
        self.assertIsInstance(app, Flask)

        # Verificar que se ha configurado correctamente la base de datos
        self.assertEqual(app.config['SECRET_KEY'], 'test')
        self.assertEqual(app.config['DATABASE'], os.path.join(app.instance_path, 'test_datos.sqlite'))

        # Verificar que se han registrado correctamente los blueprints
        self.assertIn('auth', app.blueprints)
        self.assertIn('views', app.blueprints)

if __name__ == '__main__':
    unittest.main()
