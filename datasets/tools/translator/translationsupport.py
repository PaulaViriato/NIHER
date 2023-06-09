from uliontsetranslators import translators as uliontset
from threading import Thread
import argparse
import random
import tqdm
import time
import json
import re
import os

class TranslationSupport:
    def __init__ (self, pattern_word = '----------', path_languages = None,
                  timeout = 300.0, path_translators = None, version = 'all',
                  path_write = "translation_support.json"):
        self.pattern_word        = pattern_word
        self.path_translators    = path_translators
        self.path_languages      = path_languages
        self.path_write          = path_write
        self.timeout             = timeout
        self.version             = version
        self.pass_thread         = [True, True]
        self.exceptions          = []
        self.init_values()

        total = int(len(list(self.languages.keys()))**2)
        total *= len(list(self.translators.keys()))
        self.range_progress = tqdm.tqdm(range(total), desc='Process Translation Support', ncols=100)

    def read_translators (self):
        self.translators = {}
        if (self.path_translators != None):
            try:
                with open(self.path_translators, 'r') as jfile:
                    self.translators = json.load(jfile)
            except Exception as e:
                self.exceptions.append("[read_translators] "+str(e))
                self.path_translators = None
                self.read_translators()
        else:
            if (self.version == 'fa'): self.translators = {'niutrans': 'China', 'iflytekv1': 'China', 'googlev1': 'America'}
            elif (self.version == 'fb'): self.translators = {'systran': 'France', 'tilde': 'Latvia', 'mirai': 'Japan'}
            elif (self.version == 'fc'): self.translators = {'youdaov1': 'China', 'youdaov2': 'China', 'languagewire': 'Denmark'}
            elif (self.version == 'va'): self.translators = {'alibabav1': 'China', 'alibabav2': 'China', 'baiduv1': 'China'}
            elif (self.version == 'vb'): self.translators = {'baiduv2': 'China', 'iciba': 'China', 'mymemory': 'Italy'}
            elif (self.version == 'vc'): self.translators = {'iflytekv2': 'China', 'googlev2': 'America', 'volcengine': 'China'}
            elif (self.version == 'vd'): self.translators = {'lingvanex': 'Cyprus', 'bing': 'America', 'yandex': 'Russia'}
            elif (self.version == 've'): self.translators = {'itranslate': 'Austria', 'sogou': 'China', 'modernmt': 'Italy'}
            elif (self.version == 'vf'): self.translators = {'apertium': 'Apertium', 'reverso': 'France', 'cloudyi': 'China'}
            elif (self.version == 'vg'): self.translators = {'deepl': 'Germany', 'qqtransmart': 'China', 'translatecom': 'America'}
            elif (self.version == 'vh'): self.translators = {'qqfanyi': 'China', 'argos': 'America', 'translateme': 'Lithuania'}
            elif (self.version == 'vi'): self.translators = {'youdaov3': 'China', 'papago': 'South Korea', 'iflyrec': 'China'}
            elif (self.version == 'vj'): self.translators = {'yeekit': 'China', 'caiyun': 'China', 'elia': 'Spain'}
            elif (self.version == 'vk'): self.translators = {'judic': 'Belgium', 'mglip': 'China', 'utibet': 'China'}
            elif (self.version == 'failing'):
                self.translators = {'niutrans': 'China', 'iflytekv1': 'China', 'googlev1': 'America',
                                    'systran': 'France', 'tilde': 'Latvia', 'mirai': 'Japan',
                                    'youdaov1': 'China', 'youdaov2': 'China', 'languagewire': 'Denmark'}
            elif (self.version == 'working'):
                self.translators = {'alibabav1': 'China', 'alibabav2': 'China', 'baiduv1': 'China', 'baiduv2': 'China',
                                    'iciba': 'China', 'mymemory': 'Italy', 'iflytekv2': 'China', 'googlev2': 'America',
                                    'volcengine': 'China', 'lingvanex': 'Cyprus', 'bing': 'America', 'yandex': 'Russia',
                                    'itranslate': 'Austria', 'sogou': 'China', 'modernmt': 'Italy', 'apertium': 'Apertium',
                                    'reverso': 'France', 'cloudyi': 'China', 'deepl': 'Germany', 'qqtransmart': 'China',
                                    'translatecom': 'America', 'qqfanyi': 'China', 'argos': 'America', 'translateme': 'Lithuania',
                                    'youdaov3': 'China', 'papago': 'South Korea', 'iflyrec': 'China', 'yeekit': 'China',
                                    'caiyun': 'China', 'elia': 'Spain', 'judic': 'Belgium', 'mglip': 'China', 'utibet': 'China'}
            else:
                self.translators = {'niutrans': 'China', 'iflytekv1': 'China', 'googlev1': 'America', 'systran': 'France',
                                    'tilde': 'Latvia', 'mirai': 'Japan', 'youdaov1': 'China', 'youdaov2': 'China',
                                    'languagewire': 'Denmark', 'alibabav1': 'China', 'alibabav2': 'China', 'baiduv1': 'China',
                                    'baiduv2': 'China', 'iciba': 'China', 'mymemory': 'Italy', 'iflytekv2': 'China',
                                    'googlev2': 'America', 'volcengine': 'China', 'lingvanex': 'Cyprus', 'bing': 'America',
                                    'yandex': 'Russia', 'itranslate': 'Austria', 'sogou': 'China', 'modernmt': 'Italy',
                                    'apertium': 'Apertium', 'reverso': 'France', 'cloudyi': 'China', 'deepl': 'Germany',
                                    'qqtransmart': 'China', 'translatecom': 'America', 'qqfanyi': 'China', 'argos': 'America',
                                    'translateme': 'Lithuania', 'youdaov3': 'China', 'papago': 'South Korea', 'iflyrec': 'China',
                                    'yeekit': 'China', 'caiyun': 'China', 'elia': 'Spain', 'judic': 'Belgium', 'mglip': 'China',
                                    'utibet': 'China'}

    def read_languages (self):
        if (self.path_languages != None):
            try:
                with open(self.path_languages, 'r') as jfile:
                    self.languages = json.load(jfile)
            except Exception as e:
                self.exceptions.append("[read_languages] "+str(e))
                self.path_languages = None
                self.read_languages()
        else:
            self.languages = ['ace', 'ach', 'acr', 'acu', 'ada', 'adh', 'af', 'agr', 'ake', 'am', 'amk',
                'amu', 'any', 'ar', 'arn', 'ata', 'ay', 'az', 'azb', 'ba', 'bm', 'bas', 'bba', 'bch',
                'bci', 'bcl', 'bdh', 'bdu', 'be', 'bem', 'ber', 'bfa', 'bg', 'bhw', 'bi', 'bin', 'bn',
                'bno', 'bnp', 'bqj', 'bqp', 'br', 'bs', 'bsn', 'btx', 'bum', 'bus', 'byr', 'bzj', 'ca',
                'cab', 'cak', 'cas', 'cbl', 'cce', 'ccp', 'cdf', 'ceb', 'cfm', 'cha', 'che', 'chk',
                'chq', 'chr', 'cht', 'cjk', 'cjp', 'ckb', 'cki', 'cnh', 'cni', 'co', 'cop', 'cpb', 'crh',
                'crs', 'cs', 'ctd', 'cv', 'cy', 'czt', 'da', 'de', 'dhv', 'dik', 'djk', 'dop', 'dtp',
                'dua', 'duo', 'dv', 'dyu', 'dz', 'ee', 'efi', 'el', 'en', 'enx', 'eo', 'es', 'et', 'eu',
                'fa', 'fi', 'tl', 'fj', 'fo', 'fr', 'fuv', 'fy', 'ga', 'gaa', 'gbi', 'gbo', 'gd', 'gil',
                'gl', 'gnw', 'gof', 'gu', 'gub', 'guc', 'gug', 'gur', 'guw', 'gv', 'gym', 'ha', 'haw',
                'he', 'her', 'hi', 'hil', 'hlb', 'hmo', 'hr', 'ht', 'hu', 'hui', 'huv', 'hwc', 'hy',
                'iba', 'ibg', 'id', 'ifa', 'ifb', 'ify', 'ig', 'ikk', 'ilo', 'iou', 'is', 'ish', 'iso',
                'it', 'izz', 'ja', 'jac', 'jae', 'jiv', 'jmc', 'jv', 'ka', 'ka', 'kab', 'kac', 'kam',
                'kbh', 'kbo', 'kbp', 'kea', 'kek', 'keo', 'kg', 'ki', 'kk', 'kle', 'km', 'kmb', 'kn',
                'knj', 'ko', 'kpg', 'kqn', 'krs', 'ksd', 'ku', 'kwy', 'ky', 'kyu', 'la', 'lb', 'lcm',
                'lcp', 'lg', 'ln', 'lnd', 'lo', 'loz', 'lsi', 'lt', 'lua', 'lub', 'lue', 'lun', 'lus',
                'lv', 'mad', 'mh', 'mam', 'map', 'mau', 'mbb', 'mdy', 'cnr', 'meu', 'mfe', 'mg', 'mhr',
                'mi', 'mk', 'ml', 'mn', 'mni', 'mn', 'mos', 'mps', 'mr', 'mrj', 'mrw', 'ms', 'mt', 'muv',
                'hmn', 'my', 'nav', 'nba', 'ndc', 'ndo', 'ne', 'ngl', 'nhg', 'nia', 'nij', 'niu', 'nl',
                'no', 'nop', 'ntm', 'ny', 'nyk', 'nyn', 'nyu', 'nyy', 'nzi', 'ojb', 'om', 'ond', 'or',
                'os', 'otq', 'pa', 'pag', 'pap', 'pck', 'pcm', 'pil', 'pis', 'pl', 'poh', 'pon', 'pot',
                'ppk', 'prk', 'ps', 'pss', 'pt', 'ptu', 'quc', 'quh', 'quw', 'quz', 'qxr', 'rar', 'rmn',
                'rn', 'rnd', 'ro', 'ru', 'rug', 'rw', 'sd', 'seh', 'sg', 'shi', 'shp', 'si', 'sid', 'sk',
                'sl', 'sm', 'sn', 'so', 'sop', 'spy', 'sq', 'sr', 'srm', 'ssd', 'ssx', 'st', 'su', 'sv',
                'sw', 'swc', 'swp', 'sxn', 'syc', 'ta', 'tbz', 'tdt', 'te', 'teo', 'tet', 'tex', 'tg',
                'tl', 'th', 'ti', 'tig', 'tih', 'tiv', 'tk', 'tll', 'tmh', 'tn', 'to', 'toj', 'tpi',
                'tpm', 'tr', 'ts', 'tsc', 'tt', 'ttj', 'tum', 'tvl', 'tw', 'ty', 'tyv', 'tzh', 'tzo',
                'udm', 'uk', 'umb', 'ur', 'urh', 'usp', 'uz', 've', 'vi', 'vun', 'wal', 'war', 'wes',
                'wls', 'wlx', 'wo', 'wrs', 'wsk', 'xal', 'xh', 'xsm', 'yap', 'yi', 'yo', 'yon', 'yua',
                'yue', 'zh', 'zne', 'zu', 'zyb']

    def init_values (self):
        self.read_translators()
        self.read_languages()
        self.available = {}

        new_languages = {}
        for lang in self.languages:
            new_languages[lang] = {"from": {}, "to": {}}
            self.available[lang] = {"from": [], "to": []}
        self.languages = new_languages

        for key in self.translators.keys():
            region = self.translators[key]
            self.translators[key] = {"region": region, "nfrom": {}, "available": 0, "from": {},
                                     "time": self.timeout, "server": uliontset.server.TranslatorsServer()}
            for lang in self.languages.keys():
                self.translators[key]["from"][lang] = []
                self.translators[key]["nfrom"][lang] = []

            if (key in self.translators[key]["server"].not_en_langs.keys()):
                self.translators[key]["nfrom"]['en'] = list(self.languages.keys())
                for lang in self.languages.keys():
                    self.translators[key]["nfrom"][lang].append('en')

            if (key in self.translators[key]["server"].not_zh_langs.keys()):
                self.translators[key]["nfrom"]['zh'] = list(self.languages.keys())
                for lang in self.languages.keys():
                    self.translators[key]["nfrom"][lang].append('zh')

    def merge_data (self, initial_path = None, final_path = None, filename = None):
        if (initial_path == None): self.set_path_write(final_path, True)
        else:
            self.set_path_write(initial_path, True)
            with open(final_path, 'r') as jfile:
                data = json.load(jfile)
                languages, available, translators, exceptions = {}, {}, {}, []
                for lang in self.languages.keys():
                    languages[lang] = {"from": {}, "to": {}}
                    available[lang] = {"from": [], "to": []}
                    for transl in self.languages[lang]["from"].keys():
                        languages[lang]["from"][transl] = self.languages[lang]["from"][transl]
                    for transl in self.languages[lang]["to"].keys():
                        languages[lang]["to"][transl] = self.languages[lang]["to"][transl]
                    for transl in data["languages"][lang]["from"].keys():
                        languages[lang]["from"][transl] = data["languages"][lang]["from"][transl]
                    for transl in data["languages"][lang]["to"].keys():
                        languages[lang]["to"][transl] = data["languages"][lang]["to"][transl]
                    for langf in self.languages[lang]["from"]:
                        if (langf not in languages[lang]["from"]): languages[lang]["from"].append(langf)
                    for langt in self.languages[lang]["to"]:
                        if (langt not in languages[lang]["to"]): languages[lang]["to"].append(langt)
                    for langf in data["languages"][lang]["from"]:
                        if (langf not in languages[lang]["from"]): languages[lang]["from"].append(langf)
                    for langt in data["languages"][lang]["to"]:
                        if (langt not in languages[lang]["to"]): languages[lang]["to"].append(langt)

                for key in self.translators.keys():
                    translators[key] = {}
                    translators[key]["region"] = self.translators[key]["region"]
                    translators[key]["nfrom"] = self.translators[key]["nfrom"].copy()
                    translators[key]["available"] = self.translators[key]["available"]
                    translators[key]["from"] = self.translators[key]["from"].copy()
                    translators[key]["time"] = self.translators[key]["time"]
                    translators[key]["server"] = uliontset.server.TranslatorsServer()

                for key in data["translators"].keys():
                    if (len(data["translators"][key]["available"]) > 0):
                        translators[key] = {}
                        translators[key]["region"] = data["translators"][key]["region"]
                        translators[key]["nfrom"] = data["translators"][key]["nfrom"].copy()
                        translators[key]["available"] = data["translators"][key]["available"]
                        translators[key]["from"] = data["translators"][key]["from"].copy()
                        translators[key]["time"] = data["translators"][key]["time"]
                        translators[key]["server"] = uliontset.server.TranslatorsServer()

                for exception in self.exceptions: exceptions.append(exception)
                for exception in data["exceptions"]: exceptions.append(exception)

                self.languages = languages.copy()
                self.available = available.copy()
                self.translators = translators.copy()
                self.exceptions = exceptions

                for key in self.translators.keys():
                    for lang in self.languages.keys():
                        lnfrom, lfrom = [], []
                        for item in self.translators[key]["from"][lang]:
                            if (item not in lfrom): lfrom.append(item)
                        for item in self.translators[key]["nfrom"][lang]:
                            if (item not in lnfrom): lnfrom.append(item)
                        self.translators[key]["from"][lang] = lfrom
                        self.translators[key]["nfrom"][lang] = lnfrom
        self.write_data(filename)

    def write_data (self, path = None):
        if (self.pass_thread[0] == False): return
        self.pass_thread[0] = False

        path_data = path
        if (path == None): path_data = self.path_write

        data = {}
        data["languages"] = self.languages.copy()
        data["translators"] = {}
        for key in self.translators.keys():
            data["translators"][key] = {}
            data["translators"][key]["region"] = self.translators[key]["region"]
            data["translators"][key]["nfrom"] = self.translators[key]["nfrom"].copy()
            data["translators"][key]["available"] = self.translators[key]["available"]
            data["translators"][key]["from"] = self.translators[key]["from"].copy()
            data["translators"][key]["time"] = self.translators[key]["time"]
        data["available"] = self.available.copy()
        data["exceptions"] = self.exceptions

        try:
            with open(path_data, 'w') as jfile:
                json.dump(data, jfile, indent=4)
        except Exception as e:
            self.exceptions.append("[write_data] "+str(e))
            if (path == None): return
            if (path_data != self.path_write): self.write_data()
        self.pass_thread[0] = True

    def get_pattern_word (self): return self.pattern_word
    def get_path_translators (self): return self.path_translators
    def get_path_languages (self): return self.path_languages
    def get_path_write (self): return self.path_write
    def get_timeout (self): return self.timeout
    def get_exceptions (self): return self.exceptions
    def get_languages (self): return self.languages
    def get_available (self): return self.available
    def get_translators (self): return self.translators

    def set_pattern_word (self, pattern_word): self.pattern_word = pattern_word
    def set_timeout (self, timeout): self.timeout = timeout
    def set_exceptions (self, exceptions): self.exceptions = exceptions
    def set_translators (self, translators): self.translators = translators
    def set_languages (self, languages): self.languages = languages
    def set_exceptions (self, exceptions): self.exceptions = exceptions

    def set_path_translators (self, path_translators):
        self.path_translators = path_translators
        self.read_translators()

    def set_path_languages (self, path_languages):
        self.path_languages = path_languages
        self.read_languages()

    def recover_path_write (self):
        aux_lang = self.languages.copy()
        aux_avai = self.available.copy()
        self.read_languages()
        for lang in self.languages:
            if (lang not in aux_lang.keys()): aux_lang[lang] = {"from": {}, "to": {}}
            if (lang not in aux_avai.keys()): aux_avai[lang] = {"from": [], "to": []}
        self.languages = aux_lang
        self.available = aux_avai

        for key in self.translators.keys():
            if ("nfrom" not in self.translators[key].keys()): self.translators[key]["nfrom"] = {}
            for lng in self.languages.keys():
                if (lng not in self.translators[key]["from"].keys()):
                    self.translators[key]["from"][lng] = []
                if (lng not in self.translators[key]["nfrom"].keys()):
                    self.translators[key]["nfrom"][lng] = []
            self.translators[key]["server"] = uliontset.server.TranslatorsServer()

    def set_path_write (self, path_write, recover = False):
        self.path_write = path_write
        if (recover):
            try:
                with open(self.path_write, 'r') as jfile:
                    data = json.load(jfile)
                    if ("languages" in data.keys()): self.languages = data["languages"].copy()
                    if ("available" in data.keys()): self.available = data["available"].copy()
                    if ("translators" in data.keys()): self.translators = data["translators"].copy()
                    if ("exceptions" in data.keys()): self.exceptions = data["exceptions"]
                    self.recover_path_write()
            except Exception as e:
                self.exceptions.append("[set_path_write] "+str(e))
                self.init_values()

    def translation (self, origin, destiny, translator):
        result = uliontset.server.translation_process(server = self.translators[translator]["server"],
                                                      pattern_word = self.pattern_word, translator = translator,
                                                      origin = origin, destiny = destiny, exceptions = self.exceptions,
                                                      timeout = float(self.timeout),
                                                      region = self.translators[translator]["region"],
                                                      not_language = self.translators[translator]["nfrom"])
        if (result[3]):
            self.translators[translator]["from"][origin].append(destiny)
            self.translators[translator]["time"] = result[2]

            while (self.pass_thread[1] == False):
                time.sleep(0.0001*float(random.randint(0, 1000)))
            self.pass_thread[1] = False
            self.languages[origin]["from"][translator] = result[2]
            self.languages[destiny]["to"][translator] = result[2]
            self.available[origin]["from"].append(destiny)
            self.available[destiny]["to"].append(origin)
            self.pass_thread[1] = True

    def check_processed (self, origin, destiny, translator):
        result = [False, False]
        try:
            if ((destiny in self.translators[translator]["from"][origin])or
                (destiny in self.translators[translator]["nfrom"][origin])):
                result[0] = True
        except Exception as e:
            self.exceptions.append("[check_processed] Error: "+str(e)+
                                   "; Phase: 0; From: "+origin+
                                   "; To: "+destiny+"; Translator: "+translator)
            result[0] = False
        try:
            if ((origin in self.translators[translator]["from"][destiny])or
                (origin in self.translators[translator]["nfrom"][destiny])):
                result[1] = True
        except Exception as e:
            self.exceptions.append("[check_processed] Error: "+str(e)+
                                    "; Phase: 1; From: "+origin+
                                    "; To: "+destiny+"; Translator: "+translator)
            result[1] = False
        return result

    def check_translation (self, pattern_language, lang, translator):
        checks = self.check_processed(pattern_language, lang, translator)
        if (checks[0] == False): self.translation(pattern_language, lang, translator)
        if (checks[1] == False): self.translation(lang, pattern_language, translator)
        self.translators[translator]["available"] += 1

    def process_server (self, translator, path):
        self.translators[translator]["server"].set_server_region(translator = translator,
                        region = self.translators[translator]["region"],
                        exceptions = self.exceptions)
        process_languages = list(self.languages.keys())
        process_languages = random.sample(process_languages, k=len(process_languages))
        for i in range(len(process_languages)):
            for destiny in process_languages[i+1:]:
                self.check_translation(process_languages[i], destiny, translator)
                self.range_progress.update(2)
            self.range_progress.update(1)
            self.write_data(path)

    def process (self, path = None):
        path_data, threads = path, []
        if (path == None): path_data = self.path_write

        for translator in self.translators.keys():
            threads.append(Thread(target=self.process_server, args=(translator, path_data,)))
            threads[-1].start()

        while (len(threads) > 0):
            remove_threads = []
            for i in range(len(threads)):
                if (threads[i].is_alive() == False):
                    threads[i].join()
                    remove_threads.append(i)
            remove_threads.sort(reverse=True)
            for rt in remove_threads: del(threads[rt])
        self.write_data(path_data)

    def execute (self, path = None, times = 3):
        path_data = path
        if (path == None): path_data = self.path_write
        for i in range(times):
            self.set_path_write(path_data, True)
            self.process(path_data)

def parse_args ():
    parser = argparse.ArgumentParser(description="It generates a previous mapping of available and free "+
                                     "languages and translators. It uses UlionTse's translators library "+
                                     "(https://github.com/UlionTse/translators), version 5.7.1, for text "+
                                     "translation.")
    parser.add_argument("--path", type=str, default=os.getcwd()+"\\translation_support.json",
                        help="Path for storing the mapping between languages and translators.")
    parser.add_argument("--version", type=str, default="all", help="Translator suite version "+
                        "available: 'all', 'failing', 'working', 'fa', 'fb', 'fc', 'va', ..., 'vk'.")
    parser.add_argument("--timeout", type=int, default=300, help="Maximum translation time.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    path, version, timeout = args.path, args.version, args.timeout
    path = path.replace(".json", "_"+version+".json")
    translation_support = TranslationSupport(path_write = path,
                          version = version, timeout = float(timeout))
    translation_support.execute(times = 1)