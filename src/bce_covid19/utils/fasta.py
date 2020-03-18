import os
from typing import Set, Iterator, List

from Bio import SeqRecord, SeqIO


def parse_fasta(data_path: str, file_name: str) -> Iterator[SeqRecord.SeqRecord]:
    """

    Args:
        data_path: the path to parse the fasta file
        file_name: the fasta file name to load parse.

    Returns: Iterator, yields one sequence at a time.

    """
    with open(os.path.join(data_path, file_name), "rU") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            yield record


def remove_fasta_files(fasta_ids: Set[str], fasta_path: str) -> None:
    """
    Removes the unused protein fasta files from the disc.

     Args:
        fasta_ids: the fasta ids to delete
        fasta_path: the dir where the fasta ids are saved in.

    """
    for fasta_id in fasta_ids:
        try:
            os.remove(os.path.join(fasta_path, f"{fasta_id}.fasta"))
        except FileNotFoundError:
            pass


def save_fasta_file(fasta_id: str, fasta_rec: List[SeqRecord.SeqRecord], fasta_path: str) -> None:
    """
    Save the fasta sequence on disc.

    Args:
        fasta_rec: the fasta sequence record list.
        fasta_id: the protein ID of the sequence.
        fasta_path: the dir where the fasta ids are saved in.

    """
    SeqIO.write(sequences=fasta_rec, handle=os.path.join(fasta_path, f"{fasta_id}.fasta"),
                format="fasta")
