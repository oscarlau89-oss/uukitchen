# recipe_data.py
# V17.2 修正版：修复了食材与菜名不符的脏数据 (Data Cleaned)

RECIPES_DB = {
    # ==================================================
    # 🌅 早餐 (Breakfast)
    # ==================================================
    "breakfast": [
        {"name": "🎃 南瓜小米粥", "ingredients": ["南瓜", "小米"], "full_ingredients": "老南瓜 60g，小米 30g", "time": "25分钟", "difficulty": "⭐", "steps_list": ["小米泡20分钟。", "水开下米煮15分钟。", "下南瓜丁煮10分钟。", "压泥混合。"], "nutrition": "养胃", "tags": ["易消化"], "desc": "经典养胃"},
        {"name": "🥕 胡萝卜鸡蛋饼", "ingredients": ["胡萝卜", "鸡蛋", "面粉"], "full_ingredients": "胡萝卜，鸡蛋，面粉", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["胡萝卜擦丝焯水。", "调蛋糊。", "煎两面黄。"], "nutrition": "维A", "tags": ["手指食物"], "desc": "软嫩"},
        {"name": "🥔 土豆丝鸡蛋饼", "ingredients": ["土豆", "鸡蛋", "面粉"], "full_ingredients": "土豆，鸡蛋，面粉", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["土豆擦丝不洗。", "拌蛋液面粉。", "煎熟。"], "nutrition": "能量", "tags": ["焦香"], "desc": "香脆"},
        {"name": "🥛 牛奶燕麦粥", "ingredients": ["牛奶", "燕麦"], "full_ingredients": "牛奶，燕麦", "time": "5分钟", "difficulty": "⭐", "steps_list": ["燕麦煮软。", "加牛奶煮微沸。"], "nutrition": "钙", "tags": ["通便"], "desc": "奶香"},
        {"name": "🥬 青菜瘦肉粥", "ingredients": ["青菜", "猪肉", "大米"], "full_ingredients": "大米，肉末，青菜", "time": "30分钟", "difficulty": "⭐", "steps_list": ["煮白粥。", "肉末滑散放入。", "出锅放青菜。"], "nutrition": "补铁", "tags": ["荤素"], "desc": "全面"},
        {"name": "🐟 鳕鱼鲜蔬粥", "ingredients": ["鳕鱼", "大米", "西兰花"], "full_ingredients": "鳕鱼，大米，西兰花", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["鳕鱼蒸熟捣碎。", "放入粥里煮。", "加菜碎。"], "nutrition": "DHA", "tags": ["补脑"], "desc": "鲜美"},
        {"name": "🥞 香蕉松饼", "ingredients": ["香蕉", "鸡蛋", "面粉"], "full_ingredients": "香蕉，鸡蛋，面粉", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["香蕉压泥加蛋。", "加面粉调糊。", "无油煎熟。"], "nutrition": "钾", "tags": ["无糖"], "desc": "天然甜"},
        {"name": "🍞 芝士厚蛋烧", "ingredients": ["鸡蛋", "奶酪"], "full_ingredients": "鸡蛋，奶酪片", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["蛋液加奶。", "卷入奶酪煎熟。"], "nutrition": "钙", "tags": ["补钙"], "desc": "拉丝"},
        {"name": "🥪 鸡蛋三明治", "ingredients": ["面包", "鸡蛋"], "full_ingredients": "吐司，鸡蛋", "time": "5分钟", "difficulty": "⭐", "steps_list": ["煮蛋压碎拌酱。", "夹入吐司切边。"], "nutrition": "便携", "tags": ["野餐"], "desc": "方便"},
        {"name": "🍠 紫薯芝士球", "ingredients": ["红薯", "奶酪"], "full_ingredients": "紫薯/红薯，芝士", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["薯泥包芝士。", "搓圆烤熟。"], "nutrition": "花青素", "tags": ["零食"], "desc": "软糯"},
        {"name": "🌽 玉米面窝窝", "ingredients": ["玉米", "面粉"], "full_ingredients": "玉米面，面粉", "time": "20分钟", "difficulty": "⭐⭐", "steps_list": ["揉团捏窝。", "蒸15分钟。"], "nutrition": "粗粮", "tags": ["纤维"], "desc": "金黄"},
        {"name": "🥚 蒸水蛋", "ingredients": ["鸡蛋"], "full_ingredients": "鸡蛋，温水", "time": "10分钟", "difficulty": "⭐", "steps_list": ["1.5倍温水搅匀。", "过筛去泡。", "蒸10分钟。"], "nutrition": "易吸收", "tags": ["嫩滑"], "desc": "镜面"},
        {"name": "🍜 鸡汤细面", "ingredients": ["鸡肉", "面条", "青菜"], "full_ingredients": "鸡汤，细面，青菜", "time": "15分钟", "difficulty": "⭐", "steps_list": ["鸡汤煮面。", "加青菜烫熟。"], "nutrition": "滋补", "tags": ["汤面"], "desc": "鲜美"},
        {"name": "🥑 牛油果拌饭", "ingredients": ["牛油果", "鸡蛋", "大米"], "full_ingredients": "牛油果，蛋黄，米饭", "time": "5分钟", "difficulty": "⭐", "steps_list": ["牛油果压泥。", "拌入热饭和蛋黄。"], "nutrition": "好脂肪", "tags": ["大脑"], "desc": "森林黄油"},
        {"name": "🍝 番茄肉酱面", "ingredients": ["猪肉", "西红柿", "面条"], "full_ingredients": "番茄，肉末，面条", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["番茄炒沙加肉炖酱。", "面煮熟。", "浇汁。"], "nutrition": "开胃", "tags": ["酸甜"], "desc": "浓郁"},
        {"name": "🥣 杂粮二米糊", "ingredients": ["小米", "大米"], "full_ingredients": "小米，大米", "time": "20分钟", "difficulty": "⭐", "steps_list": ["破壁机打糊。"], "nutrition": "润肠", "tags": ["好吸收"], "desc": "液体营养"},
        {"name": "🥟 鲜虾小馄饨", "ingredients": ["虾仁", "猪肉", "馄饨皮"], "full_ingredients": "虾仁，肉泥，馄饨皮", "time": "20分钟", "difficulty": "⭐⭐⭐", "steps_list": ["混合做馅。", "包馄饨。", "煮熟。"], "nutrition": "钙", "tags": ["一口一个"], "desc": "皮薄"},
        {"name": "🎃 南瓜发糕", "ingredients": ["南瓜", "面粉"], "full_ingredients": "南瓜泥，面粉，酵母", "time": "40分钟", "difficulty": "⭐⭐⭐", "steps_list": ["发酵至两倍大。", "蒸20分钟。"], "nutrition": "易消化", "tags": ["蓬松"], "desc": "松软"},
        {"name": "🐟 鳕鱼肠蛋卷", "ingredients": ["鸡蛋", "鳕鱼"], "full_ingredients": "鸡蛋，鳕鱼肠", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["摊蛋皮。", "卷入鱼肠。", "切段。"], "nutrition": "蛋白", "tags": ["造型"], "desc": "可爱"},
        {"name": "🥛 奶香馒头片", "ingredients": ["面包", "鸡蛋"], "full_ingredients": "馒头/面包，蛋液", "time": "8分钟", "difficulty": "⭐", "steps_list": ["裹蛋液。", "煎两面黄。"], "nutrition": "能量", "tags": ["改造"], "desc": "剩饭变身"},
    ],

    # ==================================================
    # ☀️ 午餐 (Lunch)
    # ==================================================
    "lunch_meat": [
        {"name": "🍅 番茄土豆炖牛腩", "ingredients": ["牛肉", "土豆", "西红柿"], "full_ingredients": "牛腩，番茄，土豆", "time": "60分钟", "difficulty": "⭐⭐⭐", "steps_list": ["牛肉焯水。", "番茄炒沙炖肉。", "加土豆炖软。"], "nutrition": "补铁", "tags": ["维C"], "desc": "拌饭神器"},
        {"name": "🥩 彩椒牛肉粒", "ingredients": ["牛肉", "彩椒"], "full_ingredients": "牛里脊，彩椒", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["牛肉腌制滑油。", "彩椒快炒。", "混合。"], "nutrition": "维生素", "tags": ["嫩"], "desc": "色彩丰富"},
        {"name": "🥔 土豆肥牛卷", "ingredients": ["牛肉", "土豆"], "full_ingredients": "肥牛，土豆", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["土豆煎焦黄。", "下肥牛调味炒熟。"], "nutrition": "能量", "tags": ["好做"], "desc": "吉野家风味"},
        {"name": "🥩 芦笋炒牛肉", "ingredients": ["牛肉", "芦笋"], "full_ingredients": "牛里脊，芦笋", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["芦笋焯水。", "牛肉快炒。"], "nutrition": "叶酸", "tags": ["清爽"], "desc": "清新"},
        {"name": "🥩 滑蛋牛肉", "ingredients": ["牛肉", "鸡蛋"], "full_ingredients": "牛里脊，鸡蛋", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["牛肉浆好。", "蛋液混合滑炒。"], "nutrition": "双蛋白", "tags": ["软嫩"], "desc": "港式"},
        
        {"name": "🍖 糖醋里脊(番茄)", "ingredients": ["猪肉", "西红柿"], "full_ingredients": "里脊，番茄酱", "time": "30分钟", "difficulty": "⭐⭐⭐", "steps_list": ["肉条炸熟。", "裹番茄浓汁。"], "nutrition": "开胃", "tags": ["酸甜"], "desc": "宝宝最爱"},
        {"name": "🥘 肉末蒸豆腐", "ingredients": ["猪肉", "豆腐"], "full_ingredients": "肉末，内脂豆腐", "time": "15分钟", "difficulty": "⭐", "steps_list": ["肉末炒香。", "铺豆腐上蒸10分。"], "nutrition": "钙", "tags": ["易消化"], "desc": "入口即化"},
        {"name": "🥕 胡萝卜肉丸", "ingredients": ["猪肉", "胡萝卜"], "full_ingredients": "肉泥，胡萝卜", "time": "25分钟", "difficulty": "⭐⭐⭐", "steps_list": ["搅打上劲。", "水煮成丸。"], "nutrition": "低脂", "tags": ["软糯"], "desc": "可汤可菜"},
        {"name": "🥩 肉末茄子", "ingredients": ["猪肉", "茄子"], "full_ingredients": "肉末，茄子", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["茄子炒软。", "加肉末焖煮。"], "nutrition": "软烂", "tags": ["下饭"], "desc": "不爱吃菜也吃"},
        {"name": "🥒 黄瓜炒肉片", "ingredients": ["猪肉", "黄瓜"], "full_ingredients": "里脊，黄瓜", "time": "10分钟", "difficulty": "⭐", "steps_list": ["肉片滑熟。", "下黄瓜快炒。"], "nutrition": "清爽", "tags": ["家常"], "desc": "简单"},

        {"name": "🍗 香菇蒸滑鸡", "ingredients": ["鸡肉", "香菇"], "full_ingredients": "鸡腿肉，香菇", "time": "25分钟", "difficulty": "⭐⭐", "steps_list": ["鸡肉腌制。", "混香菇蒸20分。"], "nutrition": "不上火", "tags": ["嫩滑"], "desc": "原汁原味"},
        {"name": "🌽 玉米鸡丁", "ingredients": ["鸡肉", "玉米", "胡萝卜"], "full_ingredients": "鸡胸，玉米，胡萝卜", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["鸡丁滑炒。", "加蔬菜丁炒熟。"], "nutrition": "纤维", "tags": ["色彩"], "desc": "五彩斑斓"},
        {"name": "🍗 照烧鸡腿", "ingredients": ["鸡肉", "西兰花"], "full_ingredients": "鸡腿，西兰花", "time": "20分钟", "difficulty": "⭐⭐", "steps_list": ["煎两面黄。", "加汁焖煮。"], "nutrition": "蛋白", "tags": ["满足"], "desc": "大口吃肉"},
        {"name": "🐔 宫保鸡丁(免辣)", "ingredients": ["鸡肉", "花生", "黄瓜"], "full_ingredients": "鸡肉，黄瓜，花生", "time": "15分钟", "difficulty": "⭐⭐⭐", "steps_list": ["糖醋汁调味。", "快炒。"], "nutrition": "开胃", "tags": ["下饭"], "desc": "酸甜口"},
        {"name": "🥔 土豆炖鸡块", "ingredients": ["鸡肉", "土豆"], "full_ingredients": "鸡块，土豆", "time": "30分钟", "difficulty": "⭐⭐", "steps_list": ["炒香。", "炖20分钟。"], "nutrition": "能量", "tags": ["家常"], "desc": "软烂"},

        {"name": "🐟 清蒸鳕鱼", "ingredients": ["鳕鱼", "姜"], "full_ingredients": "鳕鱼，姜", "time": "15分钟", "difficulty": "⭐", "steps_list": ["腌制。", "蒸8分钟。"], "nutrition": "DHA", "tags": ["补脑"], "desc": "深海营养"},
        {"name": "🐟 彩椒三文鱼", "ingredients": ["三文鱼", "彩椒"], "full_ingredients": "三文鱼，彩椒", "time": "12分钟", "difficulty": "⭐⭐", "steps_list": ["煎熟鱼丁。", "炒彩椒。"], "nutrition": "Omega3", "tags": ["明目"], "desc": "色彩丰富"},
        {"name": "🦐 虾仁滑蛋", "ingredients": ["虾仁", "鸡蛋"], "full_ingredients": "虾仁，鸡蛋", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["虾仁焯水。", "滑蛋。"], "nutrition": "嫩滑", "tags": ["高蛋白"], "desc": "经典"},
        {"name": "🐟 茄汁巴沙鱼", "ingredients": ["鱼", "西红柿"], "full_ingredients": "巴沙鱼，番茄", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["炒番茄酱。", "煮鱼片。"], "nutrition": "无刺", "tags": ["开胃"], "desc": "酸甜"},
        {"name": "🦐 宫保虾球", "ingredients": ["虾仁", "黄瓜"], "full_ingredients": "虾仁，黄瓜，花生", "time": "15分钟", "difficulty": "⭐⭐⭐", "steps_list": ["糖醋汁。", "快炒。"], "nutrition": "开胃", "tags": ["下饭"], "desc": "酸甜"},
    ],
    
    "lunch_veg": [
        {"name": "🥦 蒜蓉西兰花", "ingredients": ["西兰花"], "full_ingredients": "西兰花，蒜", "time": "8分钟", "difficulty": "⭐", "steps_list": ["焯水。", "爆炒。"], "nutrition": "维C", "tags": ["纤维"], "desc": "必备"},
        {"name": "🥕 清炒胡萝卜", "ingredients": ["胡萝卜"], "full_ingredients": "胡萝卜", "time": "10分钟", "difficulty": "⭐", "steps_list": ["多油煸炒。", "焖软。"], "nutrition": "维A", "tags": ["护眼"], "desc": "甜甜的"},
        {"name": "🥬 蚝油生菜", "ingredients": ["生菜"], "full_ingredients": "生菜，蚝油", "time": "5分钟", "difficulty": "⭐", "steps_list": ["焯水。", "淋汁。"], "nutrition": "纤维", "tags": ["快手"], "desc": "水灵"},
        {"name": "🍄 什锦菌菇", "ingredients": ["香菇", "口蘑"], "full_ingredients": "杂菇", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["焯水。", "炒出汁。"], "nutrition": "免疫力", "tags": ["鲜"], "desc": "鲜美"},
        {"name": "🥔 地三鲜(少油)", "ingredients": ["土豆", "茄子", "彩椒"], "full_ingredients": "土豆，茄子，彩椒", "time": "20分钟", "difficulty": "⭐⭐⭐", "steps_list": ["煎熟。", "炒匀。"], "nutrition": "丰富", "tags": ["下饭"], "desc": "东北菜"},
        {"name": "🥬 菠菜炒蛋", "ingredients": ["菠菜", "鸡蛋"], "full_ingredients": "菠菜，鸡蛋", "time": "10分钟", "difficulty": "⭐", "steps_list": ["焯水。", "混炒。"], "nutrition": "叶酸", "tags": ["补铁"], "desc": "经典"},
        {"name": "🍅 糖拌西红柿", "ingredients": ["西红柿"], "full_ingredients": "番茄，糖", "time": "3分钟", "difficulty": "⭐", "steps_list": ["切片。", "撒糖。"], "nutrition": "茄红素", "tags": ["酸甜"], "desc": "凉菜"},
        {"name": "🥔 酸辣土豆丝", "ingredients": ["土豆"], "full_ingredients": "土豆，醋", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["泡水去淀粉。", "爆炒。"], "nutrition": "开胃", "tags": ["脆"], "desc": "国民菜"},
        {"name": "🎃 蒸贝贝南瓜", "ingredients": ["南瓜"], "full_ingredients": "南瓜", "time": "20分钟", "difficulty": "⭐", "steps_list": ["整只蒸。"], "nutrition": "代餐", "tags": ["甜"], "desc": "粉糯"},
        {"name": "🍆 蒜泥茄子", "ingredients": ["茄子"], "full_ingredients": "茄子，蒜泥", "time": "15分钟", "difficulty": "⭐", "steps_list": ["蒸软。", "撕条拌匀。"], "nutrition": "少油", "tags": ["软"], "desc": "健康"},
        {"name": "🍅 菜花炒西红柿", "ingredients": ["西红柿", "西兰花"], "full_ingredients": "花菜，番茄", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["花菜焯水。", "茄汁炒。"], "nutrition": "抗氧化", "tags": ["酸甜"], "desc": "开胃"},
        {"name": "🥬 手撕包菜", "ingredients": ["青菜"], "full_ingredients": "圆白菜，醋", "time": "8分钟", "difficulty": "⭐", "steps_list": ["手撕。", "爆炒。"], "nutrition": "维C", "tags": ["脆"], "desc": "下饭"},
        {"name": "🥒 拍黄瓜", "ingredients": ["黄瓜"], "full_ingredients": "黄瓜，蒜", "time": "5分钟", "difficulty": "⭐", "steps_list": ["拍碎。", "拌匀。"], "nutrition": "清爽", "tags": ["解腻"], "desc": "凉菜"},
        {"name": "🌽 松仁玉米", "ingredients": ["玉米"], "full_ingredients": "玉米粒", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["炒熟勾芡。"], "nutrition": "粗粮", "tags": ["甜"], "desc": "勺子挖"},
        {"name": "🍄 香菇油菜", "ingredients": ["香菇", "青菜"], "full_ingredients": "香菇，油菜", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["摆盘炒熟。"], "nutrition": "维C", "tags": ["搭配"], "desc": "好看"},
    ],

    # ==================================================
    # 🌙 晚餐 (Dinner) - 清淡/易消化
    # ==================================================
    "dinner_meat": [
        {"name": "🐟 鲈鱼豆腐汤", "ingredients": ["鱼", "豆腐"], "full_ingredients": "鲈鱼，豆腐", "time": "30分钟", "difficulty": "⭐⭐", "steps_list": ["煎鱼。", "炖白汤。", "下豆腐。"], "nutrition": "高钙", "tags": ["汤"], "desc": "好消化"},
        {"name": "🐔 椰子鸡", "ingredients": ["鸡肉"], "full_ingredients": "鸡块，椰子水", "time": "30分钟", "difficulty": "⭐⭐", "steps_list": ["椰子水煮鸡。", "不加调料。"], "nutrition": "清甜", "tags": ["不油"], "desc": "海南菜"},
        {"name": "🥚 蛤蜊蒸蛋", "ingredients": ["鸡蛋", "海鲜"], "full_ingredients": "蛤蜊，鸡蛋", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["煮开口。", "加蛋液蒸。"], "nutrition": "锌", "tags": ["鲜"], "desc": "鲜美"},
        {"name": "🦐 蒸酿秋葵", "ingredients": ["虾仁", "秋葵"], "full_ingredients": "秋葵，虾滑", "time": "15分钟", "difficulty": "⭐⭐⭐", "steps_list": ["填虾滑。", "蒸熟。"], "nutrition": "粘液蛋白", "tags": ["造型"], "desc": "星星"},
        {"name": "🍲 珍珠糯米丸", "ingredients": ["猪肉", "大米"], "full_ingredients": "肉丸，糯米", "time": "30分钟", "difficulty": "⭐⭐⭐", "steps_list": ["裹糯米。", "蒸熟。"], "nutrition": "能量", "tags": ["软糯"], "desc": "晶莹"},
        {"name": "🥬 白菜酿肉", "ingredients": ["猪肉", "青菜"], "full_ingredients": "白菜，肉馅", "time": "20分钟", "difficulty": "⭐⭐⭐", "steps_list": ["白菜卷肉。", "蒸熟。"], "nutrition": "纤维", "tags": ["低脂"], "desc": "翡翠白玉"},
        {"name": "🥚 猪肉炖蛋", "ingredients": ["猪肉", "鸡蛋"], "full_ingredients": "肉饼，鸡蛋", "time": "20分钟", "difficulty": "⭐⭐", "steps_list": ["肉饼铺底。", "打蛋蒸。"], "nutrition": "滋补", "tags": ["传统"], "desc": "客家菜"},
        {"name": "🍄 香菇酿肉", "ingredients": ["猪肉", "香菇"], "full_ingredients": "香菇，肉馅", "time": "20分钟", "difficulty": "⭐⭐⭐", "steps_list": ["填肉。", "蒸熟。"], "nutrition": "多糖", "tags": ["精致"], "desc": "小碗菜"},
        {"name": "🐟 鱼泥豆腐羹", "ingredients": ["鱼", "豆腐"], "full_ingredients": "鱼泥，豆腐", "time": "15分钟", "difficulty": "⭐", "steps_list": ["煮成羹。"], "nutrition": "易吸收", "tags": ["流食"], "desc": "吞咽"},
        {"name": "🥣 冬瓜汆丸子", "ingredients": ["猪肉", "冬瓜"], "full_ingredients": "冬瓜，肉丸", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["煮冬瓜。", "下丸子。"], "nutrition": "低脂", "tags": ["汤菜"], "desc": "清爽"},
        {"name": "🦐 虾仁豆腐", "ingredients": ["虾仁", "豆腐"], "full_ingredients": "虾仁，豆腐", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["炒虾仁。", "焖豆腐。"], "nutrition": "高钙", "tags": ["滑嫩"], "desc": "拌饭"},
        {"name": "🍗 蒸鸡翅", "ingredients": ["鸡肉", "土豆"], "full_ingredients": "鸡翅，土豆", "time": "30分钟", "difficulty": "⭐⭐", "steps_list": ["腌制。", "蒸熟。"], "nutrition": "不上火", "tags": ["脱骨"], "desc": "软烂"},
        {"name": "🦐 丝瓜炒虾仁", "ingredients": ["虾仁"], "full_ingredients": "丝瓜，虾仁", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["快炒。"], "nutrition": "补水", "tags": ["清爽"], "desc": "清甜"},
        {"name": "🥕 胡萝卜肉丸", "ingredients": ["猪肉", "胡萝卜"], "full_ingredients": "肉泥，胡萝卜", "time": "25分钟", "difficulty": "⭐⭐⭐", "steps_list": ["煮丸子。"], "nutrition": "低脂", "tags": ["软糯"], "desc": "连汤吃"},
        {"name": "🥬 莲藕蒸肉饼", "ingredients": ["猪肉", "莲藕"], "full_ingredients": "肉泥，莲藕", "time": "20分钟", "difficulty": "⭐⭐", "steps_list": ["混合蒸。"], "nutrition": "润肺", "tags": ["脆爽"], "desc": "口感好"},
    ],

    "dinner_veg": [
        {"name": "🥬 上汤娃娃菜", "ingredients": ["娃娃菜"], "full_ingredients": "娃娃菜，虾皮", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["高汤煮软。", "连汤吃。"], "nutrition": "汤鲜", "tags": ["软烂"], "desc": "暖胃"},
        {"name": "🌽 玉米烧冬瓜", "ingredients": ["冬瓜", "玉米"], "full_ingredients": "冬瓜，玉米", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["红烧汁焖。"], "nutrition": "利尿", "tags": ["甜"], "desc": "素菜荤做"},
        {"name": "🥬 粉丝娃娃菜", "ingredients": ["娃娃菜"], "full_ingredients": "娃娃菜，粉丝，蒜", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["蒜蓉蒸。"], "nutrition": "入味", "tags": ["下饭"], "desc": "吸汁"},
        {"name": "🥒 腐竹拌黄瓜", "ingredients": ["黄瓜", "豆腐"], "full_ingredients": "腐竹，黄瓜", "time": "10分钟", "difficulty": "⭐", "steps_list": ["凉拌。"], "nutrition": "钙", "tags": ["豆制品"], "desc": "清爽"},
        {"name": "🎃 南瓜蒸百合", "ingredients": ["南瓜"], "full_ingredients": "南瓜，百合", "time": "20分钟", "difficulty": "⭐", "steps_list": ["蒸熟。"], "nutrition": "润肺", "tags": ["甜"], "desc": "养生"},
        {"name": "🥒 响油黄瓜", "ingredients": ["黄瓜"], "full_ingredients": "黄瓜，蒜", "time": "5分钟", "difficulty": "⭐", "steps_list": ["卷起。", "淋热油。"], "nutrition": "补水", "tags": ["造型"], "desc": "精致"},
        {"name": "🌽 奶香玉米", "ingredients": ["玉米", "牛奶"], "full_ingredients": "玉米，牛奶", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["牛奶煮。"], "nutrition": "粗粮", "tags": ["香"], "desc": "奶香"},
        {"name": "🥦 凉拌木耳", "ingredients": ["木耳"], "full_ingredients": "木耳，洋葱", "time": "10分钟", "difficulty": "⭐", "steps_list": ["焯水过凉。", "拌匀。"], "nutrition": "排毒", "tags": ["脆"], "desc": "爽口"},
        {"name": "🥕 蒸胡萝卜丝", "ingredients": ["胡萝卜"], "full_ingredients": "胡萝卜，面粉", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["裹粉蒸。", "蘸汁。"], "nutrition": "维A", "tags": ["主食"], "desc": "老味道"},
        {"name": "🍄 蚝油杏鲍菇", "ingredients": ["香菇"], "full_ingredients": "杏鲍菇，蚝油", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["干煸。", "调味。"], "nutrition": "口感", "tags": ["鲜"], "desc": "像肉"},
    ],

    # ==================================================
    # 🥣 汤羹 (Soup)
    # ==================================================
    "soup": [
        {"name": "🥣 芙蓉鲜蔬汤", "ingredients": ["菠菜", "鸡蛋"], "full_ingredients": "菠菜，蛋清", "time": "5分钟", "difficulty": "⭐", "steps_list": ["淋蛋液。", "撒菜碎。"], "nutrition": "清淡", "tags": ["补水"], "desc": "翡翠白玉"},
        {"name": "🥣 紫菜蛋花汤", "ingredients": ["鸡蛋"], "full_ingredients": "紫菜，鸡蛋", "time": "5分钟", "difficulty": "⭐", "steps_list": ["水开淋蛋。"], "nutrition": "碘", "tags": ["快手"], "desc": "经典"},
        {"name": "🥣 番茄菌菇汤", "ingredients": ["西红柿", "香菇"], "full_ingredients": "番茄，杂菇", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["炒出汁。", "煮菌菇。"], "nutrition": "开胃", "tags": ["酸甜"], "desc": "开胃"},
        {"name": "🥣 丝瓜蛋汤", "ingredients": ["鸡蛋"], "full_ingredients": "丝瓜，鸡蛋", "time": "8分钟", "difficulty": "⭐", "steps_list": ["炒丝瓜。", "煮蛋。"], "nutrition": "补水", "tags": ["夏天"], "desc": "清热"},
        {"name": "🥣 豆腐蛤蜊汤", "ingredients": ["豆腐", "海鲜"], "full_ingredients": "蛤蜊，豆腐", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["煮开口。", "炖豆腐。"], "nutrition": "锌", "tags": ["鲜"], "desc": "海味"},
        {"name": "🥣 猪肝菠菜汤", "ingredients": ["猪肉", "菠菜"], "full_ingredients": "猪肝，菠菜", "time": "10分钟", "difficulty": "⭐⭐", "steps_list": ["煮猪肝。", "烫菠菜。"], "nutrition": "补铁", "tags": ["明目"], "desc": "补血"},
        {"name": "🥣 罗宋汤(儿版)", "ingredients": ["牛肉", "西红柿", "土豆"], "full_ingredients": "牛肉，番茄，土豆", "time": "50分钟", "difficulty": "⭐⭐⭐", "steps_list": ["炒香炖煮。"], "nutrition": "全面", "tags": ["浓郁"], "desc": "西式"},
        {"name": "🥣 玉米排骨汤", "ingredients": ["猪肉", "玉米"], "full_ingredients": "排骨，玉米", "time": "60分钟", "difficulty": "⭐⭐", "steps_list": ["炖1小时。"], "nutrition": "滋补", "tags": ["清甜"], "desc": "啃骨头"},
        {"name": "🥣 山药排骨汤", "ingredients": ["猪肉", "山药"], "full_ingredients": "排骨，山药", "time": "60分钟", "difficulty": "⭐⭐", "steps_list": ["炖烂。"], "nutrition": "健脾", "tags": ["养生"], "desc": "汤浓"},
        {"name": "🥣 莲藕排骨汤", "ingredients": ["猪肉", "莲藕"], "full_ingredients": "排骨，莲藕", "time": "60分钟", "difficulty": "⭐⭐", "steps_list": ["炖粉糯。"], "nutrition": "润肺", "tags": ["秋天"], "desc": "拉丝"},
        {"name": "🥣 白萝卜羊肉汤", "ingredients": ["羊肉"], "full_ingredients": "羊肉，白萝卜", "time": "60分钟", "difficulty": "⭐⭐⭐", "steps_list": ["去膻炖烂。"], "nutrition": "暖身", "tags": ["冬天"], "desc": "温补"},
        {"name": "🥣 鲫鱼豆腐汤", "ingredients": ["鱼", "豆腐"], "full_ingredients": "鲫鱼，豆腐", "time": "40分钟", "difficulty": "⭐⭐⭐", "steps_list": ["煎鱼炖白。"], "nutrition": "高钙", "tags": ["补钙"], "desc": "奶白"},
        {"name": "🥣 鱼头豆腐汤", "ingredients": ["鱼", "豆腐"], "full_ingredients": "鱼头，豆腐", "time": "40分钟", "difficulty": "⭐⭐⭐", "steps_list": ["煎鱼炖白。"], "nutrition": "DHA", "tags": ["聪明"], "desc": "黄金搭档"},
        {"name": "🥣 虫草花鸡汤", "ingredients": ["鸡肉"], "full_ingredients": "鸡肉，虫草花", "time": "50分钟", "difficulty": "⭐⭐", "steps_list": ["炖煮。"], "nutrition": "免疫力", "tags": ["金黄"], "desc": "好喝"},
        {"name": "🥣 南瓜浓汤", "ingredients": ["南瓜", "牛奶"], "full_ingredients": "南瓜，牛奶", "time": "20分钟", "difficulty": "⭐⭐", "steps_list": ["打泥煮开。"], "nutrition": "纤维", "tags": ["西餐"], "desc": "香甜"},
        {"name": "🥣 银耳雪梨汤", "ingredients": ["水果"], "full_ingredients": "银耳，雪梨", "time": "40分钟", "difficulty": "⭐⭐", "steps_list": ["炖出胶。"], "nutrition": "润肺", "tags": ["甜汤"], "desc": "止咳"},
        {"name": "🥣 绿豆汤", "ingredients": ["水果"], "full_ingredients": "绿豆", "time": "40分钟", "difficulty": "⭐", "steps_list": ["煮开花。"], "nutrition": "消暑", "tags": ["夏天"], "desc": "解渴"},
        {"name": "🥣 味噌汤", "ingredients": ["豆腐"], "full_ingredients": "味噌，豆腐", "time": "10分钟", "difficulty": "⭐", "steps_list": ["化开味噌。"], "nutrition": "豆类", "tags": ["日式"], "desc": "异域"},
        {"name": "🥣 酸辣汤(微辣)", "ingredients": ["豆腐", "鸡蛋", "木耳"], "full_ingredients": "豆腐，木耳，蛋", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["勾芡加醋。"], "nutrition": "开胃", "tags": ["暖身"], "desc": "发汗"},
        {"name": "🥣 冬瓜肉丸汤", "ingredients": ["猪肉", "冬瓜"], "full_ingredients": "冬瓜，肉丸", "time": "15分钟", "difficulty": "⭐⭐", "steps_list": ["煮熟。"], "nutrition": "解腻", "tags": ["清爽"], "desc": "不油"},
    ],

    # ==================================================
    # 🍎 水果 (Fruit)
    # ==================================================
    "fruit": [
        "🍎 苹果片", "🍌 香蕉段", "🫐 蓝莓", "🥝 猕猴桃片", "🍊 橙子切块", 
        "🍇 去皮葡萄", "🐉 火龙果", "🍓 草莓", "🍈 哈密瓜", "🍒 车厘子", 
        "🍐 炖雪梨", "🥭 芒果丁", "🍑 桃子", "🍉 西瓜", "🍍 菠萝", 
        "🍅 圣女果", "🍊 砂糖橘", "🥑 牛油果泥", "🥥 椰子肉", "🍐 香梨"
    ]
}

FRIDGE_CATEGORIES = {
    "🥩 肉禽蛋海鲜": ["鸡蛋", "牛肉", "猪肉", "鸡肉", "鳕鱼", "虾仁", "三文鱼", "鱼", "火腿", "排骨", "鸭肉", "蛤蜊", "猪肝", "干贝", "羊肉"],
    "🥦 蔬菜菌菇": ["西红柿", "胡萝卜", "西兰花", "土豆", "南瓜", "青菜", "菠菜", "冬瓜", "香菇", "玉米", "彩椒", "娃娃菜", "红薯", "秋葵", "西葫芦", "口蘑", "山药", "茄子", "莲藕", "黄瓜", "芦笋", "白菜", "洋葱", "荷兰豆", "木耳", "空心菜", "海带", "鲜百合", "白萝卜"],
    "🍚 主食/干货/奶": ["大米", "小米", "面粉", "面条", "豆腐", "燕麦", "牛奶", "奶酪", "面包", "馄饨皮", "紫菜", "粉丝", "腐竹", "年糕", "意面", "黑芝麻粉"]
}

# 食材同义词映射（用于标准化食材名称）
SYNONYM_MAP = {
    "番茄": "西红柿", "洋柿子": "西红柿", 
    "洋芋": "土豆", "马铃薯": "土豆",
    "大虾": "虾仁", "基围虾": "虾仁", "明虾": "虾仁",
    "花菜": "西兰花",
    "圆白菜": "青菜", "白菜": "青菜", "油菜": "青菜", "娃娃菜": "青菜",
    "牛腩": "牛肉", "牛柳": "牛肉", "肥牛": "牛肉",
    "肉末": "猪肉", "里脊": "猪肉", "五花肉": "猪肉", "排骨": "猪肉",
    "鸡腿": "鸡肉", "鸡翅": "鸡肉", "鸡胸": "鸡肉",
    "龙利鱼": "鱼", "巴沙鱼": "鱼", "鳕鱼": "鱼", "三文鱼": "鱼", "鲈鱼": "鱼", "鲫鱼": "鱼"
}

def normalize(name):
    """标准化食材名称，处理同义词"""
    clean_name = name.strip()
    return SYNONYM_MAP.get(clean_name, clean_name)