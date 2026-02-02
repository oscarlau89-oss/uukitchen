import streamlit as st
import random
import time
import requests
import datetime
import json
import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont

# 🌟 导入数据
try:
    from recipe_data import RECIPES_DB, FRIDGE_CATEGORIES
except ImportError:
    st.error("❌ 找不到 recipe_data.py！")
    st.stop()

# ==========================================
# 1. 工程配置
# ==========================================
st.set_page_config(
    page_title="Bluey美食魔法屋 v50.0",
    page_icon="🦴",
    layout="centered",
    initial_sidebar_state="auto"
)

# 📂 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "menu_history.json")
USER_DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
FONT_FILE = os.path.join(BASE_DIR, "SimHei.ttf")
# 头像图片路径（支持多种格式和文件名）
AVATAR_FILE = None
# 优先查找webp格式（GitHub自动转换的格式）
for filename in ["bluey.png.webp", "bluey.webp", "bluey.png", "bluey.jpg", "bluey.jpeg", "avatar.png.webp", "avatar.webp", "avatar.png", "avatar.jpg", "头像.png.webp", "头像.webp", "头像.png", "头像.jpg"]:
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        AVATAR_FILE = path
        break

# ==========================================
# 2. 核心资源引擎
# ==========================================
@st.cache_resource
def load_custom_font():
    if not os.path.exists(FONT_FILE):
        url = "https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf"
        try:
            r = requests.get(url, timeout=30)
            with open(FONT_FILE, "wb") as f: f.write(r.content)
        except: return ImageFont.load_default()
    return FONT_FILE

def get_pil_font(size):
    try: return ImageFont.truetype(load_custom_font(), size)
    except: return ImageFont.load_default()

def load_user_data():
    default = {
        "nickname": "Bingo", "age": "2岁", "height": "90", "weight": "13",
        "nutrition_goals": ["补钙"], "allergens": ["牛奶", "牛肉"], 
        "fridge_items": ["鸡蛋", "西红柿", "土豆"], 
        "pushplus_token": "", "dislikes": [], "likes": []
    }
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f); default.update(saved)
        except: pass
    return default

def save_user_data():
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.user_data, f, ensure_ascii=False, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history_item(menu_state):
    history = load_history()
    item = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "menu": {
            "breakfast": menu_state['breakfast']['name'] if menu_state['breakfast'] else "未设置",
            "lunch": [
                menu_state['lunch_meat']['name'] if menu_state['lunch_meat'] else "未设置",
                menu_state['lunch_veg']['name'] if menu_state['lunch_veg'] else "未设置",
                menu_state['lunch_soup']['name'] if menu_state['lunch_soup'] else "未设置"
            ],
            "dinner": [
                menu_state['dinner_meat']['name'] if menu_state['dinner_meat'] else "未设置",
                menu_state['dinner_veg']['name'] if menu_state['dinner_veg'] else "未设置",
                menu_state['dinner_soup']['name'] if menu_state['dinner_soup'] else "未设置"
            ],
            "fruit": menu_state['fruit'] if menu_state['fruit'] else "未设置"
        }
    }
    history.insert(0, item)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    st.toast("已收藏到历史", icon="✅")

if 'user_data' not in st.session_state: st.session_state.user_data = load_user_data()
if 'menu_state' not in st.session_state:
    st.session_state.menu_state = {
        "breakfast": None, "lunch_meat": None, "lunch_veg": None, "lunch_soup": None,
        "dinner_meat": None, "dinner_veg": None, "dinner_soup": None, "fruit": None,
        "shopping_list": []
    }
if 'view_mode' not in st.session_state: st.session_state.view_mode = "dashboard"
if 'focus_dish' not in st.session_state: st.session_state.focus_dish = None

# ==========================================
# 3. 像素级 CSS 锁定 (Mobile Lock-in)
# ==========================================
st.markdown("""
<style>
    /* 1. 强制页面不出现横向滚动条 */
    .stApp { background-color: #F2F2F7; overflow-x: hidden; }
    .main > div { padding-left: 1rem !important; padding-right: 1rem !important; }
    /* 移动端进一步减小padding */
    @media (max-width: 768px) {
        .main > div { 
            padding-left: 0.5rem !important; 
            padding-right: 0.5rem !important; 
        }
        /* 确保header容器不超出屏幕 */
        .element-container:has(.header-box) {
            width: 100% !important;
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
    }
    h1, h2, h3, h4, p, span, div, button { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}

    /* 2. 顶部 Header (Flex 强控) */
    .header-box {
        display: flex; align-items: center; justify-content: flex-start;
        padding: 5px 0; margin-top: -50px; margin-bottom: 10px; width: 100%;
        gap: 8px;
        box-sizing: border-box;
    }
    /* 移动端header优化 */
    @media (max-width: 768px) {
        .header-box {
            padding: 5px 0;
            margin-top: -50px;
            margin-bottom: 8px;
            gap: 4px !important; /* 减小gap */
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box;
        }
        .header-title {
            font-size: 15px !important; /* 进一步减小字体 */
            margin-left: 4px !important;
            flex: 1;
            min-width: 0;
            max-width: calc(100% - 50px); /* 确保不超出 */
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
    }
    /* 强行锁定图片尺寸，防止变大 */
    .avatar-img { 
        width: 50px !important; height: 50px !important; min-width: 50px !important;
        border-radius: 50%; border: 2px solid white; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); object-fit: cover;
        display: block !important;
    }
    /* 图片加载失败时的备用样式 */
    .avatar-img:before {
        content: "🦴";
        display: block;
        width: 50px;
        height: 50px;
        line-height: 50px;
        text-align: center;
        background: #FF9500;
        border-radius: 50%;
    }
    .header-title { 
        font-size: 20px; font-weight: 800; color: #1C1C1E; 
        margin-left: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    
    /* 3. 强制缩小列间距 (解决图标太远问题) */
    [data-testid="column"] { 
        padding: 0 !important; 
        margin: 0 !important;
        flex-shrink: 0 !important; /* 防止列收缩 */
        flex-basis: auto !important;
        width: auto !important;
        min-width: 0 !important;
        max-width: none !important;
    }
    /* 新的HTML图标布局样式 - 完全控制布局 */
    .icon-row-top,
    .icon-row-dish {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }
    .icon-btn-top,
    .icon-btn-dish {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 8px 4px !important;
        margin: 0 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: opacity 0.2s !important;
    }
    .icon-btn-top:hover,
    .icon-btn-dish:hover {
        opacity: 0.7 !important;
    }
    .icon-emoji {
        font-size: 24px !important;
        line-height: 1 !important;
        display: inline-block !important;
    }
    /* 菜品图标颜色 */
    .icon-like .icon-emoji {
        color: #FF3B30 !important;
    }
    .icon-cook .icon-emoji {
        color: #007AFF !important;
        font-weight: bold !important;
    }
    .icon-dislike .icon-emoji,
    .icon-swap .icon-emoji {
        color: #8E8E93 !important;
    }
    [data-testid="stHorizontalBlock"] { 
        gap: 2px !important; /* 桌面端小间距 */
        display: flex !important; 
        flex-wrap: nowrap !important; /* 强制不换行 */
        width: 100% !important;
        max-width: 100% !important;
        overflow: visible !important;
        padding: 0 !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }
    /* 移动端强制图标一行显示，紧凑排列 */
    @media (max-width: 768px) {
        /* 顶部header区域：左侧头像+名字更紧凑 */
        .header-box {
            margin-right: 0 !important;
            gap: 4px !important;
            padding: 5px 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box;
        }
        .header-title {
            font-size: 15px !important;
            margin-left: 4px !important;
            flex: 1;
            min-width: 0;
            max-width: calc(100% - 50px);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .avatar-img {
            width: 45px !important;
            height: 45px !important;
            min-width: 45px !important;
            flex-shrink: 0 !important;
        }
        
        /* 移动端：强制顶部3个图标和菜品4个图标紧密排列，确保一页显示 */
        /* 顶部3个图标的列容器 */
        [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
        }
        /* 顶部3个图标的列 */
        [data-testid="column"] {
            padding: 0 1px !important;
            margin: 0 !important;
            flex: 1 1 0 !important;
            min-width: 0 !important;
            max-width: 33.33% !important;
            box-sizing: border-box !important;
        }
        /* 顶部3个图标按钮 */
        button[key="dl_btn"],
        button[key="wx_btn"],
        button[key="pl_btn"],
        button[key="dl_btn_disabled"],
        button[data-testid="baseButton-download"][key="dl_btn"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            padding: 4px 2px !important;
            margin: 0 !important;
            font-size: 4vw !important;
            line-height: 1 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        /* 菜品卡片的4个图标列 */
        .dish-card [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
        }
        .dish-card [data-testid="column"] {
            padding: 0 1px !important;
            margin: 0 !important;
            flex: 1 1 0 !important;
            min-width: 0 !important;
            max-width: 25% !important;
            box-sizing: border-box !important;
        }
        /* 菜品4个图标按钮 */
        .dish-card button[key*="lk_"],
        .dish-card button[key*="dl_"],
        .dish-card button[key*="ck_"],
        .dish-card button[key*="sw_"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            padding: 4px 2px !important;
            margin: 0 !important;
            font-size: 3.5vw !important;
            line-height: 1 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        /* 菜品标签样式 */
        .dish-label {
            padding-left: 5px;
            margin-bottom: 3px;
        }
        /* 移动端：进一步减小卡片间距和内部空间 */
        .dish-card {
            margin-bottom: 8px !important;
            border-radius: 12px !important;
        }
        .card-banner {
            padding: 4px !important;
            font-size: 13px !important;
        }
        .dish-label {
            font-size: 14px !important;
            margin-bottom: 2px !important;
            padding-top: 2px !important;
        }
        .ing-scroll {
            padding: 2px 8px 6px 8px !important;
            gap: 3px !important;
        }
        .pill {
            padding: 1px 6px !important;
            font-size: 10px !important;
        }
        /* 生成按钮也缩小，但保持美观 */
        .gen-btn {
            margin: 5px 0 !important;
        }
        .gen-btn button {
            height: 46px !important;
            font-size: 16px !important;
            min-width: 180px !important;
            padding: 0 20px !important;
            margin: 0 auto !important;
        }
        /* 减小所有不必要的间距 */
        .main > div {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
        }
        /* 移动端：确保所有图标按钮紧密排列，不超出屏幕 */
        /* 强制所有图标按钮去掉背景和边框，减小尺寸 */
        button[key*="dl_btn"],
        button[key*="wx_btn"],
        button[key*="pl_btn"],
        button[key*="lk_"],
        button[key*="dl_"],
        button[key*="ck_"],
        button[key*="sw_"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 4px 2px !important;
            margin: 0 !important;
        }
    }

    /* 顶部图标按钮样式 - 让边框无限接近图标大小 */
    button[key="dl_btn"],
    button[key="wx_btn"],
    button[key="pl_btn"],
    button[aria-label*="Download"],
    button[aria-label*="下载"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 24px !important;
        padding: 2px !important;
        margin: 0 !important;
        color: #1C1C1E !important;
        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* 通用顶部按钮样式 - 让边框无限接近图标大小 */
    div[data-testid="column"]:nth-child(2) button,
    div[data-testid="column"]:nth-child(3) button,
    div[data-testid="column"]:nth-child(4) button,
    div[data-testid="column"] button[kind="secondary"],
    div[data-testid="column"] button[kind="primary"],
    div[data-testid="column"] button[type="button"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 24px !important;
        padding: 2px !important;
        margin: 0 !important;
        color: #1C1C1E !important;
        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* 顶部按钮容器也缩小 */
    div[data-testid="column"]:nth-child(2),
    div[data-testid="column"]:nth-child(3),
    div[data-testid="column"]:nth-child(4) {
        padding: 0 !important;
        margin: 0 !important;
        flex: 0 0 auto !important;
    }
    /* 移动端进一步优化图标按钮 */
    @media (max-width: 768px) {
        .icon-btn {
            padding: 0 !important;
            margin: 0 !important;
        }
    .icon-btn button {
            height: 36px !important;
            font-size: 16px !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 10px !important;
        }
    }
    /* 移除顶部图标按钮的背景色 */
    div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button,
    div[data-testid="column"]:nth-of-type(4) button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 4. 生成按钮 (美观整洁，居中) - 使用更强制性的选择器 */
    .gen-btn,
    div:has(button[key="gen_btn"]),
    .element-container:has(button[key="gen_btn"]) {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 5px 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    .gen-btn button,
    button[key="gen_btn"],
    button[key="gen_btn"][kind="primary"],
    button[key="gen_btn"][kind="secondary"],
    div:has(button[key="gen_btn"]) button,
    .element-container:has(button[key="gen_btn"]) button {
        width: auto !important;
        min-width: 200px !important;
        max-width: 90% !important;
        height: 50px !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #FF9500, #FF7B00) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: 2px solid #FF7B00 !important;
        box-shadow: 0 4px 12px rgba(255, 159, 28, 0.25) !important;
        margin: 0 auto !important;
        padding: 0 24px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }
    .gen-btn button:hover,
    button[key="gen_btn"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(255, 159, 28, 0.35) !important;
    }
    /* 确保生成按钮的容器居中 - 使用更具体的选择器 */
    div:has(button[key="gen_btn"]),
    .element-container:has(button[key="gen_btn"]),
    div:has(button[key="gen_btn"]) > div,
    [data-testid="stButton"]:has(button[key="gen_btn"]) {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    /* 确保生成按钮的容器居中 */
    div:has(button[key="gen_btn"]),
    .element-container:has(button[key="gen_btn"]),
    div:has(button[key="gen_btn"]) > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    /* 5. 菜品卡片 (紧凑) */
    .dish-card {
        background: white; border-radius: 15px; margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03); overflow: hidden;
    }
    .card-banner { padding: 6px; text-align: center; color: white; font-weight: 800; font-size: 14px; letter-spacing: 2px; }
    .bg-orange { background: #FF9500; } .bg-blue { background: #007AFF; } .bg-purple { background: #AF52DE; }

    /* 菜名 */
    .dish-label { 
        font-size: 15px; font-weight: 700; color: #1C1C1E; 
        line-height: 1.5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-left: 5px;
        margin-bottom: 3px;
        padding-top: 3px;
    }
    
    /* 菜品图标按钮 - 让边框无限接近图标大小，使用更强制性的选择器 */
    .dish-card [data-testid="column"] button,
    .dish-card [data-testid="column"] button[kind="secondary"],
    .dish-card [data-testid="column"] button[kind="primary"],
    .dish-card [data-testid="column"] button[type="button"],
    .dish-card button,
    .dish-card [data-testid="column"] > * button {
        background: transparent !important; 
        border: none !important;
        font-size: 20px !important; 
        width: 30px !important; 
        height: 30px !important; 
        padding: 1px !important; 
        margin: 0 !important;
        box-shadow: none !important; 
        color: #8E8E93 !important;
        min-width: 30px !important;
        max-width: 30px !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* 菜品按钮容器也缩小 */
    .dish-card [data-testid="column"] {
        padding: 0 2px !important;
        margin: 0 !important;
        flex: 0 0 auto !important;
    }
    /* 喜欢按钮红色 - 通过key识别 */
    .dish-card button[key*="lk_"] {
        color: #FF3B30 !important;
    }
    /* 烹饪按钮蓝色 */
    .dish-card button[key*="ck_"] {
        color: #007AFF !important;
        font-weight: bold !important;
    }

    /* 食材条 - 更紧凑 */
    .ing-scroll { 
        display: flex; overflow-x: auto; gap: 4px; padding: 3px 10px 8px 10px; 
        -webkit-overflow-scrolling: touch; scrollbar-width: none;
    }
    .ing-scroll::-webkit-scrollbar { display: none; }
    .pill { background: #F2F2F7; color: #3A3A3C; padding: 2px 8px; border-radius: 8px; font-size: 11px; font-weight: 600; white-space: nowrap; }
    .pill-hit { background: #FFF4E5; color: #FF9500; }

    /* 历史 & 清单 */
    .hist-item { background: white; border-radius: 12px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #FF9500; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
    .hist-card { background: white; border-radius: 12px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #FF9500; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
    .hist-head { font-weight: 700; color: #1C1C1E; font-size: 15px; margin-bottom: 5px; }
    .hist-txt { color: #666; font-size: 13px; line-height: 1.6; }
    .receipt-card { background: #FFF; padding: 15px; border: 1px dashed #DDD; border-radius: 10px; font-size: 14px; text-align: center; margin-top: 15px;}
    
    /* 隐藏所有用于触发的隐藏按钮及其容器 - 确保完全不占据空间 */
    .element-container:has(button[key*="_hidden"]),
    .element-container:has(button[key="dl_btn_hidden"]),
    .element-container:has(button[key="wx_btn_hidden"]),
    .element-container:has(button[key="pl_btn_hidden"]),
    div:has(button[key*="_hidden"]),
    div:has(button[key="dl_btn_hidden"]),
    div:has(button[key="wx_btn_hidden"]),
    div:has(button[key="pl_btn_hidden"]),
    [data-testid="stButton"]:has(button[key*="_hidden"]),
    [data-testid="stDownloadButton"]:has(button[key*="_hidden"]),
    button[key*="_hidden"],
    button[key="dl_btn_hidden"],
    button[key="wx_btn_hidden"],
    button[key="pl_btn_hidden"],
    button[key*="lk_"][key*="_hidden"],
    button[key*="dl_"][key*="_hidden"],
    button[key*="ck_"][key*="_hidden"],
    button[key*="sw_"][key*="_hidden"] {
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        width: 0 !important;
        height: 0 !important;
        min-width: 0 !important;
        min-height: 0 !important;
        max-width: 0 !important;
        max-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        overflow: hidden !important;
        border: none !important;
        box-shadow: none !important;
    }
    /* 确保隐藏按钮的父容器也不占据空间 */
    .element-container:has(button[key*="_hidden"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* 顶部 3 个图标：缩短白框长度，并让图标居中 */
    [data-testid="column"] .stButton > button[key="dl_btn"],
    [data-testid="column"] .stButton > button[key="dl_btn_disabled"],
    [data-testid="column"] .stButton > button[key="wx_btn"],
    [data-testid="column"] .stButton > button[key="pl_btn"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;

        min-width: 32px !important;
        width: 32px !important;
        height: 32px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 16px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        font-size: 20px !important;
    }

    /* 菜卡片里 4 个图标：白框缩小，图标居中 */
    .dish-card .stButton > button[key*="lk_"],
    .dish-card .stButton > button[key*="dl_"],
    .dish-card .stButton > button[key*="ck_"],
    .dish-card .stButton > button[key*="sw_"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;

        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 14px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 业务逻辑
# ==========================================

SYNONYM_MAP = {"番茄": "西红柿", "洋柿子": "西红柿", "洋芋": "土豆", "马铃薯": "土豆", "大虾": "虾仁", "基围虾": "虾仁", "花菜": "西兰花", "圆白菜": "青菜", "白菜": "青菜", "娃娃菜": "青菜", "牛腩": "牛肉", "肥牛": "牛肉", "肉末": "猪肉", "里脊": "猪肉", "排骨": "猪肉", "鸡腿": "鸡肉", "鸡翅": "鸡肉", "龙利鱼": "鱼", "巴沙鱼": "鱼", "鳕鱼": "鱼"}
RED_MEAT = ["牛肉", "猪肉", "排骨", "羊肉", "猪肝"]

def normalize_ingredient(name):
    return SYNONYM_MAP.get(name.strip(), name.strip())

def mock_ocr_process(img):
    time.sleep(0.8)
    return ["西红柿", "基围虾", "娃娃菜"]

def toggle_feedback(dish_name, action):
    likes = st.session_state.user_data['likes']
    dislikes = st.session_state.user_data['dislikes']
    if action == 'like':
        if dish_name in likes:
            likes.remove(dish_name)
        else: 
            if dish_name not in likes:
                likes.append(dish_name)
            if dish_name in dislikes:
                dislikes.remove(dish_name)
    elif action == 'dislike':
        if dish_name in dislikes:
            dislikes.remove(dish_name)
        else:
            if dish_name not in dislikes:
                dislikes.append(dish_name)
            if dish_name in likes:
                likes.remove(dish_name)
    save_user_data()

def restock_from_shopping_list():
    needed = st.session_state.menu_state['shopping_list']
    if needed:
        cur = set(st.session_state.user_data['fridge_items'])
        cur.update(needed)
        st.session_state.user_data['fridge_items'] = list(cur)
        save_user_data()
        update_shopping_list()
        st.success("已入库！")
        time.sleep(0.5)
        st.rerun()

def get_random_dish(pool, fridge, allergens, exclude_names=[], prefer_type=None):
    safe = []
    norm_fridge = set([normalize_ingredient(i) for i in fridge] + fridge)
    for d in pool:
        if d['name'] in exclude_names: continue
        is_safe = True
        for ing in d['ingredients']:
            if any(alg in ing for alg in allergens):
                is_safe = False
                break
        if not is_safe: continue
        if prefer_type == "white_meat":
            if any(ing in RED_MEAT for ing in d['ingredients']): continue
        
        miss = sum(1 for ing in d['ingredients'] if normalize_ingredient(ing) not in norm_fridge)
        dc = d.copy(); dc['missing_count'] = miss
        safe.append(dc)
    
    if not safe: return None
    tier0 = [d for d in safe if d['missing_count'] == 0]
    tier1 = [d for d in safe if d['missing_count'] == 1]
    tier2 = [d for d in safe if d['missing_count'] > 1]
    final_pool = tier0 if tier0 else (tier1 if tier1 else tier2)
    
    likes = st.session_state.user_data['likes']
    dislikes = st.session_state.user_data['dislikes']
    weighted = []
    for d in final_pool:
        score = 10
        if d.get('missing_count') == 0: score += 50
        if d['name'] in likes: score += 100
        if d['name'] in dislikes: score = 1
        weighted.extend([d] * score)
    return random.choice(weighted) if weighted else None

def generate_full_menu():
    fridge = st.session_state.user_data['fridge_items']
    allergies = st.session_state.user_data['allergens']
    ms = st.session_state.menu_state
    
    ms['breakfast'] = get_random_dish(RECIPES_DB['breakfast'], fridge, allergies)
    ms['lunch_meat'] = get_random_dish(RECIPES_DB['lunch_meat'], fridge, allergies)
    ms['lunch_veg'] = get_random_dish(RECIPES_DB['lunch_veg'], fridge, allergies)
    ms['lunch_soup'] = get_random_dish(RECIPES_DB['soup'], fridge, allergies)
    
    lunch_ings = ms['lunch_meat']['ingredients'] if ms['lunch_meat'] else []
    is_red = any(normalize_ingredient(i) in RED_MEAT for i in lunch_ings)
    pool_dm = RECIPES_DB.get('dinner_meat', []) or RECIPES_DB['lunch_meat']
    pool_dv = RECIPES_DB.get('dinner_veg', []) or RECIPES_DB['lunch_veg']
    pref = "white_meat" if is_red else None
    
    exclude_lunch_meat = [ms['lunch_meat']['name']] if ms['lunch_meat'] else []
    exclude_lunch_soup = [ms['lunch_soup']['name']] if ms['lunch_soup'] else []
    ms['dinner_meat'] = get_random_dish(pool_dm, fridge, allergies, exclude_lunch_meat, pref) or get_random_dish(pool_dm, fridge, allergies, exclude_lunch_meat)
    ms['dinner_veg'] = get_random_dish(pool_dv, fridge, allergies)
    ms['dinner_soup'] = get_random_dish(RECIPES_DB['soup'], fridge, allergies, exclude_lunch_soup)
    ms['fruit'] = random.choice(RECIPES_DB['fruit'])
    
    update_shopping_list()
    st.session_state.view_mode = "dashboard"

def update_shopping_list():
    norm_fridge = set([normalize_ingredient(i) for i in st.session_state.user_data['fridge_items']])
    needed = set()
    ms = st.session_state.menu_state
    for k, d in ms.items():
        if isinstance(d, dict):
            for ing in d.get('ingredients', []):
                if normalize_ingredient(ing) not in norm_fridge:
                    needed.add(ing)
    st.session_state.menu_state['shopping_list'] = list(needed)

def swap_dish(key, pool_key):
    fridge = st.session_state.user_data['fridge_items']
    allergies = st.session_state.user_data['allergens']
    current = st.session_state.menu_state[key]
    exclude = [current['name']] if current else []
    
    pool = RECIPES_DB.get(pool_key, [])
    if 'meat' in pool_key and not pool: pool = RECIPES_DB['lunch_meat']
    if 'veg' in pool_key and not pool: pool = RECIPES_DB['lunch_veg']
    
    new_d = get_random_dish(pool, fridge, allergies, exclude)
    if new_d:
        st.session_state.menu_state[key] = new_d
        update_shopping_list()

def create_menu_card_image(menu, nickname):
    width, height = 800, 1200
    img = Image.new('RGB', (width, height), color='#FFFDF5')
    draw = ImageDraw.Draw(img)
    title_font = get_pil_font(60)
    header_font = get_pil_font(40)
    text_font = get_pil_font(30)
    small_font = get_pil_font(24)
    
    draw.rectangle([30, 30, 770, 1170], outline="#FF9500", width=5)
    draw.text((400, 120), f"{nickname} 的今日食谱", font=title_font, fill='#FF9500', anchor="mm")
    
    y = 260
    def add_sec(title, dishes):
        nonlocal y
        draw.text((400, y), f"• {title} •", font=header_font, fill='#333', anchor="mm")
        y += 75
        for d in dishes:
            draw.text((400, y), d, font=text_font, fill='#555', anchor="mm")
            y += 55
        y += 40
        
    add_sec("早餐", [menu['breakfast']['name'] if menu['breakfast'] else "未设置", "🥛 热牛奶"])
    add_sec("午餐", [
        menu['lunch_meat']['name'] if menu['lunch_meat'] else "未设置",
        menu['lunch_veg']['name'] if menu['lunch_veg'] else "未设置",
        menu['lunch_soup']['name'] if menu['lunch_soup'] else "未设置"
    ])
    add_sec("晚餐", [
        menu['dinner_meat']['name'] if menu['dinner_meat'] else "未设置",
        menu['dinner_veg']['name'] if menu['dinner_veg'] else "未设置",
        menu['dinner_soup']['name'] if menu['dinner_soup'] else "未设置"
    ])
    add_sec("今日水果", [menu['fruit'] if menu['fruit'] else "未设置"])
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def send_to_wechat():
    token = st.session_state.user_data['pushplus_token']
    if not token: 
        st.error("🚫 请在侧边栏填写 Token")
        return
    ms = st.session_state.menu_state
    if not ms['breakfast']: return
    content = f"<h1>{st.session_state.user_data['nickname']} 今日食谱</h1><hr><h3>🌅 早餐</h3><p>{ms['breakfast']['name'] if ms['breakfast'] else '未设置'}</p><h3>☀️ 午餐</h3><p>{ms['lunch_meat']['name'] if ms['lunch_meat'] else '未设置'}<br>{ms['lunch_veg']['name'] if ms['lunch_veg'] else '未设置'}<br>{ms['lunch_soup']['name'] if ms['lunch_soup'] else '未设置'}</p><h3>🌙 晚餐</h3><p>{ms['dinner_meat']['name'] if ms['dinner_meat'] else '未设置'}<br>{ms['dinner_veg']['name'] if ms['dinner_veg'] else '未设置'}<br>{ms['dinner_soup']['name'] if ms['dinner_soup'] else '未设置'}</p><p>🍎 加餐：{ms['fruit'] if ms['fruit'] else '未设置'}</p><hr><p>🛒 待买：{', '.join(ms['shopping_list']) if ms['shopping_list'] else '无'}</p>"
    data = {"token": token, "title": f"食谱-{st.session_state.user_data['nickname']}", "content": content, "template": "html"}
    try: requests.post('http://www.pushplus.plus/send', json=data, timeout=5); st.success("✅ 已推送")
    except: st.error("❌ 推送失败")

def generate_weekly():
    st.toast("✅ 周计划已生成")

def enter_cook_mode(dish):
    st.session_state.focus_dish = dish
    st.session_state.view_mode = "cook"

def exit_cook_mode():
    st.session_state.view_mode = "dashboard"

# ==========================================
# 5. UI 渲染 (View)
# ==========================================

# 侧边栏
with st.sidebar:
    # 使用本地图片作为头像
    if AVATAR_FILE and os.path.exists(AVATAR_FILE):
        try:
            st.image(AVATAR_FILE, width=80, use_container_width=False)
        except:
            st.markdown('<div style="width:80px;height:80px;background:linear-gradient(135deg, #FF9500, #FF7B00);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:48px;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.1);line-height:1;">🦴</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="width:80px;height:80px;background:linear-gradient(135deg, #FF9500, #FF7B00);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:48px;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.1);line-height:1;">🦴</div>', unsafe_allow_html=True)
        st.caption("💡 请将头像图片命名为 bluey.png 或 bluey.png.webp 放在项目目录中")
    
    with st.expander("📝 档案设置 (含过敏原)", expanded=True):
        u = st.session_state.user_data
        u['nickname'] = st.text_input("昵称", u['nickname'])
        st.session_state.user_data['height'] = st.text_input("身高", st.session_state.user_data.get('height',''))
        st.session_state.user_data['weight'] = st.text_input("体重", st.session_state.user_data.get('weight',''))
        
        st.markdown("**🚫 过敏原 (自动过滤)**")
        default_al = ["牛奶", "奶粉", "牛肉", "鸡蛋", "虾", "鱼", "花生", "麦麸"]
        cur_al = st.session_state.user_data.get('allergens', [])
        sel_al = st.multiselect("选择", default_al, default=[x for x in cur_al if x in default_al])
        cust_al = st.text_input("其他 (逗号分隔)", value=",".join([x for x in cur_al if x not in default_al]))
        
        st.session_state.user_data['pushplus_token'] = st.text_input("Token", st.session_state.user_data['pushplus_token'], type="password")
        if st.button("保存档案"):
            final = sel_al
            if cust_al: final.extend([x.strip() for x in cust_al.split(',') if x.strip()])
            st.session_state.user_data['allergens'] = list(set(final))
            save_user_data()
            st.success("已保存")

    with st.expander("🧊 冰箱管理"):
        img = st.camera_input("拍照", label_visibility="collapsed")
        if img: 
            items = mock_ocr_process(img)
            cur = set(st.session_state.user_data['fridge_items'])
            cur.update(items)
            st.session_state.user_data['fridge_items'] = list(cur)
            save_user_data()
            st.success(f"已入库: {','.join(items)}")
            time.sleep(1)
            st.rerun()
        
        cur_f = st.session_state.user_data['fridge_items']
        new_f_std = []
        for c, l in FRIDGE_CATEGORIES.items():
            st.markdown(f"**{c}**")
            new_f_std.extend(st.multiselect(c, l, default=[x for x in l if x in cur_f], key=f"f_{c}", label_visibility="collapsed"))
        
        all_std = [x for l in FRIDGE_CATEGORIES.values() for x in l]
        cust = [x for x in cur_f if x not in all_std]
        st.markdown("**📝 其他**")
        kept_cust = st.multiselect("自定义", cust, default=cust, key="f_cust", label_visibility="collapsed")
        new_in = st.text_input("新增")
        if st.button("更新库存"):
            final = new_f_std + kept_cust
            if new_in: final.extend([x.strip() for x in new_in.split(',') if x.strip()])
            st.session_state.user_data['fridge_items'] = list(set(final))
            save_user_data()
            st.rerun()

# 烹饪模式
if st.session_state.view_mode == "cook" and st.session_state.focus_dish:
    d = st.session_state.focus_dish
    st.button("⬅️ 返回", on_click=exit_cook_mode)
    st.markdown(f"""
    <div style="background:white; border-radius:20px; padding:20px; margin-top:10px;">
        <h2 style="text-align:center;">{d['name']}</h2>
        <div style="text-align:center; color:#888; margin:10px 0;">{d.get('time','--')} | {d.get('difficulty','--')}</div>
        <div style="background:#F9F9F9; padding:15px; border-radius:10px; margin-bottom:20px;">
            {' '.join([f'<span style="background:white; border:1px solid #EEE; padding:2px 8px; border-radius:8px; margin:2px; display:inline-block;">{i}</span>' for i in d['ingredients']])}
        </div>
        {''.join([f'<div style="margin-bottom:15px;"><b>{i+1}.</b> {s}</div>' for i,s in enumerate(d.get('steps_list',[]))])}
    </div>""", unsafe_allow_html=True)

# 仪表盘
else:
    # 1. 顶部 Header
    # 头像和名字在第一行
    if AVATAR_FILE and os.path.exists(AVATAR_FILE):
        # 将本地图片转换为base64编码，以便在HTML中使用
        with open(AVATAR_FILE, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            # 处理webp格式（包括bluey.png.webp这种情况）
            img_ext = os.path.splitext(AVATAR_FILE)[1].lower().replace('.', '')
            if img_ext == 'webp' or AVATAR_FILE.endswith('.webp'):
                img_mime = "image/webp"
            elif img_ext in ['png', 'jpg', 'jpeg']:
                img_mime = f"image/{img_ext}"
            else:
                img_mime = "image/png"
            img_src = f"data:{img_mime};base64,{img_data}"
    else:
        img_src = None
    
    if img_src:
        st.markdown(f'''
        <div class="header-box">
            <img src="{img_src}" 
                 class="avatar-img" 
                 alt="Bluey"
                 style="object-fit: cover; background: linear-gradient(135deg, #FF9500, #FF7B00);">
            <div class="header-title">Hi, {st.session_state.user_data["nickname"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="header-box">
            <div style="width:50px;height:50px;background:linear-gradient(135deg, #FF9500, #FF7B00);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;border:2px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.1);flex-shrink:0;">🦴</div>
            <div class="header-title">Hi, {st.session_state.user_data["nickname"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 2. 顶部三个图标（下载 / 推送 / 计划）——直接使用 Streamlit 按钮，避免复杂 HTML+JS
    col_dl, col_wx, col_pl = st.columns(3)
    with col_dl:
        if st.session_state.menu_state['breakfast']:
            st.download_button(
                "📥",
                data=create_menu_card_image(
                    st.session_state.menu_state,
                    st.session_state.user_data['nickname']
                ),
                file_name="menu.png",
                key="dl_btn",
                use_container_width=True,
            )
        else:
            st.button("📥", disabled=True, key="dl_btn_disabled", use_container_width=True)
    with col_wx:
        st.button("💬", on_click=lambda: st.toast("✅ 已发送微信"), key="wx_btn", use_container_width=True)
    with col_pl:
        st.button("📅", on_click=lambda: st.toast("📅 计划已生成"), key="pl_btn", use_container_width=True)

    # 3. 生成按钮（美观整洁，居中显示）
    st.markdown(
        '''
        <div style="display: flex; justify-content: center; align-items: center; margin: 2px 0 8px 0; padding: 0; width: 100%;">
        ''',
        unsafe_allow_html=True,
    )
    if st.button("✨ 生成今日菜单", key="gen_btn", use_container_width=False):
        with st.spinner("魔法规划中..."):
            time.sleep(0.5)
            generate_full_menu()
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. 渲染卡片
    def render_card(title, bg_class, keys, pool_keys):
        # 卡片外层
        st.markdown(
            f'<div class="dish-card"><div class="card-banner {bg_class}">{title}</div>',
            unsafe_allow_html=True,
        )
        for idx, k in enumerate(keys):
            d = st.session_state.menu_state[k]
            if not d:
                continue
            is_l = d['name'] in st.session_state.user_data['likes']
            is_dl = d['name'] in st.session_state.user_data['dislikes']
            
            # 菜名单独一行
            st.markdown(f'<div class="dish-label">{d["name"]}</div>', unsafe_allow_html=True)

            # 四个图标按钮在菜名下面，直接使用 Streamlit 按钮，通过 CSS 控制紧凑外观
            b1, b2, b3, b4 = st.columns(4)
            with b1: 
                if st.button("❤️" if is_l else "🙂", key=f"lk_{k}", use_container_width=True):
                    toggle_feedback(d['name'], 'like')
                    st.rerun()
            with b2:
                label = "⚫" if is_dl else "😐"
                if st.button(label, key=f"dl_{k}", use_container_width=True):
                    toggle_feedback(d['name'], 'dislike')
                    st.rerun()
            with b3:
                if st.button("🍳", key=f"ck_{k}", use_container_width=True):
                    enter_cook_mode(d)
                    st.rerun()
            with b4:
                if st.button("🔄", key=f"sw_{k}", use_container_width=True):
                    swap_dish(k, pool_keys[idx])
                    st.rerun()

            # 食材标签
            nf = [normalize_ingredient(i) for i in st.session_state.user_data['fridge_items']]
            ing_html = "".join(
                [
                    f'<span class="pill {"pill-hit" if normalize_ingredient(i) in nf else ""}">{i}</span>'
                    for i in d['ingredients']
                ]
            )
            st.markdown(f'<div class="ing-scroll">{ing_html}</div>', unsafe_allow_html=True)
            if k != keys[-1]:
                st.markdown(
                    "<hr style='margin:0 15px; border:0; border-top:1px solid #F0F0F0;'>",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.menu_state['breakfast']:
        render_card("早 餐", "bg-orange", ['breakfast'], ['breakfast'])
        render_card("午 餐", "bg-blue", ['lunch_meat', 'lunch_veg', 'lunch_soup'], ['lunch_meat', 'lunch_veg', 'soup'])
        render_card("晚 餐", "bg-purple", ['dinner_meat', 'dinner_veg', 'dinner_soup'], ['dinner_meat', 'dinner_veg', 'soup'])
        
        missing = st.session_state.menu_state['shopping_list']
        if missing:
            st.markdown(f"""<div class="receipt-card"><div style="font-weight:bold; margin-bottom:5px;">🛒 缺货清单</div><div style="font-size:13px; color:#555;">{'、'.join(missing)}</div></div>""", unsafe_allow_html=True)
            if st.button("📦 一键入库", use_container_width=True): restock_from_shopping_list()
        
        with st.expander("📜 历史收藏"):
            for h in load_history()[:5]:
                lunch_str = h["menu"]["lunch"][0] if h["menu"]["lunch"] and len(h["menu"]["lunch"]) > 0 else "未设置"
                st.markdown(f'<div class="hist-card"><div class="hist-head">📅 {h["date"]}</div><div class="hist-txt">🌅 {h["menu"]["breakfast"]}<br>☀️ {lunch_str}...</div></div>', unsafe_allow_html=True)# 临时文件，用于修复缩进