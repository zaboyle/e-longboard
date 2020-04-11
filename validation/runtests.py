#!/usr/bin/python
# encoding: utf-8

import argparse
import subprocess

# python -m pytest -n 2 validation/tests/test_bms.py
parser = argparse.ArgumentParser(description='unittest run script')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
parser.add_argument('-d', '--debug_on_fail', action='store_true', help='drop into pdb on test failure')
parser.add_argument('-k', '--keywords', type=str, help='run test cases with keyword search')
parser.add_argument('-t', '--num_threads', type=int, help='number of threads to run with')

args, other_args = parser.parse_known_args()

program_str = 'python -m pytest'
if args.num_threads:
	program_str += ' -n {}'.format(args.num_threads)
if args.keywords:
	program_str += ' -k {}'.format(args.keywords)
if args.debug_on_fail:
	program_str += ' --pdb'
if args.verbose:
	program_str += ' -v'

print(program_str)
process = subprocess.Popen(program_str, shell=True)
process.wait()
