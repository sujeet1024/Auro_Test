from bs4 import BeautifulSoup
import time

class AllBooks():
    def __init__(self):
        self.books = {}

    def add_order(self, book_name, operation, price, vol, order_id):
        if book_name not in self.books:
            self.books[book_name] = OrderBook(book_name)

        new_order = Order(
            order_id,
            operation,
            price,
            vol
        )
        self.books[book_name].add_order(new_order)

    def delete_order(self, book_name, order_id):
        self.books[book_name].remove(order_id)

    def __str__(self):
        print_str = ""
        for book in self.books.values():
            print_str += str(book) + "\n"
        return print_str

class OrderBook():
    def __init__(self, book_name):
        self.sell = []
        self.buy = []
        self.book_name = book_name

    def remove(self, order_id):
        for order in self.sell:
            if order.id == order_id:
                self.sell.remove(order)
                return
        for order in self.buy:
            if order.id == order_id:
                self.buy.remove(order)
                return

    def add_order(self, order):
        if order.operation == 'SELL':
            self.sell.append(order)
        else:
            self.buy.append(order)

        self.sell.sort(key=lambda x: x.price)
        self.buy.sort(key=lambda x: x.price, reverse=True)

        self.match()

    def match(self):
        while self.sell and self.buy and self.sell[0].price <= self.buy[0].price:
            sell_order = self.sell[0]
            buy_order = self.buy[0]

            if sell_order.vol == buy_order.vol:
                self.sell.pop(0)
                self.buy.pop(0)
            elif sell_order.vol > buy_order.vol:
                sell_order.vol -= buy_order.vol
                self.buy.pop(0)
            else:
                buy_order.vol -= sell_order.vol
                self.sell.pop(0)

    def __str__(self):
        print_str = "book: {}\n".format(self.book_name)
        print_str += "\t\tBuy -- Sell\t\t\n"
        print_str += "="*30 + "\n"
        for i in range(max(len(self.buy), len(self.sell))):
            buy = self.buy[i] if i < len(self.buy) else None
            sell = self.sell[i] if i < len(self.sell) else None
            if buy is None:
                print_str += "\t\t -- {}\t\t\n".format(str(sell))
            elif sell is None:
                print_str += "\t\t{} -- \t\t\n".format(str(buy))
            else:
                print_str += "\t\t{} -- {}\t\t\n".format(str(buy), str(sell))
        return print_str


class Order():
    def __init__(self, id, operation, price, vol):
        self.id = id
        self.operation = operation 
        self.price = price
        self.vol = vol

    def __str__(self):
        return "{}@{}".format(self.price, self.vol)


    

if __name__ == "__main__":

    book_keeper = AllBooks()

    with open('small_orders.xml', 'r') as f:
        data = f.read()


    lines = data.split('\n')
    lines = lines[2:-1]
    start_time = time.time()
    for l in lines:
        l = l.replace("=\" ", "\"")
        l = l.replace("=\" ", "\"")
        l = l.replace("=\" ", "\"")
        l = l.replace("=\" ", "\"")
        l = l.replace("=\" ", "\"")
        l = l.replace("<", "")
        l = l.replace("/>", "")
        # print(l)
        instr_type = l.split()[0]
        if instr_type == "AddOrder":
            book_name = l.split()[1].split("\"")[1]
            operation = l.split()[2].split("\"")[1]
            price = l.split()[3].split("\"")[1]
            price = float(price)
            vol = l.split()[4].split("\"")[1]
            vol = float(vol)
            order_id = l.split()[5].split("\"")[1]
            book_keeper.add_order(book_name, operation, price, vol, order_id)

        else:
            book_name = l.split()[1].split("\"")[1]
            order_id = l.split()[2].split("\"")[1]
            book_keeper.delete_order(book_name, order_id)

    end_time  = time.time()
    print(book_keeper)
    print("Total processing time: {}".format(end_time - start_time))
    # print(lines)
