#!/bin/python3

# Complete the 'solve' function below.


def solve():
    # Write your code here
    import datetime
    import sys
    from bisect import insort

    class Order:
        def __init__(self, an_order):
            self.time = datetime.datetime.strptime(an_order[0], "%H:%M:%S")
            self.client_id = int(an_order[1])
            self.direction = an_order[2]
            self.size = int(an_order[3])
            self.otype = an_order[4]
            self.price = float(an_order[5])

        def __lt__(self, other):
            # used by bisect.insort to keep limit order lists in sorted order
            # primary key: price, increasing for sells, decreasing for buys
            if self.direction == "s":  # sell orders from smaller to larger
                if self.price < other.price:
                    return True
            elif self.price > other.price:  # buy orders from larger to smaller
                return True
            if self.price == other.price:  
                # sort orders with same price by increasing trade time
                return self.time < other.time
            else:
                return False

    class OrderBook:
        # maintain two lists for limit orders, process trades as they arrive
        def __init__(self):
            self.sell_limit = []
            self.buy_limit = []

        def add_limit(self, order):
            # add limit order to appropriate list, with __lt__ sort order
            if order.direction == "s":
                insort(self.sell_limit, order)
            else:
                insort(self.buy_limit, order)

        def print_trade(self, time, buy_id, sell_id, price, size):  
            # print a single trade
            tstr= time.strftime('%H:%M:%S')
            print(f"{tstr} {buy_id} {sell_id} {price:.2f} {size}")

        def process_order(self, order):
            if order.direction == "s":  # sell order
                opposite_book = self.buy_limit  # opposing book of limit orders
                sell_id = order.client_id
            else:
                opposite_book = self.sell_limit
                buy_id = order.client_id
            while order.size and opposite_book:
                # order still isn't filled and opposing limit book has entries
                ob = opposite_book[0]
                if ob.direction == "s":  # opposite side is selling
                    sell_id = ob.client_id
                    if order.otype == "l" and ob.price > order.price:  # lowest offer too high
                        break
                else:
                    buy_id = ob.client_id
                    if order.otype == "l" and ob.price < order.price:  # highest bid too low
                        break
                if order.size >= ob.size:  # order can only be partially filled
                    order.size -= ob.size
                    self.print_trade(order.time, buy_id, sell_id, ob.price, ob.size)
                    opposite_book.pop(0)
                else:  # we are filled
                    ob.size -= order.size
                    self.print_trade(order.time, buy_id, sell_id, ob.price, order.size)
                    order.size = 0
            if (order.otype == "l") and order.size:  
                # remaining shares in limit order, add to book
                self.add_limit(order)

    def read_one_order():
        # read an order from standard input
        an_order = sys.stdin.readline().rstrip().split()
        return Order(an_order)

    # "main" routine
    the_order_book = OrderBook()
    ninputs = int(sys.stdin.readline().strip())
    for i in range(ninputs):
        order = read_one_order()
        the_order_book.process_order(order)

if __name__ == "__main__":
    solve()
