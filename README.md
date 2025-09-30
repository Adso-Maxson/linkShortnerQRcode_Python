Simple code to shorten URL and generate QR code from the shortened link.

The software tests the following link shortening servers:
            "http://tinyurl.com",
            "Is.gd": "http://is.gd",
            "Da.gd": "http://da.gd",
            "Chilp.it": "http://chilp.it",
            "Clck.ru": "http://clck.ru",
            "Qps.ru": "http://qps.ru",
            "Ouo.io": "http://ouo.io",
            "0x0.st": "http://0x0.st",
            # NOVAS URLs ADICIONADAS:
            "Shrturi.com": "https://shrturi.com",
            "Cleanuri.com": "https://cleanuri.com",
            "Shortest.cx": "https://shortest.cx",
            "T.ly": "https://t.ly",
            "Picsee.io": "https://picsee.io",
            "Kutt.it": "https://kutt.it",
            "Zws.im": "https://zws.im",
            "Tiny.cc": "https://tiny.cc",
            "Shorturl.at": "https://shorturl.at",
            "V.gd": "https://v.gd",
            "Small.sx": "https://small.sx",
            "Link.sx": "https://link.sx",
            "Hmm.sx": "https://hmm.sx",
            "Pty.sx": "https://pty.sx",
            "Sqzk.ru": "https://sqzk.ru",
If the server successfully connects, it uses the generated link to create a QR code.

needs:
pip install cx_freeze pyshorteners qrcode[pil] Pillow
