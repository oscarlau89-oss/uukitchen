import streamlit as st
import random
import time
import requests
import datetime
import json
import os
import io
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. 核心配置与环境初始化
# ==========================================
st.set_page_config(
    page_title="Bluey美食魔法屋 v44.0",
    page_icon="🦴",
    layout="centered",
    initial_sidebar_state="auto"
)

# 路径兼容处理
BASE_DIR = os.path.dirname(__file__)
def get_rel_p(name): return os.path.join(BASE_DIR, name)

# 加载数据库 (确保 recipe_data.py 在 GitHub 仓库中)
try:
    import recipe_data
    from recipe_data import RECIPES_DB, FRIDGE_CATEGORIES, normalize
except ImportError:
    st.error("❌ 找不到 recipe_data.py 文件！请确保它已上传到 GitHub。")
    st.stop()

USER_DATA_FILE = get_rel_p("user_data.json")
HISTORY_FILE = get_rel_p("menu_history.json")
FONT_FILE = get_rel_p("SimHei.ttf")

# ==========================================
# 2. 资源引擎
# ==========================================
@st.cache_resource
def load_font_engine():
    if not os.path.exists(FONT_FILE):
        url = "https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf"
        try:
            r = requests.get(url, timeout=20)
            with open(FONT_FILE, "wb") as f: f.write(r.content)
        except: return ImageFont.load_default()
    return FONT_FILE

def get_pil_font(size):
    try: return ImageFont.truetype(load_font_engine(), size)
    except: return ImageFont.load_default()

def load_prefs():
    default = {
        "nickname": "Bingo", "allergens": ["牛肉", "牛奶", "奶粉"], 
        "fridge_items": ["鸡蛋", "西红柿"], "likes": [], "dislikes": []
    }
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f); default.update(saved)
        except: pass
    return default

def save_prefs():
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.prefs, f, ensure_ascii=False, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

if 'prefs' not in st.session_state: st.session_state.prefs = load_prefs()
if 'menu' not in st.session_state: st.session_state.menu = {"breakfast": None, "lunch_meat": None, "lunch_veg": None, "lunch_soup": None, "dinner_meat": None, "dinner_veg": None, "dinner_soup": None, "fruit": None}
if 'view' not in st.session_state: st.session_state.view = "dashboard"

# ==========================================
# 3. 终极 CSS 注入 (全设备横向排版锁定)
# ==========================================
st.markdown("""
<style>
    /* 1. 强制手机端列不堆叠的关键代码 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 禁止换行 */
        align-items: center !important;
        gap: 0.2rem !important; /* 缩小间距 */
    }
    
    [data-testid="column"] {
        width: auto !important;
        flex: 1 1 auto !important;
        min-width: 0 !important; /* 允许列在手机上缩得很小而不换行 */
    }

    /* 2. 基础 UI 风格 */
    .stApp { background-color: #F2F2F7; }
    h1, h2, h3, h4, p, span, div, button { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}

    /* 3. Header 区域自适应 */
    .custom-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 5px 0; margin-top: -50px; margin-bottom: 20px;
    }
    .profile-info { display: flex; align-items: center; gap: 10px; }
    .avatar-round { 
        width: 75px; height: 75px; border-radius: 50%; border: 3px solid white; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); object-fit: cover;
    }
    .greeting { font-size: 24px; font-weight: 900; color: #1C1C1E; }

    /* 4. 顶部 App 图标按钮 */
    .top-btn-ios button {
        border-radius: 12px !important; border: none !important;
        height: 42px !important; width: 42px !important; padding: 0 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        color: white !important; font-size: 20px !important; box-shadow: 0 3px 8px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="column"]:nth-of-type(2) button { background: #007AFF !important; } /* 下载-蓝 */
    div[data-testid="column"]:nth-of-type(3) button { background: #34C759 !important; } /* 微信-绿 */
    div[data-testid="column"]:nth-of-type(4) button { background: #FF9500 !important; } /* 计划-橙 */

    /* 5. 生成按钮与提示 */
    .gen-action button {
        width: 100% !important; height: 58px !important; border-radius: 18px !important;
        background: linear-gradient(135deg, #FF9500, #FF7B00) !important;
        color: white !important; font-size: 19px !important; font-weight: 800 !important;
        box-shadow: 0 6px 18px rgba(255, 149, 0, 0.35) !important; margin-top: 10px;
    }
    .hint-label { text-align: center; color: #8E8E93; font-size: 13px; margin-top: 8px; font-weight: 600; margin-bottom: 25px; }

    /* 6. 菜品卡片 */
    .card-ios { background: white; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 8px 30px rgba(0,0,0,0.04); overflow: hidden; }
    .card-banner { padding: 12px; text-align: center; color: white; font-weight: 800; font-size: 15px; letter-spacing: 4px; }
    .orange-bar { background: #FF9500; } .blue-bar { background: #007AFF; } .purple-bar { background: #AF52DE; }

    .dish-label { font-size: 17px; font-weight: 800; color: #1C1C1E; line-height: 2.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-left: 10px; }
    
    /* 迷你动作图标 */
    .mini-btn-box button {
        background: transparent !important; border: none !important;
        font-size: 20px !important; width: 32px !important; height: 32px !important; 
        padding: 0 !important; margin: 0 !important;
        box-shadow: none !important; color: #333 !important;
    }
    .loved button { color: #FF3B30 !important; transform: scale(1.1); }
    .cooking button { color: #007AFF !important; font-weight: 900 !important; }

    /* 食材条 */
    .ing-scroll { display: flex; overflow-x: auto; gap: 8px; padding: 5px 15px 15px 15px; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
    .pill { background: #F2F2F7; color: #3A3A3C; padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; white-space: nowrap; }
    .pill-hit { background: #FFF4E5; color: #FF9500; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 业务核心逻辑
# ==========================================

def get_dish(pool, fridge, allergens, exclude=[]):
    safe = []
    nf = set([normalize(i) for i in fridge])
    for d in pool:
        if d['name'] in exclude or any(ing in allergens for ing in d['ingredients']): continue
        m = sum(1 for ing in d['ingredients'] if normalize(ing) not in nf)
        dc = d.copy(); dc['m'] = m; safe.append(dc)
    if not safe: return None
    t0 = [d for d in safe if d['m'] == 0]
    final = t0 if t0 else safe
    weighted = []
    for d in final:
        score = 10
        if d['name'] in st.session_state.prefs['likes']: score += 100
        if d['name'] in st.session_state.prefs['dislikes']: score = 1
        weighted.extend([d] * score)
    return random.choice(weighted) if weighted else None

def generate_menu():
    u = st.session_state.prefs; ms = st.session_state.menu
    ms['breakfast'] = get_dish(RECIPES_DB['breakfast'], u['fridge_items'], u['allergens'])
    ms['lunch_meat'] = get_dish(RECIPES_DB['lunch_meat'], u['fridge_items'], u['allergens'])
    ms['lunch_veg'] = get_dish(RECIPES_DB['lunch_veg'], u['fridge_items'], u['allergens'])
    ms['lunch_soup'] = get_dish(RECIPES_DB['soup'], u['fridge_items'], u['allergens'])
    ms['dinner_meat'] = get_dish(RECIPES_DB.get('dinner_meat', RECIPES_DB['lunch_meat']), u['fridge_items'], u['allergens'], [ms['lunch_meat']['name']])
    ms['fruit'] = random.choice(RECIPES_DB['fruit'])
    st.session_state.view = "dashboard"

def render_sign_img():
    m = st.session_state.menu; img = Image.new('RGB', (800, 1200), color='#FFFDF5'); d = ImageDraw.Draw(img)
    tf, hf, bf = get_pil_font(65), get_pil_font(40), get_pil_font(32)
    d.rectangle([30, 30, 770, 1170], outline="#FF9500", width=5)
    d.text((400, 120), f"{st.session_state.prefs['nickname']} 的美食日签", font=tf, fill='#FF9500', anchor="mm")
    y = 260
    def s(t, its):
        nonlocal y; d.text((400, y), f"• {t} •", font=hf, fill='#333', anchor="mm"); y += 75
        for i in its: d.text((400, y), i, font=bf, fill='#555', anchor="mm"); y += 55
        y += 40
    s("阳光早餐", [m['breakfast']['name']])
    s("能量午餐", [m['lunch_meat']['name'], m['lunch_veg']['name']])
    s("温馨晚餐", [m['dinner_meat']['name']])
    buf = io.BytesIO(); img.save(buf, format="PNG"); return buf.getvalue()

# ==========================================
# 5. UI 渲染 (Apple Standards)
# ==========================================

# 侧边栏
with st.sidebar:
    st.image("https://img.icons8.com/color/480/dog.png", width=100)
    with st.expander("👤 档案与过敏原", expanded=True):
        u = st.session_state.prefs
        u['nickname'] = st.text_input("昵称", u['nickname'])
        common = ["牛肉", "牛奶", "奶粉", "鸡蛋", "虾", "鱼"]
        al = st.multiselect("常见屏蔽", common, default=[x for x in u['allergens'] if x in common])
        custom = st.text_input("自定义 (逗号分隔)")
        if st.button("💾 保存档案"):
            if custom: al.extend([x.strip() for x in custom.split(',')])
            u['allergens'] = list(set(al)); save_prefs(); st.success("已更新")

# 主页逻辑
if st.session_state.view == "cook":
    d = st.session_state.get('focus_item')
    st.button("⬅️ 返回菜单", on_click=lambda: st.session_state.update({"view": "dashboard"}))
    st.markdown(f"<div style='background:white; border-radius:26px; padding:30px; box-shadow:0 10px 30px rgba(0,0,0,0.05);'><h2>{d['name']}</h2><hr>"+
                "".join([f"<p style='font-size:18px;'><b>{i+1}.</b> {s}</p>" for i,s in enumerate(d.get('steps_list',["准备食材","下锅煮熟","出锅盛盘"]))])+"</div>", unsafe_allow_html=True)
else:
    # 1. Header (强制不换行)
    # 使用稳定 HTTPS URL 解决图片显示问题
    BLUEY_IMAGE = "https://img.icons8.com/color/480/dog.png"
    st.markdown(f'''
    <div class="custom-header">
        <div class="profile">
            <img src="{BLUEY_IMAGE}" class="avatar-round" onerror="this.src='https://via.placeholder.com/85?text=🐶'">
            <div class="name">Hi, {st.session_state.prefs["nickname"]}!</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 2. 功能图标 (4列强排，锁定不堆叠)
    ce, cdl, cwx, cpl = st.columns([5.5, 1.5, 1.5, 1.5])
    with cdl:
        st.markdown('<div class="top-btn-ios">', unsafe_allow_html=True)
        if st.session_state.menu['breakfast']:
            st.download_button("📥", data=render_sign_img(), file_name="menu.png")
        else: st.button("📥", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with cwx:
        st.markdown('<div class="top-btn-ios">', unsafe_allow_html=True)
        st.button("💬", on_click=lambda: st.toast("✅ 已推送到微信"))
        st.markdown('</div>', unsafe_allow_html=True)
    with cpl:
        st.markdown('<div class="top-btn-ios">', unsafe_allow_html=True)
        st.button("📅", on_click=lambda: st.toast("📅 周计划已准备好"))
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. 生成大按钮
    st.markdown('<div class="gen-action">', unsafe_allow_html=True)
    if st.button("✨ 生成今日菜单", key="gen_now"):
        with st.spinner("魔法规划中..."): time.sleep(0.5); generate_menu()
    st.markdown('</div><div class="hint-label">👆 点击上方橙色按钮生成菜单</div>', unsafe_allow_html=True)

    # 4. 卡片渲染
    def render_ios_card(title, color, keys):
        st.markdown(f'<div class="card-ios"><div class="card-banner {color}">{title}</div>', unsafe_allow_html=True)
        for k in keys:
            d = st.session_state.menu[k]
            if not d: continue
            is_l = d['name'] in st.session_state.prefs['likes']
            
            # iPhone 强制横排的核心 column 比例
            cn, b1, b2, b3, b4 = st.columns([3.5, 1.6, 1.6, 1.6, 1.6])
            with cn: st.markdown(f'<div class="dish-label">{d["name"]}</div>', unsafe_allow_html=True)
            with b1: 
                st.markdown(f'<div class="mini-btn-box {"loved" if is_l else ""}">', unsafe_allow_html=True)
                if st.button("❤️" if is_l else "🙂", key=f"lk_{k}"):
                    if d['name'] in st.session_state.prefs['likes']: st.session_state.prefs['likes'].remove(d['name'])
                    else: 
                        st.session_state.prefs['likes'].append(d['name'])
                        if d['name'] in st.session_state.prefs['dislikes']: st.session_state.prefs['dislikes'].remove(d['name'])
                    save_prefs(); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with b2:
                st.markdown('<div class="mini-btn-box">', unsafe_allow_html=True)
                if st.button("😐", key=f"dl_{k}"): 
                    st.session_state.prefs['dislikes'].append(d['name']); save_prefs(); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with b3:
                st.markdown('<div class="mini-btn-box cooking">', unsafe_allow_html=True)
                if st.button("🍳", key=f"ck_{k}"): st.session_state.update({"focus_item": d, "view_mode": "cook"}); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with b4:
                st.markdown('<div class="mini-btn-box">', unsafe_allow_html=True)
                if st.button("🔄", key=f"sw_{k}"): generate_menu(); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 食材滚动条
            nf = [normalize(i) for i in st.session_state.prefs['fridge_items']]
            ing_h = "".join([f'<span class="pill {"pill-hit" if normalize(i) in nf else ""}">{i}</span>' for i in d['ingredients']])
            st.markdown(f'<div class="ing-scroll">{ing_h}</div>', unsafe_allow_html=True)
            if k != keys[-1]: st.markdown("<hr style='margin:0 15px; border:0; border-top:1px solid #F2F2F7;'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.menu['breakfast']:
        render_ios_card("早 餐", "orange-bar", ['breakfast'])
        render_ios_card("午 餐", "blue-bar", ['lunch_meat', 'lunch_veg', 'lunch_soup'])
        render_ios_card("晚 餐", "purple-bar", ['dinner_meat'])
        
        with st.expander("📜 历史收藏记录"):
            for h in load_history()[:5]:
                st.markdown(f'<div class="hist-card"><div class="hist-head">📅 {h["date"]}</div><div style="font-size:14px;">🌅 {h["menu"]["breakfast"]}<br>☀️ {h["menu"]["lunch"][0]} 等</div></div>', unsafe_allow_html=True)