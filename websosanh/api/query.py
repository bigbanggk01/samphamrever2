from itertools import product


class query:
    def insertProduct(name,price,url, imageLink, category_id):
        productInsert = "INSERT INTO public.api_product(name, price, url, \"imageLink\", category_id) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(name, price, url, imageLink, category_id)
        return productInsert