from base.exceptions import SeazoneAPIException


class CheckinLaterThanCheckoutException(SeazoneAPIException):
    def __init__(self):
        super().__init__(
            detail="A data de Check-in não pode ser maior ou igual a data de Check-out.",
            codigo="checkin_later_than_checkout"
        )


class ExceedGuestLimitException(SeazoneAPIException):
    def __init__(self, limite):
        super().__init__(
            detail=f"O número de hóspedes excede o limite: {limite}",
            codigo="exceed_guest_limit"
        )


class OverlappingBookingException(SeazoneAPIException):
    def __init__(self):
        super().__init__(
            detail="Já existe uma reserva para essas datas neste imóvel.",
            codigo="overlap"
        )
