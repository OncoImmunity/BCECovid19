import glob
import os
import re
import shutil
import subprocess
import tarfile
import zipfile


def gzip_decompress_folder(compressed_folder_path: str) -> None:
    """
    Function to decompress a tar.gz file.

    Decompress a specified file in a given directory. The compressed file will be deleted.

    Args:
        compressed_folder_path: the path to the compressed folder. It has to end with .tar.gz
    """

    with tarfile.open(compressed_folder_path, "r:gz") as tar_file:
        tar_file.extractall(path=os.path.dirname(compressed_folder_path))

    os.remove(compressed_folder_path)


def gzip_compress_folder(uncompressed_folder_path: str) -> None:
    """
    Function which compresses a folder with tar.gz

    The non-compressed folder will be deleted.

    Args:
        uncompressed_folder_path: the path to the uncompressed folder. It should NOT include the tar.gz suffix.
    """

    with tarfile.open(f"{uncompressed_folder_path}.tar.gz", "w:gz") as tar_file:
        tar_file.add(name=uncompressed_folder_path, arcname=os.path.basename(uncompressed_folder_path))

    shutil.rmtree(uncompressed_folder_path)


def zip_decompress_folder(compressed_folder_path: str) -> None:
    """
    Function to decompress a zip folder.

    Decompress a specified folder in a given directory. The compressed folder will be deleted.

    (Unittest in test folder)

    Args:
        compressed_folder_path: the path to the compressed folder. It has to end with .zip
    """
    folder_name = re.search(r"(.+).zip", os.path.basename(compressed_folder_path)).group(1)
    data_path = os.path.join(os.path.dirname(compressed_folder_path), folder_name)

    with zipfile.ZipFile(compressed_folder_path, "r") as zip_ref:
        zip_ref.extractall(path=data_path)

    os.remove(compressed_folder_path)


def split_targz_file(compressed_folder_path: str, chunk_size: int = 2000 * 1000 * 1000) -> None:
    """
    Split a big tar-gz file into chunks of size chunk_size.

    The main folder will be deleted.

    Args:
        compressed_folder_path: the path to the compressed folder. It has to end with tar.gz
        chunk_size: the size of the individual files. Default is 2G in bytes.

    """

    with open(compressed_folder_path, 'rb') as infile:
        for n, raw_bytes in enumerate(iter(lambda: infile.read(chunk_size), b'')):
            with open(f"{compressed_folder_path}.part_{n}", 'wb') as outfile:
                outfile.write(raw_bytes)

    os.remove(compressed_folder_path)


def ensemble_targz_files(compressed_chunks_file_path: str, compressed_folder_path: str) -> None:
    """
    Ensemble several chunks of files into one file.

    The chunks will be deleted.

    Args:
        compressed_chunks_file_path: path to the chunk files, should end with tar.gz.part_* to get all the files.
        compressed_folder_path: the path and name of the compressed file to create. Should end in tar.gz

    """

    subprocess.call(f"cat {compressed_chunks_file_path} > {compressed_folder_path}", shell=True,
                    cwd=os.path.dirname(compressed_folder_path))
    # delete
    for chunk_file in glob.glob(pathname=compressed_chunks_file_path):
        os.remove(chunk_file)
