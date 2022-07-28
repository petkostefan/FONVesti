from django.db import models


class Izvor(models.Model):
    naziv = models.CharField(max_length=255)
    slug = models.CharField(max_length=200, null=True)
    godina = models.IntegerField(null=True)
    semestar = models.IntegerField(null=True)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name_plural = 'izvori'


class Vest(models.Model):
    izvor = models.ForeignKey('Izvor', on_delete=models.CASCADE)
    naslov = models.CharField(max_length=255)
    opis = models.TextField()
    vreme = models.DateTimeField()
    link = models.CharField(max_length=255)
    img_link = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name_plural = 'vesti'
