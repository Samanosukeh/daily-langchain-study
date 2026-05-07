```python
import unittest
from unittest.mock import MagicMock, patch

class TesteCalculadora(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_soma(self):
        self.assertEqual(self.calc.somar(2, 3), 5)
        self.assertEqual(self.calc.somar(-1, 1), 0)
        self.assertEqual(self.calc.somar(0, 0), 0)

    def test_subtracao(self):
        self.assertEqual(self.calc.subtrair(5, 3), 2)
        self.assertEqual(self.calc.subtrair(10, -5), 15)

    @patch('builtins.print')
    def test_exibir_resultado(self, mock_print):
        self.calc.exibir(10)
        mock_print.assert_called_once_with("Resultado: 10")

class Calculadora:
    def somar(self, a, b):
        return a + b

    def subtrair(self, a, b):
        return a - b

    def exibir(self, valor):
        print(f"Resultado: {valor}")

if __name__ == '__main__':
    unittest.main()
```