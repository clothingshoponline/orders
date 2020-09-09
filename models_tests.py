# models_tests.py

import unittest
import orders.models as orders

class TestLineClass(unittest.TestCase):
    def test_create_line(self):
        line = orders.Line('B00000', 5)
        self.assertEqual(line.sku, 'B00000')
        self.assertEqual(line.qty, 5)

    def test_str_representation(self):
        line = orders.Line('B0', 5)
        self.assertEqual(str(line), 'B0: 5')


class TestPackageClass(unittest.TestCase):

    def test_create_package(self):
        package = orders.Package('1234')

        self.assertEqual(package.invoice, '1234')

    def test_add_line(self):
        package = orders.Package('1234')
        package.add('B0', 5)

        self.assertEqual(len(package.lines()), 1)
        self.assertEqual(package.lines()[0].sku, 'B0')
        self.assertEqual(package.lines()[0].qty, 5)

        package.add('B0', 3)

        self.assertEqual(len(package.lines()), 1)
        self.assertEqual(package.lines()[0].sku, 'B0')
        self.assertEqual(package.lines()[0].qty, 8)

        package.add('C0', 2)
        items = []
        for line in package.lines():
            items.append((line.sku, line.qty))

        self.assertEqual(len(package.lines()), 2)
        self.assertIn(('B0', 8), items)
        self.assertIn(('C0', 2), items)

    def test_str_representation(self):
        package = orders.Package('1234')
        package.add('C0', 4)

        self.assertEqual(str(package), '1234\n    C0: 4')

        package.add('B0', 2)

        self.assertEqual(str(package), '1234\n    B0: 2\n    C0: 4')

    def test_contains(self):
        package = orders.Package('1234')
        package.add('B0', 2)
        package.add('C0', 1)

        self.assertTrue(package.contains('C0', 1))
        self.assertFalse(package.contains('D0', 1))
        self.assertFalse(package.contains('B0', 3))
        self.assertTrue(package.contains('B0', 1))
        self.assertTrue(package.contains('B0', 2))

class TestOrderClass(unittest.TestCase):

    def test_create_order(self):
        order = orders.Order()

        self.assertEqual(order.po_number, '')
        self.assertEqual(order.marketplace, '')
    
    def test_add_and_lines_in_package(self):
        order = orders.Order()

        with self.assertRaisesRegex(ValueError, 'invoice does not exist'):
            order.lines_in_package('1')

        order.add('A', 2, '1')
        order.add('B', 3, '2')
        order.add('C', 4, '1')
        order.add('B', 5, '2')

        with self.assertRaisesRegex(ValueError, 'invoice does not exist'):
            order.lines_in_package('3')

        items1 = []
        for line in order.lines_in_package('1'):
            items1.append((line.sku, line.qty))
        
        self.assertIn(('A', 2), items1)
        self.assertIn(('C', 4), items1)

        items2 = order.lines_in_package('2')

        self.assertEqual(len(items2), 1)
        self.assertEqual(items2[0].sku, 'B')
        self.assertEqual(items2[0].qty, 8)

    def test_invoice_containing(self):
        order = orders.Order()
        order.add('A', 2, '1')
        order.add('B', 3, '2')
        order.add('C', 4, '1')
        order.add('B', 5, '2')

        with self.assertRaisesRegex(ValueError, 'qty of sku does not exist'):
            order.invoice_containing('D', 2)

        self.assertEqual(order.invoice_containing('A', 2), '1')
        self.assertEqual(order.invoice_containing('B', 8), '2')
        self.assertEqual(order.invoice_containing('C', 2), '1')

    def test_str_representation(self):
        order = orders.Order()
        order.add('A', 2, '1')
        order.add('B', 3, '2')
        order.add('C', 4, '1')
        order.add('B', 5, '2')

        self.assertEqual(str(order), '\n1\n    A: 2\n    C: 4\n2\n    B: 8')

    def test_invoices(self):
        order = orders.Order()
        order.add('A', 1, 'E')
        order.add('B', 2, 'F')
        order.add('C', 3, 'E')

        self.assertEqual(order.invoices(), ['E', 'F'])


if __name__ == '__main__':
    unittest.main()