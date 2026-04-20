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
