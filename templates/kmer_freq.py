#!/usr/bin/env python

import sys
from Bio import SeqIO
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from Bio.SeqIO.FastaIO import SimpleFastaParser
from collections import Counter,OrderedDict
from itertools import product,groupby
import math
import multiprocessing
import pandas as pd
from tqdm import tqdm
import argparse

def parse_args():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    #parser.add_argument("fastx", help="Fasta/fastq file containing read sequences", type=str, default="$qced_reads")

    # Optional arguments
    parser.add_argument("-k", help="k-mer size [5]", type=int, default=5)
    parser.add_argument("-t", "--threads", help="Number of threads to use [4]", type=int, default=32)
    parser.add_argument("-c", "--count", help="Provide raw k-mer raw counts, not normalized [False]", action="store_true", default=False)
    parser.add_argument("-f", "--frac", help="Provide k-mer counts normalized by total number of k-mers [False]", action="store_true", default=False)

    # Parse arguments
    args = parser.parse_args()

    return args

def launch_pool( procs, funct, args ):
    p    = multiprocessing.Pool(processes=procs)
    try:
        results = p.map(funct, args)
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
    return results

def chunks( l, n ):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def rev_comp_motif( motif ):
    """
    Return the reverse complement of the input motif.
    """
    COMP = {"A":"T", \
            "T":"A", \
            "C":"G", \
            "G":"C", \
            "W":"S", \
            "S":"W", \
            "M":"K", \
            "K":"M", \
            "R":"Y", \
            "Y":"R", \
            "B":"V", \
            "D":"H", \
            "H":"D", \
            "V":"B", \
            "N":"N", \
            "X":"X", \
            "*":"*"}
    rc_motif = []
    for char in motif[::-1]:
        rc_motif.append( COMP[char] )
    return "".join(rc_motif)

def build_all_kmers( k ):
    kmers   = []
    for seq in product("ATGC",repeat=k):
        kmers.append( "".join(seq) )
    return kmers

def combine_kmers_list( all_kmers ):
    combined = set()
    for kmer in all_kmers:
        if rev_comp_motif(kmer) in combined:
            pass
        else:
            combined.add(kmer)
    combined = list(combined)
    combined.sort()
    return combined

def kmer_freq ( seq_str, k, combined_kmers, kmer_names_only=False ):
    seq_str    = seq_str.upper()
    
    all_kmer_n = Counter()
    for j in range( len(seq_str)-(k-1) ):
        motif = seq_str[j:j+k]
        all_kmer_n[motif] += 1

    # Combine forward and reverse complement motifs into one count
    combined_kmer_n = Counter()
    for kmer in combined_kmers:
        kmer_rc               = rev_comp_motif(kmer)
        combined_kmer_n[kmer] = all_kmer_n[kmer] + all_kmer_n[kmer_rc]
    return combined_kmer_n

def calc_seq_kmer_freqs( tup ):
    read_id        = tup[0]
    seq            = tup[1]
    k              = tup[2]
    combined_kmers = tup[3]
    i              = tup[4]
    count          = tup[5]
    frac           = tup[6]
    
    seq_comp            = []
    combined_kmer_n     = kmer_freq( seq, k, combined_kmers )
    ord_combined_kmer_n = OrderedDict(sorted(combined_kmer_n.items()))

    for kmer,n in ord_combined_kmer_n.items():
        if count:
            kmer_comp = n
        elif frac:
            kmer_comp = float(n) / sum(combined_kmer_n.values())
        else:
            kmer_comp = math.log(float(n + 1) / sum(combined_kmer_n.values())) # adding pseudocount for log transform
        seq_comp.append(kmer_comp)

    return read_id, seq_comp

def build_args_for_kmer_calc(read_num, target_range, args, read_id, seq, k, combined_kmers, lengths_d, count, frac):
    status = "keep going"
    if read_num>=target_range[0] and read_num<=target_range[1]:

        # if read_num%1000==0: print("Loading...",target_range, read_num)

        args.append( (read_id, seq, k, combined_kmers, read_num, count, frac) )
        lengths_d[read_id] = len(seq)
    elif read_num>target_range[1]:
        status = "over"
    return args,status

def launch_seq_kmers_pool( fastx, ftype, k, threads, target_range, combined_kmers, count, frac ):
    
    args      = []
    lengths_d = {}

    if ftype=="fastq":
        for read_num, (read_id, seq, qual) in enumerate(FastqGeneralIterator(open(fastx))):
            args,status = build_args_for_kmer_calc(read_num, target_range, args, read_id, seq, k, combined_kmers, lengths_d, count, frac)
            if status=="over":
                break

    elif ftype=="fasta":
        for read_num, (read_id, seq) in enumerate(SimpleFastaParser(open(fastx))):
            args,status = build_args_for_kmer_calc(read_num, target_range, args, read_id, seq, k, combined_kmers, lengths_d, count, frac)
            if status=="over":
                break
    
    results = launch_pool( threads, calc_seq_kmer_freqs, args )
    
    return dict(results), lengths_d

def print_comp_vectors(read_num, target_range, comp_vectors, read_id, lengths_d):
    status = "keep going"
    if read_num>=target_range[0] and read_num<=target_range[1]:

        # if read_num%1000==0: print("writing...",target_range, read_num)
        comp_vec_str = "\t".join( map(lambda x: str(round(x,4)), comp_vectors[read_id]))
        print("%s\t%i\t%s" % (read_id.split(" ")[0], lengths_d[read_id], comp_vec_str))
    elif read_num>target_range[1]:
        status = "over"
    return status

def write_output( fastx, ftype, comp_vectors, lengths_d, target_range ):

    if ftype=="fastq":
        for read_num, (read_id, seq, qual) in enumerate(FastqGeneralIterator(open(fastx))):
            status = print_comp_vectors(read_num, target_range, comp_vectors, read_id, lengths_d)
            if status=="over":
                break

    elif ftype=="fasta":
        for read_num, (read_id, seq) in enumerate(SimpleFastaParser(open(fastx))):
            status = print_comp_vectors(read_num, target_range, comp_vectors, read_id, lengths_d)
            if status=="over":
                break

def get_n_reads(fastx, ftype):
    n_lines = 0
    with open(fastx) as f:
        for i, l in enumerate(f):
            n_lines += 1
    
    if ftype=="fastq":
        n_reads = len([read_tup for read_tup in FastqGeneralIterator(open(fastx))])
    elif ftype=="fasta":
        n_reads = len([read_tup for read_tup in SimpleFastaParser(open(fastx))])
    return n_reads

def check_input_format(fastx):
    for line in open(fastx).readlines():
        break

    if line[0]=="@":
        ftype = "fastq"
    elif line[0]==">":
        ftype = "fasta"
    else:
        raise("Unexpected file type! Only *.fasta, *.fa, *.fsa, *.fna, *.fastq, and *.fq recognized.")
    return ftype

def main(args):
    ftype  = check_input_format(sys.argv[0])
    n_reads = get_n_reads(sys.argv[0], ftype)

    chunk_n_reads = 5000

    all_kmers = build_all_kmers(args.k)
    combined_kmers = combine_kmers_list(all_kmers)

    print("read\tlength\t%s" % "\t".join(combined_kmers))

    read_chunks = list(chunks(range(n_reads), chunk_n_reads))

    for chunk in tqdm(read_chunks):
        target_range = (chunk[0], chunk[-1])
        
        comp_vectors,lengths_d = launch_seq_kmers_pool( "$qced_reads",     \
                                                        ftype,          \
                                                        args.k,         \
                                                        args.threads,   \
                                                        target_range,   \
                                                        combined_kmers, \
                                                        args.count,     \
                                                        args.frac )
        write_output( sys.argv[0], ftype, comp_vectors, lengths_d, target_range )

if __name__=="__main__":
    args = parse_args()

    main(args)