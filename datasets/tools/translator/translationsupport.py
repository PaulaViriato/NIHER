from uliontsetranslators import translators as uliontset
from threading import Thread
import argparse
import tqdm
import time
import json
import re
import os

class TranslationSupport:
    def __init__ (self, pattern_language = 'en', pattern_word = '你好。\n欢迎你！',
                  path_languages = None, timeout = 30.0, path_translators = None,
                  path_write = "translation_support.json", cores = 1):
        self.pattern_language    = pattern_language
        self.pattern_word        = pattern_word
        self.cores               = cores
        self.path_translators    = path_translators
        self.path_languages      = path_languages
        self.path_write          = path_write
        self.timeout             = timeout
        self.exceptions          = []
        self.init_values(timeout = timeout)

        try:
            result = uliontset.preaccelerate(timeout = int(timeout), translators = self.translators,
                                             exceptions = self.exceptions)
            for translator in result["success"]:
                self.translators[translator[0]] = self.translators[translator[0]]
                self.translators[translator[0]]["time"] = translator[1]
            for translator in result["fail"]:
                self.translators[translator[0]] = self.translators[translator[0]]
        except Exception as e: self.exceptions.append("[__init__] "+str(e))
        self.range_progress = tqdm.tqdm(range(100), desc='Process Translation Support', ncols=100)

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

    def init_values (self, timeout = 30.0):
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
            self.translators[key] = {"region": region, "nfrom": {},
                                     "available": 0, "from": {},
                                     "time": timeout}
            for lang in self.languages.keys():
                self.translators[key]["from"][lang] = []
                self.translators[key]["nfrom"][lang] = []

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
        path_data = path
        if (path == None): path_data = self.path_write

        data = {}
        data["languages"] = self.languages.copy()
        data["available"] = self.available.copy()
        data["translators"] = self.translators.copy()
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

    def get_pattern_language (self): return self.pattern_language
    def get_pattern_word (self): return self.pattern_word
    def get_cores (self): return self.cores
    def get_path_translators (self): return self.path_translators
    def get_path_languages (self): return self.path_languages
    def get_path_write (self): return self.path_write
    def get_timeout (self): return self.timeout
    def get_exceptions (self): return self.exceptions
    def get_languages (self): return self.languages
    def get_available (self): return self.available
    def get_translators (self): return self.translators

    def set_pattern_language (self, pattern_language): self.pattern_language = pattern_language
    def set_pattern_word (self, pattern_word): self.pattern_word = pattern_word
    def set_cores (self, cores): self.cores = cores
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

    def search_new_language (self, message, translator):
        blocks = re.findall(r'\[([^]]+)\]', message)
        if ((len(blocks) == 2)and((" from_" in message)or(" to_" in message)or
            ((" from " in message)and(" to " in message)))):
            try:
                keys = blocks[0].replace("'", "").split(", ")
                langs = blocks[1].replace("'", "").split(", ")

                for key in keys:
                    for lang in langs:
                        mss_from, mss_to = key, lang
                        if (" to_" in message): mss_from, mss_to = lang, key
                        if (lang not in self.languages.keys()):
                            self.languages[lang] = {"from": {}, "to": {}}
                            self.available[lang] = {"from": [], "to": []}

                        if (mss_from not in self.translators[translator]["nfrom"].keys()):
                            self.translators[translator]["nfrom"][mss_from] = []
                        if (mss_from not in self.translators[translator]["from"].keys()):
                            self.translators[translator]["from"][mss_from] = []
                        self.translators[translator]["nfrom"][mss_from].append(mss_to)
                return True
            except Exception as e:
                self.exceptions.append("[search_new_language] Error: "+str(e)+
                                       "; Message: "+message+
                                       "; Translator: "+translator)
                return False
        else: return False

    def translation (self, origin, destiny, translator):
        try:
            delay = time.time()
            tnl = uliontset.TranslatorsServer().translate_text(query_text = self.pattern_word,
                                translator = translator, from_language = origin, to_language = destiny,
                                if_print_warning = False, timeout = float(self.timeout),
                                region = self.translators[translator]["region"], exceptions = self.exceptions)
            delay = time.time() - delay

            if (tnl != None):
                self.translators[translator]["from"][origin].append(destiny)
                self.languages[origin]["from"][translator] = delay
                self.languages[destiny]["to"][translator] = delay
                self.available[origin]["from"].append(destiny)
                self.available[destiny]["to"].append(origin)
                self.translators[translator]["available"] += 1
                self.translators[translator]["time"] = delay
            else:
                if (origin not in self.translators[translator]["nfrom"].keys()):
                    self.translators[translator]["nfrom"][origin] = []
                self.translators[translator]["nfrom"][origin].append(destiny)
        except Exception as e:
            if (self.search_new_language(str(e), translator) == False):
                if (origin not in self.translators[translator]["nfrom"].keys()):
                    self.translators[translator]["nfrom"][origin] = []
                self.translators[translator]["nfrom"][origin].append(destiny)
                self.exceptions.append("[translation] Error: "+str(e)+
                    "; From: "+origin+"; To: "+destiny+"; Translator: "+translator)

    def check_translation (self, lang, translator, processed):
        if (processed[0] == False): self.translation(self.pattern_language, lang, translator)
        if (processed[1] == False): self.translation(lang, self.pattern_language, translator)

    def check_threads (self, threads, size = -1):
        while (((size == -1)and(len(threads) == self.cores))or
               ((size >= 0)and(len(threads) > size))):
            remove_threads = []
            for i in range(len(threads)):
                if (threads[i].is_alive() == False):
                    threads[i].join()
                    remove_threads.append(i)
            remove_threads.sort(reverse=True)
            for rt in remove_threads: del(threads[rt])
        return threads

    def check_processed (self, origin, destiny, translator):
        result = [False, False]
        try:
            if ((destiny in self.translators[translator]["from"][origin])or
                (destiny in self.translators[translator]["nfrom"][origin])):
                result[0] = True
        except Exception as e:
            self.exceptions.append("[check_processed] Error: "+str(e)+"; Phase: 0; "+
                        "From: "+origin+"; To: "+destiny+"; Translator: "+translator)
            result[0] = False

        try:
            if ((origin in self.translators[translator]["from"][destiny])or
                (origin in self.translators[translator]["nfrom"][destiny])):
                result[1] = True
        except Exception as e:
            self.exceptions.append("[check_processed] Error: "+str(e)+"; Phase: 1; "+
                        "From: "+origin+"; To: "+destiny+"; Translator: "+translator)
            result[1] = False

        return result

    def progress_bar (self, processed, language, translator):
        progress = 0.0
        langs = len(list(self.languages.keys()))
        trnlt = len(list(self.translators.keys()))
        mult = langs*trnlt
        total = langs*langs*trnlt
        progress += float(mult*processed)
        progress += float(list(self.languages.keys()).index(language)*trnlt+
                          list(self.translators.keys()).index(translator))
        if (progress != 0.0): progress = float(progress//total)
        self.range_progress.update(int(progress*100.0))

    def process (self, path = None):
        path_data = path
        if (path == None): path_data = self.path_write
        processed, removel, threads = 0, [], []

        while (len(list(self.languages.keys())) > processed):
            self.pattern_language = list(self.languages.keys())[processed]
            for lang in list(self.languages.keys()):
                if (lang == self.pattern_language): continue
                for translator in self.translators.keys():
                    cprocessed = self.check_processed(self.pattern_language,
                                                      lang, translator)
                    if (False in cprocessed):
                        threads = self.check_threads(threads)
                        threads.append(Thread(target=self.check_translation,
                                              args=(lang, translator, cprocessed,)))
                        threads[-1].start()
                    self.progress_bar(processed, lang, translator)
                threads = self.check_threads(threads, 0)
                self.write_data(False, path_data)
            processed += 1

        threads = self.check_threads(threads, 0)
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

    translation_support = TranslationSupport(path_write = path, cores = 20)
    translation_support.execute(times = 1)
    translation_support.write_data(True, final)