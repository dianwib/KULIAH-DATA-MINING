import urllib as link
html = link.urlopen("http://surabaya.tribunnews.com/topic/berita-gresik?&page=").read()
print (html)