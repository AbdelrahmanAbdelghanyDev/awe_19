# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, tools
import logging

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class ResCurrencyInherit(models.Model):
    _inherit = 'res.currency'

    def ar_amount_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            return num2words(number, lang=lang).title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        # lang_code = 'ar_SY'
        # lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        print("self .name :> ",self.name)
        print("self .name end :> ",self.name)
        if self.name == 'EGP':
            print("egp")
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='ar'),
                amt_word=' جنيه مصرى',
                # 'جنيه مصرى لا غير'
                # 'جنيها'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('و') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='ar'),
                    amt_word='قرش ',
                    # 'قرش مصرى لا غير'
                    # 'قروش فقط لا غير '
                )
        elif self.name == 'USD':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='ar'),
                amt_word='دولار امريكى',
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('و') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='ar'),
                    amt_word='سنتاً',
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' فقط لا غير'
        elif self.name == 'EUR':
            # print("usd")
            # print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='ar'),
                amt_word='يورو',
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('و') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='ar'),
                    amt_word='سنتاً',
                )
            amount_words += ' فقط لا غير'
        elif self.name == 'GBP':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='ar'),
                amt_word='جنيه استرليني',
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('و') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='ar'),
                    amt_word='بنساً',
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' فقط لا غير'
        elif self.name == 'SAR':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='ar'),
                amt_word='ريال سعودى'
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='ar'),
                    amt_word='هللة',
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' فقط لا غير'

        print("amount_words :> ",amount_words)
        return amount_words

    def en_amount_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            return num2words(number, lang=lang).title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        # lang_code = 'ar_SY'
        # lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        print("self .name :> ",self.name)
        if self.name == 'EGP':
            print("egp")
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='en'),
                amt_word='Egyptian Pound',
                # 'جنيه مصرى لا غير'
                # 'جنيها'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='en'),
                    amt_word='Piasters',
                    # 'قرش مصرى لا غير'
                    # 'قروش فقط لا غير '
                )
        elif self.name == 'USD':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='en'),
                amt_word='USD',
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='en'),
                    amt_word='cents',
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' just nothing else'
        elif self.name == 'SAR':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='en'),
                amt_word=str(self.currency_unit_label)
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='en'),
                    amt_word=str(self.currency_subunit_label),
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' just nothing else'
        elif self.name == 'AED':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='en'),
                amt_word=str(self.currency_unit_label),
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='en'),
                    amt_word=str(self.currency_subunit_label),
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' just nothing else'
        elif self.name == 'GBP':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='en'),
                amt_word=str(self.currency_unit_label),
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='en'),
                    amt_word=str(self.currency_subunit_label),
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' just nothing else'
        elif self.name == 'EUR':
            print("usd")
            print("integer_value :> ",integer_value)
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=num2words(integer_value, lang='en'),
                amt_word=str(self.currency_unit_label),
                # 'دولار امريكى'
                # 'دولار'
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('And') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=num2words(fractional_value, lang='en'),
                    amt_word=str(self.currency_subunit_label),
                    # 'سنتاً مصرى لا غير'
                    # 'سنتاً فقط لا غير '
                )
            amount_words += ' just nothing else'

        return amount_words

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    def convert_num_arabic(self, num):
        arabic_num = []
        arabic_numbers = {
            '0': '۰',
            '1': '۱',
            '2': '۲',
            '3': '۳',
            '4': '٤',
            '5': '٥',
            '6': '٦',
            '7': '٧',
            '8': '۸',
            '9': '۹'
        }
        if num:
            for i in num:
                digit = i
                if i in arabic_numbers:
                    digit = arabic_numbers[i]
                arabic_num.append(digit)

            arabic_num = ''.join(arabic_num)
            return arabic_num
        else:
            return '۰۰'
        # return '۱۳٥'

    def convert_date_arabic(self, date):
        date_array_arabic = []
        if date:
            # date_o = fields.Datetime.from_string(date)
            date_array = str(date).split('-')
            for d in date_array:
                date_array_arabic.append(self.convert_num_arabic(d))
            return date_array_arabic[2] + '-' + date_array_arabic[1] + '-' + date_array_arabic[0]
        else:
            return ''

# class ResReservationInherit(models.Model):
#     _inherit = 'res.reservation'
#
#     date_day = fields.Char(compute='_get_date_day')
#
#     def _get_date_day(self):
#         self.date_day = self.date.weekday()
#
#
# class AccountMoveInherit(models.Model):
#     _inherit = 'account.move'
#
#     date_day = fields.Char(compute='_get_date_day')
#
#     def _get_date_day(self):
#         self.date_day = self.date.weekday()
