

"""

用于辅助其他函数完成功能的函数

get_abs_path 获取项目的绝对路径 用于引用项目内文件
cooldown 为脚本提供冷却的装饰器
draw_text_center 为绘制文本提供居中写法
load_songs 用于加载乐曲数据
search_song 通过给定关键词返回歌曲信息列表 <-可以使用sqlite替换csv更快速读取
get_cover_image 通过歌曲url下载歌曲封面 <-可以把封面本地化
input_bg 对歌曲封面进行模糊化与裁剪处理
{...}_load 加载用于绘制的素材
paste_me 绘制水印
draw_song_card 用于绘制单曲信息卡片
draw_score_card 用于绘制单曲成绩卡片
paste_single 绘制单曲成绩并作处理
player_info 绘制指定玩家的顶部信息栏  <-可改成官方接口
paste_b50 通过调用水鱼接口获取玩家简略成绩 并绘制指定用户best50
paste_grades 通过玩家给定关键词并调用全部成绩获取指定用户的等级分数列表
"""
import os
import time
import csv
import json
import random
from PIL import Image, ImageDraw, ImageFont,ImageFilter,ImageEnhance
from nonebot import get_driver
from .records import get_b50,get_full_grade
import requests
requests.packages.urllib3.disable_warnings()
from io import BytesIO
config = get_driver().config
botname=next(iter(config.nickname))
#获得项目绝对路径
def get_abs_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(base_dir))
    return project_dir

#读取水鱼有 但是dxrting.csv未记录歌曲id
with open(rf"{get_abs_path()}/data/wmc/datasets/extra.json","r",encoding="utf-8") as f:
    extra=json.load(f)

#版本映射
version={
    "maimai": "maimai.png",
    "maimai PLUS": "maimai-plus.png",
    "GreeN": "green.png",
    "GreeN PLUS": "green-plus.png",
    "ORANGE": "orange.png",
    "ORANGE PLUS": "orange-plus.png",
    "PiNK": "pink.png",
    "PiNK PLUS": "pink-plus.png",
    "MURASAKi": "murasaki.png",
    "MURASAKi PLUS": "murasaki-plus.png",
    "MiLK": "milk.png",
    "MiLK PLUS": "milk-plus.png",
    "FiNALE": "finale.png",
    "maimaiでらっくす": "maimaidx.png",
    "maimaiでらっくす PLUS": "maimaidx-plus.png",
    "Splash": "splash.png",
    "Splash PLUS": "splash-plus.png",
    "UNiVERSE": "universe.png",
    "UNiVERSE PLUS": "universe-plus.png",
    "FESTiVAL": "festival.png",
    "FESTiVAL PLUS": "festival-plus.png",
    "BUDDiES": "buddies.png",
    "BUDDiES PLUS": "buddies-plus.png",
    "PRiSM": "prism.png",
    "PRiSM PLUS": "prism-plus.png",
    "CiRCLE": "circle.png",
    "CiRCLE PLUS": "circle-plus.png"
}


#所需的文件目录
TITLE_DIR = rf"{get_abs_path()}/data/wmc/materials/version-title/"
BG_DIR=rf"{get_abs_path()}/data/wmc/materials/version-bg/"
DX_DIR=rf"{get_abs_path()}/data/wmc/materials/isdx/"
SSS_DIR=rf"{get_abs_path()}/data/wmc/materials/ev/"
RT_DIR=rf"{get_abs_path()}/data/wmc/materials/rtframe/"
STAR_DIR=rf"{get_abs_path()}/data/wmc/materials/star/"
FC_DIR=rf"{get_abs_path()}/data/wmc/materials/isfc/"
FDX_DIR=rf"{get_abs_path()}/data/wmc/materials/isfdx/"
COVER_DIR=rf"{get_abs_path()}/data/wmc/materials/covers/"
PLATE_DIR=rf"{get_abs_path()}/data/wmc/materials/plate"


W = 800  # 宽度（横版）
H = 600  # 高度
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
LINE_COLOR = (255, 255, 255)
FONT_PATH = rf"{get_abs_path()}/data/Fonts/msyhbd.ttc"
DIFF_INDEX={"BASIC":0, "ADV":1,
              "EXP":2,
              "MST":3,
              "REM":4}
DIFF_COLOR = [(80, 200, 120), (255, 220, 100),
              (220, 80, 80),
              (160, 100, 180),
              (190, 160, 210)]


#cd控制装饰器 使用此装饰器要在开头多传入一个用户标识符(uid\gid)
def cooldown(cd_seconds,tip=True):
    cd_dict = {}
    tip_flag = True

    def decorator(func):
        async def wrapper(uid,handler,*args,**kwargs):
            nonlocal tip_flag
            now = time.time()
            if uid not in cd_dict:
                cd_dict[uid] = 0

            if cd_dict[uid] > now:
                if tip_flag and tip:
                    tip_flag = False
                    await handler.finish(f"太急啦，{int(cd_dict[uid]-now)}秒后再试试吧~")
                return

            cd_dict[uid] = now + cd_seconds
            tip_flag = True
            await func(handler,*args,**kwargs)

        return wrapper
    return decorator


#draw.text的居中写法
def draw_text_center(draw, text, font, box, fill="white"):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = box[0] + (box[2] - box[0] - text_w) / 2
    y = box[1] + (box[3] - box[1] - text_h) / 2
    draw.text((x, y), text, font=font, fill=fill)



#在 dxrating.csv 中读取乐曲数据
def load_songs(csv_path):
    songs = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    return songs

# 加载一下歌曲 下面很多地方要用歌曲查询
songs:list = load_songs(rf"{get_abs_path()}/data/wmc/datasets/dxdata.csv")


#在给定中搜索指定关键词的乐曲数据 优先级为 id/title/alias 如果 使用alias查询会有多个选项
def search_song(keyword):
    keyword = keyword.strip().lower()
    result = []

    for s in songs:
        sid = s["internalId"].strip().lower()
        if keyword=='?':
            break
        if keyword == sid:
            return [s]

    for s in songs:
        title = s["曲名"].strip().lower()
        if keyword == title:
            result.append(s)
    for s in songs:
        alias = s["别名"].strip().lower().split(" \ ")
        if keyword in alias:
            if s not in result:
                result.append(s)

    return result

#用于使用别名查询的情况 输出字符串
def multi_output(result):
    if len(result)==0:
        return "未找到该曲目！"
    selectstr = "您想寻找的可能是:\n"
    for s in result:
        selectstr += (f"{s['internalId']} {s['曲名']}\n")
    selectstr += "(=^･ω･^=)直接通过id查找就好啦~"
    return selectstr

#使用在search_info() 中查询到的reid 从dxrating.net的图片接口中下载歌曲封面
def get_cover_image(image_reid):
    try:
        """url = f"https://shama.dxrating.net/images/cover/v2/{image_name}.jpg"
        resp = requests.get(url, timeout=10,verify=False)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img = img.resize((160, 160), Image.Resampling.LANCZOS)"""

        img = Image.open(COVER_DIR + f"{image_reid}.png")
        return img
    except Exception as e:
        print(e)
        return Image.new("RGB", (160, 160), (200, 200, 200))



#模糊化歌曲封面并将封面裁剪为bg_size 通常用于卡牌背景
def input_bg(img,bg_size=(800, 600), blur_radius=15, alpha=250):
    wh=max(bg_size)
    img=img.resize((wh,wh))
    w, h = bg_size
    max_side = max(w, h)
    left = (max_side-w) // 2
    top = (max_side-h) // 2
    img_crop = img.crop((left, top, left+w, top+h))
    img_blur = img_crop.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img_blur.putalpha(alpha)
    img=ImageEnhance.Brightness(img_blur).enhance(0.7)
    return img


#加载 指定版本 标题页面
def version_title_load(ver):
    ver=version[ver]
    img=Image.open(TITLE_DIR+f"{ver}").convert("RGBA").resize((150,75))
    return img

#加载 标准乐谱/dx乐谱 标识
def dx_load(s):
    if s=="std":
        img=Image.open(DX_DIR+"std.png").convert("RGBA").resize((70,25))
        return img
    if s=="dx":
        img=Image.open(DX_DIR+"dx.png").convert("RGBA").resize((70,25))
        return img

#加载 评价 标识
def sss_load(s):
    img = Image.open(SSS_DIR + f"{s}.png").convert("RGBA")
    return img

#加载 rating框 标识
def rtframe_load(s):
    img = Image.open(RT_DIR + f"{s}.png").convert("RGBA")
    return img

#加载 dx星级 标识
def star_load(s):
    img = Image.open(STAR_DIR + f"{s}.png").convert("RGBA")
    return img

#加载 FC/FC+/AP/AP+ 标识
def fc_load(s):
    img=Image.open(FC_DIR+f"{s}.png").convert("RGBA")
    return img

#加载 FS/FS+/FDX/FDX+/SYNC 标识
def fdx_load(s):
    img = Image.open(FDX_DIR + f"{s}.png").convert("RGBA")
    return img

#绘制bot主水印
def paste_me(draw, size,fontsize=12):
    font= ImageFont.truetype(FONT_PATH, fontsize)
    w,h=size
    draw_text_center(draw,f"Designed by Rei / Generated by {botname}",font,(w/2-20,h-int(fontsize/2)-int(h/60),w/2+20,h-int(fontsize/2)-int(h/60)))


#绘制给定单曲卡片
def draw_song_card(song):
    """song 通过search_info 函数返回的列表值其一 也可是dxrating.csv 的某一行"""


    #读取版本对应的代表歌曲(/data/wmc/version-bg/)并作处理作为背景
    ver=song['版本']
    ver=version[ver]
    ver_bg = Image.open(BG_DIR+f"{ver}")
    img = input_bg(ver_bg)
    draw = ImageDraw.Draw(img)

    #加载所需字体
    font_title = ImageFont.truetype(FONT_PATH, 28)
    font_normal = ImageFont.truetype(FONT_PATH, 16)
    font_small = ImageFont.truetype(FONT_PATH, 12)

    #绘制上部分方框
    draw.rectangle([30, 30, W-30, 230], outline=LINE_COLOR, width=2)

    # 插入封面
    cover_img = get_cover_image(song["索引"])
    img.paste(cover_img, (40, 40))

    # h绘制右侧歌曲信息
    draw.text((220, 40), f"{song['曲名']}", fill=TEXT_COLOR, font=font_title)
    draw.text((220, 80), f"{song['曲师']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((220, 110), f"BPM：{song['BPM']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((220, 140), f"ID: {song['internalId']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((340, 110), f"版本：{song['版本']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((340, 140), f"分类：{song['分类']}", fill=TEXT_COLOR, font=font_normal)

    version_title=version_title_load(song['版本'])
    img.paste(version_title,(W-200,150),mask=version_title)

    is_dx=dx_load(song['类型'])
    img.paste(is_dx,(220,170),mask=is_dx)

    draw.text((220, 200), f"JP: {song['JP']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((280, 200), f"INT: {song['INT']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((340, 200), f"USA: {song['USA']}", fill=TEXT_COLOR, font=font_normal)
    draw.text((400, 200), f"CN: {song['CN']}", fill=TEXT_COLOR, font=font_normal)

    #绘制下部分表格
    draw.rectangle([30, 240, W - 30, H - 30], outline=LINE_COLOR, width=2)

    # 横版表格配置
    y_start = 260
    x_start = 50
    col_width = 120
    row_height = 30

    # 难度表头
    # 因为 data/wmc/data2csv.py 读取json的时候把basic映射成了bsc 但是水鱼啥的用的都是basic 所以这里变得很神秘
    diffs = ["BASIC", "ADV", "EXP", "MST", "REM"]
    diff_names = ["BSC", "ADV", "EXP", "MST", "REM"]
    x = x_start
    #循环绘制难度index
    for i, name in enumerate(diff_names):
        draw.text((x + 10+col_width, y_start), name, fill=DIFF_COLOR[i], font=font_normal)
        x += col_width
    draw.line([x_start, y_start + 25, W - 50, y_start + 25], fill=LINE_COLOR, width=1)
    y = y_start + row_height

    # 表格行数据
    rows = [
        ("Level", lambda d: f"{song[f'{d}_定数']}"),
        ("Tap", lambda d: f"{song[f'{d}_TAP']}"),
        ("Hold", lambda d: f"{song[f'{d}_HOLD']}"),
        ("Slide", lambda d: f"{song[f'{d}_SLIDE']}"),
        ("Touch", lambda d: f"{song[f'{d}_TOUCH']}"),
        ("Break", lambda d: f"{song[f'{d}_BREAK']}"),
        ("Total", lambda d: f"{song[f'{d}_TOTAL']}"),
        ("Designer", lambda d: f"{song[f'{d}_谱师']}" if d in ["EXP", "MST", "REM"] else ""),
    ]

    # 绘制每行
    for label, get_val in rows:
        draw.text((x_start, y), label, fill=TEXT_COLOR, font=font_normal) #绘制行label
        x = x_start + col_width
        for i, d in enumerate(diffs):
            val = get_val(d)
            if label=="Designer": #designer(谱师) 没有绿黄的 所以直接跳 然后布局也不一样
                if d=="BASIC" or d=="ADV":continue
                draw.text((x + 10, y), val, fill=DIFF_COLOR[i], font=font_normal)
                x+=1.5*col_width
            else:
                draw.text((x + 10, y), val, fill=DIFF_COLOR[i], font=font_normal)
                x += col_width

        draw.line([x_start, y + 25, W - 50, y + 25], fill=LINE_COLOR, width=1)
        y += row_height
    paste_me(draw,(800,600))

    return img

#绘制单曲成绩卡片
def create_score_card(
    title: str, #歌曲标题
    achieve:float, #达成率
    ds:float, #定数
    rt:int, #单曲ra
    dx:int, #dx分
    id:int, #歌曲id
    ev:str, #歌曲评价
    isfc:str, #是否fc
    isfdx:str, #是否fdx
    card_width: int = 900,
    card_height: int = 450,
    radius: int = 45,
    dif:int=3,
) -> Image.Image:
    """
    :param title: 歌曲的标题
    :param achieve: 玩家的歌曲达成率
    :param ds: 歌曲定数
    :param rt: 此曲此达成率对应的ra
    :param dx: 玩家的歌曲dx分数
    :param id: 歌曲的id
    :param ev: 玩家的达成评级 (SSS+等)
    :param isfc: 玩家的此曲联机评价 (fc/fcp/ap/app)
    :param isfdx: 玩家的此曲拼机评价 (fs/fsp/fdx/fdxp/sync)
    :param card_width: 卡宽 通常固定
    :param card_height: 卡高 通常固定
    :param radius: 卡片圆角 通常固定
    :param dif: 歌曲难度 （0/1/2/3/4 BASIC/ADV/EXP/MST/REM）
    :return:
    """


    #依旧加载字体
    font_big = ImageFont.truetype(FONT_PATH, 72)
    font_mid = ImageFont.truetype(FONT_PATH, 45)
    font_small = ImageFont.truetype(FONT_PATH, 40)

    #读取歌曲信息
    dif = next(k for k, v in DIFF_INDEX.items() if v ==dif)
    try:info=search_song(str(id))[0]
    except:
        try:info=search_song(extra[str(id)])[0] #国服提前上 json没有id的歌
        except:info=search_song("INTERNET YAMERO")[0]

    #拿到封面
    cover=get_cover_image(info["索引"])

    #歌曲的总dx分 (所有音符*3) 与星级计算
    fulldx=int(info[f"{dif}_TOTAL"])*3
    if (dx/fulldx)<0.85:
        star=0
    elif (dx/fulldx)<0.90:
        star=1
    elif (dx/fulldx)<0.95:
        star=2
    elif (dx/fulldx)<0.97:
        star=3
    elif (dx/fulldx)<0.99:
        star=4
    elif (dx/fulldx)<0.995:
        star=5
    else:star=6

    #读取 dx标识 文件 （id>10000视作dx谱）
    isdx="std" if int(id)<10000 else "dx"
    isdx_pic=dx_load(isdx).resize((210,75))

    #加载 评价标识 文件
    ev_pic=sss_load(ev).resize((250,105))

    #加载 连击/拼机评价 文件
    try:fc_pic=fc_load(isfc).resize((150,150))
    except:fc_pic=None
    try:fdx_pic=fdx_load(isfdx).resize((150,150))
    except:fdx_pic=None

    #根据star加载 星级 文件
    if 0<star<3:
        star_pic = star_load(1)  #绿星
    elif 2<star<5:
        star_pic=star_load(2)  #橙星
    else:
        star_pic=star_load(3) #金星
    star_pic=star_pic.resize((56,56))

    #初始化card  需要rgba绘制圆角
    card = Image.new("RGBA", (900,450), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    w, h = card_width, card_height

    #以歌曲封面进行处理作为背景 并绘制圆角贴在card上
    bg=input_bg(cover,(w,h))
    bg_box = (0, 0, w, h)
    bg_w, bg_h = bg_box[2] - bg_box[0], bg_box[3] - bg_box[1]
    bg = bg.convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255,width=3)
    bg.putalpha(mask)
    card.paste(bg, bg_box[:2], mask=bg)

    #贴封面
    cover_resize=cover.resize((300,300))
    card.paste(cover_resize, (25, 25))

    #绘制右侧文字
    text_x = 350
    text_y = 20
    draw.rounded_rectangle([text_x-15, text_y-10,w-20 , text_y+80],
                           radius=radius, outline=DIFF_COLOR[DIFF_INDEX[dif]],fill=DIFF_COLOR[DIFF_INDEX[dif]], width=3) #标题的容器
    draw.text((text_x, text_y), title, font=font_mid, fill="white") #标题
    draw_text_center(draw,str(id),font_mid,(text_x-280,text_y+370,text_x-80,text_y+370)) #歌曲id 在封面下方居中
    card.paste(isdx_pic, (text_x-280,text_y+280),mask=isdx_pic) #dx标识
    draw.text((text_x-5, text_y + 70), f"{achieve:.4f}%", font=font_big, fill="white") #达成率
    draw.text((text_x, text_y + 160), str(ds)+"->"+str(rt), font=font_mid, fill="white") #定数与rt
    draw.text((text_x, text_y + 220), f"{dx}/{fulldx}", font=font_mid, fill="white") #dx分

    card.paste(ev_pic,(text_x-20,text_y+300),mask=ev_pic) #评价
    star_x = text_x
    for epc in range(star):
        card.paste(star_pic,(star_x+260,text_y+190),mask=star_pic) #星级
        star_x+=50
    if fc_pic:
        card.paste(fc_pic,(text_x+230,text_y+280),mask=fc_pic) #连击
    if fdx_pic:
        card.paste(fdx_pic,(text_x+380,text_y+280),mask=fdx_pic) #拼机

    return card

#加载乐曲信息并使用create_score_card绘制卡片
def paste_single(single):
    single_info=search_song(f"{single['song_id']}")
    score_card = create_score_card(
        title=single["title"],
        achieve=single["achievements"],
        ds=single["ds"],
        rt=single["ra"],
        dx=single["dxScore"],
        id=single["song_id"],
        ev=single["rate"],
        isfc=single["fc"],
        isfdx=single["fs"],
        dif=single["level_index"]
    )
    return score_card.resize((300,150)).convert("RGBA")

#绘制卡片顶部用户信息
def player_info(qq):
    # 加载查询者设置的收藏品json （是在qq独立设置的 不是舞萌里用的 这里日后如果能接入舞萌接口可以换成玩家的）
    with open(rf"{get_abs_path()}/data/wmc/datasets/userinfo.json", "r", encoding="utf-8") as f:
        user_info = json.load(f)
    record=get_b50(qq)

    #加载字体
    FONT_RATING = ImageFont.truetype(FONT_PATH, 48)

    #爬查询者qq头像
    ulr=f"https://q1.qlogo.cn/g?b=qq&nk={qq}&s=640"
    resp=requests.get(ulr)
    photo= Image.open(BytesIO(resp.content)).convert("RGBA")

    #如果玩家没设置 直接用默认的
    try:
        bgid=user_info[str(qq)]["plate"]
        if not bgid:
            raise Exception
    except:bgid=11

    #爬收藏品
    url=f"https://assets2.lxns.net/maimai/plate/{bgid}.png"
    resp=requests.get(url)
    bg=Image.open(BytesIO(resp.content)).convert("RGBA")

    #水鱼名字
    nickname = record["nickname"]

    #计算玩家的b35r与b15r
    records = record["charts"]
    b35=records["sd"]
    b15=records["dx"]
    sdrt=0
    dxrt=0
    for sd in b35:sdrt+=sd["ra"]
    for dx in b15:dxrt+=dx["ra"]
    rt=sdrt+dxrt

    #傻子最爱的堆if 读框体
    if rt<1000:rtf=rtframe_load("0")
    elif rt<2000:rtf=rtframe_load("1000")
    elif rt < 4000:rtf=rtframe_load("2000")
    elif rt < 7000:rtf=rtframe_load("4000")
    elif rt < 10000:rtf=rtframe_load("7000")
    elif rt < 12000:rtf=rtframe_load("10000")
    elif rt < 13000:rtf=rtframe_load("12000")
    elif rt < 14000:rtf=rtframe_load("13000")
    elif rt < 14250:rtf=rtframe_load("14000")
    elif rt < 14500:rtf=rtframe_load("14250")
    elif rt < 14750:rtf=rtframe_load("14500")
    elif rt < 15000:rtf=rtframe_load("14750")
    elif rt < 15250:rtf=rtframe_load("15000")
    elif rt < 15500:rtf=rtframe_load("15250")
    elif rt < 15750:rtf=rtframe_load("15500")
    elif rt < 16000:rtf=rtframe_load("15750")
    elif rt < 16250:rtf=rtframe_load("16000")
    elif rt < 16500:rtf=rtframe_load("16250")
    elif rt < 16750:rtf=rtframe_load("16500")
    else:rtf=rtframe_load("16750")

    #尺寸调准
    photo = photo.resize((250, 250))
    rtf = rtf.resize((440, 80))
    bg = bg.resize((1800, 290))

    #画图
    card=bg
    draw = ImageDraw.Draw(card)

    card.paste(bg,(0,0),mask=bg)
    card.paste(photo,(20,20))
    card.paste(rtf,(360,20),mask=rtf)
    for idx,string in enumerate(str(rt)):
        draw.text((565+idx*35,25),string,fill=(255,215,0),font=FONT_RATING)
    draw.rounded_rectangle([360,120,700,180], radius=15, outline=(0,0,0), width=1,fill=(255,255,255))
    draw.text((380,125), f"{nickname}", font_size=36,fill=(0,0,0))
    draw.rounded_rectangle([360, 210, 800, 240], radius=15, outline=(0, 0, 0), fill=(255,255,255),width=1)
    draw.text((380,210),f"Best35:{sdrt} + Best15:{dxrt} = {rt}",font_size=24,fill=(0,0,0))

    return card

#绘制总体b50
def paste_b50(qq):
    # 加载查询者设置的收藏品json （是在qq独立设置的 不是舞萌里用的 这里日后如果能接入舞萌接口可以换成玩家的）
    with open(rf"{get_abs_path()}/data/wmc/datasets/userinfo.json", "r", encoding="utf-8") as f:
        user_info = json.load(f)

    #所需的玩家/乐曲
    record=get_b50(qq) #玩家的简略信息
    top=player_info(qq) #顶部玩家信息栏
    records=record["charts"] #玩家的b50
    b15=records["dx"] #b35
    b35=records["sd"] #b15
    b50=b15+b35 #将35与15放在一个列表里
    b35_pic=[] #b35的卡片列表
    b15_pic=[] #b15的卡片列表
    #以玩家单曲ra最高的乐曲背景作为背景图 如果b50为空 则在songs里随机加载乐曲作为封面
    bg=None
    try:
        bg=get_cover_image(user_info[str(qq)]["bg"])
        if not bg:
            raise Exception
    except Exception as e:
        print(e)
        max=None
        maxrt=0
        for single in b50:
            if single["ra"]>maxrt:
                maxrt=single["ra"]
                max=single
        try:
            bg = get_cover_image(search_song(max["title"])[0]["索引"])
        except:
            bg = get_cover_image(songs[random.randint(0, len(songs))]["索引"])

    #加载所有歌曲的卡片
    for single in b35:b35_pic.append(paste_single(single))
    for single in b15: b15_pic.append(paste_single(single))

    #绘制
    card=input_bg(bg,bg_size=(1800,2400))
    draw = ImageDraw.Draw(card)

    x_s=100
    y_s=420
    wid=300
    hei=150
    cols=5
    rows=10
    x_int=20
    y_int=25
    card.paste(top,(0,0))

    for row in range(rows):
        y=y_s+row*(y_int+hei)
        if row<=6:
            for col in range(cols):
                try:card.paste(b35_pic[row*5+col],(x_s+col*(x_int+wid),y),mask=b35_pic[row*5+col])
                except:continue

        elif row>6:
            y+=100
            for col in range(cols):
                try:card.paste(b15_pic[row * 5 + col-35], (x_s + col * (x_int + wid), y),mask=b15_pic[row * 5 + col-35])
                except:continue
    paste_me(draw,(1800,2400),36)
    return card


#绘制某等级的b50
def paste_grade(qq,keys,index):
    if not index:index=1
    index=int(index)
    #判断等级是否有效
    if keys not in ["1","2","3","4","5","6","7","8","8+","9","9+","10","10+","11","11+","12","12+","13","13+","14","14+","15"]:
        return 2,"没有这个等级哦"
    # 加载查询者设置的收藏品json （是在qq独立设置的 不是舞萌里用的 这里日后如果能接入舞萌接口可以换成玩家的）
    with open(rf"{get_abs_path()}/data/wmc/datasets/userinfo.json", "r", encoding="utf-8") as f:
        user_info = json.load(f)

    #所需的玩家/乐曲
    import_token=user_info[str(qq)]["token"]
    records=get_full_grade(import_token)["records"]

    top=player_info(qq) #顶部玩家信息栏

    #指定成绩降序
    record = [r for r in records if r["level"] == f"{keys}"]
    record=sorted(record,key=lambda x:x["achievements"],reverse=True)

    #判断指定索引里有没有成绩
    length=len(record)
    if length < 50*index-50:
        return 2,"索引超长"

    b50=record[50*index-50:50*index]
    b50_pic=[]
    #以玩家单曲ra最高的乐曲背景作为背景图 如果b50为空 则在songs里随机加载乐曲作为封面
    bg=None
    try:
        bg=get_cover_image(user_info[str(qq)]["bg"])
        if not bg:
            raise Exception
    except Exception as e:
        print(e)
        max=None
        maxrt=0
        for single in b50:
            if single["ra"]>maxrt:
                maxrt=single["ra"]
                max=single

        try:bg = get_cover_image(search_song(max["title"])[0]["索引"])
        except:bg = get_cover_image(songs[random.randint(0, len(songs))]["索引"])

    #加载所有歌曲的卡片
    for single in b50: b50_pic.append(paste_single(single))

    #绘制
    card=input_bg(bg,bg_size=(1800,2400))
    draw = ImageDraw.Draw(card)

    x_s=100
    y_s=420
    wid=300
    hei=150
    cols=5
    rows=10
    x_int=20
    y_int=25
    card.paste(top,(0,0))
    for row in range(rows):
        y=y_s+row*(y_int+hei)
        for col in range(cols):
            try:card.paste(b50_pic[row*5+col],(x_s+col*(x_int+wid),y),mask=b50_pic[row*5+col])
            except:continue

    paste_me(draw,(1800,2400),36)
    return 1,card

