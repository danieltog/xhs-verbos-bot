"""
Extensiones del currículo A1 — Módulos 04 a 07
"""

EXTRA_MODULOS = [

    # ═══════════════════════════════════════════
    # MÓDULO 4: DÍAS Y MESES
    # ═══════════════════════════════════════════
    {
        "titulo": "Días, meses y fechas",
        "slug": "04_dias_meses",
        "lecciones": [
            {
                "slug": "016-dias-semana",
                "tema": "Los días de la semana",
                "objetivo": "Aprender los 7 días de la semana en español",
                "explicacion": "西班牙语中一周有7天。lunes星期一，martes星期二，miércoles星期三，jueves星期四，viernes星期五，sábado星期六，domingo星期天。注意西班牙语的星期都是阳性名词，用artículo el：el lunes，el martes。复数形式：los lunes（不变）。",
                "puntos": [
                    "lunes — 星期一",
                    "martes — 星期二",
                    "miércoles — 星期三",
                    "jueves — 星期四",
                    "viernes — 星期五",
                    "sábado — 星期六",
                    "domingo — 星期天",
                    "Hoy es... — 今天是...",
                ],
                "ejemplos": [
                    {"frase": "Hoy es lunes. Mañana es martes.", "traduccion": "今天是星期一。明天是星期二。", "analisis": ["Hoy = 今天", "Mañana = 明天"]},
                    {"frase": "Los sábados no trabajo.", "traduccion": "星期六我不工作。", "analisis": ["Los sábados = 每个星期六（复数）", "no trabajo = 我不工作"]},
                ],
                "ejercicio": {
                    "frase": "¿Qué día es hoy? a) lunes b) enero c) 2026",
                    "traduccion": "今天是什么日子？（选出正确的答案）",
                    "solucion": "lunes",
                    "analisis": ["lunes = 星期几", "enero = 月份", "2026 = 年份"],
                },
            },
            {
                "slug": "017-meses-ano",
                "tema": "Los meses del año",
                "objetivo": "Aprender los 12 meses en español",
                "explicacion": "西班牙语12个月：enero一月，febrero二月，marzo三月，abril四月，mayo五月，junio六月，julio七月，agosto八月，septiembre九月，octubre十月，noviembre十一月，diciembre十二月。月份也是阳性名词，用en + mes：en enero，en diciembre。月份不大写。",
                "puntos": [
                    "enero / febrero / marzo / abril", "mayo / junio / julio / agosto",
                    "septiembre / octubre / noviembre / diciembre",
                    "¿En qué mes estamos? — 现在是几月？",
                    "Estamos en... — 现在是...月",
                ],
                "ejemplos": [
                    {"frase": "Estamos en marzo. La primavera empieza.", "traduccion": "现在是三月。春天开始了。", "analisis": ["Estamos en = 我们在...（月份）", "primavera = 春天"]},
                    {"frase": "Mi cumpleaños es en diciembre.", "traduccion": "我的生日在十二月。", "analisis": ["Mi cumpleaños = 我的生日", "en + mes = 在某月"]},
                ],
                "ejercicio": {
                    "frase": "Ordena: marzo, enero, mayo, noviembre", "traduccion": "按顺序排列这些月份",
                    "solucion": "enero, marzo, mayo, noviembre",
                    "analisis": ["enero=1, marzo=3, mayo=5, noviembre=11"],
                },
            },
            {
                "slug": "018-las-fechas",
                "tema": "Las fechas",
                "objetivo": "Aprender a decir la fecha completa",
                "explicacion": "西班牙语说日期：先日再月再年。用Hoy es + 数字 + de + 月份 + de + 年份。注意日期用基数词（uno, dos...），只有每月第一天用 primero。ej: Hoy es primero de enero de 2026。Hoy es dos de marzo。问日期：¿Qué fecha es hoy?",
                "puntos": [
                    "Hoy es [día] de [mes] — 今天是...月...日",
                    "Primero de [mes] — 每月第一天用 primero",
                    "¿Qué fecha es hoy? — 今天几号？",
                    "¿Cuándo es...? — ...是什么时候？",
                ],
                "ejemplos": [
                    {"frase": "Hoy es 15 de septiembre.", "traduccion": "今天是9月15日。", "analisis": ["15 = quince", "de = 的（连接日和月）"]},
                    {"frase": "— ¿Cuándo es tu cumpleaños? — El 8 de mayo.", "traduccion": "你的生日是什么时候？5月8日。", "analisis": ["¿Cuándo? = 什么时候？", "El + fecha = 在...日"]},
                ],
                "ejercicio": {
                    "frase": "¿Cómo se dice \"2026年3月5日\"?",
                    "traduccion": "用西班牙语说「2026年3月5日」",
                    "solucion": "5 de marzo de 2026",
                    "analisis": ["先日后月再年", "5 = cinco (不是quinto)"],
                },
            },
            {
                "slug": "019-las-estaciones",
                "tema": "Las estaciones del año",
                "objetivo": "Aprender las 4 estaciones y el clima básico",
                "explicacion": "四季：primavera春天，verano夏天，otoño秋天，invierno冬天。用en + estación说在某个季节。描述天气用 hacer：hace frío冷，hace calor热，hace buen tiempo天气好，hace mal tiempo天气差。用 llueve下雨，nieva下雪。",
                "puntos": [
                    "primavera — 春天", "verano — 夏天", "otoño — 秋天", "invierno — 冬天",
                    "Hace frío / calor — 天气冷/热",
                    "Llueve / Nieva — 下雨/下雪",
                ],
                "ejemplos": [
                    {"frase": "En verano hace mucho calor.", "traduccion": "夏天很热。", "analisis": ["En verano = 在夏天", "mucho calor = 很热"]},
                    {"frase": "En invierno nieva en las montañas.", "traduccion": "冬天山上会下雪。", "analisis": ["nieva = 下雪 (nevar)", "montañas = 山"]},
                ],
                "ejercicio": {
                    "frase": "¿Qué estación es? Hace frío y nieva.",
                    "traduccion": "这是什么季节？天气冷而且下雪。",
                    "solucion": "Invierno（冬天）",
                    "analisis": ["hace frío = 冷", "nieva = 下雪 → 冬天"],
                },
            },
            {
                "slug": "020-repaso-tiempo",
                "tema": "Repaso: días, meses y estaciones",
                "objetivo": "Repasar el calendario completo",
                "explicacion": "今天我们复习：一周7天，一年12个月，4个季节，以及如何说日期和天气。",
                "puntos": [
                    "Días: lunes a domingo",
                    "Meses: enero a diciembre",
                    "Estaciones: primavera, verano, otoño, invierno",
                    "Fechas: Hoy es [día] de [mes]",
                    "Clima: hace frío/calor, llueve, nieva",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Completa: Hoy es 25 de ______ (diciembre/diciembre) y hace ______ (frío/calor).",
                    "traduccion": "填空：今天是12月25日，天气很冷。",
                    "solucion": "diciembre / frío",
                    "analisis": ["diciembre = 十二月 (Navidad)", "hace frío = 冬天冷"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 5: LA HORA
    # ═══════════════════════════════════════════
    {
        "titulo": "La hora",
        "slug": "05_hora",
        "lecciones": [
            {
                "slug": "021-hora-en-punto",
                "tema": "La hora en punto",
                "objetivo": "Aprender a decir la hora exacta",
                "explicacion": "西班牙语说时间用动词 ser。Es la una para 1点。Son las + 数字 para 2点以上。问时间：¿Qué hora es? 回答：Es la una（1点），Son las dos（2点），Son las tres（3点），等等。注意12点用 Son las doce。",
                "puntos": [
                    "¿Qué hora es? — 几点了？",
                    "Es la una. — 1点。",
                    "Son las dos / tres / cuatro... — 2/3/4...点",
                    "Son las doce. — 12点。",
                    "De la mañana — 早上 / De la tarde — 下午 / De la noche — 晚上",
                ],
                "ejemplos": [
                    {"frase": "— ¿Qué hora es? — Es la una de la tarde.", "traduccion": "几点了？下午1点。", "analisis": ["Es la una = 1点（单数）", "de la tarde = 下午"]},
                    {"frase": "Son las ocho de la mañana.", "traduccion": "早上8点。", "analisis": ["Son las ocho = 8点（复数）", "de la mañana = 早上"]},
                ],
                "ejercicio": {
                    "frase": "¿Qué hora es? Son las ____ (diez/diez).", "traduccion": "几点了？10点。",
                    "solucion": "Son las diez.",
                    "analisis": ["Son las = 用于2点以上", "diez = 10"],
                },
            },
            {
                "slug": "022-hora-y-media",
                "tema": "La hora y media / y cuarto",
                "objetivo": "Aprender a decir la hora con minutos",
                "explicacion": "说半点用 y media：Son las dos y media（2点半）。说一刻钟用 y cuarto：Son las tres y cuarto（3点一刻）。说差几分用 menos cuarto：Son las cuatro menos cuarto（差一刻4点/3点45）。口语中也说 Son las cuatro cuarenta y cinco（4点45分）。",
                "puntos": [
                    "Y media — 半 (ej: 2:30 → las dos y media)",
                    "Y cuarto — 一刻 (ej: 3:15 → las tres y cuarto)",
                    "Menos cuarto — 差一刻 (ej: 4:45 → las cinco menos cuarto)",
                    "Y [minutos] — ...分 (ej: 3:10 → las tres y diez)",
                    "Menos [minutos] — 差...分 (ej: 4:50 → las cinco menos diez)",
                ],
                "ejemplos": [
                    {"frase": "Son las seis y media. Es hora de cenar.", "traduccion": "6点半了。该吃晚饭了。", "analisis": ["y media = 半", "hora de cenar = 晚饭时间"]},
                    {"frase": "La clase empieza a las nueve menos cuarto.", "traduccion": "课在8点45开始。", "analisis": ["a las = 在...点", "nueve menos cuarto = 差一刻9点"]},
                ],
                "ejercicio": {
                    "frase": "¿Qué hora es? 2:30 → Son las ____ y ____.",
                    "traduccion": "2:30怎么说？",
                    "solucion": "Son las dos y media.",
                    "analisis": ["dos y media = 2点半"],
                },
            },
            {
                "slug": "023-hora-exacta",
                "tema": "La hora exacta con minutos",
                "objetivo": "Decir la hora con cualquier minuto",
                "explicacion": "说具体时间：Son las [hora] y [minutos] 或者 Son las [hora] menos [minutos]。从1分到30分用y，从31分到59分用menos。也可以用24小时制。注意：media hora = 半小时，cuarto de hora = 一刻钟。",
                "puntos": [
                    "Son las [hora] y [minutos] — ...点...分 (1-30分)",
                    "Son las [hora] menos [minutos] — 差...分到...点 (31-59分)",
                    "Tren / avión / clase a las... — 火车/飞机/课在...点",
                    "¿A qué hora? — 在几点？",
                ],
                "ejemplos": [
                    {"frase": "El tren sale a las siete y veinticinco.", "traduccion": "火车7点25分发车。", "analisis": ["sale = 出发 (salir)", "a las = 在...点"]},
                    {"frase": "Son las ocho menos cinco. ¡Tengo prisa!", "traduccion": "差5分8点。我赶时间！", "analisis": ["menos cinco = 差5分", "tengo prisa = 我赶时间"]},
                ],
                "ejercicio": {
                    "frase": "¿A qué hora es la clase? a las 3:20 → a las tres y ____.",
                    "traduccion": "课在3点20 → 用西班牙语说",
                    "solucion": "a las tres y veinte",
                    "analisis": ["3:20 = tres y veinte"],
                },
            },
            {
                "slug": "024-repaso-hora",
                "tema": "Repaso: la hora",
                "objetivo": "Repasar cómo decir la hora",
                "explicacion": "复习说时间：¿Qué hora es? Es la una / Son las ...。y media半点，y cuarto一刻，menos cuarto差一刻。记住a la / a las表示在几点。",
                "puntos": [
                    "Es la una / Son las...",
                    "y media / y cuarto / menos cuarto",
                    "¿A qué hora? — 在几点？",
                    "De la mañana/tarde/noche",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Escribe: 1:15pm, 6:30am, 11:45pm", "traduccion": "写出：下午1:15，早上6:30，晚上11:45",
                    "solucion": "la una y cuarto de la tarde / las seis y media de la mañana / las doce menos cuarto de la noche",
                    "analisis": ["1:15 = y cuarto", "6:30 = y media", "11:45 = menos cuarto"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 6: ARTÍCULOS
    # ═══════════════════════════════════════════
    {
        "titulo": "Los artículos",
        "slug": "06_articulos",
        "lecciones": [
            {
                "slug": "025-articulo-determinado",
                "tema": "El artículo determinado (el, la, los, las)",
                "objetivo": "Aprender los artículos definidos",
                "explicacion": "西班牙语定冠词：el阳性单数，la阴性单数，los阳性复数，las阴性复数。相当于英语的the。el libro书，la mesa桌子，los libros书们，las mesas桌子们。用在已知的、特定的事物上。也用在抽象概念和星期前面：el lunes，la primavera。",
                "puntos": [
                    "el — 阳性单数 (el libro)", "la — 阴性单数 (la mesa)",
                    "los — 阳性复数 (los libros)", "las — 阴性复数 (las mesas)",
                    "用el/los指代整体类别：Los perros son animales.",
                ],
                "ejemplos": [
                    {"frase": "El libro está en la mesa.", "traduccion": "书在桌子上。", "analisis": ["El libro = 那本书（特定）", "la mesa = 那张桌子"]},
                    {"frase": "Los estudiantes están en la clase.", "traduccion": "学生们在教室里。", "analisis": ["Los estudiantes = 那（些）学生", "la clase = 教室"]},
                ],
                "ejercicio": {
                    "frase": "Completa: ____ casa es grande. (el/la)", "traduccion": "填空：房子很大。",
                    "solucion": "La casa es grande.",
                    "analisis": ["casa = 阴性 → la"],
                },
            },
            {
                "slug": "026-articulo-indeterminado",
                "tema": "El artículo indeterminado (un, una, unos, unas)",
                "objetivo": "Aprender los artículos indefinidos",
                "explicacion": "西班牙语不定冠词：un阳性单数（一个），una阴性单数，unos阳性复数（一些），unas阴性复数。相当于英语a/an/some。un libro一本书，una mesa一张桌子，unos libros一些书，unas mesas一些桌子。用于第一次提到的事物或非特定的事物。注意：hay后面常用不定冠词：Hay un libro en la mesa。",
                "puntos": [
                    "un — 一个 (阳性: un perro)", "una — 一个 (阴性: una casa)",
                    "unos — 一些 (阳性: unos libros)", "unas — 一些 (阴性: unas mesas)",
                    "Hay + un/una... — 有（一个）...",
                ],
                "ejemplos": [
                    {"frase": "Tengo un libro muy interesante.", "traduccion": "我有一本很有趣的书。", "analisis": ["un libro = 一本书（非特定）", "muy interesante = 很有趣"]},
                    {"frase": "En la mesa hay unas manzanas.", "traduccion": "桌子上有一些苹果。", "analisis": ["Hay = 有", "unas manzanas = 一些苹果"]},
                ],
                "ejercicio": {
                    "frase": "Completa: Necesito ____ lápiz. (un/una)",
                    "traduccion": "填空：我需要一支铅笔。",
                    "solucion": "Necesito un lápiz.",
                    "analisis": ["lápiz = 阳性 → un"],
                },
            },
            {
                "slug": "027-contracciones-al-del",
                "tema": "Contracciones: al y del",
                "objetivo": "Aprender las contracciones obligatorias",
                "explicacion": "西班牙语有两个必须的缩合：a + el = al，de + el = del。Voy al colegio（我去学校，不是voy a el colegio）。El libro del profesor（老师的书，不是de el profesor）。注意：只有el会缩合，la/los/las不缩合。a la / de la / a los / de los 都不变。",
                "puntos": [
                    "a + el = al", "de + el = del",
                    "Ej: Voy al cine. (不是 a el cine)",
                    "Ej: La casa del profesor. (不是 de el profesor)",
                    "No se contrae con la/los/las",
                ],
                "ejemplos": [
                    {"frase": "Vamos al parque los domingos.", "traduccion": "我们星期天去公园。", "analisis": ["al = a + el", "los domingos = 每个星期天"]},
                    {"frase": "El libro del estudiante está aquí.", "traduccion": "学生的书在这里。", "analisis": ["del = de + el", "estudiante = 学生"]},
                ],
                "ejercicio": {
                    "frase": "Corrige: Voy a el supermercado.",
                    "traduccion": "改正：Voy a el supermercado.",
                    "solucion": "Voy al supermercado.",
                    "analisis": ["a + el supermercado → al supermercado"],
                },
            },
            {
                "slug": "028-repaso-articulos",
                "tema": "Repaso: artículos",
                "objetivo": "Repasar los artículos determinados e indeterminados",
                "explicacion": "复习冠词：定冠词el/la/los/las，不定冠词un/una/unos/unas。记住缩合al和del。选择冠词时要注意名词的阴阳性和单复数。",
                "puntos": [
                    "el / la / los / las — the", "un / una / unos / unas — a/an/some",
                    "al = a + el", "del = de + el",
                    "¡Practica! ¡Es muy importante!",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Completa: ____ perro ____ amigo. (el, del, al, un)",
                    "traduccion": "填空：朋友的狗 / 一条狗",
                    "solucion": "El perro del amigo. / Un perro.",
                    "analisis": ["El perro (定冠词)", "del amigo (de + el)", "Un perro (不定冠词)"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 7: GÉNERO
    # ═══════════════════════════════════════════
    {
        "titulo": "Género: masculino y femenino",
        "slug": "07_genero",
        "lecciones": [
            {
                "slug": "029-masculino-femenino",
                "tema": "Reglas generales del género",
                "objetivo": "Distinguir el género de los sustantivos",
                "explicacion": "西班牙语名词有阴阳性。一般规则：以-o结尾通常是阳性（el libro，el perro），以-a结尾通常是阴性（la casa，la mesa）。但有很多例外！以-dad/ción/sión/tad结尾的单词是阴性（la ciudad，la canción）。以-or结尾通常是阳性（el amor，el color，但la flor例外）。人/animals的性别随自然性别（el hombre，la mujer）。",
                "puntos": [
                    "-o → 阳性 (el libro, el carro)",
                    "-a → 阴性 (la casa, la mesa)",
                    "-dad, -ción, -sión, -tad → 阴性 (la ciudad, la canción)",
                    "-or → 阳性 (el amor, el color)",
                    "自然性别决定：el hombre / la mujer",
                ],
                "ejemplos": [
                    {"frase": "El libro rojo está en la mesa blanca.", "traduccion": "红皮书在白色桌子上。", "analisis": ["libro (masc) → el, rojo", "mesa (fem) → la, blanca"]},
                    {"frase": "La canción es muy bonita.", "traduccion": "这首歌很动听。", "analisis": ["canción (-ción) → 阴性 la", "bonita (fem) = 动听的"]},
                ],
                "ejercicio": {
                    "frase": "¿Masculino o femenino? ciudad, libro, canción, perro, flor",
                    "traduccion": "判断阴阳性：城市、书、歌曲、狗、花",
                    "solucion": "ciudad(F), libro(M), canción(F), perro(M), flor(F)",
                    "analisis": ["ciudad: -dad → fem", "flor: excepción → fem"],
                },
            },
            {
                "slug": "030-excepciones-genero",
                "tema": "Excepciones importantes",
                "objetivo": "Conocer las excepciones más comunes",
                "explicacion": "重要的例外：以-a结尾的阳性词：el día（天），el mapa（地图），el problema（问题），el tema（主题），el sistema（系统），el programa（节目/程序），el idioma（语言）。以-o结尾的阴性词：la mano（手），la radio（收音机）。有些词改变冠词改变意思：el capital（资金）vs la capital（首都），el frente（前线）vs la frente（额头）。",
                "puntos": [
                    "el día / el mapa / el problema / el tema — 以-a结尾但是阳性",
                    "la mano / la radio — 以-o结尾但是阴性",
                    "el capital (资金) ≠ la capital (首都)",
                    "Aprende el género con el artículo (带着冠词一起记)",
                ],
                "ejemplos": [
                    {"frase": "El problema es muy difícil.", "traduccion": "这个问题很难。", "analisis": ["problema (-ma结尾) = 阳性", "difícil = 难的"]},
                    {"frase": "Me duele la mano derecha.", "traduccion": "我的右手疼。", "analisis": ["la mano = 手（阴性）", "derecha = 右边的"]},
                ],
                "ejercicio": {
                    "frase": "¿el o la? ___ mapa, ___ mano, ___ día, ___ radio",
                    "traduccion": "用el或la填空",
                    "solucion": "el mapa, la mano, el día, la radio",
                    "analisis": ["mapa (masc excepción)", "mano (fem excepción)"],
                },
            },
            {
                "slug": "031-genero-personas",
                "tema": "Género en personas y profesiones",
                "objetivo": "Cambiar el género en personas y trabajos",
                "explicacion": "人和职业的阴阳性变化：-o变-a：amigo→amiga，maestro→maestra。辅音结尾加-a：profesor→profesora，señor→señora。以-ista结尾不变：el/la turista，el/la artista。有些职业两种性别都能做：el médico / la médica。注意有些词固定阴性：la persona（人），la víctima（受害者）。",
                "puntos": [
                    "amigo → amiga", "profesor → profesora",
                    "-ista: el/la turista, el/la artista",
                    "医生：el médico / la médica",
                    "固定阴性：la persona, la víctima",
                ],
                "ejemplos": [
                    {"frase": "Ella es profesora de español.", "traduccion": "她是西班牙语老师。", "analisis": ["profesora = profesora (fem)", "de español = 西班牙语的"]},
                    {"frase": "Mi amigo Luis es muy simpático.", "traduccion": "我的朋友Luis很友善。", "analisis": ["amigo (masc)", "simpático = 友善的"]},
                ],
                "ejercicio": {
                    "frase": "Femenino de: profesor, amigo, estudiante, médico",
                    "traduccion": "写出阴性形式：profesor, amigo, estudiante, médico",
                    "solucion": "profesora, amiga, estudiante (igual), médica",
                    "analisis": ["profesor→profesora +a", "estudiante no cambia"],
                },
                "es_repaso": True,
            },
        ],
    },
]
