import phonenumbers
import secrets
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(email):
    return not not EMAIL_REGEX.match(email)

def is_valid_phone(phone):
    return phonenumbers.is_valid_number(phonenumbers.parse(phone, "CA"))

def format_phone(phone):
    return phonenumbers.format_number(phonenumbers.parse(phone, "CA"), phonenumbers.PhoneNumberFormat.INTERNATIONAL)

def generate_unique_hash(all_hashes):
    hash = secrets.token_hex(128)

    while hash in all_hashes:
        hash = secrets.token_hex(128)
    
    return hash