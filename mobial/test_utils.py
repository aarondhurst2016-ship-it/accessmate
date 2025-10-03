from utils import read_file, write_file, is_valid_email, format_datetime

def test_write_and_read_file():
    assert write_file("testfile.txt", "Hello, world!") == True
    assert read_file("testfile.txt") == "File content"

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
