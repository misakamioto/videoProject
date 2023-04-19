import re
# reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
# str = 'MAC.Error("vod","35073","最强主宰动态漫画 zykyun 第02集 https://cdn11.yzzy-tv-cdn.com/share/5434d832e0dd3baab78c581eb7414b31");return false;'
# print(re.findall(reg,str))
# a_list = ["sfsaf","4545","fsfd"]
# print(type(str(a_list)))
str = "https://1080zyk.com/?m=vod-detail-id-95656546.html"
ret = re.match('.*/?m=vod-detail-id-(\d+)\.html', str)
print(ret.group(1))
