
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
        try:
            transaction,err = TransactionController.create_transaction_record(**create_transaction_dict)

            if transaction:
                code=0
                msg="ok"
            if err:
                code, msg = err[0],err[1]
                response = {"status": code, "message": msg}
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = {
                "status": "code",
                "message": msg,
            }

            logger.info("Response: %s" % response)

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {"status":Errors.DatabaseError.GENERIC_CREATE[0],"message":Errors.DatabaseError.GENERIC_CREATE[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        try:
            transaction_filter={"id":transaction_id}
            transaction,err = TransactionController.get_transaction(**transaction_filter)

            if err:
                code, msg = err[0],err[1]
                response = {"status": code, "message": msg}
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = {
                        "amount":transaction["amount"],
                        "parent_id":transaction["parent_id"],
                        "type":transaction["type"]
                        }

            logger.info("Response: %s" % response)

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {"status":Errors.DatabaseError.GENERIC_LIST[0],"message":Errors.DatabaseError.GENERIC_LIST[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListTransaction(APIView):

    def get(self, request, *args, **kwargs):
        logger.info("********** Inside Transaction List API By Type**********")
        logger.info("Request data: %s" % request.data)
        transaction_type = kwargs.get('type')

        code = None
        msg = None
        if not transaction_type:
            code, msg = Errors.Missing.TRANSACTION_ID_MISSING

        try:
            transaction_filter={"type":transaction_type}
            transaction_list,err = TransactionController.get_transaction_list(**transaction_filter)
            resp = []
            for transaction in transaction_list:
                resp.append(transaction["id"])
            if err:
                code, msg = err[0],err[1]
                response = {"status": code, "message": msg}
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = {"transactions":resp}

            logger.info("Response: %s" % response)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {"status":Errors.DatabaseError.GENERIC_LIST[0],"message":Errors.DatabaseError.GENERIC_LIST[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        try:
            total_sum , err = TransactionController.calculate_sum_of_linked_transactions(transaction_id=transaction_id)
            if err:
                code, msg = err[0],err[1]
                response = {"status": code, "message": msg}
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response ={"sum":total_sum}

            logger.info("Response: %s" % response)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {"status":Errors.Generic.GENERIC[0],"message":Errors.Generic.GENERIC[1]}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

transaction             = Transaction.as_view()
transaction_list        = ListTransaction.as_view()
related_transaction_sum = RelatedTransactionSum.as_view()


