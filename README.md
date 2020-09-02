# orders

This repository contains objects and functions to interact with the S&S Activewear API at api.ssactivewear.com.

## Files included

- `orders.py`: Contains the Order, Package, and Line classes.
- `corp_api.py`: Contains functions that interact with the S&S Activewear API.
- `api_global.py`: Contains global variables and functions that can be used across many functions. 
- `orders_tests.py`: Contains unit tests for `orders.py` classes.

## Usage

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
sku = 'B0'
qty = 3
invoice = '1'

order.add(sku, qty, invoice)
```

#### Get Items within Invoice

```
lines = order.lines_in_package(invoice)

# lines is a list of Line objects (each Line contains sku and qty)
```

#### Access Sku and Quantity in Line Objects

```
line = lines[0]
sku = line.sku
qty = line.qty
```

#### Get Invoice for Specified Sku and Quantity

```
invoice = order.invoice_containing(sku, qty)
```

#### Get List of Invoices within Order

```
invoices = order.invoices()
```

