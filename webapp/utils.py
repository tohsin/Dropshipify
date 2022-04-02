from webapp.models import User, Product, Store, Order, OrderItem
from . import db

def add_orderItem(order, product_id):
    found_order_item_for_product = False
    print('Entering loop to find order item')
    for order_item in order.order_item:
        print('Entered loop to find order item')
        #check if we have a product in that order from order item
        if order_item.product_id == product_id:
                #we found the product of that cart now we adding to it
                print('found a match for product id')
                found_order_item_for_product = True
                order_item.quantity+=1
                db.session.commit()
                break
    #if loop finished and we didnt find anything
    if not found_order_item_for_product:
        print("Didn't find the order item required so try creating new one ")
                #create order item mapped to product
        item = OrderItem( product_id = product_id, order=order)
        db.session.add(item)
        db.session.commit()
        
  
    

def get_Order_object(orders, product, user):
    found_order_with_store = False
    u_order = None
    print('about to enter loop to find order')
    for order in orders:
        print('entered loop to search for order matching store')
        if order.store_id == product.store_id:
            u_order = order
            print('found order that matches the store')
            found_order_with_store = True
            break
    if not found_order_with_store:
        print('didnt find order in first place so creating new one')
        u_order = Order(store_id = product.store_id, 
                        user = user)
        db.session.add(u_order)
        db.session.commit()
    return u_order
