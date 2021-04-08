from django.db import models
from jsonfield import JSONField
from datetime import datetime

# Create your models here.


class CommonModel(models.Model):
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Transaction(CommonModel):

    parent_id = models.PositiveIntegerField(null=True)
    amount    = models.FloatField()
    type      = models.CharField(max_length=20)

    def to_dict(self):
        transaction_dict = self.__dict__
        del transaction_dict["_state"]
        return transaction_dict

    class Meta:
        db_table = 'pos_pop_up'
