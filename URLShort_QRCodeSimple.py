import pyshorteners
import qrcode

# Encurtar URL
url_original = "https://www.exemplo.com"
shortener = pyshorteners.Shortener()
url_encurtada = shortener.tinyurl.short(url_original)

print(f"URL encurtada: {url_encurtada}")

# Gerar QR Code
qr = qrcode.make(url_encurtada)
qr.save("qrcode_url_encurtada.png")
print("QR code gerado: qrcode_url_encurtada.png")