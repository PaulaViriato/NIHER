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
                  timeout = 30.0, path_translators = None,
                  path_write = "translation_support.json"):
        self.pattern_word        = pattern_word
        self.path_translators    = path_translators
        self.path_languages      = path_languages
        self.path_write          = path_write
        self.timeout             = timeout
        self.pass_thread         = [True, True]
        self.exceptions          = []
        self.init_values()

        total = int(len(list(self.languages.keys()))**2)
        total *= len(list(self.translators.keys()))
        self.range_progress = tqdm.tqdm(range(total), desc='Process Translation Support', ncols=100)

    def read_translators (self):
        if (self.path_translators != None):
            try:
                with open(self.path_translators, 'r') as jfile:
                    self.translators = json.load(jfile)
            except Exception as e:
                self.exceptions.append("[read_translators] "+str(e))
                self.path_translators = None
                self.read_translators()
        else:
            self.translators = {'niutrans': 'China', 'alibabav1': 'China', 'alibabav2': 'China', 'baiduv1': 'China',
                                'baiduv2': 'China', 'iciba': 'China', 'mymemory': 'Italy', 'iflytekv1': 'China',
                                'iflytekv2': 'China', 'googlev1': 'America', 'googlev2': 'America', 'volcengine': 'China',
                                'lingvanex': 'Cyprus', 'bing': 'America', 'yandex': 'Russia', 'itranslate': 'Austria',
                                'sogou': 'China', 'modernmt': 'Italy', 'systran': 'France', 'apertium': 'Apertium',
                                'reverso': 'France', 'cloudyi': 'China', 'deepl': 'Germany', 'qqtransmart': 'China',
                                'translatecom': 'America', 'tilde': 'Latvia', 'qqfanyi': 'China', 'argos': 'America',
                                'translateme': 'Lithuania', 'youdaov1': 'China', 'youdaov2': 'China', 'youdaov3': 'China',
                                'papago': 'South Korea', 'mirai': 'Japan', 'iflyrec': 'China', 'yeekit': 'China',
                                'languagewire': 'Denmark', 'caiyun': 'China', 'elia': 'Spain',
                                'judic': 'Belgium', 'mglip': 'China', 'utibet': 'China'}

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

    def organize (self, data):
        removed_translators = []
        for key in data["translators"].keys():
            aux_lng, max_to, max_from = [], 0, 0
            for lng in data["translators"][key]["from"].keys():
                data["translators"][key]["from"][lng] = sorted(
                    set(data["translators"][key]["from"][lng]))
                len_lng = len(data["translators"][key]["from"][lng])
                if (len_lng == 0):
                    aux_lng.append(lng)
                    max_from -= 1
                elif (len_lng > max_to): max_to = len_lng
                max_from += 1
            for lng in aux_lng: _ = data["translators"][key]["from"].pop(lng)
            data["translators"][key]["available"] = int(max(max_to, max_from))
            data["translators"][key].pop("nfrom")
            if (data["translators"][key]["available"] == 0):
                removed_translators.append(key)
        for key in removed_translators: data["translators"].pop(key)

        aux_lang, aux_avai = [], []
        for lang in data["languages"].keys():
            data["languages"][lang]["from"] = {key: value for key, value in sorted(
                data["languages"][lang]["from"].items(), key=lambda item: item[1])}
            data["languages"][lang]["to"] = {key: value for key, value in sorted(
                data["languages"][lang]["to"].items(), key=lambda item: item[1])}

            if ((len(list(data["languages"][lang]["from"].keys())) == 0)or
                (len(list(data["languages"][lang]["to"].keys())) == 0)):
                aux_lang.append(lang)

            data["available"][lang]["from"] = sorted(set(data["available"][lang]["from"]))
            data["available"][lang]["to"] = sorted(set(data["available"][lang]["to"]))

            if ((len(data["available"][lang]["from"]) == 0)or
                (len(data["available"][lang]["to"]) == 0)):
                aux_avai.append(lang)
        for lang in aux_lang: _ = data["languages"].pop(lang)
        for lang in aux_avai: _ = data["available"].pop(lang)

    def write_data (self, final = False, path = None):
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

        if (final): data = self.organize(data)
        try:
            with open(path_data, 'w') as jfile: json.dump(data, jfile, indent=4)
            if (final):
                self.init_values()
                self.exceptions = []
        except Exception as e:
            self.exceptions.append("[write_data] "+str(e))
            if (path == None): return
            if (path_data != self.path_write): self.write_data(final)

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
                    if ("languages" in data.keys()): self.languages = data["languages"]
                    if ("available" in data.keys()): self.available = data["available"]
                    if ("translators" in data.keys()): self.translators = data["translators"]
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
            self.translators[translator]["available"] += 1
            self.translators[translator]["time"] = result[2]

            while (self.pass_thread[1] == False):
                time.sleep(0.0001*float(random.randint(0, 1000)))
            self.pass_thread[1] = False
            self.languages[origin]["from"][translator] = result[2]
            self.languages[destiny]["to"][translator] = result[2]
            self.available[origin]["from"].append(destiny)
            self.available[destiny]["to"].append(origin)
            self.pass_thread[1] = True

    def check_translation (self, pattern_language, lang, translator, processed):
        if (processed[0] == False): self.translation(pattern_language, lang, translator)
        if (processed[1] == False): self.translation(lang, pattern_language, translator)

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

    def process_server (self, translator, path):
        self.translators[translator]["server"].set_server_region(translator = translator,
                        region = self.translators[translator]["region"],
                        exceptions = self.exceptions)
        origin_languages = list(self.languages.keys())
        destiny_languages = list(self.languages.keys())
        random.shuffle(origin_languages)
        random.shuffle(destiny_languages)

        for origin in origin_languages:
            for destiny in destiny_languages:
                if (destiny != origin):
                    cprocessed = self.check_processed(origin, destiny, translator)
                    if (False in cprocessed):
                        self.check_translation(origin, destiny, translator, cprocessed)
                self.range_progress.update(1)
            self.write_data(False, path)

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
        self.write_data(False, path_data)

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
    parser.add_argument("--path", type=str, default=os.getcwd()+"\\translation_support_.json",
                        help="Path for storing the mapping between languages and translators.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    path, final = args.path, args.path
    if ("_.json" in args.path): final = final.replace("_.json", ".json")
    elif (".json" in args.path): path = final.replace(".json", "_.json")
    elif (args.path[-1] == "_"):
        path += ".json"
        final = path.replace("_.json", ".json")
    else:
        path += "_.json"
        final += ".json"

    translation_support = TranslationSupport(path_write = path)
    translation_support.execute(times = 1)
    translation_support.write_data(True, final)