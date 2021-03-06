# models_tests.py

import unittest
import orders.models as orders

class TestLineClass(unittest.TestCase):
    def test_create_line(self):
        line = orders.Line('B00000', 5)
        self.assertEqual(line.sku, 'B00000')
        self.assertEqual(line.qty_ordered, 5)
        self.assertEqual(line.qty_shipped, 0)

        line = orders.Line('B0', 5, 2)
        self.assertEqual(line.qty_ordered, 5)
        self.assertEqual(line.qty_shipped, 2)

        line = orders.Line('B0', qty_shipped=8)
        self.assertEqual(line.qty_ordered, 0)
        self.assertEqual(line.qty_shipped, 8)

        line.add(9, 8)
        line.add(qty_shipped=3)
        self.assertEqual(line.qty_ordered, 9)
        self.assertEqual(line.qty_shipped, 19)

    def test_str_representation(self):
        line = orders.Line('B0', 3, 4)
        self.assertEqual(str(line), 'B0 - ordered: 3, shipped: 4')


class TestPackageClass(unittest.TestCase):

    def test_create_package(self):
        package = orders.Package('1234')

        self.assertEqual(package.invoice, '1234')
        self.assertEqual(package.carrier, '')
        self.assertEqual(package.tracking, '')

    def test_add_line(self):
        package = orders.Package('1234')
        package.add('B0', 5, 6)

        self.assertEqual(len(package.lines()), 1)
        self.assertEqual(package.lines()[0].sku, 'B0')
        self.assertEqual(package.lines()[0].qty_ordered, 5)
        self.assertEqual(package.lines()[0].qty_shipped, 6)

        package.add('B0', qty_shipped=2)

        self.assertEqual(len(package.lines()), 1)
        self.assertEqual(package.lines()[0].sku, 'B0')
        self.assertEqual(package.lines()[0].qty_ordered, 5)
        self.assertEqual(package.lines()[0].qty_shipped, 8)

        package.add('C0', 2)
        items = []
        for line in package.lines():
            items.append((line.sku, line.qty_ordered, 
                          line.qty_shipped))

        self.assertEqual(len(package.lines()), 2)
        self.assertIn(('B0', 5, 8), items)
        self.assertIn(('C0', 2, 0), items)

    def test_str_representation(self):
        package = orders.Package('1234')
        package.add('C0', 4)

        package_str = '1234\n    C0 - ordered: 4, shipped: 0'
        self.assertEqual(str(package), package_str)

        package.add('B0', 2, 5)

        package_str = ('1234\n    B0 - ordered: 2, shipped: 5'
                      + '\n    C0 - ordered: 4, shipped: 0')
        self.assertEqual(str(package), package_str)

    def test_contains(self):
        package = orders.Package('1234')
        package.add('B0', 2)
        package.add('C0', 1)
        package.add('A0', 7, 8)

        self.assertTrue(package.contains('C0', 1))
        self.assertFalse(package.contains('D0', 1))
        self.assertFalse(package.contains('B0', 3))
        self.assertTrue(package.contains('B0', 1))
        self.assertTrue(package.contains('B0', 2))
        self.assertTrue(package.contains('A0', 7, 8))
        self.assertTrue(package.contains('A0', qty_shipped=5))
        self.assertFalse(package.contains('A0', qty_shipped=9))

class TestOrderClass(unittest.TestCase):

    def test_create_order(self):
        order = orders.Order()

        self.assertEqual(order.po_number, '')
        self.assertEqual(order.marketplace, '')
    
    def test_add_and_lines_in_package(self):
        order = orders.Order()

        with self.assertRaisesRegex(ValueError, "invoice '1' not in order ''"):
            order.lines_in_package('1')

        order.add('1', 'A', 2, 6)
        order.add('2', 'B', 3)
        order.add('1', 'C', 4)
        order.add('2', 'B', 5)
        order.add('2', 'B', qty_shipped=1)

        with self.assertRaisesRegex(ValueError, "invoice '3' not in order ''"):
            order.lines_in_package('3')

        items1 = []
        for line in order.lines_in_package('1'):
            items1.append((line.sku, line.qty_ordered, line.qty_shipped))
        
        self.assertIn(('A', 2, 6), items1)
        self.assertIn(('C', 4, 0), items1)

        items2 = order.lines_in_package('2')

        self.assertEqual(len(items2), 1)
        self.assertEqual(items2[0].sku, 'B')
        self.assertEqual(items2[0].qty_ordered, 8)
        self.assertEqual(items2[0].qty_shipped, 1)

    def test_invoice_containing(self):
        order = orders.Order()
        order.add('1', 'A', 2)
        order.add('2', 'B', 3, 1)
        order.add('1', 'C', 4)
        order.add('2', 'B', 5)

        with self.assertRaisesRegex(ValueError, ("qty_ordered 2 and qty_shipped 0 "
                                                 + "for sku 'D' not in order ''")):
            order.invoice_containing('D', 2)

        self.assertEqual(order.invoice_containing('A', 2, 0), '1')
        self.assertEqual(order.invoice_containing('B', 8, 1), '2')
        self.assertEqual(order.invoice_containing('C', 2), '1')

    def test_str_representation(self):
        order = orders.Order()
        order.po_number = '1234'
        order.add('1', 'A', 2)
        order.add('2', 'B', 3, 1)
        order.add('1', 'C', qty_shipped=4)
        order.add('2', 'B', 5)

        self.assertEqual(str(order), ('1234\n 1\n    A - ordered: 2, shipped: 0'
                                      + '\n    C - ordered: 0, shipped: 4'
                                      + '\n 2\n    B - ordered: 8, shipped: 1'))

    def test_invoices(self):
        order = orders.Order()
        order.add('E', 'A', 1)
        order.add('F', 'B', 2)
        order.add('E', 'C', 3, 1)

        self.assertEqual(order.invoices(), ['E', 'F'])


if __name__ == '__main__':
    unittest.main()