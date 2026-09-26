import secrets
import base64

def generate_secret_key():
    # Generate 32 random bytes
    random_bytes = secrets.token_bytes(32)
    # Convert to base64 string
    secret_key = base64.b64encode(random_bytes).decode('utf-8')
    return secret_key

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("\nAdd this to your .env file:")
    print(f"JWT_SECRET_KEY={secret_key}")
    print("\nOr run this command:")
    print(f'echo "JWT_SECRET_KEY={secret_key}" >> .env') 