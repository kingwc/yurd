import sys
sys.path.append('../myapp')
import pytest
from src import main

def test_test():
    assert main.func(1) == 2
    