from django.test import TestCase
from transaction.controller.transaction_controller import TransactionController
# Create your tests here.


class TransactionTest(TestCase):

    def test_create_transaction_without_parent(self):
        """Create a transaction record without parent"""
        transaction_details={
                                "id" : 8,
                                "amount" :11,
                                "type":'debit'
                            }

        transaction,err = TransactionController.create_transaction_record(**transaction_details)

        self.assertEqual(transaction_details.get("id"),transaction.get("id"))

    def test_create_transaction_with_parent(self):
        """Create a transaction record with parent"""
        parent_transaction_details = {
            "id": 1,
            "amount": 12,
            "type": 'debit'
        }

        parent_transaction, err = TransactionController.create_transaction_record(**parent_transaction_details)

        transaction_details={
                                "id" : 9,
                                "amount" :12,
                                "type":'debit',
                                "parent_id":1
                            }

        transaction,err = TransactionController.create_transaction_record(**transaction_details)

        self.assertEqual(parent_transaction.get("id"),transaction.get("parent_id"))

    def test_get_transaction(self):
        transaction_details = {
            "id": 15,
            "amount": 12,
            "type": 'debit'
        }
        transaction, err = TransactionController.create_transaction_record(**transaction_details)
        transaction,err = TransactionController.get_transaction(**transaction_details)
        self.assertEqual(transaction_details.get("id"), transaction.get("id"))


    def test_get_transaction_list(self):
        first_transaction_details = {
            "id": 20,
            "amount": 11,
            "type": 'debit'
        }
        first_transaction, err = TransactionController.create_transaction_record(**first_transaction_details)
        second_transaction_details = {
            "id": 21,
            "amount": 12,
            "type": 'debit',
            "parent_id":20
         }

        second_transaction,err = TransactionController.create_transaction_record(**second_transaction_details)

        third_transaction_details = {
            "id": 22,
            "amount": 100,
            "type": 'credit',
            "parent_id": 21
        }

        third_transaction,err = TransactionController.create_transaction_record(**third_transaction_details)

        transaction_filter = {"type":"debit"}
        transaction_list, err = TransactionController.get_transaction_list(**transaction_filter)

        self.assertEqual(len(transaction_list), 2)

    def test_calculate_sum_of_linked_transaction(self):
        first_transaction_details = {
            "id": 9,
            "amount": 11,
            "type": 'debit'
        }
        first_transaction, err = TransactionController.create_transaction_record(**first_transaction_details)
        second_transaction_details = {
            "id": 10,
            "amount": 12,
            "type": 'debit',
            "parent_id":9
         }

        second_transaction,err = TransactionController.create_transaction_record(**second_transaction_details)

        third_transaction_details = {
            "id": 11,
            "amount": 100,
            "type": 'credit',
            "parent_id": 10
        }

        third_transaction,err = TransactionController.create_transaction_record(**third_transaction_details)

        forth_transaction_details = {
            "id": 12,
            "amount": 100,
            "type": 'credit',
            "parent_id": None
        }

        forth_transaction, err = TransactionController.create_transaction_record(**forth_transaction_details)


        total_amount, err = TransactionController.calculate_sum_of_linked_transactions(transaction_id=9)
        actual_total_amount = first_transaction_details.get("amount")+second_transaction_details.get("amount")+third_transaction_details.get("amount")
        self.assertEqual(total_amount, actual_total_amount)

    def test_calculate_sum_of_linked_transaction_with_no_transaction(self):

        total_amount, err = TransactionController.calculate_sum_of_linked_transactions(transaction_id=22)

        self.assertEqual(total_amount, 0)
