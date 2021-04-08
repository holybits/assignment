
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from transaction.serializers.transaction import CreateTransactionSerializer,ListTransactionSerializer
from transaction.controller.transaction_controller import TransactionController

from utils.config import Errors
from utils.app_logger import AppLogger


logger = AppLogger(tag="RFID Views")


class Transaction(APIView):

    def put(self, request, *args, **kwargs):
        logger.info("********** Inside Transaction API **********")
        logger.info("Request data: %s" % request.data)

        transaction_id = kwargs.get('transaction_id')
        code= None
        msg = None
        if not transaction_id:
            code, msg = Errors.Missing.TRANSACTION_ID_MISSING
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        validation_check_response = CreateTransactionSerializer(
            data=request
        )
        validation_check_response.is_valid(raise_exception=True)

        create_transaction_dict = {
            "id":transaction_id,
            "amount":request.data["amount"],
            "parent_id":request.data.get("parent_id",None),
            "type":request.data["type"]

        }
        transaction,err = TransactionController.create_transaction_record(**create_transaction_dict)

        if transaction:
            code=0
            msg="ok"
        if err:
            code, msg = err[0],err[1]
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = {
            "status": code,
            "message": msg,
        }

        logger.info("Response: %s" % response)

        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        logger.info("********** Inside Transaction API **********")
        logger.info("Request data: %s" % request.data)
        transaction_id = kwargs.get('transaction_id')

        code = None
        msg = None
        if not transaction_id:
            code, msg = Errors.Missing.TRANSACTION_ID_MISSING
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        transaction_filter={"id":transaction_id}
        transaction,err = TransactionController.get_transaction(**transaction_filter)

        if err:
            code, msg = err[0],err[1]
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        del transaction['id']
        response = transaction

        logger.info("Response: %s" % response)

        return Response(response, status=status.HTTP_200_OK)


class ListTransaction(APIView):

    def get(self, request, *args, **kwargs):
        logger.info("********** Inside Transaction List API By Type**********")
        logger.info("Request data: %s" % request.data)
        transaction_type = kwargs.get('type')

        code = None
        msg = None
        if not transaction_type:
            code, msg = Errors.Missing.TRANSACTION_ID_MISSING
            error = True

        transaction_filter={"type":transaction_type}
        transaction_list,err = TransactionController.get_transaction_list(**transaction_filter)
        resp = []
        for transaction in transaction_list:
            del transaction['id']
            resp.append(transaction)
        if err:
            code, msg = err[0],err[1]
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = {"transactions":resp}

        logger.info("Response: %s" % response)

        return Response(response, status=status.HTTP_200_OK)


class RelatedTransactionSum(APIView):

    def get(self, request, *args, **kwargs):
        logger.info("****Inside Related Transaction Sum API *****")
        transaction_id = kwargs.get('transaction_id')

        code = None
        msg = None
        if not transaction_id:
            code, msg = Errors.Missing.TRANSACTION_ID_MISSING
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        total_sum , err = TransactionController.calculate_sum_of_linked_transactions(transaction_id=transaction_id)
        if err:
            code, msg = err[0],err[1]
            response = {"status": code, "message": msg}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response ={"sum":total_sum}

        logger.info("Response: %s" % response)

        return Response(response, status=status.HTTP_200_OK)

transaction             = Transaction.as_view()
transaction_list        = ListTransaction.as_view()
related_transaction_sum = RelatedTransactionSum.as_view()


