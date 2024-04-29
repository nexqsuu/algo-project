from typing import Callable
from kmp import kmp_search
from rk  import rabin_karp
from boyer import boyer_moore
from memory_profiler import profile
import time
import cProfile
def profileCalls(text:str, pattern:str, max_matches:int, algo:Callable[[str, str, int], list[int]], runCount=1000):
    with cProfile.Profile() as pr:
        for _ in range(runCount):
            algo(text, pattern, max_matches) 
        pr.print_stats()

def runtime(text:str, pattern:str, max_matches:int, algo:Callable[[str, str, int], list[int]], runCount=1000):
    runs:list[float] = []
    for _ in range(runCount):
        start = time.time()
        algo(text, pattern, max_matches) 
        runs.append(time.time()-start) # end - start
    avg = sum(runs)/runCount
    print(f"{algo.__name__}: {avg=}")
    print()
def main():
    '''Run if main module'''
    # accept a file name as input using argparse
    import argparse
    parser = argparse.ArgumentParser(description='Benchmark string search algorithms')
    parser.add_argument('filename', help='File to search')
    # pattern
    parser.add_argument('pattern', help='Pattern to search for')
    # max_matches
    parser.add_argument('max_matches',  type=int, help='Maximum number of matches to find', default=float('inf'))
    # Runs
    parser.add_argument('--runs', type=int, help='Number of runs to average over', default=1000)
    args = parser.parse_args()
    with open(args.filename) as f:
        text = f.read()
        runtime(text, args.pattern, args.max_matches, kmp_search, args.runs)
        profileCalls(text, args.pattern, args.max_matches, kmp_search, args.runs)
        # runtime(text, args.pattern, args.max_matches, boyer_moore, args.runs)
        runtime(text, args.pattern, args.max_matches, rabin_karp, args.runs)
        profileCalls(text, args.pattern, args.max_matches, rabin_karp, args.runs)

if __name__ == '__main__':
    main()
