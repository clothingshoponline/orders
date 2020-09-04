# orders

This repository contains objects and functions to interact with the S&S Activewear API at api.ssactivewear.com.

## Files included

- `orders.py`: Contains the Order, Package, and Line classes.
- `corp_api.py`: Contains functions that interact with the S&S Activewear API.
- `api_global.py`: Contains global variables and functions that can be used across many functions. 
- `orders_tests.py`: Contains unit tests for `orders.py` classes.

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

## Usage of S&S Activewear API

_Note: The global variables within_ `ACCOUNT` _and_ `PASSWORD` _in_ `api_global.py` _must be set up as environmental variables in order to access the S&S Activewear API._

#### Get Order

```
po_number = '111'
marketplace = 'amazon'

# Returns an Order object
order = corp_api.get_order(po_number, marketplace)
```

#### Return Order

```
order = orders.Order()
order.po_number = '111'
order.marketplace = 'amazon'
order.add('B0', 3, '1')

code = 1   # corresponds to return reasons indicated at https://api.ssactivewear.com/V2/Returns_Post.aspx 

# optional
comment = 'package was lost in transit'
test = False
email = ''   # send confirmation email
```

###### Test Return

_Note: Will be cancelled shortly after creation_

```
# Returns a Return Authorization (RA) Number
ra = corp_api.return_request(order, code)
```

###### Real Return

```
ra = corp_api.return_request(order, code, comment, test, email)
```
