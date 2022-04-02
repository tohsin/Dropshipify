

from webapp import db
from webapp.models import User, Store,Product

import uuid as uuid
from werkzeug.security import generate_password_hash 
def create_dummydata():
        db.drop_all()
        db.create_all()
        print('***** Datebase created ****')
        db.session.add(
            User(email='lily@gmail.com', password=generate_password_hash('elysium8', method='sha256'),first_name= 'Lily', last_name='nwobodo',\
                mailing_address = 'abuja under the left side of love', city= 'abuja',\
                    state = 'Abuja', zip_ = '23424',mailing_phone_number="+23495896056"))
        db.session.add(
            User(email='oluwatosinoseni@gmail.com', password=generate_password_hash('elysium8', method='sha256'),first_name= 'Tosin', last_name='oseni',\
                mailing_address = '2 kazzem ajayo close ogudu association', city= 'Lagos',\
                    state = 'Lagos', zip_ = '100242',mailing_phone_number="+2349026287884"))
        db.session.commit()
        #create stores for both users
        user_to_get_store = User.query.get_or_404(1)
        pic_filename = '/Users/elena/dev/Dropshipify/webapp/static/dummyimages/store1.jpeg'
            #set pic name
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        new_store = Store(store_name = "Soul Dwellers", store_icon = pic_name,\
               store_description = 'Premium looking bags for top achievers',user_id = 1 )
        db.session.add(new_store)
        user_to_get_store.is_retailer = True
        db.session.commit()
        print('Created store for lily')
        
        user_to_get_store = User.query.get_or_404(1)
        pic_filename1 = '/Users/elena/dev/Dropshipify/webapp/static/dummyimages/dior.png'
            #set pic name
        pic_name = str(uuid.uuid1()) + "_" + pic_filename1
        new_product1 = Product(product_name = 'Blue Dior', 
                                  price = 23.3,
                                  ansii = '2343', 
                                  product_link = 'https:r4rr4',
                                  number_available = 63,
                                  description = 'Bad man looking good in dior',
                                  number_shipped = 63 ,
                                  product_image = 'dior.png',
                                  store_id = user_to_get_store.store.id
                                  )
        db.session.add(new_product1)
        
        pic_filename2 = '/Users/elena/dev/Dropshipify/webapp/static/dummyimages/ybag.jpg'
            #set pic name
        pic_name = str(uuid.uuid1()) + "_" + pic_filename2
        new_product2 = Product(product_name = 'Yellow Dior', 
                                  price = 87.3,
                                  ansii = '2343', 
                                  product_link = 'https:r4rr4',
                                  number_available = 8,
                                  description = 'Bad man looking good in yellow dior',
                                  number_shipped = 8,
                                  product_image = 'ybag.jpg',
                                  store_id = user_to_get_store.store.id
                                  )
        db.session.add(new_product2)
        pic_filename3 = '/Users/elena/dev/Dropshipify/webapp/static/dummyimages/socks.jpg'
            #set pic name
        pic_name = str(uuid.uuid1()) + "_" + pic_filename3
        new_product3 = Product(product_name = 'Red socks', 
                                  price = 86.3,
                                  ansii = '2343', 
                                  product_link = 'https:r4rr4',
                                  number_available = 12,
                                  description = 'crispy feeling socks',
                                  number_shipped = 12,
                                  product_image = 'socks.jpg',
                                  store_id = user_to_get_store.store.id
                                  )
        db.session.add(new_product3)
        pic_filename4 = '/Users/elena/dev/Dropshipify/webapp/static/dummyimages/browbag.jpg'
            #set pic name
        pic_name = str(uuid.uuid1()) + "_" + pic_filename4
        new_product4 = Product(product_name = 'Brown  Bag', 
                                  price = 200.3,
                                  ansii = '2343', 
                                  product_link = 'https:r4rr4',
                                  number_available = 87,
                                  description = 'Bad Bitvhes only',
                                  number_shipped = 87,
                                  product_image = 'browbag.jpg',
                                  store_id = user_to_get_store.store.id
                                  )
        db.session.add(new_product4)
        pic_filename5 = '/Users/elena/dev/Dropshipify/webapp/static/dummyimages/ashoka.jpg'
            #set pic name
        pic_name = str(uuid.uuid1()) + "_" + pic_filename5
        new_product5 = Product(product_name = 'Ahoka Dior', 
                                  price = 90,
                                  ansii = '2343', 
                                  product_link = 'https:r4rr4',
                                  number_available = 8,
                                  description = 'premium ashoka bag to store you beatiful hand for mrraige',
                                  number_shipped = 8,
                                  product_image = 'ashoka.jpg',
                                  store_id = user_to_get_store.store.id
                                  )
        db.session.add(new_product5)
        db.session.commit()