from django.db import models

class EndUser(models.Model):    
    OFFICE_TYPE_CHOICES = [
        (1, 'Executives'),
        (2, 'Division'),
        (3, 'Section'),
        (4, 'Unit'),
        (5, 'Provincial')
    ]

    office_type = models.IntegerField(max_length=2, choices=OFFICE_TYPE_CHOICES, verbose_name='Office Type')
    office_name = models.CharField(max_length=255, blank=False, verbose_name='Office Name')

    def __str__(self):
        return self.office_name

    class Meta:
        ordering = ['office_type']