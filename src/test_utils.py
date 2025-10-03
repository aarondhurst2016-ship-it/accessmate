# Tests for utils.py
from utils import read_file, write_file, is_valid_email, format_datetime
import os

def test_write_and_read_file():
    test_path = "testfile.txt"
    test_text = "Hello, world!"
    assert write_file(test_path, test_text) == True
    assert read_file(test_path) == test_text
    os.remove(test_path)

def test_is_valid_email():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("invalid-email") == False

def test_format_datetime():
    dt_str = format_datetime()
    assert isinstance(dt_str, str)
    assert len(dt_str) > 0

if __name__ == "__main__":
    test_write_and_read_file()
    test_is_valid_email()
    test_format_datetime()
    print("All utils tests passed.")
