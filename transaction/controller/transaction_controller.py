import traceback
from transaction.repository.transaction_repository import TransactionRepository

from utils.app_logger import AppLogger
from utils.config import Errors
logger = AppLogger(tag='Transaction Controller')

transaction_repository = TransactionRepository()


class TransactionController(object):

    @staticmethod
    def create_transaction_record(**kwargs):
        try:
            logger.info("Inside create transaction controller method")
            parent_id = kwargs.get("parent_id")
            if parent_id:
                filter = {"id":parent_id}
                transaction,err = transaction_repository.get_transaction(**filter)
                if not transaction:
                    return  None,Errors.NotFound.PARENT_TRANSACTION_NOT_FOUND

            transaction ,err= transaction_repository.create_transaction_record(**kwargs)
            if err is not None:
                return None, err
            logger.info("Exiting create transaction controller method")
            return transaction,None
        except Exception as e:
            raise e


    @staticmethod
    def calculate_sum_of_linked_transactions(transaction_id):
        try:
            logger.info(f"Calculating sum of linked transaction with transaction id : {transaction_id}")
            total_amount = 0

            parent_transaction_filters = {"id":transaction_id}
            parent_transaction,err = TransactionController.get_transaction(**parent_transaction_filters)

            if err:
                return None,err

            total_amount = total_amount + parent_transaction.get("amount") if parent_transaction else 0

            if not parent_transaction:
                return total_amount, None
            total_descendant_amount,err= TransactionController.calculate_sum_of_all_descendant_transaction(parent_id=transaction_id)
            if err:
                return None,err
            total_amount = total_amount + total_descendant_amount
            logger.info(f"Total sum of linked transaction with transaction id : {transaction_id} is :{total_amount}")
            return total_amount, None
        except Exception as e:
            raise e



    @staticmethod
    def calculate_sum_of_all_descendant_transaction(parent_id):
        try:
            logger.info(f"Calculating sum of descendant transaction with transaction id : {parent_id}")
            total_amount = 0
            unique_ancestor_id = {parent_id: True}
            child_transaction_filter = {"parent_id":parent_id}
            child_transactions,err = TransactionController.get_transaction_list(**child_transaction_filter)
            if err:
                return None,err

            while child_transactions:
                grand_child_transaction_ids = []
                for child_transaction in child_transactions:
                    total_amount = total_amount + child_transaction.get("amount")
                    if not unique_ancestor_id.get(child_transaction.get("id")):
                        grand_child_transaction_ids.append(child_transaction.get("id"))
                        unique_ancestor_id.update({child_transaction.get("id"):True})

                grand_child_transaction_list = []
                for key in grand_child_transaction_ids:
                    grand_child_transaction_filter = {"parent_id":key}
                    grand_child_transactions ,err= TransactionController.get_transaction_list(**grand_child_transaction_filter)
                    if err:
                        return None, err
                    grand_child_transaction_list.extend(grand_child_transactions)
                child_transactions = grand_child_transaction_list #updating child transaction

            logger.info(f"Total sum of linked transaction with descendant id : {parent_id} is :{total_amount}")
            return total_amount, None
        except Exception as e:
            raise e


    @staticmethod
    def get_transaction(**filters):
        try:
            logger.info("Inside get transaction controller method")
            transaction,err = transaction_repository.get_transaction(**filters)
            if err:
                return None,err
            return transaction,None
        except Exception as e:
            raise e

    @staticmethod
    def get_transaction_list(**filters):
        try:
            logger.info("Inside get transaction list controller method")
            transaction,err = transaction_repository.get_transaction_list(**filters)
            if err:
                return None,err
            return transaction,None
        except Exception as e:
            raise e