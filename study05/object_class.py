### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.__code=item_code
        self.__name=item_name
        self.__price=price
    
    def get_code(self):
        return self.__code
    
    def get_name(self):
        return self.__name
    
    def get_price(self):
        return self.__price
    
    def get_amount(self):
        return self.__amount
    
    def get_sum(self):
        return self.__sum
    
    def get_deposit(self):
        return self.__deposit
    
    def get_change(self):
        return self.__change
    
    def set_amount(self, amount):
        self.__amount = amount
        self.__sum = int(self.__price) * int(self.__amount)
    
    def set_deposit(self, deposit):
        self.__deposit = deposit
        self.__change = int(self.__deposit) - self.__sum

    def get_display_info(self):
        return "コード：{}、名前：{}、単価：{}".format(self.__code, self.__name, self.__price)
  
    def get_subtotal(self):
        return "名前：{}、単価：{}、個数：{}、小計：{}".format(self.__name, self.__price, self.__amount, self.get_sum())
    
    def get_write_info(self):
        return "コード：{}、名前：{}、単価：{}、個数：{}、小計：{}".format(
                self.__code, self.__name, self.__price, self.__amount, self.get_sum())
    
    def get_display_sum(self):
        return "個数：{}、合計金額：{}".format(self.__amount, self.get_sum())
    
    def get_display_change(self):
        return "お返し:{}".format(self.__change)
    
### オーダークラス
class Order:
    
    def __init__(self):
        self.item_order_list=[]
    
    def add_item_order(self,item):
        self.item_order_list.append(item)
        
    def get_item_order_list(self):
        return self.item_order_list

    def sum_item_list(self):
        """
        オーダーに登録されたリストの金額を合計する
        return 合計金額
        """
        order_sum = 0
        for item in self.item_order_list:
            order_sum = order_sum + item.get_sum()
        
        return order_sum
