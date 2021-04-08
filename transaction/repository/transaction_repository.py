import traceback

from transaction.models import *
from utils.app_logger import AppLogger
from utils.config import Errors

logger = AppLogger(tag='Transaction Repository')

class TransactionRepository(object):

    @staticmethod
    def create_transaction_record(**kwargs):
        try:
            logger.info(f"Creating Transaction with : {kwargs}")
            transaction = Transaction.objects.create(**kwargs)
            logger.info(f"Transaction Created Successfully.")
            return transaction.to_dict(), None
        except Exception as e:
            logger.debug(traceback.format_exc(e))
            return None, Errors.Database.GENERIC_CREATE

    @staticmethod
    def get_transaction(**filters):
        try:
            logger.info(f"Fetching Transaction with filters: {filters}")
            transaction = Transaction.objects.filter(**filters).first()
            transaction = transaction.to_dict() if transaction else None
            logger.info(f"Transaction : {transaction}")
            return transaction, None
        except Exception as e:
            logger.debug(traceback.format_exc(e))
            return None, Errors.Database.GENERIC_LIST

    @staticmethod
    def get_transaction_list(**filters):
        try:
            logger.info(f"Fetching Transaction list with filters: {filters}")
            transactions = Transaction.objects.filter(**filters)
            transaction_list =[]
            for transaction in transactions:
                transaction_list.append(transaction.to_dict())
            logger.info(f"Transactions : {transaction_list}")
            return transaction_list, None
        except Exception as e:
            logger.debug(traceback.format_exc(e))
            return None, Errors.Database.GENERIC_LIST