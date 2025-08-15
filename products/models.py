from django.db import models

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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