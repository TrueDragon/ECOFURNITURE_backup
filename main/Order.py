class Order():
    def __init__(self, customer_id, order_id, item_id, item_quantity):
        self.__customer_id = customer_id
        self.__order_id = order_id
        self.__item_id = item_id
        self.__item_quantity = item_quantity

    def get_customer_id(self):
        return self.__customer_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def get_item_id(self):
        return self.__item_id

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def get_item_quantity(self):
        return self.__item_quantity

    def set_item_quantity(self, item_quantity):
        self.__item_quantity = item_quantity

    def __str__(self):
        return f"[{self.__customer_id}, {self.__order_id}, {self.__item_id}, {self.__item_quantity}]"