from django.db import models


class Product(models.Model):

    CATEGORIES = [
        ("none", "None"),
        ("men", "Men"),
        ("women", "Women"),
        ("kids", "Kids"),
        ("beauty", "Beauty"),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="none")
    price = models.IntegerField(default=0)
    score = models.SmallIntegerField(default=0)
    description = models.TextField()
    img_path = models.CharField()
    number = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
