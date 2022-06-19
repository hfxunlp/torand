#encoding: utf-8

import sys
from .torand import torandom

def cli():
	_print_help = (len(sys.argv) < 2)
	if not _print_help:
		_sind = 1
		_fast_mode = True
		if sys.argv[1][-1].isalpha():
			if sys.argv[1].find("f") < 0:
				_fast_mode = False
			_sind += 1
		try:
			b = [int(_) for _ in sys.argv[_sind:]]
		except Exception as e:
			print(e)
			_print_help = True
		if not _print_help:
			if b and all(_ > 0 for _ in b):
				for _ in b:
					print(torandom(_, fast_mode=_fast_mode))
			else:
				_print_help = True
	if _print_help:
		print("Usage:\n\ttorand (f/s) k\nor\n\tpython -m torand (f/s) k\nto generate k real random bytes. Where \"f\" and \"s\" are optional arguments for the hash-based fast generation mode and the standard generation mode respectively, default is \"f\".")

if __name__ == "__main__":
	cli()
