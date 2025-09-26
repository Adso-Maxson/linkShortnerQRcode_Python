Simple code to shorten URL and generate QR code from the shortened link.

The software tests the following link shortening servers:
TinyURL
ls.gd
Da.gd 
Chilp.it 
Clck.ru 
Qps.ru
Ouo.io 
Git.io
If the server successfully connects, it uses the generated link to create a QR code.

needs:
pip install cx_freeze pyshorteners qrcode[pil] Pillow
