g = ['и','а','у','о','ы','э','ю','я','е','ё']
g1 = ['И','А','У','О','Ы','Э','Ю','Я','Е','Ё']
s = ['б','в','д','г','ж','з','й','к','л','н','м','п','р','с','т','ф','х','ц','ч','ш','щ']
s1 = ['Б','В','Д','Г','Ж','З','Й','К','Л','Н','М','П','Р','С','Т','Ф','Х','Ц','Ч','Ш','Щ']
print("******************************")
print("&&&Я ТВОЙ ТЕКСТ ЩИФРОВАЛ!!!&&&")
print("##############################")
print("=======Arkadiy Savelev========")
print("Введи свойт текст только на русском, по братски)")
word=input()
def decr(word):
  kek = ""
  for i in word:
    if i in g:
      dex = g.index(i)
      kek += g[dex-5]
    elif i in g1:
      dex = g1.index(1)
      kek += g1[dex-5]
    elif i in s:
      dex=s.index(i)
      kek+=s[dex-4]
    elif i in s1:
      dex=s1.index(i)
      kek+=s1[dex-4]
    else:
      kek += i
  return kek
def encr(word):
  kek = ""
  for i in word:
    if i in g:
      dex = g.index(i)%len(g)
      kek += g[(dex+5)%len(g)]
    elif i in g1:
      dex = g1.index(i)%len(g1)
      kek += blst[(dex+5)%len(g1)]
    elif i in s:
      dex = s.index(i)%len(s)
      kek += s[(dex+4)%len(s)]
    elif i in s1:
      dex = s1.index(i)%len(s1)
      kek += s1[(dex+4)%len(s1)]
    else:
      kek += i
  return kek
print("Введи 1, чтобы показать зашифрованный текст")
print("Введи 0, чтобы выйти")
n=int(input())
if n==1:
  print(decr(word))
else:
  pass
