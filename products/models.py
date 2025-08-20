from django.db import models


# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Slider(TimeStamp):
    slide_1 = models.ImageField(upload_to='media/')
    slide_2 = models.ImageField(upload_to='media/')
    slide_3 = models.ImageField(upload_to='media/')


class Category(TimeStamp):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.is_active:
            return 'Active'
        else:
            return 'InActive'

    def delete_category(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


LABEL_CHOICES = (
    ('B', 'Best Seller'),
    ('S', 'Sale'),
    ('N', 'New'),
    ('T', 'Top Rate'),
)


class Product(TimeStamp):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/', null=True)
    side_image_1 = models.ImageField(upload_to='media/', blank=True, null=True)
    side_image_2 = models.ImageField(upload_to='media/', blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.is_active:
            return 'Active'
        else:
            return 'InActive'

    def delete_product(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
