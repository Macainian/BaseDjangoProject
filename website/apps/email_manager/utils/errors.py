class EmailsAreDisabledError(Exception):
    pass


class NoRecipientsError(Exception):
    pass


class TooManyRecipientsError(Exception):
    pass


class FailedToSendEmailError(Exception):
    pass


class MailServerIsDownError(Exception):
    pass
