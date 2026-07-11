"""Generate ADMIN_PASSWORD_HASH for .env

Usage:
  python hash_password.py "your-password"
"""

import sys

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python hash_password.py "your-password"')
    print(pwd_context.hash(sys.argv[1]))


if __name__ == "__main__":
    main()
