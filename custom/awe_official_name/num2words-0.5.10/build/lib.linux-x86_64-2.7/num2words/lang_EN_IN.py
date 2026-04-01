# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

from .lang_EN import Num2Word_EN
GENERIC_DOLLARS = ('dollar', 'dollars')
GENERIC_CENTS = ('cent', 'cents')


class Num2Word_EN_IN(Num2Word_EN):
    CURRENCY_FORMS = {
        'AUD': (GENERIC_DOLLARS, GENERIC_CENTS),
        'CAD': (GENERIC_DOLLARS, GENERIC_CENTS),
        # repalced by EUR
        'EEK': (('kroon', 'kroons'), ('sent', 'senti')),
        'EUR': (('euro', 'euro'), GENERIC_CENTS),
        'GBP': (('pound sterling', 'pounds sterling'), ('penny', 'pence')),
        # replaced by EUR
        'LTL': (('litas', 'litas'), GENERIC_CENTS),
        # replaced by EUR
        'LVL': (('lat', 'lats'), ('santim', 'santims')),
        'USD': (GENERIC_DOLLARS, GENERIC_CENTS),
        'RUB': (('rouble', 'roubles'), ('kopek', 'kopeks')),
        'SEK': (('krona', 'kronor'), ('öre', 'öre')),
        'NOK': (('krone', 'kroner'), ('øre', 'øre')),
        'PLN': (('zloty', 'zlotys', 'zlotu'), ('grosz', 'groszy')),
        'MXN': (('peso', 'pesos'), GENERIC_CENTS),
        'RON': (('leu', 'lei'), ('ban', 'bani')),
        'INR': (('rupee', 'rupees'), ('paisa', 'paise')),
        'EGP': (('pound', 'pounds'), ('piastre', 'piastres')),

    }

    CURRENCY_ADJECTIVES = {
        'AUD': 'Australian',
        'CAD': 'Canadian',
        'EEK': 'Estonian',
        'USD': 'US',
        'RUB': 'Russian',
        'NOK': 'Norwegian',
        'MXN': 'Mexican',
        'RON': 'Romanian',
        'INR': 'Indian',
        'EGP': 'Egypt',
    }

    def set_high_numwords(self, high):
        self.cards[10 ** 7] = "crore"
        self.cards[10 ** 5] = "lakh"
