def calc_tax(amount):
    # placeholder: simple flat 10% tax and 5% profit margin
    tax = amount * 0.10
    profit = amount * 0.05
    return {'amount': amount, 'tax': tax, 'profit': profit, 'net': amount - tax}
