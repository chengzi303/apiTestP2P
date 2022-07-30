from bs4 import BeautifulSoup

html = """
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""
soup=BeautifulSoup(html, 'html.parser')

# 获取title对象
print(soup.title)
# 获取title标签名称
print(soup.title.name)
# 获取title值
print(soup.title.string)

# 获取p标签对象
print(soup.p)
# 获取p标签所有
print(soup.find_all('p'))
# 获取p标签第一个id属性值
print(soup.p['id'])

# 依次打印所有a标签的href值和a标签的值
for s in soup.find_all('a'):
    print("href={} text={}".format(s['href'], s.string))