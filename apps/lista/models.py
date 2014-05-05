# coding=utf-8
from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=45, verbose_name='imię')
    surname = models.CharField(max_length=45, verbose_name='nazwisko')
    degree = models.CharField(max_length=45, verbose_name='tytuł naukowy')
    faculty = models.CharField(max_length=45, null=True, blank=True, verbose_name='wydział')

    class Meta:
        verbose_name = 'Nauczyciel'
        verbose_name_plural = 'Nauczyciele'

    def __unicode__(self):
        return self.name+" "+self.surname
