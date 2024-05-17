import secrets

def generate_secret_key():
    secret_key = secrets.token_hex(16)
    return secret_key


