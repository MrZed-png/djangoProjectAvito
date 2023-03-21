ads = []
for ad in page_odj:
    ads.append({"id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url
                })

{
    "id": 21,
    "name": "Сибирская котята, 3 месяца",
    "price": 2500,
    "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
    "address": "",
    "is_published": true,
    "image": "/media/images/post1.jpg"
}

res = users.annatate(total_ads=Count('ad', filter=Q(ad__published=True)))