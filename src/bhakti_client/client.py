from bhakti import BhaktiClient
from bhakti.database import DBEngine

BHAKTI_SERVER = '127.0.0.1'
BHAKTI_PORT = 23860
EOF = b'<eof>'
TIMEOUT = 4.0
BUFFER_SIZE = 256
VERBOSE = True

bhakti_client = BhaktiClient(
    server=BHAKTI_SERVER,  # optional, default to 127.0.0.1
    port=BHAKTI_PORT,  # optional, default to 23860
    eof=EOF,  # optional, default to b'<eof>'
    timeout=TIMEOUT,  # optional, default to 4.0 seconds
    buffer_size=BUFFER_SIZE,  # optional, default to 256 bytes
    db_engine=DBEngine.DIPAMKARA,  # optional, default to dipamkara
    verbose=VERBOSE  # optional, default to false
)
