"""
Please perform all work in this editor.

Question #1 Maximum Loss
For a given dataset of prices over a time period, provide a method that will return the maximum loss for the entire period. 

Examples:

For a series of prices [1,2,3,7,6,5,1,9,7,5,8], assuming prices are ordered by date ascending, the maximum loss is 6, resulting from a buy at 7 and a sell at 1.

For a series of prices [1,9,6,7,6,5,7,2,5,8], assuming prices are ordered by date ascending, the maximum loss is 7, resulting from a buy at 9 and a sell at 2.
"""
import pytest

# options
# * code the algo
# * use pandas to create price diff product over all days and select peak

def max_loss(prices):
    # careful of memory taking in a list
    max_price = 0
    max_loss = 0
    for px in prices:
        if px < 0:
            raise ValueError("Negative price detected")
        if px > max_price:
            max_price = px
            continue
        loss = max_price - px
        if loss > max_loss:
            max_loss = loss
    print(max_loss)
    return max_loss


def test_max_loss_a():
    prices = [1,2,3,7,6,5,1,9,7,5,8]
    out = max_loss(prices)
    assert out == 6
    print(out == 6)


def test_max_loss_b():
    prices = [1,9,6,7,6,5,7,2,5,8]
    out = max_loss(prices)
    assert out == 7
    print(out == 7)


def test_negative_price():
    prices = [1,-1]
    with pytest.raises(ValueError):
        assert max_loss(prices)


test_max_loss_a()
test_max_loss_b()
test_negative_price()