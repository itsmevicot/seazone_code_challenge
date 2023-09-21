from base.exceptions import SeazoneAPIException


class PastActivationDateException(SeazoneAPIException):
    def __init__(self):
        super().__init__(
            detail="A data de ativação não pode ser menor que a data atual.",
            codigo="past_activation_date"
        )
