
import requests
from bs4 import BeautifulSoup

url = "https://nitdgp.ac.in/"
r = requests.get(url)

htmlContent = r.content
print(htmlContent)

soup = BeautifulSoup(htmlContent, 'html.parser')

print(soup.prettify())

title = soup.title
print(type(title.string))
print(type(soup))
print(type(title))

paras = soup.find_all('p')
print(paras)
