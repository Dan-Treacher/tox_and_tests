# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pytest
from src.functions import square, root


def test_square_function():
    # When
    subject = square(4)

    # Then
    assert subject == 16
    assert isinstance(subject, int)


def test_root_function():
    # When
    subject = root(16)

    # Then
    assert subject == 4
    assert isinstance(subject, float)
