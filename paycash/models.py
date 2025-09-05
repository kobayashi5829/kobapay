from django.db import models
from accounts.models import CustomUser

class Deal(models.Model):
    DEAL_CHOICES = [
        ('C', 'Charge'),
        ('P', 'Pay'),
    ]

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    deal_type = models.CharField(verbose_name='取引タイプ', choices=DEAL_CHOICES)
    amount = models.IntegerField(verbose_name='金額', blank=False, null=False)
    content = models.TextField(verbose_name='内容', blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Deal'

    def __str__(self):
        return str(self.id)