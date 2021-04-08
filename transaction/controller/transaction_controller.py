import traceback
from transaction.repository.transaction_repository import TransactionRepository

from utils.app_logger import AppLogger

logger = AppLogger(tag='Transaction Controller')

transaction_repository = TransactionRepository()

class TransactionController(object):

    @staticmethod
    def create_transaction_record(**kwargs):
        logger.info("Inside create transaction controller method")
        transaction ,err= transaction_repository.create_transaction_record(**kwargs)
        if err is not None:
            return None, err
        logger.info("Exiting create transaction controller method")
        return transaction,None

    @staticmethod
    def calculate_sum_of_linked_transactions(transaction_id):

        logger.info(f"Calculating sum of linked transaction with transaction id : {transaction_id}")
        total_sum = 0
        unique_parent_id = {transaction_id:True}
        print(unique_parent_id)
        parent_transaction_filters = {"id":transaction_id}
        parent_transaction,err = transaction_repository.get_transaction(**parent_transaction_filters)

        if err:
            return None,err

        total_sum = total_sum + parent_transaction.get("amount") if parent_transaction else 0

        if not parent_transaction:
            return total_sum,None

        child_transaction_filter = {"parent_id":parent_transaction.get("id")}
        child_transactions,err = transaction_repository.get_transaction_list(**child_transaction_filter)
        if err:
            return None,err

        while child_transactions:
            grand_child_transaction_ids = []
            for child_transaction in child_transactions:
                total_sum = total_sum + child_transaction.get("amount")
                if not unique_parent_id.get(child_transaction.get("id")):
                    grand_child_transaction_ids.append(child_transaction.get("id"))
                    unique_parent_id.update({child_transaction.get("id"):True})

            grand_child_transaction_list = []
            for key in grand_child_transaction_ids:
                print(key)
                grand_child_transaction_filter = {"parent_id":key}
                grand_child_transactions ,err= transaction_repository.get_transaction_list(**grand_child_transaction_filter)
                if err:
                    return None, err
                grand_child_transaction_list.extend(grand_child_transactions)
            child_transactions = grand_child_transaction_list #updating child transaction

        logger.info(f"Total sum of linked transaction with transaction id : {transaction_id} is :{total_sum}")
        return total_sum,None

    @staticmethod
    def get_transaction(**filters):
        logger.info("Inside get transaction controller method")
        transaction,err = transaction_repository.get_transaction(**filters)
        if err:
            return None,err
        return transaction,None

    @staticmethod
    def get_transaction_list(**filters):
        logger.info("Inside get transaction list controller method")
        transaction,err = transaction_repository.get_transaction_list(**filters)
        if err:
            return None,err
        return transaction,None