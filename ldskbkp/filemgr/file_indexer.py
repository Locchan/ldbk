import datetime
import mimetypes
import os
from alive_progress import alive_bar
import hashlib

from __main__ import logger, run_uuid
from ldskbkp.conf.config import FILEMGR_HASH_READ_CHUNK_SIZE, IGNORED_FILES, GIBIBYTE, MEBIBYTE
from ldskbkp.database.connection import get_transaction
from ldskbkp.database.models import File

indexing_start_time = None
total_size = 0
last_filesize = 0
bytes_left = 0


def get_files(dirpath, root):
    subfolders, files = [], []
    for f in os.scandir(dirpath):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            file_path = f.path.replace(root+"/", "")
            if file_path not in IGNORED_FILES:
                files.append(file_path)
    for dirpath in list(subfolders):
        f = get_files(dirpath, root)
        files.extend(f)
    return files


def calculate_hash(filepath):
    global total_size, bytes_left, last_filesize
    sha256 = hashlib.sha256()
    filesize = os.stat(filepath).st_size
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(FILEMGR_HASH_READ_CHUNK_SIZE)
            if not data:
                break
            sha256.update(data)
    sha_hash = sha256.hexdigest()
    bytes_left -= filesize
    last_filesize = filesize
    return sha_hash


def register_files(dirpath):
    global total_size, bytes_left, indexing_start_time
    files_new = []
    files_changed = []
    files_deleted = []
    errors = []
    logger.debug("Registering files...")
    files = get_files(dirpath, dirpath)
    files_len = len(files)
    for afile in files:
        total_size += os.stat(afile).st_size
    logger.info("There's {} files. Total size: {:.2f}GiB".format(files_len, total_size / GIBIBYTE))
    bytes_left = total_size
    session, session_transaction = get_transaction()
    with session_transaction:
        files_in_database = session.query(File).all()
        files_in_database_names = set([x.path for x in files_in_database])
        for afile in files_in_database_names:
            if afile not in files:
                files_deleted.append(files_deleted)
        indexing_start_time = datetime.datetime.now()
        with alive_bar(int(total_size / MEBIBYTE), force_tty=True, spinner=None, refresh_secs=1) as bar:
            for ind, afile in enumerate(files):
                try:
                    has_to_be_added = True
                    new_file = True
                    fullpath = os.path.join(dirpath, afile)
                    if not os.access(fullpath, os.R_OK):
                        errors.append((afile, "Access denied"))
                        continue
                    logger.debug("Registering {}".format(fullpath))
                    stat = os.stat(fullpath)
                    size = stat.st_size
                    mime_type = ";".join(str(x) for x in mimetypes.guess_type(fullpath) if x is not None)
                    created_on = datetime.datetime.fromtimestamp(stat.st_ctime)
                    modified_on = datetime.datetime.fromtimestamp(stat.st_mtime)
                    sha256 = calculate_hash(fullpath)
                    logger.debug("Registered. SIZE: {}; MIME: {}; CREATED: {}; MODIFIED: {}; SHA256: {}"
                                 .format(size, mime_type, created_on, modified_on, sha256))
                    # If a file is already in database, add it only if hash does not match
                    for afileindb in files_in_database:
                        if afileindb.path == afile:
                            new_file = False
                            if afileindb.sha256 == sha256:
                                logger.debug("File {} is already in the database.".format(afile))
                                has_to_be_added = False
                                break
                            else:
                                files_changed.append(afile)
                    if new_file:
                        files_new.append(afile)
                    if has_to_be_added:
                        session.add(File(path=afile, size=size, sha256=sha256, mime=mime_type, backed_up=False,
                                         created_on=created_on, modified_on=modified_on, ldbk_run_uuid=run_uuid))
                except Exception as e:
                    errors.append((afile, e.__class__.__name__))
                if ind + 1 == files_len:
                    bar(int(total_size / MEBIBYTE) - bar.current())
                else:
                    bar()
            return files_new, files_changed, files_deleted, errors
