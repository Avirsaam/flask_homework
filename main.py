from flask import Flask
from flask import render_template
import random

app = Flask(__name__)

CATEGORIES_RU = {'shoes': 'обувь',
                'jackets': 'куртки',
                'clothes': 'верхняя одежда'}

class ShopItem:
    def __init__(self, sku, name, price, category, description, popularity, sale=100):
        self.sku = sku
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.popularity = popularity
        self.sale = sale
        
    
    def __repr__(self):
        return f'ShopItem({self.sku}, {self.name}, {self.price}, {self.category}, {self.description})'
    
class Repository:
    _repo = []
    _instance = None
    
    NAMES = {'clothes':['одежда','свитер', 'брюки', 'рубашка', 'джемпер', 'шорты', 'платье', 'юбка', 'топ' ],
            'shoes': ['обувь','ботинки', 'тапочки', 'слипоны', 'сандали', 'сапоги', 'ботфорты', 'кроссовки'],
            'jackets': ['куртки', 'дублёнка', 'аляска', 'пальто', 'бушлат']}

    DESCRIPTION = 'Laboris Lorem sunt labore culpa aliquip tempor quis minim. Adipisicing veniam proident in reprehenderit do ipsum cupidatat occaecat fugiat magna. Aliqua eu dolor culpa nisi sint duis fugiat consectetur. Aliquip occaecat officia elit veniam reprehenderit officia aliquip deserunt. Culpa non nulla id laboris qui qui Lorem officia quis.'
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, number_of_items=30):        
        for _ in range(number_of_items):
            sku = f'SKU{random.randint(1, 99999):>06}'
            category = random.choice(list(Repository.NAMES.keys()))
            name = random.choice(Repository.NAMES[category][1:])
            price = random.randint(1000, 99999)
            description = Repository.DESCRIPTION[:random.randint(10, len(Repository.DESCRIPTION.split()))]
            popularity = random.randint(1, 5)
            if random.random() > 0.7:
                sale = random.random() * 100
            else:
                sale = 100
            self._repo.append(ShopItem(sku, name, price, category, description, popularity, sale))
            
    
    def get_list_of_categories(self):        
        return set(item.category for item in self._repo)
    
    def get_items_by_category(self, category):
        return (item for item in self._repo if item.category == category)
    
    def get_item(self, sku):
        
        return next((item for item in self._repo if item.sku == sku), None)
    


@app.route('/')
def index():
    context = {'text_content1': 'Et ipsum elit cillum proident cillum minim commodo elit. Ipsum pariatur sunt quis officia Lorem pariatur aute nisi sunt ad aute. Culpa fugiat voluptate id consequat occaecat officia culpa id do amet consequat. Ad consequat ad Lorem non sunt dolore nisi nostrud reprehenderit reprehenderit enim. In cupidatat excepteur nulla ut irure dolore reprehenderit incididunt tempor non. Ex adipisicing sit et et. Esse aliqua veniam cupidatat elit eu ullamco aute voluptate.',
               'picture_content1': 'https://dummyimage.com/600x400/000/b3b3b3.png'}
    return render_template('index.html', **context)


@app.route('/about/')
def about():
    address = {'building': '20',
               'street': 'Проспект Мира',
               'tel': '+7-987-654-32-11',
               'email': 'sales@myshop.rr'}
    context = {'address': address,
               'shop_photo': 'https://dummyimage.com/600x600/000/b3ff3b3.png'}
    return render_template('about.html', **context)

@app.route('/list_of_categories/')
def list_of_categories():
           
    context = {'header': 'Категории товаров',
               'sub_header': ' ',
               'category_list': repo.get_list_of_categories()
               }
    return render_template('all_categories.html', **context)


@app.route('/items_by_category/<category>/')
def items_by_category(category):
    
    header = 'Товары в категории:'
    sub_header = CATEGORIES_RU[category].capitalize()        
    
    context = {'header': header,
               'sub_header': sub_header,
               'items': repo.get_items_by_category(category)
               }
    return render_template('category.html', **context)

@app.route('/get_item/<sku>/')
def get_item(sku):
    item = repo.get_item(sku)
    print(item)
    context = {'item': item }    
    return render_template('item.html', **context)


if __name__ == '__main__':
    repo = Repository()    
    #print(*repo.get_items_by_category('shoes'))
    app.run(debug=True)
    


