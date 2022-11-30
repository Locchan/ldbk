# Will read files in this-sized chunks when hashing
FILEMGR_HASH_READ_CHUNK_SIZE = 65536

KIBIBYTE = 1024
MEBIBYTE = KIBIBYTE * 1024
GIBIBYTE = MEBIBYTE * 1024

KILOBYTE = 1000
MEGABYTE = KILOBYTE * 1000
GIGABYTE = MEGABYTE * 1000

DB_CONFIG_KEYS = {
    "version": "ldbk_database_version"
}

LDBK_DATABASE_FILENAME = "ldbk.db"

IGNORED_FILES = [
    LDBK_DATABASE_FILENAME
]

CLI_YN_ANSWERS = {
    "positive": ["y", "yes"],
    "negative": ["n", "no"]
}

DISK_TYPES = {
    "DVD-R": 4692251770
}