from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = "your-secret-key"
email = "test@example.com"

serializer = URLSafeTimedSerializer(SECRET_KEY)
token = serializer.dumps(email, salt="password-reset-salt")
print("Generated token:", token)

# Simulate decoding
decoded_email = serializer.loads(token, salt="password-reset-salt")
print("Decoded email:", decoded_email)
