Create Virtual environment in python
python3 -m venv venv
to install all libraries
pip install -r requirements.txt 

pip freeze >requirements.txt

Windows
$ py -3 -m venv venv

Activate virtual environment:
venv\Scripts\activate

tell flask whicj app to use
export FLASK_APP=main.py

then create dummy data with command
flask test

TODO:
[] Add to cart button should populate cart/order table with the item. 
[] Wishlist button should add the item to wishlist object/table/
[] View cart page should display all items in the user's cart
[] Delete button for cart items should remove them from the cart
[] Changes in Quantity box should be reflected with user input
[] Checkout button should at least update the status of the order items to 'pending'
[] Pending orders page should display orders for the store where status is pending
[] Delivered button on pending orders page should update the status of the order, hence remove the item from the list
[] Order history page should display all orders for the store
[] View products page should display all products on the page
[] Add to cart button on product decription page should be functional 
[] Wishlist button on product descriptions page should be functional
[] Users should be notified when actions they perform are successful;;

UI Pages:
[] Retailer Store Home
[] Shopper Home
[] Check out page


Suggestion for cart databasse
*Sent you the stuff