import copy
import json
from datetime import datetime

from rest_framework import serializers

from utils.config import Errors
from utils.app_logger import AppLogger

logger = AppLogger(tag='Transaction Controller')


class CreateTransactionSerializer(serializers.BaseSerializer):

    def to_internal_value(self, request):
        logger.info("Validating the data call to serializer.")

        data = request.data

        transaction_id = data.get("transaction_id")
        amount         = data.get("amount")
        type           = data.get("type")

        error = False

        if not amount:
            code, msg = Errors.Missing.TRANSACTION_AMOUNT_MISSING
            error = True

        if not type:
            code, msg = Errors.Missing.TRANSACTION_TYPE_MISSING
            error = True

        if error:
            response = {"status": code, "message": msg}
            raise serializers.ValidationError(response)

        return data


class ListTransactionSerializer(serializers.BaseSerializer):

    def to_internal_value(self, request):
        logger.info("Validating the data call to serializer.")

        data = request.data

        transaction_id = data.get("transaction_id")

        error = False

        if not transaction_id:
            code, msg = Errors.Missing.TRANSACTION_ID_MISSING
            error = True

        if error:
            response = {"status": code, "message": msg}
            raise serializers.ValidationError(response)

        return data

