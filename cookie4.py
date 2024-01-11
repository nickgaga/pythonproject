import urllib.parse

data = "Lat%3A 41.4628487%2C Long%3A 15.5257368"

# Decodifica i dati utilizzando urllib.parse.unquote()
decoded_data = urllib.parse.unquote(data)

print(decoded_data)
