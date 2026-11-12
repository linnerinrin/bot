"""
选取不同版本的代表曲目封面用于绘制不同版本的背景
"""

from tester.utils import get_cover_image, load_songs, search_song
version={
    143: "maimai.png",
    #143: "maimai-plus.png",
    264: "green.png",
    324: "green-plus.png",
    379: "orange.png",
    365: "orange-plus.png",
    462: "pink.png",
    531: "pink-plus.png",
    589: "murasaki.png",
    614: "murasaki-plus.png",
    643: "milk.png",
    773: "milk-plus.png",
    834: "finale.png",
    11026: "maimaidx.png",
    11102: "maimaidx-plus.png",
    11216: "splash.png",
    11222: "splash-plus.png",
    11311: "universe.png",
    11394: "universe-plus.png",
    11457: "festival.png",
    11530: "festival-plus.png",
    11663: "buddies.png",
    11673: "buddies-plus.png",
    11741: "prism.png",
    "Xaleid◆scopiX": "prism-plus.png",
    "7 Wonders": "circle.png",
    "AiAe": "circle-plus.png"
}
CSV_PATH= r"dxdata.csv"
songs = load_songs(CSV_PATH)
for key,value in version.items():
    song = search_song(str(key), songs)
    get_cover_image(song[0]["索引"]).save(fr"version-bg/{value}")