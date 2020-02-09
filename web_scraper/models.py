from django.db import models

# Create your models here.


class HmTable(models.Model):
    title = models.CharField(max_length=200)
    item_link = models.CharField(max_length=200)
    image_source = models.CharField(max_length=300)
    regular_price = models.FloatField()
    sale_price = models.FloatField()
    update_time = models.DateTimeField('updated at')

    def __str__(self):
        return self.title
