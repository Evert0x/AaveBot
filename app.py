import os
os.environ["TOTALITY_ENDPOINT"] = "http://localhost:5000"
from tg import main
import threading,settings
import sys

if __name__ == '__main__':
    main()
