"""
Author: Peiqi Wang
Course: CST8002 Practical Project 2
Professor: Tyler DeLay
Due Date: 2025-02-16
Description: This module defines the Record class, which represents a data entity.
"""

class Record:
    """
    Represents a single record in the dataset.
    """
    def __init__(self, csduid, csd, period, description, unit, value):
        """
        Initializes a new instance of the Record class.
        """
        self.csduid = csduid
        self.csd = csd
        self.period = period
        self.description = description
        self.unit = unit
        self.value = value

    def __str__(self):
        """
        Returns and output a string format of the Record object.
        """
        return f"{self.csduid}: {self.csd} - {self.period} - {self.description} - {self.unit} - {self.value}"