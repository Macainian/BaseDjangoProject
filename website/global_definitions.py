SUPERUSER_MEMBER_ID = 1

BANNED_USERNAMES = []


class StatusCodes:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501


class EmailBatchTypeNames:
    FORGOT_PASSWORD = "Forgot Password"
    FORGOT_USERNAME = "Forgot Username"
    NEW_STAFF_MEMBER_INVITATION = "New Staff Member Invitation"
    NEW_USER_REGISTRATION = "New User Registration"


class EmailBatchStatusNames:
    EMAIL_BATCH_FAILED = "Email Batch Failed"
    EMAIL_BATCH_PARTIALLY_SENT = "Email Batch Sent Partially"
    PENDING_EMAIL_BATCH_SEND = "Pending Email Batch Send"
    EMAIL_BATCH_SENT_COMPLETELY = "Email Batch Sent Completely"


class EmailBatchTemplateNames:
    FORGOT_PASSWORD = "Forgot Password"
    FORGOT_USERNAME = "Forgot Username"
    NEW_STAFF_MEMBER_INVITATION = "New Staff Member Invitation"


class EmailInstanceStatusNames:
    EMAIL_INSTANCE_ACTION_TAKEN = "Email Instance Action Taken"
    EMAIL_INSTANCE_FAILED = "Email Instance Failed"
    EMAIL_INSTANCE_LINK_CLICKED = "Email Instance Link Clicked"
    EMAIL_INSTANCE_OPENED = "Email Instance Opened"
    EMAIL_INSTANCE_SENT = "Email Instance Sent"
    PENDING_EMAIL_INSTANCE_SEND = "Pending Email Instance Send"


class ServerType:
    DEV = "dev"
    QA = "qa"
    PROD = "prod"
