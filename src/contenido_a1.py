#!/usr/bin/env python3
"""
Contenido A1 — Datos estructurados del currículo DELE A1.
El content_factory.py lee esto para generar los scripts YAML.
Edita este archivo para modificar el contenido de las lecciones.
"""

A1_CURRICULO = {
    "nivel": "A1",
    "modulos": [

        # ═══════════════════════════════════════════
        # MÓDULO 1: SALUDOS
        # ═══════════════════════════════════════════
        {
            "titulo": "Saludos y presentaciones",
            "slug": "01_saludos",
            "lecciones": [

                {
                    "slug": "001-saludos-formales",
                    "tema": "Saludos formales e informales",
                    "tema_zh": "正式和非正式问候",
                    "objetivo": "Aprender a saludar en diferentes contextos",
                    "explicacion": "先来看正式问候。对不熟悉的人，我们用 Buenos días 早上好（到中午12点），Buenas tardes 下午好（到晚上8点），Buenas noches 晚上好。日常和朋友打招呼用 Hola 你好，Qué tal 怎么样，Cómo estás 你好吗。回答可以说 Bien gracias 好的谢谢，Muy bien 非常好，Más o menos 一般般。告别用 Adiós 再见，Hasta luego 回头见，Hasta mañana 明天见。",
                    "puntos": [
                        "Buenos días — 早上好（到中午12点）",
                        "Buenas tardes — 下午好（到晚上8点）",
                        "Buenas noches — 晚上好 / 晚安",
                        "Hola — 你好（任何时候）",
                        "¿Qué tal? — 怎么样？",
                    ],
                    "ejemplos": [
                        {
                            "frase": "— ¡Buenos días! ¿Cómo está usted?",
                            "traduccion": "早上好！您好吗？（正式）",
                            "analisis": ["Buenos días = 早上好", "usted = 您（正式）"],
                        },
                        {
                            "frase": "— ¡Hola! ¿Qué tal? — Muy bien, ¿y tú?",
                            "traduccion": "你好！怎么样？非常好，你呢？",
                            "analisis": ["¿y tú? = 你呢？（非正式）", "¿y usted? = 您呢？（正式）"],
                        },
                        {
                            "frase": "Adiós, ¡hasta mañana!",
                            "traduccion": "再见，明天见！",
                            "analisis": ["Hasta mañana = 明天见", "Hasta luego = 回头见"],
                        },
                    ],
                    "ejercicio": {
                        "frase": 'Completa: Buenos ____, Buenas ____, Buenas ____',
                        "traduccion": "填空：早上好，下午好，晚上好",
                        "solucion": "Buenos días, Buenas tardes, Buenas noches",
                        "analisis": ["días = 天/日子", "tardes = 下午", "noches = 晚上"],
                    },
                    "refran": "«Hola y adiós son las primeras palabras que abren puertas.»",
                },

                {
                    "slug": "002-presentaciones",
                    "tema": "Presentarse y preguntar el nombre",
                    "tema_zh": "自我介绍和询问名字",
                    "objetivo": "Aprender a decir quién eres y preguntar el nombre",
                    "explicacion": "自我介绍有三种方式。Me llamo 加名字最常用。Soy 加名字更简洁。Mi nombre es 加名字更正式。问对方名字说 ¿Cómo te llamas?（非正式）或 ¿Cómo se llama?（正式）。认识新朋友时说 Mucho gusto 很高兴认识你。男生说 Encantado，女生说 Encantada。",
                    "puntos": [
                        "Me llamo [nombre] — 我叫...",
                        "Soy [nombre] — 我是...",
                        "¿Cómo te llamas? — 你叫什么？",
                        "Mucho gusto — 很高兴认识你",
                        "Encantado / Encantada — 幸会",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Hola, me llamo María.",
                            "traduccion": "你好，我叫María。",
                            "analisis": ["Me llamo = 我叫 (动词llamarse)", "注意 ll 发音像中文的 y"],
                        },
                        {
                            "frase": "— ¿Cómo te llamas? — Me llamo Pablo, ¿y tú?",
                            "traduccion": "你叫什么？我叫Pablo，你呢？",
                            "analisis": ["¿Y tú? = 你呢？", "这是非正式对话"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Completa: — Hola, ¿cómo ____ llamas? — Me ____ Pedro.",
                        "traduccion": "填空：你好，你叫什么？我叫Pedro。",
                        "solucion": "¿Cómo te llamas? Me llamo Pedro.",
                        "analisis": ["te llamas = 你叫", "me llamo = 我叫"],
                    },
                },

                {
                    "slug": "003-preguntar-nacionalidad",
                    "tema": "Preguntar y decir la nacionalidad",
                    "tema_zh": "询问和表达国籍",
                    "objetivo": "Aprender a hablar del origen y la nacionalidad",
                    "explicacion": "问国籍最常用 ¿De dónde eres? 你从哪里来。回答用 Soy de + 国家，如 Soy de China。或者说 Soy + 国籍形容词，如 Soy chino。注意国籍形容词有阴阳性变化：chino/china，mexicano/mexicana，español/española。",
                    "puntos": [
                        "¿De dónde eres? — 你从哪里来？",
                        "Soy de [país] — 我来自...",
                        "Soy [nacionalidad] — 我是...国人",
                        "Masculino vs Femenino",
                    ],
                    "ejemplos": [
                        {
                            "frase": "— Hola, ¿de dónde eres? — Soy de China.",
                            "traduccion": "你好，你从哪里来？我来自中国。",
                            "analisis": ["¿De dónde eres? = 你从哪里来？", "Soy de + país = 我来自..."],
                        },
                        {
                            "frase": "Ella es china y él es japonés.",
                            "traduccion": "她是中国人，他是日本人。",
                            "analisis": ["china (fem) / japonés (masc)", "注意重音变化"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Completa: Él es ____ (mexicano/mexicana). Ella es ____ (japonés/japonesa).",
                        "traduccion": "填空：他是墨西哥人。她是日本人。",
                        "solucion": "Él es mexicano. Ella es japonesa.",
                        "analisis": ["mexicano (masc) ✅", "japonesa (fem) ✅"],
                    },
                },

                {
                    "slug": "004-numero-telefono",
                    "tema": "Números de teléfono y contacto",
                    "tema_zh": "电话号码和联系方式",
                    "objetivo": "Aprender los números 0-10 y dar información de contacto",
                    "explicacion": "西班牙语数字0到10：cero 0，uno 1，dos 2，tres 3，cuatro 4，cinco 5，seis 6，siete 7，ocho 8，nueve 9，diez 10。电话号码一位一位读。问号码说 ¿Cuál es tu número? 回答 Mi número es el... 还可以说 Mi correo es 我的邮箱是，Mi WhatsApp es。",
                    "puntos": [
                        "0 cero / 1 uno / 2 dos / 3 tres / 4 cuatro",
                        "5 cinco / 6 seis / 7 siete / 8 ocho / 9 nueve / 10 diez",
                        "¿Cuál es tu número? — 你的号码是多少？",
                        "Mi número es el... — 我的号码是...",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Mi número es el seis, cinco, dos, tres, ocho, nueve, uno, cero.",
                            "traduccion": "我的号码是6-5-2-3-8-9-1-0。",
                            "analisis": ["电话号码一位一位读", "Mi número es el... = 我的号码是..."],
                        },
                        {
                            "frase": "— ¿Cuál es tu número de teléfono? — Es el cuatro, uno, cinco, siete, dos, cero, nueve.",
                            "traduccion": "你的电话号码是多少？是4-1-5-7-2-0-9。",
                            "analisis": ["número de teléfono = 电话号码", "Es el... = 它是..."],
                        },
                    ],
                    "ejercicio": {
                        "frase": 'Escribe en español: "Mi número es el 9-3-7-1-0-4-6"',
                        "traduccion": "用西班牙语写出：我的号码是9-3-7-1-0-4-6",
                        "solucion": "Mi número es el nueve, tres, siete, uno, cero, cuatro, seis.",
                        "analisis": ["nueve=9, tres=3, siete=7, uno=1, cero=0, cuatro=4, seis=6"],
                    },
                },

                {
                    "slug": "005-repaso-saludos",
                    "tema": "Repaso: saludos y presentaciones",
                    "tema_zh": "复习：问候和介绍",
                    "objetivo": "Repasar y consolidar el primer módulo",
                    "explicacion": "今天我们复习前四课的内容。你学会了：正式和非正式问候，自我介绍和询问名字，询问国籍和来源地，以及电话号码。让我们做几个练习来巩固。",
                    "puntos": [
                        "Buenos días / Buenas tardes / Buenas noches",
                        "Hola / ¿Qué tal? / ¿Cómo estás?",
                        "Me llamo / Soy / Mucho gusto",
                        "¿De dónde eres? / Soy de...",
                    ],
                    "ejemplos": [],
                    "ejercicio": {
                        "frase": "¿Qué dices a las 8 de la mañana? a) Buenas tardes b) Buenos días c) Buenas noches",
                        "traduccion": "早上8点你该说什么？",
                        "solucion": "Buenos días",
                        "analisis": ["Buenos días = 早上（6am-12pm）", "Buenas tardes = 下午", "Buenas noches = 晚上"],
                    },
                    "es_repaso": True,
                },
            ],
        },

        # ═══════════════════════════════════════════
        # MÓDULO 2: ALFABETO
        # ═══════════════════════════════════════════
        {
            "titulo": "El alfabeto y la pronunciación",
            "slug": "02_alfabeto",
            "lecciones": [

                {
                    "slug": "006-alfabeto-pronunciacion",
                    "tema": "El alfabeto español",
                    "objetivo": "Conocer las 27 letras del alfabeto español",
                    "explicacion": "西班牙语字母表有27个字母，比英语多一个 Ñ。大部分字母发音和英语相似，但有几个不同要注意：C在a/o/u前发k音，在e/i前发s音。G在e/i前发j音。H永远不发音。LL发y音。Ñ发ny音。",
                    "puntos": [
                        "27 letras: A B C D E F G H I J K L M N Ñ O P Q R S T U V W X Y Z",
                        "H — 不发音（如：hola, hablar）",
                        "LL — 发y音（如：llamar, pollo）",
                        "Ñ — 发ny音（如：español, año）",
                        "C — 在e/i前发s音",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Hola, me llamo Carlos. ¿Y tú?",
                            "traduccion": "你好，我叫Carlos。你呢？",
                            "analisis": ["H不发音: o-la", "LL发y: me-ya-mo"],
                        },
                        {
                            "frase": "El español es fácil.",
                            "traduccion": "西班牙语很简单。",
                            "analisis": ["Ñ发ny: es-pa-nyol", "注意ñ在键盘上是单独的键"],
                        },
                    ],
                    "ejercicio": {
                        "frase": '¿Cómo se pronuncia "llamar"? a) lla-mar b) ya-mar c) la-mar',
                        "traduccion": "llamar怎么发音？",
                        "solucion": "ya-mar (LL = y)",
                        "analisis": ["LL发y音 ✅", "lla-mar ❌ (英语式发音)"],
                    },
                },

                {
                    "slug": "007-vocales",
                    "tema": "Las cinco vocales",
                    "objetivo": "Dominar la pronunciación de las vocales",
                    "explicacion": "西班牙语只有5个元音，比英语少很多。每个元音只有一个发音，非常规则。A发「啊」，E发「诶」，I发「一」，O发「哦」，U发「乌」。没有英语中的长元音和短元音区别。这是中国人学西班牙语最容易的部分！",
                    "puntos": [
                        "A = [a] 如：casa, amigo",
                        "E = [e] 如：tres, café",
                        "I = [i] 如：sí, cinco",
                        "O = [o] 如：hola, dos",
                        "U = [u] 如：tú, mucho",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Amigo, ¿café o té?",
                            "traduccion": "朋友，咖啡还是茶？",
                            "analisis": ["A = 啊: a-mi-go", "E = 诶: ca-fé", "O = 哦: ca-fé"],
                        },
                        {
                            "frase": "Sí, mucho gusto.",
                            "traduccion": "是的，很高兴认识你。",
                            "analisis": ["I = 一: sí", "U = 乌: mu-cho"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Pronuncia: MÉXICO",
                        "traduccion": "读出：MÉXICO",
                        "solucion": "Mé-xi-co (E=诶, I=一, O=哦)",
                        "analisis": ["E = 诶", "I = 一", "O = 哦"],
                    },
                },

                {
                    "slug": "008-consonantes-especiales",
                    "tema": "Consonantes especiales (C, G, J, R)",
                    "objetivo": "Aprender las consonantes más difíciles",
                    "explicacion": "几组需要特别注意的辅音。C在a/o/u前发k音（casa），在e/i前发s音（cine）。G在a/o/u前发g音（gato），在e/i前发j音（gente）。J永远发h音（jamón）。R在词首发rr音。RR双颤音是西班牙语的特色，要练习。",
                    "puntos": [
                        "C + a/o/u = [k] casa, comida",
                        "C + e/i = [s] cena, cine",
                        "G + e/i = [j] gente",
                        "J = [h] jamón, José",
                        "R vs RR = pero（但是）vs perro（狗）",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Casa, cena, cine — tres palabras con C",
                            "traduccion": "家、晚餐、电影院 — 三个带C的词",
                            "analisis": ["Casa = k音", "Cena = s音", "Cine = s音"],
                        },
                        {
                            "frase": "El perro de José come jamón.",
                            "traduccion": "José的狗在吃火腿。",
                            "analisis": ["perro = rr颤音", "José = J发h音"],
                        },
                    ],
                    "ejercicio": {
                        "frase": '¿Cómo se dice "pero"? ¿Y "perro"?',
                        "traduccion": '"pero"怎么说？"perro"呢？有什么区别？',
                        "solucion": "pero (pero) = 但是 | perro (perrro) = 狗",
                        "analisis": ["pero = 一个r，轻音", "perro = 两个r，颤音"],
                    },
                },

                {
                    "slug": "009-acentos-tilde",
                    "tema": "Acentos y la tilde",
                    "objetivo": "Entender las reglas básicas de acentuación",
                    "explicacion": "西班牙语单词有重音。有时需要写重音符号（tilde）来指示重音位置。基本规则：以n/s/元音结尾的词重音在倒数第二个音节（casa, hablan）。以其他辅音结尾的词重音在最后一个音节（comer, ciudad）。例外才写重音符号。",
                    "puntos": [
                        "以n/s/元音结尾 → 重音在倒数第二个音节",
                        "其他辅音结尾 → 重音在最后一个音节",
                        "疑问词都带重音：¿Qué? ¿Cómo? ¿Dónde?",
                        "Sí (是) vs Si (如果) — 重音改变意思",
                    ],
                    "ejemplos": [
                        {
                            "frase": "¿Cómo estás? ¿Dónde vives?",
                            "traduccion": "你好吗？你住在哪里？",
                            "analisis": ["Cómo 和 Dónde 有重音，因为是疑问词", "Estás 的重音在最后一个音节"],
                        },
                        {
                            "frase": "Sí, quiero café.",
                            "traduccion": "是的，我想要咖啡。",
                            "analisis": ["Sí (有重音) = 是", "café (有重音) = 咖啡"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "¿Lleva tilde? a) casa b) café c) como",
                        "traduccion": "哪些词有重音？",
                        "solucion": "café sí | como no | cómo sí (疑问词)",
                        "analisis": ["casa = 无重音（以元音结尾）", "café = 有重音（例外）", "cómo = 疑问词带重音"],
                    },
                },

                {
                    "slug": "010-repaso-alfabeto",
                    "tema": "Repaso: alfabeto y pronunciación",
                    "objetivo": "Repasar todo lo del módulo de pronunciación",
                    "explicacion": "今天我们复习字母和发音。记住：5个元音只有一种发音，H不发音，LL发y音，Ñ发ny音，C在e/i前变s音，G在e/i前变j音，J发h音，RR是颤音。",
                    "puntos": [
                        "5 vocales: A E I O U — siempre igual",
                        "H es muda (no suena)",
                        "LL = [y] Ñ = [ny]",
                        "C + e/i = [s]  G + e/i = [j]",
                        "R vs RR — ¡practica el rollo!",
                    ],
                    "ejemplos": [],
                    "ejercicio": {
                        "frase": 'Corrige la pronunciación: "Yo llamo a José"',
                        "traduccion": "纠正发音",
                        "solucion": "Yo (yo) lla-mo (ya-mo) a (a) Jo-sé (ho-se)",
                        "analisis": ["LL = y: ya-mo", "J = h: ho-se"],
                    },
                    "es_repaso": True,
                },
            ],
        },

        # ═══════════════════════════════════════════
        # MÓDULO 3: NÚMEROS
        # ═══════════════════════════════════════════
        {
            "titulo": "Los números",
            "slug": "03_numeros",
            "lecciones": [

                {
                    "slug": "011-numeros-0-20",
                    "tema": "Números del 0 al 20",
                    "objetivo": "Aprender los primeros 20 números",
                    "explicacion": "西班牙语数字0到20。0到15需要单独记忆。11 = once（不是 dieciuno），12 = doce，13 = trece，14 = catorce，15 = quince。16 = dieciséis 有重音，17 diecisiete，18 dieciocho，19 diecinueve，20 veinte。",
                    "puntos": [
                        "0 cero / 1 uno / 2 dos / 3 tres / 4 cuatro",
                        "5 cinco / 6 seis / 7 siete / 8 ocho / 9 nueve / 10 diez",
                        "11 once / 12 doce / 13 trece / 14 catorce / 15 quince",
                        "16 dieciséis / 17 diecisiete / 18 dieciocho / 19 diecinueve / 20 veinte",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Tengo 18 años. ¿Cuántos años tienes?",
                            "traduccion": "我18岁。你几岁？",
                            "analisis": ["18 = dieciocho", "años = 岁"],
                        },
                        {
                            "frase": "El libro cuesta 15 euros.",
                            "traduccion": "这本书15欧元。",
                            "analisis": ["15 = quince", "euros = 欧元"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Escribe en español: 7, 11, 15, 19",
                        "traduccion": "用西班牙语写出：7, 11, 15, 19",
                        "solucion": "siete, once, quince, diecinueve",
                        "analisis": ["7=siete, 11=once, 15=quince, 19=diecinueve"],
                    },
                },

                {
                    "slug": "012-numeros-20-100",
                    "tema": "Números del 20 al 100",
                    "objetivo": "Aprender a contar hasta 100",
                    "explicacion": "从20到100。20-29是veinti+数字：veintiuno, veintidós, veintitrés。30-99是十位数 + y + 个位数：treinta y uno, cuarenta y dos。注意30 treinta, 40 cuarenta, 50 cincuenta, 60 sesenta, 70 setenta, 80 ochenta, 90 noventa, 100 cien。",
                    "puntos": [
                        "20 veinte / 21 veintiuno / 22 veintidós / 30 treinta",
                        "40 cuarenta / 50 cincuenta / 60 sesenta",
                        "70 setenta / 80 ochenta / 90 noventa / 100 cien",
                        "31 = treinta y uno / 42 = cuarenta y dos",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Mi abuela tiene 87 años.",
                            "traduccion": "我奶奶87岁。",
                            "analisis": ["87 = ochenta y siete", "años = 岁"],
                        },
                        {
                            "frase": "El boleto cuesta 45 pesos.",
                            "traduccion": "这张票45比索。",
                            "analisis": ["45 = cuarenta y cinco", "pesos = 比索（墨西哥）"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Escribe: 33, 57, 99",
                        "traduccion": "写出：33, 57, 99",
                        "solucion": "treinta y tres, cincuenta y siete, noventa y nueve",
                        "analisis": ["33 = treinta y tres", "57 = cincuenta y siete", "99 = noventa y nueve"],
                    },
                },

                {
                    "slug": "013-numeros-ordinales",
                    "tema": "Números ordinales",
                    "objetivo": "Aprender los ordinales básicos (1°-10°)",
                    "explicacion": "序数词表示顺序：primero第一，segundo第二，tercero第三，cuarto第四，quinto第五，sexto第六，séptimo第七，octavo第八，noveno第九，décimo第十。注意 primero 和 tercero 在阳性名词前缩略：primer piso（第一层），tercer libro（第三本书）。",
                    "puntos": [
                        "1° primero / 2° segundo / 3° tercero / 4° cuarto / 5° quinto",
                        "6° sexto / 7° séptimo / 8° octavo / 9° noveno / 10° décimo",
                        "Primer piso (no primero piso)",
                        "Tercer libro (no tercero libro)",
                    ],
                    "ejemplos": [
                        {
                            "frase": "Vivo en el tercer piso.",
                            "traduccion": "我住在第三层。",
                            "analisis": ["Tercer = tercero的缩略", "piso = 楼层"],
                        },
                        {
                            "frase": "Ella es la primera de la clase.",
                            "traduccion": "她是班上的第一名。",
                            "analisis": ["Primera (femenino) = 第一", "注意阴阳性变化"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Completa: Vivo en el ____ (1°) piso.",
                        "traduccion": "填空：我住在第一层。",
                        "solucion": "primer",
                        "analisis": ["primer = primero的缩略形式"],
                    },
                },

                {
                    "slug": "014-la-edad",
                    "tema": "La edad",
                    "objetivo": "Preguntar y decir la edad",
                    "explicacion": "西班牙语中说年龄用动词 tener（有），不是 ser（是）。Tengo 18 años = 我有18岁。注意岁数用 años。问年龄说 ¿Cuántos años tienes? 你几岁？回答 Tengo + 数字 + años。",
                    "puntos": [
                        "¿Cuántos años tienes? — 你几岁？",
                        "Tengo [número] años — 我...岁",
                        "用tener（有），不是ser（是）",
                    ],
                    "ejemplos": [
                        {
                            "frase": "— ¿Cuántos años tienes? — Tengo 25 años.",
                            "traduccion": "你几岁？我25岁。",
                            "analisis": ["Tengo = 我有（tener的变位）", "25 años = 25岁"],
                        },
                        {
                            "frase": "Mi hermana tiene 30 años.",
                            "traduccion": "我姐姐30岁。",
                            "analisis": ["hermana = 姐妹", "tiene = 她有"],
                        },
                    ],
                    "ejercicio": {
                        "frase": '¿Cómo se dice "我20岁" en español?',
                        "traduccion": "用西班牙语说「我20岁」",
                        "solucion": "Tengo veinte años.",
                        "analisis": ["Tengo = 我有", "veinte = 20", "años = 岁"],
                    },
                },

                {
                    "slug": "015-el-precio",
                    "tema": "El precio",
                    "objetivo": "Preguntar y decir precios",
                    "explicacion": "问价格用 ¿Cuánto cuesta?（单数）或 ¿Cuánto cuestan?（复数）。回答：Cuesta [número] + moneda。墨西哥用 pesos，西班牙用 euros。可以简单说 Son 10 pesos。100 = cien，但100多要用 ciento：ciento cinco pesos。",
                    "puntos": [
                        "¿Cuánto cuesta? — 多少钱？（单数）",
                        "¿Cuánto cuestan? — 多少钱？（复数）",
                        "Cuesta / Cuestan — 价格是...",
                        "100 = cien / 101 = ciento uno",
                    ],
                    "ejemplos": [
                        {
                            "frase": "— ¿Cuánto cuesta esto? — Cuesta 50 pesos.",
                            "traduccion": "这个多少钱？50比索。",
                            "analisis": ["esto = 这个", "cuesta = 价格是（单数）"],
                        },
                        {
                            "frase": "— ¿Cuánto cuestan los zapatos? — Cuestan 800 pesos.",
                            "traduccion": "鞋子多少钱？800比索。",
                            "analisis": ["cuestan = 价格是（复数）", "800 = ochocientos"],
                        },
                    ],
                    "ejercicio": {
                        "frase": "Pregunta: ¿Cuánto ____ esto? (cuesta/cuestan)",
                        "traduccion": "填空：这个多少钱？",
                        "solucion": "¿Cuánto cuesta esto?",
                        "analisis": ["esto（这个）= 单数 → cuesta"],
                    },
                },
            ],
        },
    ],
}
