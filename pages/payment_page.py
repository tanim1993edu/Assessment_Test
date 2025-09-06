"""
Page object for the payment form used to complete an order.

On this page the user inputs credit card information and submits the
payment. Successful submission will redirect to the order confirmation
page. The selectors used here are based on common input names for card
details. They may need adjusting if the site uses different markup.
"""

from __future__ import annotations

import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


class PaymentPage(BasePage):
    """Encapsulates interactions with the payment form."""

    NAME_ON_CARD = "input[name='name_on_card']"
    CARD_NUMBER = "input[name='card_number']"
    CVC = "input[name='cvc']"
    EXPIRY_MONTH = "input[name='expiry_month']"
    EXPIRY_YEAR = "input[name='expiry_year']"
    PAY_AND_CONFIRM_BUTTON = "button#submit"  # guess: id submit

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def enter_payment_details(
        self,
        name_on_card: str,
        card_number: str,
        cvc: str,
        expiry_month: str,
        expiry_year: str,
    ) -> None:
        """Fill in the payment form with credit card details."""
        self.logger.debug("Entering payment information")
        self.fill(self.NAME_ON_CARD, name_on_card)
        self.fill(self.CARD_NUMBER, card_number)
        self.fill(self.CVC, cvc)
        self.fill(self.EXPIRY_MONTH, expiry_month)
        self.fill(self.EXPIRY_YEAR, expiry_year)

    def submit_payment(self) -> None:
        """Click the button to pay and confirm the order."""
        self.logger.info("Submitting payment and confirming the order")
        self.click(self.PAY_AND_CONFIRM_BUTTON)
