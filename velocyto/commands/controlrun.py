import sys
import os
import glob
import re
import gzip
import click
import array
import loompy
import numpy as np
import random
import string
import csv
from collections import defaultdict
import logging
from typing import *
import velocyto as vcy
from ._controlrun import _controlrun

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def id_generator(size: int=6, chars: str=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


@click.command(short_help="Runs specific negative control tests for the velocity analysis")
@click.argument("bamfile",
                type=click.Path(exists=True,
                                file_okay=True,
                                dir_okay=False,
                                readable=True,
                                resolve_path=True))
@click.argument("gtffile",
                type=click.Path(exists=True,
                                file_okay=True,
                                dir_okay=False,
                                readable=True,
                                resolve_path=True))
@click.option("--bcfile", "-b",
              help="""Valid barcodes file, to filter the bam. If --bcfile is not specified all the cell barcodes will be incuded.
              Cell barcodes should be specified in the bcfile as the `CB` tag of each read""",
              default=None,
              show_default=True,
              type=click.Path(resolve_path=True,
                              file_okay=True,
                              dir_okay=False,
                              readable=True))
@click.option("--outputfolder", "-o",
              help="Output folder, does not need to exist",
              default=None,
              type=click.Path(exists=False))
@click.option("--sampleid", "-e",
              help="The sample name that will be used to retrieve informations from metadatatable",
              default=None,
              type=click.Path(exists=False))
@click.option("--metadatatable", "-s",
              help="Table containing metadata of the various samples (csv fortmated, [row:samples, col:entry])",
              default=None,
              type=click.Path(resolve_path=True,
                              file_okay=True,
                              dir_okay=False,
                              readable=True))
@click.option("--repmask", "-m",
              help=".gtf file containing intervals sorted by chromosome, strand, position. This can be achieved by ``sort -k1,1 -k7,7 -k4,4n -o [OUTFILE] [INFILE]``",
              default=None,
              type=click.Path(resolve_path=True,
                              file_okay=True,
                              dir_okay=False,
                              readable=True))
@click.option("--logic", "-l",
              help="The logic to use for the filtering (default: Default)",
              default="Default")
@click.option("--multimap", "-M",
              help="Use reads that did not map uniquely (default: False)",
              default=False,
              is_flag=True)
@click.option("--test", "-t",
              help="Test mode. Use only if you are a developer, it will save some intermediate files.",
              default=False,
              is_flag=True)
@click.option("--molrep", "-x",
              help="Outputs a file containing the interval mapping of the molecules. (it will run slower)",
              default=False,
              is_flag=True)
@click.option("--samtools-threads", "-@",
              help="The number of threads to use to sort the bam by cellID file using samtools",
              default=16)
@click.option("--samtools-memory",
              help="The number of MB used for every thread by samtools to sort the bam file",
              default=2048)
@click.option("--controltype",
              help="The negative control that you want to run. flip or polyt",
              default="flip")
def controlrun(bamfile: str, gtffile: str,
               bcfile: str, outputfolder: str,
               sampleid: str, metadatatable: str,
               repmask: str, logic: str, molrep: bool,
               multimap: bool, test: bool, samtools_threads: int, samtools_memory: int, controltype: str,
               additional_ca: dict={}) -> None:
    """Runs a negative control of the velocity analysis

    BAMFILE bam file with sorted reads

    GTFFILE genome annotation file
    """
    _controlrun(bamfile=bamfile, gtffile=gtffile, bcfile=bcfile, outputfolder=outputfolder,
                sampleid=sampleid, metadatatable=metadatatable, repmask=repmask,
                logic=logic, molrep=molrep, multimap=multimap, test=test, samtools_threads=samtools_threads,
                samtools_memory=samtools_memory, controltype=controltype, additional_ca=additional_ca)
