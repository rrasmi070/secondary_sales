from django.test import TestCase

# Create your tests here.

# forgot password test case======================
import string
from random import randrange
import secrets
num = randrange(8, 15)
res = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)for x in range(num))
print(res)