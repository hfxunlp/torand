#encoding: utf-8

from time import time
try:
	from math import log2
except:
	from math import log
	log2 = lambda x: log(x, 2.0)
try:
	from hashlib import blake2b as hash_m
	MAX_KEY_SIZE, SALT_SIZE, PERSON_SIZE, MAX_DIGEST_SIZE = hash_m.MAX_KEY_SIZE, hash_m.SALT_SIZE, hash_m.PERSON_SIZE, hash_m.MAX_DIGEST_SIZE
except:
	from hashlib import sha512
	MAX_KEY_SIZE, SALT_SIZE, PERSON_SIZE, MAX_DIGEST_SIZE = 64, 16, 16, 64

	class hash_m:

		def __init__(self, data=b"", digest_size=MAX_DIGEST_SIZE, key=b"", salt=b"", person=b""):

			self.hash = sha512(b"".join([key, salt, person, data]))
			self.digest_size = digest_size

		def update(self, data=b""):

			self.hash.update(data)

		def digest(self):

			_rs = self.hash.digest()

			return _rs[:self.digest_size] if len(_rs) > self.digest_size else _rs

		def hexdigest(self):

			_rs = self.hexdigest()
			_esize = self.digest_size + self.digest_size

			return _rs[:_esize] if len(_rs) > _esize else _rs

hash_m_fastrand = None
fast_mode_default = True

class TRand:

	def __init__(self, *args, **kwargs):

		self.stime = None

	def __call__(self, *args, **kwargs):

		_stime = time() if self.stime is None else self.stime
		self.stime = time()

		return self.stime - _stime

def get_bytes_info(nbytes):

	_rs = []
	_count_d = {}
	_ninfo = 0.0
	_nt = float(nbytes * 8)
	_g = TRand()
	_num_g = 0

	while _ninfo < _nt:
		_cur_d = _g()
		_rs.append(_cur_d.hex())
		_count_d[_cur_d] = _count_d.get(_cur_d, 0) + 1
		_num_g += 1
		_ninfo = 0.0
		_num_g_f = float(_num_g)
		for _v in _count_d.values():
			_ = float(_v)
			_ninfo += log2(_num_g_f / _) * _
	_t = time()
	_rs.append(_t.hex())

	return "".join(_rs).encode("utf-8")

def get_hash_m(l):

	return hash_m(get_bytes_info(l), digest_size=l, key=hash_m(get_bytes_info(MAX_KEY_SIZE), digest_size=MAX_KEY_SIZE).digest(), salt=hash_m(get_bytes_info(SALT_SIZE), digest_size=SALT_SIZE).digest(), person=hash_m(get_bytes_info(PERSON_SIZE), digest_size=PERSON_SIZE).digest())

def torandom_maxhashlen_pure(l):

	return get_hash_m(l).digest()

def torandom_maxhashlen_fast(l):

	global hash_m_fastrand
	if hash_m_fastrand is None:
		hash_m_fastrand = get_hash_m(MAX_DIGEST_SIZE)

	_rb = hash_m_fastrand.digest()
	hash_m_fastrand.update(_rb + time().hex().encode("utf-8"))

	return _rb[:l] if l < MAX_DIGEST_SIZE else _rb

def torandom_maxhashlen(l, fast_mode=fast_mode_default):

	return torandom_maxhashlen_fast(l) if fast_mode else torandom_maxhashlen_pure(l)

def torandom_pure(l):

	if l <= MAX_DIGEST_SIZE:
		return torandom_maxhashlen_pure(l)
	else:
		rs = []
		_ = l
		_hash_m = get_hash_m(MAX_DIGEST_SIZE)
		while _ > MAX_DIGEST_SIZE:
			rs.append(_hash_m.digest())
			_ -= MAX_DIGEST_SIZE
			_hash_m.update(get_bytes_info(MAX_DIGEST_SIZE))
		_rb = _hash_m.digest()
		rs.append(_rb[:_] if _ < MAX_DIGEST_SIZE else _rb)
		return b"".join(rs)

def torandom_fast(l):

	global hash_m_fastrand
	if hash_m_fastrand is None:
		hash_m_fastrand = get_hash_m(MAX_DIGEST_SIZE)

	if l <= MAX_DIGEST_SIZE:
		_rb = hash_m_fastrand.digest()
		hash_m_fastrand.update(_rb + time().hex().encode("utf-8"))

		return _rb[:l] if l < MAX_DIGEST_SIZE else _rb
	else:
		rs = []
		_ = l
		while _ > MAX_DIGEST_SIZE:
			_rb = hash_m_fastrand.digest()
			rs.append(_rb)
			_ -= MAX_DIGEST_SIZE
			hash_m_fastrand.update(_rb + time().hex().encode("utf-8"))
		_rb = hash_m_fastrand.digest()
		rs.append(_rb[:_] if _ < MAX_DIGEST_SIZE else _rb)
		hash_m_fastrand.update(_rb + time().hex().encode("utf-8"))
		return b"".join(rs)

def torandom(l, fast_mode=fast_mode_default):

	return torandom_fast(l) if fast_mode else torandom_pure(l)
