from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, db_index=True),
        slug = models.SlugField(max_length=200, db_index=True, unique=True)
    )
    class Meta:
        #ordering = ['name']
        #indexes = [
        #    models.Index(fields=['name'])
        #]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main_page:product_list_by_category',
                       args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200,
                              db_index=True),
        slug=models.SlugField(max_length=200,
                              db_index=True),
        description=models.TextField(blank=True)
    )
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        #ordering = ['name']
        indexes = [
            #models.Index(fields=['id', 'slug']),
            #models.Index(fields=['name']),
            models.Index(fields=['-created']),

        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main_page:product_detail',
                       args=[self.id, self.slug])


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
