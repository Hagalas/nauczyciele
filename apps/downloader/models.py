from django.db import models
from optparse import _


class File(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(verbose_name=_('File'), upload_to='latest')
    addition_time = models.DateTimeField(verbose_name=_('Date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Plik')
        verbose_name_plural = _('Pliki')

    def __unicode__(self):
        return self.file_name