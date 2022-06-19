# torand

Generating real random bytes requires to get different results from the execution of a same operation. It is a problem for the computer, whose operations are normally deterministic (like 1 + 1 always results 2), to generate real random bytes.

We observe that the time costs can be different for the computer to run the same code. For example, we run the below code for twice:

```
from time import time
print([-(time() - time()) for _ in range(8)])
```

and it reports:

`[-0.0, 1.1920928955078125e-06, -0.0, -0.0, 9.5367431640625e-07, -0.0, -0.0, -0.0]` and `[-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 9.5367431640625e-07, -0.0]` respectively, showing the differences.

Based on this observation, we may record the time costs during the execution of codes, and generate real random bytes based on the records.

We implement this idea, (T)ime differences between (O)perations for real (Rand)om bytes generation, in python as this library.

## Usage

Install with `pip install torand`.

### Python

#### Main API

`torandom(k, fast_mode=True)`

Generate `k` random bytes. Where `fast_mode` indicates the use of hash-based fast generation (default to `True`).

#### Example

```
from torand import torandom

k = 127
rs = torandom(k, fast_mode=True)
print(rs)
print(len(rs) == k)
```

### Command Line Interface

Execute either

`python -m torand (f/s) k`

or

`torand (f/s) k`

to generate `k` real random bytes. Where `f` and `s` are optional arguments for the hash-based fast generation mode and the standard generation mode respectively, default is `f`.

## Performance

Test with CPython 3.10.5, using a single Intel Core M3-7Y30 CPU thread. Despite that this library only generates ~87.57 k random bytes per second in the standard mode, which is much slower than the `os.urandom` (~12.52 MB/s). We still like to share the idea, and the library is also useful in case we only generate some real random bytes with the idea for fast random byte generation algorithms or hash functions (this library can also achieve a generation speed of ~12.52 MB/s in the fast mode).
