from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out

def test_scrub_phone() -> None:
    out = scrub_text("My phone is 0901234567")
    assert "0901234567" not in out
    assert "REDACTED_PHONE_VN" in out

def test_scrub_passport() -> None:
    out = scrub_text("Passport: B1234567")
    assert "B1234567" not in out
    assert "REDACTED_PASSPORT" in out

def test_scrub_address() -> None:
    out = scrub_text("I live in Hà Nội today.")
    assert "Hà Nội" not in out
    assert "REDACTED_ADDRESS_VN" in out

def test_scrub_deep_defense() -> None:
    out = scrub_text("Bé Nguyễn Văn A nộp học phí 10.000.000 VND vào stk 123456789. Mã học sinh VINS-2023 truy cập từ 192.168.1.1")
    assert "Nguyễn Văn A" not in out
    assert "REDACTED_STUDENT_NAME" in out

def test_scrub_edge_cases() -> None:
    # Shattered phone number & email with at/dot
    out = scrub_text("Gọi 090 . 12 34 . 567 hoặc mail tuan at gmail dot com")
    assert "090" not in out
    assert "tuan at" not in out
    assert "REDACTED_PHONE_VN" in out
    assert "REDACTED_EMAIL" in out

    # DOB and unaccented names
    out2 = scrub_text("be Han sinh ngay 12/05/2015, lop 10A1")
    assert "Han" not in out2
    assert "12/05/2015" not in out2
    assert "10A1" not in out2
    assert "REDACTED_STUDENT_NAME" in out2
    assert "REDACTED_DOB" in out2
    assert "REDACTED_CLASS_NAME" in out2

    # False positive test: ensure non-capitalized words are NOT redacted
    out3 = scrub_text("me la ai, bo quen tui")
    assert "me la ai" in out3 # Should NOT be redacted as a name because "la" is not TitleCase
