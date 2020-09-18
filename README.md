# orders v1.0.1

This repository contains objects that store order information.

## Overview

An Order object contains Package objects. Each Package object 
contains Line objects. 

Order, Package, and Line are classes.
Everything else is an attribute.

```
Order
    .po_number
    .marketplace
    Package
        .invoice
        .carrier
        .tracking
        Line
            .sku
            .qty_ordered
            .qty_shipped
```

## Installation

```
pip install git+https://github.com/clothingshoponline/orders.git@v1.0.1
```

## Import

```
import orders
```

## Usage of Order Object

#### Create Order Object

```
order = orders.Order()
```

#### Set PO Number

```
order.po_number = '111'
```

#### Set Marketplace (Amazon, Walmart, eBay, etc.)

```
order.marketplace = 'amazon'
```

#### Add Items

```
invoice = '1'
sku = 'B0'

# optional (defaults to 0)
qty_ordered = 3
qty_shipped = 2

order.add(invoice, sku, qty_ordered, qty_shipped)
```

#### Get Items within Invoice

```
invoice = '1'

# lines is a list of Line objects
lines = order.lines_in_package(invoice)

# access Line attributes
line = lines[0]

sku = line.sku
qty_ordered = line.qty_ordered
qty_shipped = line.qty_shipped
```

#### Get Invoice for Specific Sku and Quantity

```
sku = 'B0'

# optional (defaults to 0)
qty_ordered = 3
qty_shipped = 2

invoice = order.invoice_containing(sku, qty_ordered, qty_shipped)
```

#### Get List of Invoices within Order

```
invoices = order.invoices()
```

#### View Order Content

```
print(order)
```