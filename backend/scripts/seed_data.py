import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils.timezone import make_aware
from datetime import datetime
from products.models import Supermarket, Category, GenericProduct, ProductVariant

# Supermarkets
tesco = Supermarket.objects.get_or_create(name="Tesco")[0]
billa = Supermarket.objects.get_or_create(name="Billa")[0]
albert = Supermarket.objects.get_or_create(name="Albert")[0]

# Categories
dairy = Category.objects.get_or_create(name="Dairy")[0]
bakery = Category.objects.get_or_create(name="Bakery")[0]
vegetables = Category.objects.get_or_create(name="Vegetables")[0]
eggs = Category.objects.get_or_create(name="Eggs")[0]
packaged_goods = Category.objects.get_or_create(name="Packaged Goods")[0]



# Whole milk
whole_milk = GenericProduct.objects.get_or_create(name="Whole milk", amount=1.0, unit="L", category=dairy)[0]
ProductVariant.objects.get_or_create(name="BILLA BIO Čerstvé mléko plnotučné", price=34.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Madeta Jihočeské trvanlivé mléko plnotučné 3,5%", price=18.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Olma Selské čerstvé mléko plnotučné 3,9%", price=30.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tatra Swift plnotučné mléko 3,5%", price=34.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="clever Mléko plnotučné čerstvé 3,5%", price=26.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Srdce domova Selské čerstvé mléko plnotučné 3,8 % tuku", price=38.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Srdce domova Čerstvé mléko plnotučné 3,5% tuku", price=25.9, supermarket=billa, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Madeta Jihočeské trvanlivé mléko plnotučné 3,5%", price=27.9, supermarket=tesco, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tesco Mléko UHT plnotoučné 3,5%", price=24.9, supermarket=tesco, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Olma Selské čerstvé mléko plnotučné 3,9%", price=41.9, supermarket=tesco, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tesco Čerstvé plnotučné mléko 3,5%", price=27.9, supermarket=tesco, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Albert Mléko plnotučné trvanlivé", price=23.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Albert Mléko plnotučné čerstvé", price=27.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Mléko plnotučné 3,5% trvanlivé", price=27.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Česká chuť Bio mléko čerstvé plnotučné", price=34.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Nature's Promise Bio Mléko plnotučné čerstvé", price=33.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Olma Selské mléko plnotučné čerstvé", price=41.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Olma Bio čerstvé mléko", price=42.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Čerstvé mléko sel.kunín 3 ,8%", price=36.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tatra Swift Mléko plnotučné trvanlivé", price=34.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tatra Mléko plnotučné trvanlivé", price=29.9, supermarket=albert, generic_product=whole_milk, last_updated=make_aware(datetime.now()))

# Butter
butter = GenericProduct.objects.get_or_create(name="Butter", amount=250.0, unit="g", category=dairy)[0]
ProductVariant.objects.get_or_create(name="Madeta Jihočeské máslo", price=69.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Madeta Jihočeské máslo nedělní", price=69.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tatra máslo 82%", price=74.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Milko máslo", price=67.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Milkpol máslo 82%", price=59.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Máslo", price=59.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Moravia máslo", price=69.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Srdce Domova České Máslo 84%", price=69.9, supermarket=billa, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tesco Máslo 82% tuku", price=59.9, supermarket=tesco, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Madeta Jihočeské máslo", price=69.9, supermarket=tesco, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Česká chuť Máslo", price=69.9, supermarket=albert, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Milkpol Máslo 82%", price=39.9, supermarket=albert, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Madeta Jihočeské máslo", price=79.9, supermarket=albert, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tatra Máslo", price=74.9, supermarket=albert, generic_product=butter, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="President Máslo Plaquette jemné", price=99.9, supermarket=albert, generic_product=butter, last_updated=make_aware(datetime.now()))

# Eggs size M
eggs_size_m = GenericProduct.objects.get_or_create(name="Eggs size M", amount=10.0, unit="pcs", category=eggs)[0]
ProductVariant.objects.get_or_create(name="Tesco Čerstvá vejce M 10 ks", price=69.9, supermarket=tesco, generic_product=eggs_size_m, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Čerstvá vejce od Kunína podestýlková M", price=79.9, supermarket=tesco, generic_product=eggs_size_m, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Albert Vejce z podestýlky, vel. M", price=79.9, supermarket=albert, generic_product=eggs_size_m, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="BILLA Premium Čerstvá vejce slepic ve volném výběhu M", price=89.9, supermarket=billa, generic_product=eggs_size_m, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Podestýlková vejce Srdce domova M", price=79.9, supermarket=billa, generic_product=eggs_size_m, last_updated=make_aware(datetime.now()))

# Rohlik
rohlik = GenericProduct.objects.get_or_create(name="Rohlik", amount=1.0, unit="pcs", category=bakery)[0]
ProductVariant.objects.get_or_create(name="Rohlík", price=2.9, supermarket=albert, generic_product=rohlik, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Rohlík", price=2.9, supermarket=billa, generic_product=rohlik, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Rohlík tukový", price=2.8, supermarket=tesco, generic_product=rohlik, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Rohlík staročeský", price=3.5, supermarket=tesco, generic_product=rohlik, last_updated=make_aware(datetime.now()))

# Okurka
okurka = GenericProduct.objects.get_or_create(name="Okurka", amount=1.0, unit="pcs", category=vegetables)[0]
ProductVariant.objects.get_or_create(name="Okurka hadovka", price=19.9, supermarket=albert, generic_product=okurka, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Bio Okurka Nature's Promise", price=34.9, supermarket=albert, generic_product=okurka, last_updated=make_aware(datetime.now()))

ProductVariant.objects.get_or_create(name="Tesco Okurka hadovka", price=14.9, supermarket=tesco, generic_product=okurka, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Okurka salátová", price=24.9, supermarket=billa, generic_product=okurka, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Česká farma okurka salátová", price=27.9, supermarket=billa, generic_product=okurka, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Bon Via Bio Okurka", price=36.9, supermarket=billa, generic_product=okurka, last_updated=make_aware(datetime.now()))

# Toast bread white
toast_bread_white = GenericProduct.objects.get_or_create(name="Toast bread white", amount=500.0, unit="g", category=bakery)[0]
ProductVariant.objects.get_or_create(name="BILLA Toustový chléb máslový", price=31.9, supermarket=billa, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="BILLA Toustový chléb světlý", price=29.9, supermarket=billa, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Chléb toustový světlý", price=33.9, supermarket=billa, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Ölz Pšeničný toustový chléb", price=51.9, supermarket=billa, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Baker Street – Toustový chléb", price=59.9, supermarket=billa, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tesco Toustový chléb světlý", price=29.9, supermarket=tesco, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Tesco Toustový chléb máslový", price=31.9, supermarket=tesco, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Ölz Pšeničný toustový chléb", price=51.9, supermarket=tesco, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Penam Toust světlý", price=33.9, supermarket=tesco, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Albert Toustový chléb světlý, balený", price=29.9, supermarket=albert, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Penam Toustový chléb světlý", price=34.9, supermarket=albert, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
ProductVariant.objects.get_or_create(name="Albert Toustový chléb máslový, balený", price=31.9, supermarket=albert, generic_product=toast_bread_white, last_updated=make_aware(datetime.now()))
