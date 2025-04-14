#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:45:18 2025

@author: alexandermikhailov
"""

from django.core.exceptions import ValidationError


class IMOValidator:
    """TODO: Plug to `Vessel` Model."""

    def __call__(self, value):

        numbers = []

        for _ in range(7):
            value, number = divmod(value, 10)
            numbers.append(number)

        check_sum = sum(_ * number for _, number in enumerate(numbers[1:], 2))

        if check_sum % 10 != numbers[0]:
            raise ValidationError('Not A Valid IMO-Number.')
