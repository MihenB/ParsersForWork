TOR_PORT_CONFIG = (
    {
        "Socks": 9070,
        "Control": 9071
    },
    {
        "Socks": 9062,
        "Control": 9063
    },
    {
        "Socks": 9065,
        "Control": 9066
    },
    {
        "Socks": 9067,
        "Control": 9068
    },
    {
        "Socks": 9072,
        "Control": 9073
    }
)

THREADS_COUNT = len(TOR_PORT_CONFIG)
CRAWLER_SWITCH = 23000  # Equals to IS_CRAWLER_AUTO_ROTATE = False
# IS_CRAWLER_AUTO_ROTATE = False
