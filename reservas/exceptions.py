from base.exceptions import SeazoneAPIException


class CheckinLaterThanCheckoutException(SeazoneAPIException):
    def __init__(self):
        super().__init__(
            detail="A data de Check-in não pode ser maior ou igual a data de Check-out.",
            codigo="checkin_later_than_checkout"
        )


class CheckoutEarlierThanCheckinException(SeazoneAPIException):
    def __init__(self):
        super().__init__(
            detail="A data de Check-out não pode ser menor ou igual a data de Check-in.",
            codigo="checkout_earlier_than_checkin"
        )


class ExceedGuestLimitException(SeazoneAPIException):
    def __init__(self, limite):
        super().__init__(
            detail=f"O número de hóspedes excede o limite de hóspedes: {limite}",
            codigo="exceed_guest_limit"
        )


class OverlappingBookingException(SeazoneAPIException):
    def __init__(self):
        super().__init__(
            detail="Já existe uma reserva para essas datas neste imóvel.",
            codigo="overlap"
        )
