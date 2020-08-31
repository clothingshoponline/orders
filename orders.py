# orders.py



class Line:
    def __init__(self, sku: str, qty: int):
        self.sku = sku
        self.qty = qty

    def __str__(self) -> str:
        ''' Define the string representation of a Line. '''
        return f'{self.sku}: {self.qty}'



class Package:
    def __init__(self, invoice: str):
        self.invoice = invoice

        self._lines = dict()

    def __str__(self) -> str:
        ''' Return the string representation of a Package. '''
        package_str = self.invoice
        skus = sorted(list(self._lines.keys()))
        for sku in skus:
            package_str += f'\n    {self._lines[sku]}'
        return package_str
    
    def add(self, sku: str, qty: int) -> None:
        ''' If sku already exists in self._lines, add qty to 
        self._lines[sku]. Otherwise, add Line(sku, qty) to self._lines. '''
        if sku in self._lines:
            self._lines[sku].qty += qty
        else:
            self._lines[sku] = Line(sku, qty)

    def lines(self) -> [Line]:
        ''' Return lines stored in self._lines as a list of Lines. '''
        return [line for line in self._lines.values()]

    def contains(self, sku: str, qty: int) -> bool:
        ''' Return True if the Package contains the qty of sku, False otherwise. '''
        return sku in self._lines and self._lines[sku].qty >= qty







class Order:
    def __init__(self):
        self.po_number = ''
        self.marketplace = ''

        self._packages = dict()

    def __str__(self):
        order_str = ''
        invoices = sorted(list(self._packages.keys()))
        for invoice in invoices:
            order_str += f'\n{self._packages[invoice]}'
        return order_str

    def add(self, sku: str, qty: int, invoice: str) -> None:
        ''' Add Line(sku, qty) to self._packages[invoice]. If the sku 
        does not exist, create a new Line. If the invoice does not exist,
        create a new package. '''
        if invoice in self._packages:
            self._packages[invoice].add(sku, qty)
        else:
            package = Package(invoice)
            package.add(sku, qty)
            self._packages[invoice] = package

    def lines_in_package(self, invoice: str) -> [Line]:
        ''' Returns a list of Lines within the Package with 
        the given invoice. Raise a ValueError if the order 
        does not contain the invoice. '''
        if invoice not in self._packages:
            raise ValueError('invoice does not exist')
        return self._packages[invoice].lines()

    def invoice_containing(self, sku: str, qty: int) -> str:
        ''' Return the invoice of the package containing the given sku. 
        Raise a ValueError if the given sku is not within the order. '''
        for package in self._packages.values():
            if package.contains(sku, qty):
                return package.invoice
        raise ValueError('qty of sku does not exist')

    def invoices(self) -> [str]:
        ''' Return a list of invoices within the order. '''
        return sorted(list(self._packages.keys()))