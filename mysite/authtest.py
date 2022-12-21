import unittest
from auth import register, login, logout

class TestAuth(unittest.TestCase):
    def test_register(self):
        # Arrange
        # Preparar los datos de entrada y cualquier otro recurso necesario
        data = {'name': 'John', 'direccion': '123 Main St', 'tel': '123456', 'mail': 'john@example.com', 'password': 'abc123', 'tipo': 'admin'}
        
        # Act
        # Llamar a la función a probar con los datos de entrada
        result = register(data)
        
        # Assert
        # Verificar que el resultado sea el esperado
        self.assertEqual(result, 'Success')
        
    def test_login(self):
        # Arrange
        # Preparar los datos de entrada y cualquier otro recurso necesario
        data = {'mail': 'john@example.com', 'password': 'abc123'}
        
        # Act
        # Llamar a la función a probar con los datos de entrada
        result = login(data)
        
        # Assert
        # Verificar que el resultado sea el esperado
        self.assertEqual(result, 'Success')
        
    def test_logout(self):
        # Arrange
        # Preparar los datos de entrada y cualquier otro recurso necesario
        
        # Act
        # Llamar a la función a probar con los datos de entrada
        result = logout()
        
        # Assert
        # Verificar que el resultado sea el esperado
        self.assertEqual(result, 'Success')
