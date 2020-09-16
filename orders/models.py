# models.py

# Contains the Order, Package, and Line objects.



class Line:
    def __init__(self, sku: str, qty_ordered: int = 0,
                 qty_shipped: int = 0):
        """Initialize Line with sku and qty values."""
        self.sku = sku
        self.qty_ordered = qty_ordered
        self.qty_shipped = qty_shipped

    def add(self, qty_ordered: int = 0, 
            qty_shipped: int = 0) -> None:
        """Add qtys to Line."""
        self.qty_ordered += qty_ordered
        self.qty_shipped += qty_shipped

    def __str__(self) -> str:
        """Define the string representation of a Line."""
        return (f"{self.sku} - ordered: {self.qty_ordered}, "
                + f"shipped: {self.qty_shipped}")



class Package:
    def __init__(self, invoice: str):
        """Initialize Package with invoice."""
        self.invoice = invoice
        self.carrier = ''
        self.tracking = ''

        self._lines = dict()

    def __str__(self) -> str:
        """Return the string representation of a Package."""
        package_str = self.invoice
        skus = sorted(list(self._lines.keys()))
        for sku in skus:
            package_str += f'\n    {self._lines[sku]}'
        return package_str
    
    def add(self, sku: str, qty_ordered: int = 0, 
            qty_shipped: int = 0) -> None:
        """Add the qtys to the Line of the given sku. If the sku does 
        not exist, create a new Line and add it to the Package.
        """
        if sku in self._lines:
            self._lines[sku].add(qty_ordered, qty_shipped)
        else:
            self._lines[sku] = Line(sku, qty_ordered, qty_shipped)

    def lines(self) -> [Line]:
        """Return lines stored as a list of Lines."""
        return [line for line in self._lines.values()]

    def contains(self, sku: str, qty_ordered: int = 0, 
                 qty_shipped: int = 0) -> bool:
        """Return True if the Package contains the given qtys, 
        False otherwise.
        """
        return (sku in self._lines 
                and self._lines[sku].qty_ordered >= qty_ordered 
                and self._lines[sku].qty_shipped >= qty_shipped)







class Order:
    def __init__(self):
        """Initialize an empty Order."""
        self.po_number = ''
        self.marketplace = ''

        self._packages = dict()

    def __str__(self):
        """Return the string representation of the Order."""
        order_str = ''
        invoices = sorted(list(self._packages.keys()))
        for invoice in invoices:
            order_str += f'\n{self._packages[invoice]}'
        return order_str

    def add(self, sku: str, qty: int, invoice: str) -> None:
        """Add Line(sku, qty) to self._packages[invoice]. If the sku 
        does not exist, create a new Line. If the invoice does not exist,
        create a new package.
        """
        if invoice in self._packages:
            self._packages[invoice].add(sku, qty)
        else:
            package = Package(invoice)
            package.add(sku, qty)
            self._packages[invoice] = package

    def lines_in_package(self, invoice: str) -> [Line]:
        """Returns a list of Lines within the Package with 
        the given invoice. Raise a ValueError if the order 
        does not contain the invoice.
        """
        if invoice not in self._packages:
            raise ValueError(f"invoice '{invoice}' not in order '{self.po_number}'")
        return self._packages[invoice].lines()

    def invoice_containing(self, sku: str, qty: int) -> str:
        """Return the invoice of the package containing the given sku. 
        Raise a ValueError if the given sku is not within the order.
        """
        for package in self._packages.values():
            if package.contains(sku, qty):
                return package.invoice
        raise ValueError(f"qty '{qty}' of sku '{sku}' not in order '{self.po_number}'")

    def invoices(self) -> [str]:
        """Return a list of invoices within the order."""
        return sorted(list(self._packages.keys()))