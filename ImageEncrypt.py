# 图片(伪)加密器
# 原理：建立一个映射关系，每一种颜色都唯一的对应另一种颜色（这个映射关系就是密码）。然后按照这种关系替换图片中每一个像素的颜色（这就是加密）。只要再反向替换像素颜色就可以解密。
# 经过实验发现，“加密”后的图片仍然会显示出一些图形轮廓（特别是一些颜色单一的图片），所以本程序并不能做真正意义上的加密。(也许可以用来防和谐)
# 加密出来的图片必须使用PNG或其他无损格式（使用JPG等有损压缩格式会导致图片损坏），目前只支持24位真彩色。（32位色彩将保持透明度不变，如果程序出错请检查图片位深度）

from PIL import Image
import random
import pickle

def createPassword():
    savePath = input('输入密码文件保存路径：')
    print('创建映射表……')
    pwdList = list(range(16777216)) 
    # 列表的索引和元素即表示各种颜色的对应关系
    # Example:
    # pwdList[114514] == 1919810 即表示把颜色114514替换成1919810
    print('打乱顺序……')
    for i in range(17000000):#随机替换次数，可以提高这个次数使密码更随机，但是会耗费更多时间。
        x,y = random.randint(0,16777215),random.randint(0,16777215)
        pwdList[x],pwdList[y]=pwdList[y],pwdList[x]
    print('保存密码……')
    with open(savePath,'wb') as pkl:
        pickle.dump(pwdList,pkl) #用pickle保存列表
    print('完成！')

def encrypt():
    inputPath = input('请输入原图片路径：')
    keyPath = input('请输入密码文件路径：')
    outputPath = input('请输入加密图片保存路径（扩展名必须为png等无损格式）：')
    print('载入图片……')
    im = Image.open(inputPath)
    width, height = im.size
    byteDepth = len(im.getpixel((0, 0)))#检查图片位深度
    print('载入密码……')
    with open(keyPath,'rb') as pkl:
        pwdList = pickle.load(pkl)
    print('加密中……')
    for y in range(height):
        for x in range(width):
            if byteDepth == 3:
                red, green, blue = im.getpixel((x, y))
                origcode = red*(16**4)+green*(16**2)+blue #rgb值换算成数字
                enccode = pwdList[origcode]#替换数字（加密）
                r,g,b = enccode//(16**4),(enccode%(16**4))//(16**2),enccode%(16**2)#数字换成rgb
                im.putpixel((x, y),(r,g,b))
            elif byteDepth == 4:#如果位深度为32，则保持透明度不变
                red, green, blue, alpha = im.getpixel((x, y))
                origcode = red*(16**4)+green*(16**2)+blue #rgb值换算成数字
                enccode = pwdList[origcode]#替换数字（加密）
                r,g,b = enccode//(16**4),(enccode%(16**4))//(16**2),enccode%(16**2)#数字换成rgb
                im.putpixel((x, y),(r,g,b,alpha))
            else:
                print('不支持该图像色彩！')
                break
    print('保存图片……')
    im.save(outputPath)
    print('完成！')
    
def decrypt():
    inputPath = input('请输入加密图片路径（扩展名必须为png等无损格式）：')
    keyPath = input('请输入密码文件路径：')
    outputPath = input('请输入解密图片保存路径：')
    print('载入图片……')
    im = Image.open(inputPath)
    width, height = im.size
    byteDepth = len(im.getpixel((0, 0)))#检查图片位深度
    print('载入密码……')
    with open(keyPath,'rb') as pkl:
        pwdList = pickle.load(pkl)
    declist = list(range(16777216))
    for i in range(16777216):
        declist[pwdList[i]]=i #列表索引与元素互换，便于解密
    del(pwdList)
    print('解密中……')
    for y in range(height):
        for x in range(width):
            if byteDepth == 3:
                red, green, blue = im.getpixel((x, y))
                enccode = red*(16**4)+green*(16**2)+blue #rgb值换算成数字
                deccode = declist[enccode] #解密
                r,g,b = deccode//(16**4),(deccode%(16**4))//(16**2),deccode%(16**2)#数字换成rgb
                im.putpixel((x, y),(r,g,b))
            elif byteDepth == 4:#如果位深度为32，则保持透明度不变
                red, green, blue, alpha = im.getpixel((x, y))
                enccode = red*(16**4)+green*(16**2)+blue #rgb值换算成数字
                deccode = declist[enccode] #解密
                r,g,b = deccode//(16**4),(deccode%(16**4))//(16**2),deccode%(16**2)#数字换成rgb
                im.putpixel((x, y),(r,g,b,alpha))     
            else:
                print('不支持该图像色彩！')
                break
    print('保存图片……')
    im.save(outputPath)
    print('完成！')

print('图片加密器 V1.0')
while True:
    print('''请输入指令：
1 - 创建密码
2 - 加密
3 - 解密
4 - 退出''')
    cmd = input()
    if cmd == '1':
        createPassword()
    elif cmd == '2':
        encrypt()
    elif cmd == '3':
        decrypt()
    elif cmd == '4':
        break
    else:
        print('指令有误，请重新输入。')