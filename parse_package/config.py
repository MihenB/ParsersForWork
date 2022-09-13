from proxy import protocol, login, password, ip, port

proxies_with_password = {
    f'{protocol}': f'{protocol}://{login}:{password}@{ip}:{port}'
}

# Added sing in by ip
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "_proxies",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = f"""
var config = {{
        mode: "fixed_servers",
        rules: {{
        singleProxy: {{
            scheme: "{protocol}",
            host: "{ip}",
            port: parseInt({port})
        }},
        bypassList: ["localhost"]
        }}
    }};

chrome._proxies.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{login}",
            password: "{password}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {{urls: ["<all_urls>"]}},
            ['blocking']
);
"""

cookies = {
    '__lhash_': '58530b71f44858649bd7be11e90f8d12',
    'CACHE_INDICATOR': 'false',
    'COMPARISON_INDICATOR': 'false',
    'HINTS_FIO_COOKIE_NAME': '1',
    'MVID_AB_SERVICES_DESCRIPTION': 'var2',
    'MVID_ADDRESS_COMMENT_AB_TEST': '2',
    'MVID_BLACK_FRIDAY_ENABLED': 'true',
    'MVID_CALC_BONUS_RUBLES_PROFIT': 'true',
    'MVID_CART_MULTI_DELETE': 'true',
    'MVID_CATALOG_STATE': '1',
    'MVID_CITY_ID': 'CityCZ_1638',
    'MVID_FILTER_CODES': 'true',
    'MVID_FILTER_TOOLTIP': '1',
    'MVID_FLOCKTORY_ON': 'true',
    'MVID_GEOLOCATION_NEEDED': 'true',
    'MVID_GET_LOCATION_BY_DADATA': 'DaData',
    'MVID_GIFT_KIT': 'true',
    'MVID_GTM_DELAY': 'true',
    'MVID_GUEST_ID': '21264116896',
    'MVID_IS_NEW_BR_WIDGET': 'true',
    'MVID_KLADR_ID': '7800000000000',
    'MVID_LAYOUT_TYPE': '1',
    'MVID_LP_HANDOVER': '2',
    'MVID_LP_SOLD_VARIANTS': '3',
    'MVID_MCLICK': 'true',
    'MVID_MINDBOX_DYNAMICALLY': 'true',
    'MVID_MINI_PDP': 'true',
    'MVID_MOBILE_FILTERS': 'true',
    'MVID_NEW_ACCESSORY': 'true',
    'MVID_NEW_DESKTOP_FILTERS': 'true',
    'MVID_NEW_LK': 'true',
    'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
    'MVID_NEW_LK_LOGIN': 'true',
    'MVID_NEW_LK_OTP_TIMER': 'true',
    'MVID_NEW_MBONUS_BLOCK': 'true',
    'MVID_REGION_ID': '6',
    'MVID_REGION_SHOP': 'S904',
    'MVID_SERVICES': '111',
    'MVID_SERVICES_MINI_BLOCK': 'var2',
    'MVID_TAXI_DELIVERY_INTERVALS_VIEW': 'new',
    'MVID_TIMEZONE_OFFSET': '3',
    'MVID_WEBP_ENABLED': 'true',
    'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
    'PICKUP_SEAMLESS_AB_TEST': '2',
    'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'false',
    'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
    'flacktory': 'no',
    'searchType2': '1',
    '_gid': 'GA1.2.1315951416.1660698195',
    '_ym_d': '1660698195',
    '_ym_uid': '1660698195287052004',
    '_ym_isad': '1',
    'admitad_deduplication_cookie': 'yandex.ru__organic',
    '__SourceTracker': 'yandex.ru__organic',
    'authError': '',
    'SMSError': '',
    'tmr_lvid': '8e548a59c0a46e5c7e719d4aa1b90152',
    'tmr_lvidTS': '1660698198438',
    'advcake_track_id': 'aa77e6a4-ba6d-4912-b7fd-69afcb06ebd1',
    'advcake_session_id': '944708d8-2eb4-c610-7a4a-d7a343307a97',
    'st_uid': '324877255f7c6977b533a4ade2cf0e15',
    'uxs_uid': '61b21980-1dc8-11ed-93b7-015108d003bf',
    'flocktory-uuid': 'd037278b-d31c-42b9-b713-8868ab6a4728-7',
    'afUserId': '7a621ad2-8846-4b35-a5ca-74fb8160c9dc-p',
    'AF_SYNC': '1660698199747',
    'BIGipServeratg-ps-prod_tcp80': '2466569226.20480.0000',
    'bIPs': '-314595793',
    '_dc_gtm_UA-1873769-1': '1',
    '_dc_gtm_UA-1873769-37': '1',
    'JSESSIONID': 'YnlDv82YhD114wfJmy3TW4LDv18Gd2jnSbC0bzmkcP5bnS8dH1Bv!-271293665',
    '_ga_CFMZTSS5FM': 'GS1.1.1660698195.1.1.1660698271.0.0.0',
    '_ga_BNX5WPP3YK': 'GS1.1.1660698195.1.1.1660698271.56.0.0',
    '_ga': 'GA1.2.908189133.1660698195',
    'tmr_reqNum': '22',
    'tmr_detect': '0%7C1660698276860',
    'MVID_ENVCLOUD': 'prod2',
}

headers = {
    'authority': 'www.mvideo.ru',
    'accept': 'application/json',
    'accept-language': 'ru,en;q=0.9',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '70c9f3d713934fd89d614801a0d5de49-87e6b4bcbf058018-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36',
    'x-set-application-id': 'bd48099c-4597-434c-952b-806c68a21bbb',
}

json_data = {
    'productIds': [
        '10026917',
        '10026091',
        '10026916',
        '10026823',
        '10030692',
        '10026824',
        '10030404',
        '10026884',
        '10030419',
        '10026092',
        '10026777',
        '10024694',
        '10024440',
        '10031005',
        '10029728',
        '10026655',
        '10021728',
        '10031229',
        '10031228',
        '10031225',
        '10024441',
        '10026988',
        '10031293',
        '10030239',
    ],
    'mediaTypes': [
        'images',
    ],
    'category': True,
    'status': True,
    'brand': True,
    'propertyTypes': [
        'KEY',
    ],
    'propertiesConfig': {
        'propertiesPortionSize': 5,
    },
    'multioffer': False,
}

url = 'https://2ip.ru/'

if __name__ == '__main__':
    print()
