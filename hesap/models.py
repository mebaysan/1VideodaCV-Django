from django.db import models


class Hesap(models.Model):
    isim = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefon = models.CharField(max_length=255)
    unvan = models.CharField(max_length=255)
    ozet = models.TextField()
    resim = models.ImageField()

    def __str__(self):
        return self.isim
