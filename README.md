# orders

This repository contains objects and functions to interact with the S&S Activewear API at api.ssactivewear.com.

## Files included

- `orders.py`: Contains the Order, Package, and Line classes.
- `corp_api.py`: Contains functions that interact with the S&S Activewear API.
- `api_global.py`: Contains global variables and functions that can be used across many functions. 
- `orders_tests.py`: Contains unit tests for `orders.py` classes.

## Usage

#### Create Order object

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

#### Add items

```
sku = 'B0'
qty = 3
invoice = '1'

order.add(sku, qty, invoice)
```

