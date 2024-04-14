# Copyright 2021 Mufeed Ali
# Copyright 2021 Rafael Mardojai CM
# SPDX-License-Identifier: GPL-3.0-or-later

import html
import json
import logging
import random
import re
from tempfile import NamedTemporaryFile
from typing import List

from gtts import gTTS, lang

from dialect.providers.base import (
    ProviderCapability,
    ProviderError,
    ProviderErrorCode,
    ProviderFeature,
    Translation,
)
from dialect.providers.local import LocalProvider
from dialect.providers.soup import SoupProvider

RPC_ID = 'MkEWBc'

# Predefined URLs used to make google translate requests.
TRANSLATE_RPC = '{host}/_/TranslateWebserverUi/data/batchexecute'

DEFAULT_SERVICE_URLS = (
    'translate.google.ac',
    'translate.google.ad',
    'translate.google.ae',
    'translate.google.al',
    'translate.google.am',
    'translate.google.as',
    'translate.google.at',
    'translate.google.az',
    'translate.google.ba',
    'translate.google.be',
    'translate.google.bf',
    'translate.google.bg',
    'translate.google.bi',
    'translate.google.bj',
    'translate.google.bs',
    'translate.google.bt',
    'translate.google.by',
    'translate.google.ca',
    'translate.google.cat',
    'translate.google.cc',
    'translate.google.cd',
    'translate.google.cf',
    'translate.google.cg',
    'translate.google.ch',
    'translate.google.ci',
    'translate.google.cl',
    'translate.google.cm',
    'translate.google.cn',
    'translate.google.co.ao',
    'translate.google.co.bw',
    'translate.google.co.ck',
    'translate.google.co.cr',
    'translate.google.co.id',
    'translate.google.co.il',
    'translate.google.co.in',
    'translate.google.co.jp',
    'translate.google.co.ke',
    'translate.google.co.kr',
    'translate.google.co.ls',
    'translate.google.co.ma',
    'translate.google.co.mz',
    'translate.google.co.nz',
    'translate.google.co.th',
    'translate.google.co.tz',
    'translate.google.co.ug',
    'translate.google.co.uk',
    'translate.google.co.uz',
    'translate.google.co.ve',
    'translate.google.co.vi',
    'translate.google.co.za',
    'translate.google.co.zm',
    'translate.google.co.zw',
    'translate.google.com.af',
    'translate.google.com.ag',
    'translate.google.com.ai',
    'translate.google.com.ar',
    'translate.google.com.au',
    'translate.google.com.bd',
    'translate.google.com.bh',
    'translate.google.com.bn',
    'translate.google.com.bo',
    'translate.google.com.br',
    'translate.google.com.bz',
    'translate.google.com.co',
    'translate.google.com.cu',
    'translate.google.com.cy',
    'translate.google.com.do',
    'translate.google.com.ec',
    'translate.google.com.eg',
    'translate.google.com.et',
    'translate.google.com.fj',
    'translate.google.com.gh',
    'translate.google.com.gi',
    'translate.google.com.gt',
    'translate.google.com.hk',
    'translate.google.com.jm',
    'translate.google.com.kh',
    'translate.google.com.kw',
    'translate.google.com.lb',
    'translate.google.com.ly',
    'translate.google.com.mm',
    'translate.google.com.mt',
    'translate.google.com.mx',
    'translate.google.com.my',
    'translate.google.com.na',
    'translate.google.com.ng',
    'translate.google.com.ni',
    'translate.google.com.np',
    'translate.google.com.om',
    'translate.google.com.pa',
    'translate.google.com.pe',
    'translate.google.com.pg',
    'translate.google.com.ph',
    'translate.google.com.pk',
    'translate.google.com.pr',
    'translate.google.com.py',
    'translate.google.com.qa',
    'translate.google.com.sa',
    'translate.google.com.sb',
    'translate.google.com.sg',
    'translate.google.com.sl',
    'translate.google.com.sv',
    'translate.google.com.tj',
    'translate.google.com.tr',
    'translate.google.com.tw',
    'translate.google.com.ua',
    'translate.google.com.uy',
    'translate.google.com.vc',
    'translate.google.com.vn',
    'translate.google.com',
    'translate.google.cv',
    'translate.google.cz',
    'translate.google.de',
    'translate.google.dj',
    'translate.google.dk',
    'translate.google.dm',
    'translate.google.dz',
    'translate.google.ee',
    'translate.google.es',
    'translate.google.fi',
    'translate.google.fm',
    'translate.google.fr',
    'translate.google.ga',
    'translate.google.ge',
    'translate.google.gg',
    'translate.google.gl',
    'translate.google.gm',
    'translate.google.gp',
    'translate.google.gr',
    'translate.google.gy',
    'translate.google.hn',
    'translate.google.hr',
    'translate.google.ht',
    'translate.google.hu',
    'translate.google.ie',
    'translate.google.im',
    'translate.google.iq',
    'translate.google.is',
    'translate.google.it',
    'translate.google.je',
    'translate.google.jo',
    'translate.google.kg',
    'translate.google.ki',
    'translate.google.kz',
    'translate.google.la',
    'translate.google.li',
    'translate.google.lk',
    'translate.google.lt',
    'translate.google.lu',
    'translate.google.lv',
    'translate.google.md',
    'translate.google.me',
    'translate.google.mg',
    'translate.google.mk',
    'translate.google.ml',
    'translate.google.mn',
    'translate.google.ms',
    'translate.google.mu',
    'translate.google.mv',
    'translate.google.mw',
    'translate.google.ne',
    'translate.google.nl',
    'translate.google.no',
    'translate.google.nr',
    'translate.google.nu',
    'translate.google.pl',
    'translate.google.pn',
    'translate.google.ps',
    'translate.google.pt',
    'translate.google.ro',
    'translate.google.rs',
    'translate.google.ru',
    'translate.google.rw',
    'translate.google.sc',
    'translate.google.se',
    'translate.google.sh',
    'translate.google.si',
    'translate.google.sk',
    'translate.google.sm',
    'translate.google.sn',
    'translate.google.so',
    'translate.google.sr',
    'translate.google.st',
    'translate.google.td',
    'translate.google.tg',
    'translate.google.tk',
    'translate.google.tl',
    'translate.google.tm',
    'translate.google.tn',
    'translate.google.to',
    'translate.google.tt',
    'translate.google.us',
    'translate.google.vg',
    'translate.google.vu',
    'translate.google.ws',
)


class Provider(LocalProvider, SoupProvider):
    name = 'google'
    prettyname = 'Google'

    capabilities = ProviderCapability.TRANSLATION | ProviderCapability.TTS
    features = ProviderFeature.DETECTION | ProviderFeature.MISTAKES | ProviderFeature.PRONUNCIATION

    defaults = {
        'instance_url': '',
        'api_key': '',
        'src_langs': ['en', 'fr', 'es', 'de'],
        'dest_langs': ['fr', 'es', 'de', 'en'],
    }

    _service_urls = DEFAULT_SERVICE_URLS
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://translate.google.com',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.chars_limit = 2000

    def init_trans(self, on_done, on_fail):
        languages = [
            'af',
            'sq',
            'am',
            'ar',
            'hy',
            'az',
            'eu',
            'be',
            'bn',
            'bs',
            'bg',
            'ca',
            'ceb',
            'ny',
            'zh-CN',
            'zh-TW',
            'co',
            'hr',
            'cs',
            'da',
            'nl',
            'en',
            'eo',
            'et',
            'tl',
            'fi',
            'fr',
            'fy',
            'gl',
            'ka',
            'de',
            'el',
            'gu',
            'ht',
            'ha',
            'haw',
            'iw',
            'hi',
            'hmn',
            'hu',
            'is',
            'ig',
            'id',
            'ga',
            'it',
            'ja',
            'jw',
            'kn',
            'kk',
            'km',
            'rw',
            'ko',
            'ku',
            'ky',
            'lo',
            'la',
            'lv',
            'lt',
            'lb',
            'mk',
            'mg',
            'ms',
            'ml',
            'mt',
            'mi',
            'mr',
            'mn',
            'my',
            'ne',
            'no',
            'or',
            'ps',
            'fa',
            'pl',
            'pt',
            'pa',
            'ro',
            'ru',
            'sm',
            'gd',
            'sr',
            'st',
            'sn',
            'sd',
            'si',
            'sk',
            'sl',
            'so',
            'es',
            'su',
            'sw',
            'sv',
            'tg',
            'ta',
            'tt',
            'te',
            'th',
            'tr',
            'tk',
            'uk',
            'ur',
            'ug',
            'uz',
            'vi',
            'cy',
            'xh',
            'yi',
            'yo',
            'zu',
        ]
        for code in languages:
            self.add_lang(code)

        on_done()

    def init_tts(self, on_done, on_fail):
        for code in lang.tts_langs().keys():
            self.add_lang(code, trans_src=False, trans_dest=False, tts=True)

        on_done()

    @staticmethod
    def _build_rpc_request(text: str, src: str, dest: str):
        return json.dumps(
            [
                [
                    [
                        RPC_ID,
                        json.dumps([[text, src, dest, True], [None]], separators=(',', ':')),
                        None,
                        'generic',
                    ],
                ]
            ],
            separators=(',', ':'),
        )

    def _pick_service_url(self):
        if len(self._service_urls) == 1:
            return self._service_urls[0]
        return random.choice(self._service_urls)

    @property
    def translate_url(self):
        url = TRANSLATE_RPC.format(host=self._pick_service_url()) + '?'
        params = {
            'rpcids': RPC_ID,
            'bl': 'boq_translate-webserver_20201207.13_p0',
            'soc-app': '1',
            'soc-platform': '1',
            'soc-device': '1',
            'rt': 'c',
        }

        return self.format_url(url, params=params)

    def translate(self, text, src_lang, dest_lang, on_done, on_fail):
        def on_response(data):
            try:
                token_found = False
                square_bracket_counts = [0, 0]
                resp = ''
                data = data.decode('utf-8')

                for line in data.split('\n'):
                    token_found = token_found or f'"{RPC_ID}"' in line[:30]
                    if not token_found:
                        continue

                    is_in_string = False
                    for index, char in enumerate(line):
                        if char == '\"' and line[max(0, index - 1)] != '\\':
                            is_in_string = not is_in_string
                        if not is_in_string:
                            if char == '[':
                                square_bracket_counts[0] += 1
                            elif char == ']':
                                square_bracket_counts[1] += 1

                    resp += line
                    if square_bracket_counts[0] == square_bracket_counts[1]:
                        break

                data = json.loads(resp)
                parsed = json.loads(data[0][2])
                translated_parts = None
                translated = None
                try:
                    translated_parts = list(
                        map(
                            lambda part: TranslatedPart(
                                part[0] if len(part) > 0 else '', part[1] if len(part) >= 2 else []
                            ),
                            parsed[1][0][0][5],
                        )
                    )
                except TypeError:
                    translated_parts = [
                        TranslatedPart(parsed[1][0][1][0], [parsed[1][0][0][0], parsed[1][0][1][0]])
                    ]

                first_iter = True
                translated = ""
                for part in translated_parts:
                    if not part.text.isspace() and not first_iter:
                        translated += " "
                    if first_iter:
                        first_iter = False
                    translated += part.text

                src = None
                try:
                    src = parsed[1][-1][1]
                except (IndexError, TypeError):
                    pass

                if not src == src_lang:
                    on_fail(ProviderError(ProviderErrorCode.TRANSLATION_FAILED, 'source language mismatch'))
                    return

                if src == 'auto':
                    try:
                        if parsed[0][2] in self.src_languages:
                            src = parsed[0][2]
                    except (IndexError, TypeError):
                        pass

                dest = None
                try:
                    dest = parsed[1][-1][2]
                except (IndexError, TypeError):
                    pass

                if not dest == dest_lang:
                    on_fail(ProviderError(ProviderErrorCode.TRANSLATION_FAILED, 'destination language mismatch'))
                    return

                origin_pronunciation = None
                try:
                    origin_pronunciation = parsed[0][0]
                except (IndexError, TypeError):
                    pass

                pronunciation = None
                try:
                    pronunciation = parsed[1][0][0][1]
                except (IndexError, TypeError):
                    pass

                mistake = None
                try:
                    mistake = parsed[0][1][0][0][1]
                    # Convert to pango markup
                    mistake = mistake.replace('<em>', '<b>').replace('</em>', '</b>')
                except (IndexError, TypeError):
                    pass

                result = Translation(
                    translated,
                    (text, src, dest),
                    src,
                    (mistake, self._strip_html_tags(mistake)),
                    (origin_pronunciation, pronunciation),
                )
                on_done(result)

            except Exception as exc:
                logging.warning(exc)
                on_fail(ProviderError(ProviderErrorCode.TRANSLATION_FAILED, str(exc)))

        # Form data
        data = {
            'f.req': self._build_rpc_request(text, src_lang, dest_lang),
        }

        # Request message
        message = self.create_message('POST', self.translate_url, data, self._headers, True)

        # Do async request
        self.send_and_read_and_process_response(message, on_response, on_fail, False, False)

    def _strip_html_tags(self, text):
        """Strip html tags"""
        if text is None:
            return None

        tags_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        tags_removed = tags_re.sub('', text)
        escaped = html.escape(tags_removed)
        return escaped

    def speech(self, text, language, on_done, on_fail):
        def work():
            try:
                file = NamedTemporaryFile()
                tts = gTTS(text, lang=language, lang_check=False)
                tts.write_to_fp(file)
                file.seek(0)

                on_done(file)
            except Exception as exc:
                logging.warning(exc)
                on_fail(ProviderError(ProviderErrorCode.TTS_FAILED, str(exc)))

        self.launch_thread(work)


class TranslatedPart:
    def __init__(self, text: str, candidates: List[str]):
        self.text = text
        self.candidates = candidates

    def __str__(self):
        return self.text

    def __dict__(self):
        return {
            'text': self.text,
            'candidates': self.candidates,
        }
