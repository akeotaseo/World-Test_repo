from __future__ import absolute_import
from hashlib import sha1
import sqlite3
import time
import os
import pickle
from codequick.script import Script
from codequick.utils import ensure_unicode
from collections.abc import MutableMapping, MutableSequence
buffer = bytes
__all__ = ["PersistentDict", "PersistentList", "Cache"]
profile_dir = Script.get_info("profile")
def check_filename(name):
    if os.path.sep in name:
        filepath = ensure_unicode(name)
        data_dir = os.path.dirname(filepath)
    else:
        filepath = os.path.join(profile_dir, ensure_unicode(name))
        data_dir = profile_dir
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return filepath
class _PersistentBase(object):
    def __init__(self, name):
        super(_PersistentBase, self).__init__()
        self._filepath = check_filename(name)
        self._version_string = "__codequick_storage_version__"
        self._data_string = "__codequick_storage_data__"
        self._serializer_obj = object
        self._stream = None
        self._hash = None
        self._data = None
    def _load(self):
        if os.path.exists(self._filepath):
            self._stream = file_obj = open(self._filepath, "rb+")
            content = file_obj.read()
            self._hash = sha1(content).hexdigest()
            return pickle.loads(content)
    def flush(self):
        data = {self._version_string: 2, self._data_string: self._data}
        content = pickle.dumps(data, protocol=2)
        current_hash = sha1(content).hexdigest()
        if self._hash is None or self._hash != current_hash:
            if self._stream:
                self._stream.seek(0)
                self._stream.truncate(0)
            else:
                self._stream = open(self._filepath, "wb+")
            self._stream.write(content)
            self._hash = current_hash
            self._stream.flush()
    def close(self):
        self.flush()
        self._stream.close()
        self._stream = None
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.close()
    def __len__(self):
        return len(self._data)
    def __getitem__(self, index):
        return self._data[index][0]
    def __setitem__(self, index, value):
        self._data[index] = (value, time.time())
    def __delitem__(self, index):
        del self._data[index]
    def __bool__(self):
        return bool(self._data)
    def __nonzero__(self):
        return bool(self._data)
class PersistentDict(_PersistentBase, MutableMapping):
    def __iter__(self):
        return iter(self._data)
    def __repr__(self):
        return f'{self.__class__.__name__}({dict(self.items())})'
    def __init__(self, name, ttl=None):
        super(PersistentDict, self).__init__(name)
        data = self._load()
        self._data = {}
        if data:
            version = data.get(self._version_string, 1)
            if version == 1:
                self._data = {key: (val, time.time()) for key, val in data.items()}
            else:
                data = data[self._data_string]
                if ttl:
                    self._data = {key: item for key, item in data.items() if time.time() - item[1] < ttl}
                else:
                    self._data = data
    def items(self):
        return map(lambda x: (x[0], x[1][0]), self._data.items())
class PersistentList(_PersistentBase, MutableSequence):
    def __repr__(self):
        return f'{self.__class__.__name__}({[val for val, _ in self._data]})'
    def __init__(self, name, ttl=None):
        super(PersistentList, self).__init__(name)
        data = self._load()
        self._data = []
        if data:
            if isinstance(data, list):
                self._data = [(val, time.time()) for val in data]
            else:
                data = data[self._data_string]
                if ttl:
                    self._data = [item for item in data if time.time() - item[1] < ttl]
                else:
                    self._data = data
    def insert(self, index, value):
        self._data.insert(index, (value, time.time()))
    def append(self, value):
        self._data.append((value, time.time()))
class Cache(object):
    def __init__(self, name, ttl):
        self.filepath = check_filename(name)
        self.buffer = {}
        self.ttl = ttl
        self._connect()
    def _connect(self):
        self.db = db = sqlite3.connect(self.filepath, timeout=3)
        self.cur = cur = db.cursor()
        db.isolation_level = None
        cur.execute("CREATE TABLE IF NOT EXISTS itemcache (key TEXT PRIMARY KEY, value BLOB, timestamp INTEGER)")
        db.commit()
    def execute(self, sqlquery, args, repeat=False):
        self.cur.execute("BEGIN")
        try:
            self.cur.execute(sqlquery, args)
        except sqlite3.DatabaseError as e:
            if not repeat and os.path.exists(self.filepath) and \
                    (str(e).find("file is encrypted") > -1 or str(e).find("not a database") > -1):
                Script.log("Deleting broken database file: %s", (self.filepath,), lvl=Script.DEBUG)
                self.close()
                os.remove(self.filepath)
                self._connect()
                self.execute(sqlquery, args, repeat=True)
            else:
                raise e
        except Exception as e:
            self.db.rollback()
            raise e
        else:
            self.db.commit()
    def __getitem__(self, key):
        if key in self.buffer:
            return self.buffer[key]
        else:
            item = self.cur.execute("SELECT value, timestamp FROM itemcache WHERE key = ?", (key,)).fetchone()
            if item is None:
                raise KeyError(key)
            else:
                value, timestamp = item
                if self.ttl > -1 and timestamp + self.ttl < time.time():
                    del self[key]
                    raise KeyError(key)
                else:
                    return pickle.loads(bytes(value))
    def __setitem__(self, key, value):
        data = buffer(pickle.dumps(value))
        self.execute("REPLACE INTO itemcache (key, value, timestamp) VALUES (?,?,?)", (key, data, time.time()))
    def __delitem__(self, key):
        self.execute("DELETE FROM itemcache WHERE key = ?", (key,))
    def __contains__(self, key):
        try:
            if key in self.buffer:
                return True
            else:
                self.buffer[key] = self[key]
                return True
        except KeyError:
            return False
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.close()
    def close(self):
        self.db.close()