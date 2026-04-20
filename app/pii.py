from __future__ import annotations

import hashlib
import re

PII_PATTERNS: dict[str, str] = {
    # 1. Liên hệ (Emails kể cả khi viết chữ "at" "dot" & SĐT cắt vụn)
    "email": r"(?i)[\w\.-]+(?:\s*@\s*|\s+at\s+)[\w\.-]+(?:\s*\.\s*|\s+dot\s+)\w+",
    "phone_vn": r"(?:\+84|0)(?:[ \.\-]*\d){9}\b",
    
    # 2. Định danh nhà nước
    "cccd": r"\b\d{12}\b",
    "passport": r"\b[A-Z]{1,2}\d{6,8}\b",
    
    # 3. Địa chỉ
    "address_vn": r"(?i)\b(Hà Nội|HN|TP\.HCM|HCM|Hồ Chí Minh|Đà Nẵng|Hải Phòng|Cần Thơ)\b",
    
    # 4. Thông tin Tài chính
    "credit_card": r"\b\d{4}[ \-]?\d{4}[ \-]?\d{4}[ \-]?\d{4}\b",
    "bank_account": r"(?i)(?:stk|số tài khoản|tài khoản|bank account|acc)\s*[:=]?\s*\d{8,15}",
    "currency_vn": r"(?i)(?:học phí|tiền|chi phí)\s*[:=]?\s*\d{1,3}(?:[.,]\d{3})*(?:\s*VND|\s*VNĐ|\s*đồng)?",
    
    # 5. Thông tin Trường học Đặc thù (Tên, Mã HS, Lớp, Ngày sinh)
    "student_id": r"(?i)\b(?:VS|VSC|VINS|HS)[ \-_]?\d{4,8}\b",
    "dob": r"(?i)\b(?:sinh ngày|sinh ngay|sn|dob|ngày sinh|ngay sinh)\s*[:=]?\s*\d{1,2}[\/\-\.]\d{1,2}[\/\-\.](?:\d{2}|\d{4})\b",
    "class_name": r"(?i)\b(?:lớp|lop|class)\s*(?:[1-9]|1[0-2])[a-zA-Z]\d{0,2}\b",
    # Name Heuristic: Bắt buộc từ tiếp theo phải viết hoa (Title Case) để tránh bắt nhầm chữ thường (vd: "mẹ đi chợ")
    "student_name": r"(?i)\b(?:bé|be|học sinh|hs|con|cháu|chau|phụ huynh|anh|chị|chi|mẹ|me|bố|bo)\s+(?-i:[A-ZĐ][a-zàáâãèéêìíòóôõùúăđĩũơạảấầẩẫậắằẳẵặẹẻẽềềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]*(?:\s+[A-ZĐ][a-zàáâãèéêìíòóôõùúăđĩũơạảấầẩẫậắằẳẵặẹẻẽềềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]*)*)\b",
    
    # 6. Thông tin Hệ thống
    "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
}


def scrub_text(text: str) -> str:
    safe = text
    for name, pattern in PII_PATTERNS.items():
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def summarize_text(text: str, max_len: int = 80) -> str:
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_id(id: str) -> str:
    return hashlib.sha256(id.encode("utf-8")).hexdigest()[:12]
