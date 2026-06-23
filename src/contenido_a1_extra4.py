"""
Extensiones A1 — Módulos 18 a 22
"""
EXTRA4 = [

    # ═══════════════════════════════════════════
    # MÓDULO 18: HAY / ESTÁ
    # ═══════════════════════════════════════════
    {
        "titulo": "Hay / Está(n)",
        "slug": "18_hay_esta",
        "lecciones": [
            {
                "slug": "067-hay",
                "tema": "Hay: existencia impersonal",
                "objetivo": "Usar HAY para expresar existencia",
                "explicacion": "Hay = there is/there are。无人称变化，不分单复数。Hay un libro en la mesa（有一本书）。Hay muchos libros（有很多书）。过去时：había（有）。用于：1. 存在某物（Hay una farmacia aquí），2. 数量（Hay 20 estudiantes），3. 泛指（Hay gente en la calle）。注意不要和estar混淆。Hay = 存在（不知道具体位置），Está = 具体位置。",
                "puntos": [
                    "Hay = 有（存在，不分单复数）",
                    "Hay un libro. / Hay muchos libros.",
                    "Hay + que + infinitivo: Hay que estudiar.",
                    "Pasado: Había...",
                ],
                "ejemplos": [
                    {"frase": "En mi ciudad hay un mercado muy grande.", "traduccion": "我的城市有一个很大的市场。", "analisis": ["Hay = 有", "mercado = 市场"]},
                    {"frase": "Hay que hacer la tarea todos los días.", "traduccion": "必须每天做作业。", "analisis": ["Hay que = 必须（无人称）", "tarea = 作业"]},
                ],
                "ejercicio": {
                    "frase": "¿Hay / Está? En la mesa ____ un libro. El libro ____ en la mesa.",
                    "traduccion": "桌子上有一本书。书在桌子上。",
                    "solucion": "Hay un libro. / El libro está en la mesa.",
                    "analisis": ["Hay = existencia (indefinido)", "Está = ubicación (específico)"],
                },
            },
            {
                "slug": "068-estar-ubicacion",
                "tema": "Estar para ubicaciones",
                "objetivo": "Usar estar para decir dónde están las cosas",
                "explicacion": "Estar用于具体位置。¿Dónde está el banco?（银行在哪里？）El banco está en la calle principal（银行在主街上）。注意和hay的区别：hay用于第一次提到（存在），estar用于已知的具体位置。Está a la derecha/izquierda（在右边/左边），Está al lado de（在...旁边），Está cerca de（在...附近），Está lejos de（离...远）。",
                "puntos": [
                    "Está a la derecha / izquierda", "Está al lado de / cerca de / lejos de",
                    "Está en / sobre / debajo de / detrás de",
                    "¿Dónde está...? = ...在哪里？（已知事物）",
                ],
                "ejemplos": [
                    {"frase": "El banco está a la derecha del supermercado.", "traduccion": "银行在超市的右边。", "analisis": ["a la derecha de = 在...右边", "supermercado = 超市"]},
                    {"frase": "El gato está debajo de la mesa.", "traduccion": "猫在桌子下面。", "analisis": ["debajo de = 在...下面", "gato = 猫"]},
                ],
                "ejercicio": {
                    "frase": "Responde: ¿Dónde está la biblioteca? (cerca del parque)",
                    "traduccion": "图书馆在哪里？（在公园附近）",
                    "solucion": "La biblioteca está cerca del parque.",
                    "analisis": ["cerca del = cerca de + el", "parque = 公园"],
                },
            },
            {
                "slug": "069-repaso-hay-estar",
                "tema": "Repaso: hay vs estar",
                "objetivo": "Diferenciar hay y estar claramente",
                "explicacion": "Hay = 有（存在，首次提及，不分单复数）。Estar = 在（具体位置，要配合主语人称）。¿Hay un banco por aquí?（附近有银行吗？= 不知道有没有）。¿Dónde está el banco?（银行在哪里？= 知道有银行）。",
                "puntos": [
                    "Hay = existencia (there is/are)", "Está = ubicación específica",
                    "Hay + artículo indeterminado", "Estar + artículo determinado",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "¿Hay o Está? 1. ____ un restaurante bueno aquí. 2. El restaurante ____ en la plaza.",
                    "traduccion": "用Hay或Está填空",
                    "solucion": "1. Hay un restaurante. 2. El restaurante está en la plaza.",
                    "analisis": ["1. Existencia (un) → Hay", "2. Ubicación (El) → Está"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 19: PREPOSICIONES
    # ═══════════════════════════════════════════
    {
        "titulo": "Preposiciones básicas",
        "slug": "19_preposiciones",
        "lecciones": [
            {
                "slug": "070-a-de-en",
                "tema": "Preposiciones: a, de, en",
                "objetivo": "Aprender las tres preposiciones más importantes",
                "explicacion": "Tres preposiciones fundamentales：A = 向/到/给（dirección：Voy a casa，persona：Le doy a María，hora：a las dos）。De = 的/从（posesión：el libro de Juan，origen：Soy de China，materia：café de Colombia）。En = 在/用（ubicación：estoy en casa，medio：en tren，idioma：en español，tiempo：en enero）。Son las preposiciones más usadas del español.",
                "puntos": [
                    "A: dirección, persona, hora",
                    "De: posesión, origen, materia",
                    "En: ubicación, medio, idioma, tiempo",
                ],
                "ejemplos": [
                    {"frase": "Voy a casa de María a las tres.", "traduccion": "我三点去María家。", "analisis": ["a = dirección", "de = posesión (casa de María)", "a las = hora"]},
                    {"frase": "Estudio español en la escuela.", "traduccion": "我在学校学习西班牙语。", "analisis": ["estudio = 学习", "en la escuela = 在学校"]},
                ],
                "ejercicio": {
                    "frase": "Completa con a/de/en: Soy ____ China. Vivo ____ México. Voy ____ la escuela ____ las ocho.",
                    "traduccion": "用a/de/en填空。",
                    "solucion": "Soy de China. Vivo en México. Voy a la escuela a las ocho.",
                    "analisis": ["de=origen", "en=ubicación", "a=dirección, hora"],
                },
            },
            {
                "slug": "071-con-por-para",
                "tema": "Preposiciones: con, por, para",
                "objetivo": "Diferenciar con, por y para",
                "explicacion": "Con = 和/用/带着（compañía：con amigos，instrumento：con el lápiz）。Por = 因为/通过/每/为了（causa：por ti，medio：por teléfono，frecuencia：por la mañana，precio：10 por 5）。Para = 为了/对于/去往（finalidad：para aprender，destinatario：para ti，dirección：salir para Madrid）。注意por和para的区别：por表示原因/通过，para表示目的/方向。",
                "puntos": [
                    "Con: compañía, instrumento", "Por: causa, medio, frecuencia, precio",
                    "Para: finalidad, destinatario, dirección",
                    "Por la mañana/tarde/noche",
                ],
                "ejemplos": [
                    {"frase": "Este regalo es para ti.", "traduccion": "这个礼物是给你的。", "analisis": ["para ti = 给你（destinatario）", "regalo = 礼物"]},
                    {"frase": "Gracias por tu ayuda.", "traduccion": "谢谢你的帮助。", "analisis": ["por = 因为（causa）", "ayuda = 帮助"]},
                ],
                "ejercicio": {
                    "frase": "¿Por o para? Gracias ____ venir. Esto es ____ ti.",
                    "traduccion": "用por或para填空：谢谢你来。这是给你的。",
                    "solucion": "Gracias por venir. Esto es para ti.",
                    "analisis": ["por = 因为（原因）", "para = 给（目的/接收者）"],
                },
            },
            {
                "slug": "072-otras-preposiciones",
                "tema": "Otras preposiciones: sobre, entre, sin, hasta, desde",
                "objetivo": "Ampliar el vocabulario de preposiciones",
                "explicacion": "Sobre = 在...上面/关于（sobre la mesa，un libro sobre historia）。Entre = 在...之间（entre tú y mí）。Sin = 没有（sin azúcar，sin ti）。Hasta = 直到（hasta mañana，de lunes a viernes）。Desde = 从/自从（desde casa，desde enero）。注意sin mí（没有我，不是sin yo）。Hasta luego（回头见）。",
                "puntos": [
                    "Sobre: encima de / acerca de", "Entre: entre dos o más",
                    "Sin: without (sin ti)", "Hasta: until (hasta luego)",
                    "Desde: from/since (desde casa)",
                ],
                "ejemplos": [
                    {"frase": "El libro está sobre la mesa.", "traduccion": "书在桌子上。", "analisis": ["sobre = 在...上面", "similar a 'encima de'"]},
                    {"frase": "Trabajo de lunes a viernes.", "traduccion": "我从星期一到星期五工作。", "analisis": ["de...a... = 从...到...", "sin 'desde' aquí"]},
                ],
                "ejercicio": {
                    "frase": "Completa: Café ____ (sin/con) azúcar. Te espero ____ (hasta/desde) las cinco.",
                    "traduccion": "不加糖的咖啡。我等你到五点。",
                    "solucion": "Café sin azúcar. Te espero hasta las cinco.",
                    "analisis": ["sin = 没有/不加", "hasta = 直到"],
                },
            },
            {
                "slug": "073-repaso-preposiciones",
                "tema": "Repaso: preposiciones",
                "objetivo": "Repasar todas las preposiciones básicas",
                "explicacion": "复习基本介词：a, de, en, con, por, para, sobre, entre, sin, hasta, desde。",
                "puntos": [
                    "a, de, en — las más usadas",
                    "con, por, para — importante diferenciar",
                    "sobre, entre, sin, hasta, desde — ampliar",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Traduce: 我从家走到学校。和朋友们一起。为了学习。",
                    "traduccion": "翻译成西班牙语",
                    "solucion": "Voy de casa a la escuela. Con amigos. Para estudiar.",
                    "analisis": ["de...a = 从...到", "con = 和一起", "para = 为了"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 20: PREGUNTAS Y CONECTORES
    # ═══════════════════════════════════════════
    {
        "titulo": "Preguntas y conectores básicos",
        "slug": "20_preguntas_conectores",
        "lecciones": [
            {
                "slug": "074-palabras-interrogativas",
                "tema": "Palabras interrogativas",
                "objetivo": "Aprender a hacer preguntas en español",
                "explicacion": "疑问词：¿Qué?（什么），¿Quién?（谁），¿Cómo?（怎么/什么样），¿Cuándo?（什么时候），¿Dónde?（哪里），¿Por qué?（为什么），¿Cuánto?（多少），¿Cuál?（哪个）。全部带重音符号。¿Qué hora es? ¿Quién es él? ¿Cómo estás? ¿Cuándo vienes? ¿Dónde vives? ¿Por qué estudias español? ¿Cuánto cuesta? ¿Cuál es tu número? 注意：¿Por qué?（为什么）vs Porque（因为）。",
                "puntos": [
                    "Qué (什么) / Quién (谁) / Cómo (怎么) / Cuándo (什么时候)",
                    "Dónde (哪里) / Por qué (为什么) / Cuánto (多少) / Cuál (哪个)",
                    "Siempre con tilde (acento)",
                    "¿Por qué? ≠ Porque (因为)",
                ],
                "ejemplos": [
                    {"frase": "¿Por qué estudias español? — Porque me gusta.", "traduccion": "你为什么学西班牙语？因为我喜欢。", "analisis": ["¿Por qué? = 为什么？", "Porque = 因为"]},
                    {"frase": "¿Cuántos años tienes? ¿Dónde vives?", "traduccion": "你几岁？你住在哪里？", "analisis": ["Cuántos = 多少（复数）", "Dónde = 哪里"]},
                ],
                "ejercicio": {
                    "frase": "Completa: ¿____ es tu nombre? ¿____ años tienes? ¿____ vives?",
                    "traduccion": "填空：你叫什么？你几岁？你住在哪里？",
                    "solucion": "¿Cuál es tu nombre? ¿Cuántos años tienes? ¿Dónde vives?",
                    "analisis": ["Cuál para nombre", "Cuántos para edad", "Dónde para lugar"],
                },
            },
            {
                "slug": "075-conectores",
                "tema": "Conectores básicos (y, o, pero, porque, también)",
                "objetivo": "Aprender a conectar frases simples",
                "explicacion": "基本连接词：y（和/以及），o（或者），pero（但是），porque（因为），también（也），tampoco（也不），además（此外），entonces（那么/于是）。注意y在i或hi前变e：español e inglés。o在o或ho前变u：siete u ocho。También用于肯定（也），tampoco用于否定（也不）。",
                "puntos": [
                    "y (和 / 以及)", "o (或者)", "pero (但是)", "porque (因为)",
                    "también (也) / tampoco (也不)",
                    "y → e / o → u (antes de misma vocal)",
                ],
                "ejemplos": [
                    {"frase": "Estudio español e inglés.", "traduccion": "我学习西班牙语和英语。", "analisis": ["e = y (ante i-)", "inglés = 英语"]},
                    {"frase": "Quiero ir pero no tengo tiempo.", "traduccion": "我想去但是我没有时间。", "analisis": ["pero = 但是", "no tengo tiempo = 没有时间"]},
                ],
                "ejercicio": {
                    "frase": "Completa: Hablo español ____ (y/e) chino. ¿Té ____ (o/u) café?",
                    "traduccion": "我说西班牙语和中文。茶还是咖啡？",
                    "solucion": "Hablo español y chino. ¿Té o café?",
                    "analisis": ["y + consonante → y", "o + consonante → o"],
                },
            },
            {
                "slug": "076-repaso-preguntas",
                "tema": "Repaso: preguntas y conectores",
                "objetivo": "Repasar cómo preguntar y conectar ideas",
                "explicacion": "复习疑问词和连接词，能够用西班牙语提问和连接句子。",
                "puntos": [
                    "Qué, Quién, Cómo, Cuándo, Dónde, Por qué",
                    "Y, o, pero, porque, también, además",
                    "¡Pregunta y responde!",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Haz 3 preguntas a un compañero.", "traduccion": "对一个同伴提3个问题",
                    "solucion": "¿Cómo te llamas? ¿De dónde eres? ¿Cuántos años tienes?",
                    "analisis": ["Cómo, De dónde, Cuántos"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 21: FRECUENCIA Y RUTINA
    # ═══════════════════════════════════════════
    {
        "titulo": "La frecuencia y la rutina diaria",
        "slug": "21_frecuencia_rutina",
        "lecciones": [
            {
                "slug": "077-adverbios-frecuencia",
                "tema": "Adverbios de frecuencia",
                "objetivo": "Expresar la frecuencia de las acciones",
                "explicacion": "频率副词：siempre总是，casi siempre几乎总是，normalmente通常，generalmente一般，a veces有时，de vez en cuando时不时，rara vez很少，nunca从不。位置：一般在动词前面（Siempre estudio）或句尾（Estudio todos los días）。nunca可以用在动词前（Nunca como carne）或no...nunca（No como carne nunca）。todos los días每天，todas las semanas每周。",
                "puntos": [
                    "100% → siempre, todos los días",
                    "75% → normalmente, generalmente",
                    "50% → a veces",
                    "25% → de vez en cuando",
                    "0% → nunca",
                ],
                "ejemplos": [
                    {"frase": "Siempre tomo café por la mañana.", "traduccion": "我早上总是喝咖啡。", "analisis": ["Siempre = 总是", "por la mañana = 早上"]},
                    {"frase": "Nunca como carne. Soy vegetariano.", "traduccion": "我从来不吃肉。我是素食者。", "analisis": ["Nunca = 从不（动词前）", "vegetariano = 素食者"]},
                ],
                "ejercicio": {
                    "frase": "Ordena de más a menos: nunca, a veces, siempre, normalmente",
                    "traduccion": "从多到少排序",
                    "solucion": "siempre, normalmente, a veces, nunca",
                    "analisis": ["siempre=100%", "normalmente=75%", "a veces=50%", "nunca=0%"],
                },
            },
            {
                "slug": "078-rutina-diaria",
                "tema": "La rutina diaria",
                "objetivo": "Describir las actividades diarias",
                "explicacion": "描述日常活动：Me levanto起床，Me ducho洗澡，Me visto穿衣服，Desayuno吃早餐，Voy al trabajo/salgo de casa去上班/出门，Trabajo/Estudio工作/学习，Como吃午餐，Vuelvo a casa回家，Ceno吃晚餐，Veo la televisión看电视，Me acuesto睡觉。用todos los días每天早上/午/晚：por la mañana，al mediodía，por la tarde，por la noche。",
                "puntos": [
                    "Me levanto / Me ducho / Me visto — 起床/洗澡/穿衣",
                    "Desayuno / Como / Ceno — 三餐",
                    "Voy al trabajo / Vuelvo a casa / Me acuesto",
                ],
                "ejemplos": [
                    {"frase": "Me levanto a las siete todos los días.", "traduccion": "我每天七点起床。", "analisis": ["Me levanto = 我起床（reflexivo）", "a las siete = 在七点"]},
                    {"frase": "Por la noche ceno y veo la televisión.", "traduccion": "晚上我吃晚饭和看电视。", "analisis": ["Por la noche = 晚上", "veo = ver (yo)"]},
                ],
                "ejercicio": {
                    "frase": "Ordena: me acuesto, como, me levanto, voy al trabajo",
                    "traduccion": "按顺序排列日常活动",
                    "solucion": "me levanto, voy al trabajo, como, me acuesto",
                    "analisis": ["顺序从早到晚"],
                },
            },
            {
                "slug": "079-verbos-reflexivos",
                "tema": "Verbos reflexivos",
                "objetivo": "Aprender los verbos reflexivos básicos",
                "explicacion": "反身动词带se。变位时加反身代词：me/te/se/nos/os/se。常见反身动词：levantarse起床，ducharse洗澡，vestirse穿衣服，acostarse睡觉，sentarse坐下，llamarse名叫，irse离开。以levantarse（起床）为例：yo me levanto，tú te levantas，él se levanta，nosotros nos levantamos，ellos se levantan。注意acostarse和vestirse是stem-changing。",
                "puntos": [
                    "Me levanto / Te levantas / Se levanta",
                    "Nos levantamos / Se levantan",
                    "Llamarse / Ducharse / Vestirse / Acostarse",
                ],
                "ejemplos": [
                    {"frase": "Me llamo Carlos. ¿Cómo te llamas?", "traduccion": "我叫Carlos。你叫什么？", "analisis": ["Me llamo = llamarse (yo)", "Te llamas = llamarse (tú)"]},
                    {"frase": "Ella se levanta temprano todos los días.", "traduccion": "她每天早起。", "analisis": ["se levanta = levantarse (ella)", "temprano = 早"]},
                ],
                "ejercicio": {
                    "frase": "Conjuga: Yo ____ (levantarse) tarde. Él ____ (ducharse) por la mañana.",
                    "traduccion": "我晚起。他早上洗澡。",
                    "solucion": "Yo me levanto tarde. Él se ducha por la mañana.",
                    "analisis": ["levantarse→me levanto", "ducharse→se ducha"],
                },
            },
            {
                "slug": "080-repaso-rutina",
                "tema": "Repaso: rutina y frecuencia",
                "objetivo": "Repasar la rutina diaria",
                "explicacion": "复习：用频率副词和反身动词描述你的日常生活。",
                "puntos": [
                    "Siempre / Normalmente / A veces / Nunca",
                    "Me levanto, me ducho, desayuno...",
                    "¡Describe tu día!",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Describe tu rutina en 3 frases.", "traduccion": "用3句话描述你的日常",
                    "solucion": "Me levanto a las siete. Normalmente desayuno café. Por la noche me acuesto a las once.",
                    "analisis": ["usa adverbios de frecuencia", "usa verbos reflexivos"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 22: COMIDA Y RESTAURANTE
    # ═══════════════════════════════════════════
    {
        "titulo": "La comida y el restaurante",
        "slug": "22_comida_restaurante",
        "lecciones": [
            {
                "slug": "081-vocabulario-comida",
                "tema": "Vocabulario de la comida",
                "objetivo": "Aprender vocabulario básico de alimentos",
                "explicacion": "食物词汇：fruta水果，verdura蔬菜，carne肉，pescado鱼，pan面包，arroz米饭，pasta意大利面，huevo鸡蛋，leche牛奶，queso奶酪，agua水，jugo果汁，café咖啡，té茶，cerveza啤酒，vino葡萄酒。三餐：desayuno早餐，comida/almuero午餐，cena晚餐。形容词：bueno好的，malo坏的，rico美味的，sabroso好吃的，dulce甜的，salado咸的，amargo苦的。",
                "puntos": [
                    "Fruta, verdura, carne, pescado, pan, arroz",
                    "Agua, jugo, café, té, leche, cerveza",
                    "Desayuno / Almuerzo / Cena",
                    "Rico, sabroso, dulce, salado, amargo, picante",
                ],
                "ejemplos": [
                    {"frase": "La paella es muy sabrosa.", "traduccion": "西班牙海鲜饭很好吃。", "analisis": ["paella = 西班牙海鲜饭", "sabrosa = 美味的"]},
                    {"frase": "¿Quieres café o té? — Café, por favor.", "traduccion": "你想要咖啡还是茶？咖啡，谢谢。", "analisis": ["¿Quieres? = 你想要？(querer)", "por favor = 请/谢谢"]},
                ],
                "ejercicio": {
                    "frase": "Clasifica: carne, leche, manzana, pescado, queso, arroz (origen animal o vegetal)",
                    "traduccion": "分类：动物源还是植物源",
                    "solucion": "Animal: carne, leche, pescado, queso. Vegetal: manzana, arroz.",
                    "analisis": ["origen animal: carne, leche...", "origen vegetal: frutas, arroz"],
                },
            },
            {
                "slug": "082-pedir-en-restaurante",
                "tema": "Pedir en un restaurante",
                "objetivo": "Aprender a pedir comida en español",
                "explicacion": "在餐厅点餐：常用表达。Camarero/ camarero（服务员）。Quisiera / Quiero + comida（我想要...）。¿Qué me recomienda?（你推荐什么？）。De primero... de segundo...（第一道...第二道...）。La cuenta, por favor（买单，谢谢）。Estaba muy bueno（很好吃）。常用回答：¿Qué desea?（您想要什么？）。¿Algo más?（还要什么？）。Nada más, gracias（就这些，谢谢）。",
                "puntos": [
                    "Quisiera / Quiero... — 我想要...",
                    "¿Qué me recomienda? — 你推荐什么？",
                    "La cuenta, por favor. — 买单。",
                    "De primero / De segundo — 第一道/第二道",
                ],
                "ejemplos": [
                    {"frase": "— ¿Qué desea? — Quisiera un café y un jugo de naranja.", "traduccion": "您想要什么？我想要一杯咖啡和一杯橙汁。", "analisis": ["Quisiera = 我想要（礼貌）", "jugo de naranja = 橙汁"]},
                    {"frase": "— ¿Algo más? — No, la cuenta, por favor.", "traduccion": "还要什么吗？不了，买单。", "analisis": ["¿Algo más? = 还要什么？", "la cuenta = 账单"]},
                ],
                "ejercicio": {
                    "frase": "Escribe: \"我想要一个三明治和一杯可乐\"", "traduccion": "翻译成西班牙语",
                    "solucion": "Quisiera un sándwich y una Coca-Cola.",
                    "analisis": ["quisiera = 想要（礼貌）", "un sándwich = 一个三明治"],
                },
            },
            {
                "slug": "083-repaso-comida",
                "tema": "Repaso: comida y restaurante",
                "objetivo": "Repasar el vocabulario de comida",
                "explicacion": "复习食物词汇和在餐厅点餐的表达。",
                "puntos": [
                    "Comidas: fruta, carne, pescado, pan, arroz...",
                    "Bebidas: agua, café, té, jugo, cerveza...",
                    "En el restaurante: Quisiera...",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Diálogo: Tú eres el cliente. Pide algo.", "traduccion": "对话：你是顾客。点餐。",
                    "solucion": "— Buenas tardes, ¿qué desea? — Quisiera una paella y un vaso de vino, por favor.",
                    "analisis": ["Quisiera + comida", "por favor"],
                },
                "es_repaso": True,
            },
        ],
    },
]
