from __future__ import print_function  # Requires: Python >= 2.6

import csv
import glob
import inspect
import os
import re
import subprocess
import sys
import time

sys.dont_write_bytecode = True


class My_Craw(object):
    def __init__(self):

        self.BOGON_RANGES = {}
        self.CDN_RANGES = {}
        self.ROOT_DIR = './craw/modules/trail/'
        self.NAME = "Maltrail"
        self.USERS_DIR = os.path.join(os.path.expanduser("~"), ".%s" % self.NAME.lower())
        self.PYCHARM_PRO_DIR = os.path.abspath('.') + "/craw/modules/" + "Mytrails.csv/"
        self.TRAILS_FILE = os.path.join(self.PYCHARM_PRO_DIR, "trails.csv")
        self.LOW_PRIORITY_INFO_KEYWORDS = (
            "reputation", "attacker", "spammer", "abuser", "malicious", "dnspod", "nicru", "crawler", "compromised",
            "bad history")
        self.HIGH_PRIORITY_INFO_KEYWORDS = ("mass scanner", "ipinfo")
        self.HIGH_PRIORITY_REFERENCES = (
            "bambenekconsulting.com", "github.com/stamparm/blackbook", "(static)", "(custom)")
        self.BAD_TRAIL_PREFIXES = ("127.", "192.168.", "localhost")
        self.ROOT_DIR = './craw/modules/trail/'
        self.WHITELIST = set()
        self.WHITELIST_RANGES = set()
        self.read_cdn_ranges()
        self.read_bogon_ranges()
        self.read_whitelist()

    def _chown(self, filepath):
        if not subprocess._mswindows and os.path.exists(filepath):
            try:
                os.chown(filepath, int(os.environ.get("SUDO_UID", -1)), int(os.environ.get("SUDO_GID", -1)))
            except Exception as ex:
                print("[!] chown problem with '%s' ('%s')" % (filepath, ex))

    def update_trails(self, force=False, offline=False):
        """
        Update trails from feeds
        """

        success = False
        trails = {}
        self.read_whitelist()
        try:
            if not os.path.isdir(self.USERS_DIR):
                os.makedirs(self.USERS_DIR, 0o755)
        except Exception as ex:
            exit("[!] something went wrong during creation of directory '%s' ('%s')" % (self.USERS_DIR, ex))

        self._chown(self.USERS_DIR)

        if True:
            trail_files = set()
            for dirpath, dirnames, filenames in os.walk(os.path.abspath(os.path.join(self.ROOT_DIR, "trails"))):
                for filename in filenames:
                    trail_files.add(os.path.abspath(os.path.join(dirpath, filename)))

            if not trails and (force or not os.path.isfile(self.TRAILS_FILE) or (
                    time.time() - os.stat(self.TRAILS_FILE).st_mtime) >= 5 or os.stat(
                self.TRAILS_FILE).st_size == 0 or any(
                os.stat(_).st_mtime > os.stat(self.TRAILS_FILE).st_mtime for _ in trail_files)):
                print("[i] updating trails (this might take a while)...")

                if not offline and (force or True):
                    _ = os.path.abspath(os.path.join(self.ROOT_DIR, "trails", "feeds"))
                    if _ not in sys.path:
                        sys.path.append(_)

                    filenames = sorted(glob.glob(os.path.join(_, "*.py")))
                else:
                    filenames = []

                _ = os.path.abspath(os.path.join(self.ROOT_DIR, "trails"))
                if _ not in sys.path:
                    sys.path.append(_)

                filenames += [os.path.join(_, "static")]

                filenames = [_ for _ in filenames if "__init__.py" not in _]

                for i in range(len(filenames)):
                    filename = filenames[i]

                    try:
                        module = __import__(os.path.basename(filename).split(".py")[0])
                    except (ImportError, SyntaxError) as ex:
                        print("[x] something went wrong during import of feed file '%s' ('%s')" % (filename, ex))
                        continue

                    for name, function in inspect.getmembers(module, inspect.isfunction):
                        if name == "fetch":
                            print(" [o] '%s'%s" % (module.__url__, " " * 20 if len(module.__url__) < 20 else ""))
                            sys.stdout.write(
                                "[?] progress: %d/%d (%d%%)\r" % (i, len(filenames), i * 100 / len(filenames)))
                            sys.stdout.flush()

                            try:
                                results = function()
                                while len(results) == 0:
                                    results = function()
                                classification = {}
                                maintainer_url = module.maintainer_url
                                maintainer = module.maintainer
                                list_source_url = module.list_source_url
                                current_time = time.asctime(time.localtime(time.time()))

                                for item in list(results):
                                    if self.check_whitelisted(item) or any(
                                            item.startswith(_) for _ in self.BAD_TRAIL_PREFIXES):
                                        del results[item]
                                        continue
                                    elif re.search(r"\A\d+\.\d+\.\d+\.\d+\Z", item) and (
                                            self.bogon_ip(item) or self.cdn_ip(item)):
                                        del results[item]
                                        continue
                                    elif '#' in item:
                                        del results[item]
                                        continue
                                    else:
                                        try:
                                            item.encode("utf8")
                                            results[item][0].encode("utf8")
                                            results[item][1].encode("utf8")
                                        except UnicodeDecodeError:
                                            del results[item[0]]
                                            continue

                                    if item.startswith("www.") and '/' not in item:
                                        if item[len("www."):] in results.keys():
                                            try:
                                                del results[item]
                                            except:
                                                pass
                                            continue
                                        results[item[len("www."):]] = results[item]
                                        del results[item]
                                        item = item[len("www."):]

                                    if '?' in item:
                                        if item.split('?')[0] in results.keys():
                                            try:
                                                del results[item]
                                            except:
                                                pass
                                            continue
                                        results[item.split('?')[0]] = results[item]
                                        del results[item]
                                        item = item.split('?')[0]

                                    if '//' in item:
                                        if item.replace('//', '/') in results.keys():
                                            try:
                                                del results[item]
                                            except:
                                                pass
                                            continue
                                        results[item.replace('//', '/')] = results[item]
                                        del results[item]
                                        item = item.replace('//', '/')

                                    if item != item.lower():
                                        if item.lower() in results.keys():
                                            try:
                                                del results[item]
                                            except:
                                                pass
                                            continue
                                        results[item.lower()] = results[item]
                                        del results[item]
                                        item = item.lower()

                                    if results[item][0] in classification.keys():
                                        classification[results[item][0]].append(item)
                                    else:
                                        classification[results[item][0]] = []
                                        classification[results[item][0]].append(item)

                                if results:
                                    temp_path_name, temp_file_name = os.path.split(filename)
                                    _temp_file_name = os.path.join(os.path.dirname(
                                        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                                        'trail',
                                        temp_file_name.split('.')[0])
                                    for _class in classification.items():
                                        with self._fopen(
                                                (_temp_file_name + '_' + _class[0].replace('/', '_') + '.domainset'),
                                                "w") as f:
                                            writer = csv.writer(f, delimiter=',', quotechar='\"',
                                                                quoting=csv.QUOTE_MINIMAL)
                                            f.write('# \n')
                                            f.write('# ' + temp_file_name + '\n')
                                            f.write('# ' + maintainer_url + '\n')
                                            f.write('# ' + maintainer + '\n')
                                            f.write('# ' + list_source_url + '\n')
                                            f.write('# ' + current_time + '\n')
                                            f.write('# ' + _class[0] + '\n')
                                            f.write('# \n')
                                            for item in _class[1]:
                                                writer.writerow((item,))


                            except Exception as ex:
                                print(
                                    "[x] something went wrong during processing of feed file '%s' ('%s')" % (
                                        filename, ex))

            try:
                sys.modules.pop(module.__name__)
                del module
            except Exception:
                pass

    def read_whitelist(self, ):
        _ = os.path.abspath(os.path.join(self.ROOT_DIR, "misc", "whitelist.txt"))
        if os.path.isfile(_):
            with open(_, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    elif re.search(r"\A\d+\.\d+\.\d+\.\d+/\d+\Z", line):
                        try:
                            prefix, mask = line.split('/')
                            self.WHITELIST_RANGES.add((self.addr_to_int(prefix), self.make_mask(int(mask))))
                        except (IndexError, ValueError):
                            self.WHITELIST.add(line)
                    else:
                        self.WHITELIST.add(line)

    def _fopen(self, filepath, mode="rb"):
        retval = open(filepath, mode, encoding='utf-8', newline='')
        if "w+" in mode:
            self._chown(filepath)
        return retval

    def make_mask(self, bits):
        return 0xffffffff ^ (1 << 32 - bits) - 1

    def addr_to_int(self, value):
        _ = value.split('.')
        return (int(_[0]) << 24) + (int(_[1]) << 16) + (int(_[2]) << 8) + int(_[3])

    def check_whitelisted(self, trail):
        if trail in self.WHITELIST:
            return True

        if trail and trail[0].isdigit():
            try:
                _ = self.addr_to_int(trail)
                for prefix, mask in self.WHITELIST_RANGES:
                    if _ & mask == prefix:
                        return True
            except (IndexError, ValueError):
                pass

        return False

    def bogon_ip(self, address):
        if not address:
            return False

        try:
            _ = self.addr_to_int(address)
            for prefix, mask in self.BOGON_RANGES.get(address.split('.')[0], {}):
                if _ & mask == prefix:
                    return True
        except (IndexError, ValueError):
            pass

        return False

    def cdn_ip(self, address):
        if not address:
            return False

        try:
            _ = self.addr_to_int(address)
            for prefix, mask in self.CDN_RANGES.get(address.split('.')[0], {}):
                if _ & mask == prefix:
                    return True
        except (IndexError, ValueError):
            pass

        return False

    def read_cdn_ranges(self):
        _ = os.path.abspath(os.path.join(self.ROOT_DIR, "misc", "cdn_ranges.txt"))
        if os.path.isfile(_):
            with open(_, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    else:
                        key = line.split('.')[0]
                        if key not in self.CDN_RANGES:
                            self.CDN_RANGES[key] = []
                        prefix, mask = line.split('/')
                        self.CDN_RANGES[key].append((self.addr_to_int(prefix), self.make_mask(int(mask))))

    def read_bogon_ranges(self):
        _ = os.path.abspath(os.path.join(self.ROOT_DIR, "misc", "bogon_ranges.txt"))
        if os.path.isfile(_):
            with open(_, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    else:
                        key = line.split('.')[0]
                        if key not in self.BOGON_RANGES:
                            self.BOGON_RANGES[key] = []
                        prefix, mask = line.split('/')
                        self.BOGON_RANGES[key].append((self.addr_to_int(prefix), self.make_mask(int(mask))))
