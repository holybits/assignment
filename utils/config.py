class Errors:
    # PAGE_NOT_FOUND = (6001, "Requested page does not exists")
    # UNAUTHORIZED = (6002, "Unauthorized")
    # PERMISSION_DENIED = (6003, "Permission Denied")

    class Validation:
        TRANSACTION_ID_INVALID          = (1000, "Transaction id is not valid")
        TRANSACTION_TYPE_INVALID        = (1001, "Transaction type is not valid")
        TRANSACTION_AMOUNT_INVALID      = (1000, "Transaction amount is not valid")


    class NotFound:
        TRANSACTION_NOT_FOUND                = (2001,"Transaction Not Found.")
        PARENT_TRANSACTION_NOT_FOUND         = (2002,"Parent Transaction Not Found With Given Parent ID.")


    class DatabaseError:
        GENERIC_CREATE      = (3001, "Some error occurred while creating this entity")
        GENERIC_UPDATE      = (3002, "Some error occurred while updating this entity")
        BULK_CREATE         = (3003, "Some error occurred while creating bulk entities")
        GENERIC_PATCH       = (3004, "Some error occurred while updating partially this entity")
        GENERIC_LIST        = (3005, "Some error occurred while listing this entity")


    class Missing:
        TRANSACTION_ID_MISSING      = (5001, "Transaction ID is missing.")
        TRANSACTION_AMOUNT_MISSING  = (5002, "Transaction Amount is missing.")
        TRANSACTION_TYPE_MISSING    = (5003, "Transaction Type is missing.")

    class Generic:
        GENERIC =(7001,"Oops something went wrong.")