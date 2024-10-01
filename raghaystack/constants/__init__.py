import os
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

DOCUMENT_STORE_PATH = os.path.join("artifacts", f"{TIMESTAMP}")
DOCUMENT_STORE_NAME = "document_store.json"
