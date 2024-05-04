DATABASE_URL = "postgresql://ghostchinchilla:new_password@localhost/yumhub_db"
SECRET_KEY = "''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))"