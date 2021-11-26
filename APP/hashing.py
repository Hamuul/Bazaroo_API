from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify_password(plain_pass: str, hashed_pass: str):
        return pwd_context.verify(plain_pass, hashed_pass)
