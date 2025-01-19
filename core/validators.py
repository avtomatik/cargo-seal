#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:45:18 2025

@author: alexandermikhailov
"""

from operator import mul

from django.core.exceptions import ValidationError


class IMOValidator:

    def __call__(self, value):

        numbers = []

        for _ in range(7):
            value, number = divmod(value, 10)
            numbers.append(number)

        number = numbers.pop(0)

        if sum(map(mul, numbers, range(2, 8))) % 10 != number:
            raise ValidationError('Not A Valid IMO-Number.')
