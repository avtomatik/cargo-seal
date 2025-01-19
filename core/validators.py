#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:45:18 2025

@author: alexandermikhailov
"""

from django.core.exceptions import ValidationError


class IMOValidator:
    """TODO: Implement."""

    def __call__(self, value):
        if not value:
            raise ValidationError('Not A Valid IMO-Number.')


def is_valid_imo(imo: str) -> bool:
    """
    Checks If Valid IMO Number

    Parameters
    ----------
    imo : str
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """
    return sum(
        map(lambda _: _[0] * int(_[1]), enumerate(imo[::-1][1:], start=2))
    ) % 10 == int(imo[-1])
