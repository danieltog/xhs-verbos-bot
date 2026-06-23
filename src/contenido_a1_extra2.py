"""
Extensiones A1 — Módulos 08 a 14
"""
EXTRA2 = [

    # ═══════════════════════════════════════════
    # MÓDULO 8: PLURAL
    # ═══════════════════════════════════════════
    {
        "titulo": "El plural",
        "slug": "08_plural",
        "lecciones": [
            {
                "slug": "032-formacion-plural",
                "tema": "Formación del plural",
                "objetivo": "Aprender las reglas para formar el plural",
                "explicacion": "西班牙语复数规则：以元音结尾的加-s：libro→libros，casa→casas。以辅音结尾的加-es：profesor→profesores，ciudad→ciudades。以-z结尾的变z为c再加-es：luz→luces，pez→peces。以-s结尾的如果重音不在最后一个音节则不变化el lunes→los lunes。注意重音规则：单数有重音的，复数时有时要去掉。",
                "puntos": [
                    "元音结尾 + s: libro→libros, casa→casas",
                    "辅音结尾 + es: profesor→profesores",
                    "-z → -ces: luz→luces, pez→peces",
                    "Lunes (不变): el lunes→los lunes",
                ],
                "ejemplos": [
                    {"frase": "Tengo dos libros nuevos.", "traduccion": "我有两本新书。", "analisis": ["libros = libro + s", "nuevos = 新的（复数）"]},
                    {"frase": "Hay muchas ciudades en España.", "traduccion": "西班牙有很多城市。", "analisis": ["ciudades = ciudad + es", "-dad → -dades"]},
                ],
                "ejercicio": {
                    "frase": "Plural de: profesor, luz, canción, mes",
                    "traduccion": "写出复数：profesor, luz, canción, mes",
                    "solucion": "profesores, luces, canciones, meses",
                    "analisis": ["profesor+es", "luz→luces (z→c)", "canción→canciones (tilde消失)"],
                },
            },
            {
                "slug": "033-concordancia",
                "tema": "Concordancia: sustantivo + adjetivo",
                "objetivo": "Aprender a concordar sustantivos con adjetivos",
                "explicacion": "西班牙语中形容词要和名词保持阴阳性和单复数一致。阳性+阳性：libro rojo。阴性+阴性：casa roja。复数+复数：libros rojos，casas rojas。形容词一般在名词后面。ej: un chico alto（一个高个子男孩），una chica alta（一个高个子女孩），chicos altos（高个子男孩们），chicas altas（高个子女孩们）。",
                "puntos": [
                    "Masc + Masc: libro rojo", "Fem + Fem: casa roja",
                    "Plural + Plural: libros rojos",
                    "Adj一般放在名词后面",
                ],
                "ejemplos": [
                    {"frase": "Tengo una casa blanca y un carro rojo.", "traduccion": "我有一栋白色的房子和一辆红色的车。", "analisis": ["casa (fem) → blanca", "carro (masc) → rojo"]},
                    {"frase": "Las flores amarillas son muy bonitas.", "traduccion": "黄色的花很漂亮。", "analisis": ["flores (fem/pl) → amarillas, bonitas", "concordancia completa"]},
                ],
                "ejercicio": {
                    "frase": "Corrige: un casa blanco, una libro roja",
                    "traduccion": "改正：un casa blanco, una libro roja",
                    "solucion": "una casa blanca, un libro rojo",
                    "analisis": ["casa=fem → una, blanca", "libro=masc → un, rojo"],
                },
            },
            {
                "slug": "034-repaso-plural",
                "tema": "Repaso: plural y concordancia",
                "objetivo": "Repasar la formación del plural y la concordancia",
                "explicacion": "复习：复数加-s或-es，z变c加-es，形容词和名词要保持一致。",
                "puntos": [
                    "+s (vocal) / +es (consonante)", "-z → -ces",
                    "Artículo + sustantivo + adjetivo",
                    "Todo concuerda en género y número",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Escribe en plural: El profesor alto es bueno.",
                    "traduccion": "写出复数形式",
                    "solucion": "Los profesores altos son buenos.",
                    "analisis": ["el→los", "profesor→profesores", "alto→altos", "es→son"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 9: PRESENTE -AR
    # ═══════════════════════════════════════════
    {
        "titulo": "Presente: verbos regulares -AR",
        "slug": "09_presente_ar",
        "lecciones": [
            {
                "slug": "035-intro-ar",
                "tema": "Introducción a los verbos -AR",
                "objetivo": "Aprender a conjugar verbos terminados en -AR",
                "explicacion": "西班牙语动词分三种：-ar，-er，-ir。今天我们学-ar动词。去掉词尾-ar，加上人称词尾：yo -o，tú -as，él/ella/usted -a，nosotros -amos，vosotros -áis，ellos/ellas/ustedes -an。以hablar（说/讲）为例：yo hablo，tú hablas，él habla，nosotros hablamos，ellos hablan。",
                "puntos": [
                    "yo → hablo", "tú → hablas", "él/ella/usted → habla",
                    "nosotros → hablamos", "vosotros → habláis", "ellos → hablan",
                    "Quitar -ar + añadir terminación",
                ],
                "ejemplos": [
                    {"frase": "Yo hablo español y chino.", "traduccion": "我说西班牙语和中文。", "analisis": ["hablo = hablar (yo)", "y = 和"]},
                    {"frase": "Ellos estudian en la universidad.", "traduccion": "他们在大学学习。", "analisis": ["estudian = estudiar (ellos)", "universidad = 大学"]},
                ],
                "ejercicio": {
                    "frase": "Conjuga: Yo _____ (hablar) con María.",
                    "traduccion": "变位：我和María说话。",
                    "solucion": "Yo hablo con María.",
                    "analisis": ["hablar → hablo (yo)"],
                },
            },
            {
                "slug": "036-conjugacion-hablar",
                "tema": "Practicar: hablar, estudiar, trabajar",
                "objetivo": "Practicar la conjugación de verbos -AR comunes",
                "explicacion": "三个常用-ar动词：hablar说话，estudiar学习，trabajar工作。yo hablo/estudio/trabajo，tú hablas/estudias/trabajas，él habla/estudia/trabaja，nosotros hablamos/estudiamos/trabajamos，ellos hablan/estudian/trabajan。注意estudiar的yo形式没有重音：estudio。",
                "puntos": [
                    "Hablar: hablo, hablas, habla, hablamos, hablan",
                    "Estudiar: estudio, estudias, estudia, estudiamos, estudian",
                    "Trabajar: trabajo, trabajas, trabaja, trabajamos, trabajan",
                ],
                "ejemplos": [
                    {"frase": "Ella trabaja en un hospital.", "traduccion": "她在医院工作。", "analisis": ["trabaja = trabajar (ella)", "hospital = 医院"]},
                    {"frase": "Nosotros estudiamos español todos los días.", "traduccion": "我们每天学习西班牙语。", "analisis": ["estudiamos = estudiar (nosotros)", "todos los días = 每天"]},
                ],
                "ejercicio": {
                    "frase": "¿Tú ____ (trabajar) aquí?", "traduccion": "你在这里工作吗？",
                    "solucion": "¿Tú trabajas aquí?",
                    "analisis": ["tú → trabajas"],
                },
            },
            {
                "slug": "037-otros-verbos-ar",
                "tema": "Más verbos -AR: cantar, bailar, comprar, viajar",
                "objetivo": "Ampliar el vocabulario de verbos -AR",
                "explicacion": "更多-ar动词：cantar唱歌，bailar跳舞，comprar买，viajar旅行，caminar走路，escuchar听，mirar看，tomar拿/喝，llamar叫/打电话，preguntar问，responder回答（这个是-er动词），llegar到达，llevar带/穿，necesitar需要，usar使用。注意llegar的yo形式要加u保持g音：llego。",
                "puntos": [
                    "Cantar / bailar / comprar / viajar", "Escuchar / mirar / tomar / llamar",
                    "Llegar → yo llego (保持g音)", "Necesitar / usar / caminar",
                ],
                "ejemplos": [
                    {"frase": "Ellos cantan y bailan muy bien.", "traduccion": "他们唱歌跳舞都很好。", "analisis": ["cantan = cantar (ellos)", "bailan = bailar (ellos)"]},
                    {"frase": "Necesito comprar un regalo.", "traduccion": "我需要买一个礼物。", "analisis": ["necesito = necesitar (yo)", "un regalo = 一个礼物"]},
                ],
                "ejercicio": {
                    "frase": "Yo ____ (viajar) a España este año.",
                    "traduccion": "我今年去西班牙旅行。",
                    "solucion": "Yo viajo a España este año.",
                    "analisis": ["viajar → viajo (yo)"],
                },
            },
            {
                "slug": "038-repaso-verbos-ar",
                "tema": "Repaso: verbos -AR",
                "objetivo": "Repasar la conjugación de verbos -AR",
                "explicacion": "复习-ar动词变位：去掉-ar加-o/-as/-a/-amos/-áis/-an。重要动词：hablar, estudiar, trabajar, cantar, bailar, comprar, viajar, necesitar, tomar, escuchar。",
                "puntos": [
                    "yo -o / tú -as / él -a", "nosotros -amos / ellos -an",
                    "¡Practica todos los días!",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Conjuga: Ellos ____ (escuchar) música. Yo ____ (tomar) café.",
                    "traduccion": "变位：他们听音乐。我喝咖啡。",
                    "solucion": "Ellos escuchan música. Yo tomo café.",
                    "analisis": ["escuchar→escuchan", "tomar→tomo"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 10: PRESENTE -ER / -IR
    # ═══════════════════════════════════════════
    {
        "titulo": "Presente: verbos regulares -ER e -IR",
        "slug": "10_presente_er_ir",
        "lecciones": [
            {
                "slug": "039-verbos-er",
                "tema": "Verbos regulares -ER",
                "objetivo": "Aprender a conjugar verbos -ER",
                "explicacion": "-er动词变位：去掉-er加-o/-es/-e/-emos/-éis/-en。以comer（吃）为例：yo como，tú comes，él come，nosotros comemos，ellos comen。常见-er动词：comer吃，beber喝，leer读，correr跑，vender卖，aprender学习，comprender理解，responder回答。注意leer的变位：yo leo（不是leio）。",
                "puntos": [
                    "yo como / tú comes / él come",
                    "nosotros comemos / ellos comen",
                    "Comer, beber, leer, correr, aprender",
                ],
                "ejemplos": [
                    {"frase": "Yo como frutas todos los días.", "traduccion": "我每天吃水果。", "analisis": ["como = comer (yo)", "frutas = 水果"]},
                    {"frase": "Ellos aprenden español en la escuela.", "traduccion": "他们在学校学西班牙语。", "analisis": ["aprenden = aprender (ellos)", "escuela = 学校"]},
                ],
                "ejercicio": {
                    "frase": "Nosotros ____ (beber) agua. Tú ____ (leer) un libro.",
                    "traduccion": "我们喝水。你读一本书。",
                    "solucion": "Nosotros bebemos agua. Tú lees un libro.",
                    "analisis": ["beber→bebemos", "leer→lees"],
                },
            },
            {
                "slug": "040-verbos-ir",
                "tema": "Verbos regulares -IR",
                "objetivo": "Aprender a conjugar verbos -IR",
                "explicacion": "-ir动词变位：去掉-ir加-o/-es/-e/-imos/-ís/-en。以vivir（住/生活）为例：yo vivo，tú vives，él vive，nosotros vivimos，vosotros vivís，ellos viven。常见-ir动词：vivir住，escribir写，abrir开，recibir收到，subir上（楼），compartir分享，decidir决定。注意-ir和-er的区别只在nosotros/vosotros：-emos vs -imos，-éis vs -ís。",
                "puntos": [
                    "yo vivo / tú vives / él vive",
                    "nosotros vivimos / ellos viven",
                    "Vivir, escribir, abrir, recibir, subir",
                ],
                "ejemplos": [
                    {"frase": "Yo vivo en la ciudad de México.", "traduccion": "我住在墨西哥城。", "analisis": ["vivo = vivir (yo)", "en = 在"]},
                    {"frase": "Ellos escriben una carta.", "traduccion": "他们写一封信。", "analisis": ["escriben = escribir (ellos)", "una carta = 一封信"]},
                ],
                "ejercicio": {
                    "frase": "Tú ____ (vivir) en China. Yo ____ (escribir) un mensaje.",
                    "traduccion": "你住在中国。我写一条信息。",
                    "solucion": "Tú vives en China. Yo escribo un mensaje.",
                    "analisis": ["vivir→vives", "escribir→escribo"],
                },
            },
            {
                "slug": "041-comparacion-er-ir",
                "tema": "Comparación: -ER vs -IR",
                "objetivo": "Diferenciar la conjugación de -ER e -IR",
                "explicacion": "-er和-ir变位对比：单数形式完全一样（o, es, e），复数不同：-emos(er) vs -imos(ir)，-éis(er) vs -ís(ir)，-en(en)两者相同。Comer: como, comes, come, comemos, coméis, comen。Vivir: vivo, vives, vive, vivimos, vivís, viven。注意区别只在nosotros和vosotros！",
                "puntos": [
                    "Singular: -ER e -IR igual (o, es, e)",
                    "Nosotros: -emos (ER) vs -imos (IR)",
                    "Vosotros: -éis (ER) vs -ís (IR)",
                    "Ellos: -en (ambos)",
                ],
                "ejemplos": [
                    {"frase": "Nosotros comemos juntos. Ellos viven cerca.", "traduccion": "我们一起吃。他们住在附近。", "analisis": ["comemos (ER)", "viven (IR)"]},
                    {"frase": "¿Tú aprendes español? — Sí, y escribo mucho.", "traduccion": "你学西班牙语吗？是的，我写很多。", "analisis": ["aprendes (ER)", "escribo (IR)"]},
                ],
                "ejercicio": {
                    "frase": "¿ER o IR? Nosotros ____ (comer/vivir) pan.",
                    "traduccion": "变位并判断是ER还是IR：我们吃面包。",
                    "solucion": "Nosotros comemos pan. (ER)",
                    "analisis": ["comemos = comer (ER)", "pan = 面包"],
                },
            },
            {
                "slug": "042-repaso-er-ir",
                "tema": "Repaso: verbos -ER e -IR",
                "objetivo": "Repasar la conjugación de -ER e -IR",
                "explicacion": "复习：-er动词（comer, beber, leer, aprender），-ir动词（vivir, escribir, abrir, subir）。变位规律：单数相同，复数不同。",
                "puntos": [
                    "-ER: como, comes, come, comemos, coméis, comen",
                    "-IR: vivo, vives, vive, vivimos, vivís, viven",
                    "Aprender de memoria",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Conjuga: Yo (aprender) y (escribir) cada día.",
                    "traduccion": "变位：我每天学习和写作。",
                    "solucion": "Yo aprendo y escribo cada día.",
                    "analisis": ["aprender→aprendo", "escribir→escribo"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 11: SER Y ESTAR
    # ═══════════════════════════════════════════
    {
        "titulo": "Ser y estar",
        "slug": "11_ser_estar",
        "lecciones": [
            {
                "slug": "043-ser-caracteristicas",
                "tema": "Ser: características esenciales",
                "objetivo": "Aprender los usos del verbo SER",
                "explicacion": "Ser表示本质特征。变位：yo soy，tú eres，él/ella es，nosotros somos，ellos son。用于：1. 身份和定义（Soy estudiante），2. 国籍和来源（Soy de China），3. 性格和外观（Eres alto），4. 时间和日期（Son las dos），5. 所属（Es mi libro），6. 材质（La mesa es de madera）。不可用于位置（用estar）。",
                "puntos": [
                    "Soy / eres / es / somos / son",
                    "Identidad: Soy estudiante.",
                    "Nacionalidad: Soy chino.",
                    "Características: Es alto.",
                    "Hora y fecha: Son las tres.",
                ],
                "ejemplos": [
                    {"frase": "Yo soy médico. Soy de Colombia.", "traduccion": "我是医生。我来自哥伦比亚。", "analisis": ["Soy = ser (yo)", "Soy de = 来自"]},
                    {"frase": "Ella es muy inteligente y simpática.", "traduccion": "她很聪明又友善。", "analisis": ["es = ser (ella)", "inteligente = 聪明"]},
                ],
                "ejercicio": {
                    "frase": "Yo ____ (ser) estudiante. Ella ____ (ser) profesora.",
                    "traduccion": "我是学生。她是老师。",
                    "solucion": "Yo soy estudiante. Ella es profesora.",
                    "analisis": ["yo→soy", "ella→es"],
                },
            },
            {
                "slug": "044-estar-estados",
                "tema": "Estar: estados y ubicaciones",
                "objetivo": "Aprender los usos del verbo ESTAR",
                "explicacion": "Estar表示状态和位置。变位：yo estoy，tú estás，él/ella está，nosotros estamos，ellos están。用于：1. 位置（¿Dónde está el libro?），2. 情绪和状态（Estoy cansado），3. 临时状况（La sopa está fría），4. 进行时（Estoy comiendo）。注意和ser的区别：Es bueno（他人好）vs Está bueno（东西好吃/状态好）。",
                "puntos": [
                    "Estoy / estás / está / estamos / están",
                    "Ubicación: El libro está en la mesa.",
                    "Estado: Estoy cansado / feliz / triste.",
                    "Progresivo: Estoy comiendo.",
                ],
                "ejemplos": [
                    {"frase": "¿Dónde está el baño? — Está al final del pasillo.", "traduccion": "洗手间在哪里？在走廊尽头。", "analisis": ["está = estar (3a pers)", "baño = 洗手间"]},
                    {"frase": "Hoy estoy muy contento.", "traduccion": "今天我很开心。", "analisis": ["estoy = estar (yo)", "contento = 开心（临时状态）"]},
                ],
                "ejercicio": {
                    "frase": "Yo ____ (estar) en casa. Ellos ____ (estar) cansados.",
                    "traduccion": "我在家。他们累了。",
                    "solucion": "Yo estoy en casa. Ellos están cansados.",
                    "analisis": ["yo→estoy", "ellos→están"],
                },
            },
            {
                "slug": "045-ser-vs-estar",
                "tema": "Diferencia: SER vs ESTAR",
                "objetivo": "Distinguir cuándo usar SER y cuándo ESTAR",
                "explicacion": "Ser vs Estar的核心区别：Ser是本质/永久，Estar是状态/临时。Ej: Es alta（她个子高——天生）vs Está alta（她今天看起来高——穿了高跟鞋）。Es aburrido（他这个人无聊）vs Está aburrido（他现在觉得无聊）。Ser para identidad，Estar para condición。记住缩略词：DOCTOR（Description, Occupation, Characteristic, Time, Origin, Relationship）→ Ser。PLACE（Position, Location, Action, Condition, Emotion）→ Estar。",
                "puntos": [
                    "SER = esencia, permanente",
                    "ESTAR = estado, temporal",
                    "Es guapo (天生) vs Está guapo (今天)",
                    "¿Dónde? → Estar / ¿Qué/Quién? → Ser",
                ],
                "ejemplos": [
                    {"frase": "María es alta y delgada. Hoy está cansada.", "traduccion": "María个子高又瘦。今天她累了。", "analisis": ["Es alta = 本质特征", "Está cansada = 临时状态"]},
                    {"frase": "La sopa está fría. — El restaurante es bueno.", "traduccion": "汤凉了。——这家餐厅不错。", "analisis": ["está fría = 状态（现在）", "es bueno = 评价（本质）"]},
                ],
                "ejercicio": {
                    "frase": "Completa: María ____ (ser/estar) china. Ahora ____ (ser/estar) en México.",
                    "traduccion": "María是中国人。现在她在墨西哥。",
                    "solucion": "María es china. Ahora está en México.",
                    "analisis": ["es china = nacionalidad (ser)", "está en México = ubicación (estar)"],
                },
            },
            {
                "slug": "046-repaso-ser-estar",
                "tema": "Repaso: ser y estar",
                "objetivo": "Repasar la diferencia entre ser y estar",
                "explicacion": "复习：Ser（本质）：soy/eres/es/somos/son。Estar（状态）：estoy/estás/está/estamos/están。",
                "puntos": [
                    "Ser: identidad, origen, hora, carácter",
                    "Estar: ubicación, estado, emoción",
                    "¡Practica con ejemplos!",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "El libro ____ (ser/estar) en la mesa. ____ (ser/estar) mío.",
                    "traduccion": "书在桌子上。它是我的。",
                    "solucion": "El libro está en la mesa. Es mío.",
                    "analisis": ["ubicación → está", "posesión → es"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 12: TENER, HACER, IR, VERBOS IRREGULARES
    # ═══════════════════════════════════════════
    {
        "titulo": "Verbos irregulares: tener, hacer, ir, poder, querer",
        "slug": "12_verbos_irregulares",
        "lecciones": [
            {
                "slug": "047-tener",
                "tema": "El verbo TENER",
                "objetivo": "Aprender el verbo tener y sus usos",
                "explicacion": "Tener（有）是不规则动词：yo tengo，tú tienes，él tiene，nosotros tenemos，ellos tienen。用于：1. 拥有（Tengo un carro），2. 年龄（Tengo 20 años），3. 感觉（Tengo hambre/sed/frío/calor/sueño），4. 必须（Tengo que estudiar）。注意tener que + infinitivo = 必须做某事。",
                "puntos": [
                    "tengo, tienes, tiene, tenemos, tienen",
                    "Tener + edad: Tengo 25 años.",
                    "Tener hambre/sed/frío/calor/sueño/miedo",
                    "Tener que + infinitivo = 必须",
                ],
                "ejemplos": [
                    {"frase": "Tengo hambre. Vamos a comer.", "traduccion": "我饿了。我们去吃吧。", "analisis": ["Tengo hambre = 我饿了", "Vamos a = 我们去（ir a）"]},
                    {"frase": "Ella tiene que estudiar para el examen.", "traduccion": "她必须为考试学习。", "analisis": ["tiene que = 必须", "examen = 考试"]},
                ],
                "ejercicio": {
                    "frase": "Yo ____ (tener) dos hermanos. Él ____ (tener) 30 años.",
                    "traduccion": "我有两个兄弟。他30岁。",
                    "solucion": "Yo tengo dos hermanos. Él tiene 30 años.",
                    "analisis": ["yo→tengo", "él→tiene"],
                },
            },
            {
                "slug": "048-hacer",
                "tema": "El verbo HACER",
                "objetivo": "Aprender el verbo hacer y sus usos",
                "explicacion": "Hacer（做）不规则：yo hago，tú haces，él hace，nosotros hacemos，ellos hacen。用于：1. 做某事（Hago la tarea），2. 天气（Hace frío/calor/sol/viento），3. 时间表达（Hace dos años），4. 固定短语（Hacer la cama铺床，Hacer la compra购物）。注意hago的go结尾。",
                "puntos": [
                    "hago, haces, hace, hacemos, hacen",
                    "Hace frío/calor/sol/viento — 天气",
                    "Hace + tiempo: Hace dos años...",
                    "Hacer la tarea / la cama / deporte",
                ],
                "ejemplos": [
                    {"frase": "Hoy hace mucho calor.", "traduccion": "今天很热。", "analisis": ["hace = hacer (3a pers)", "calor = 热"]},
                    {"frase": "Yo hago ejercicio todas las mañanas.", "traduccion": "我每天早上做运动。", "analisis": ["hago = hacer (yo)", "ejercicio = 运动"]},
                ],
                "ejercicio": {
                    "frase": "¿Qué tiempo hace? ____ (hacer) frío y llueve.",
                    "traduccion": "天气怎么样？天气冷而且下雨。",
                    "solucion": "Hace frío y llueve.",
                    "analisis": ["hace = hacer (3a pers impers.)"],
                },
            },
            {
                "slug": "049-ir",
                "tema": "El verbo IR (y ir + a)",
                "objetivo": "Aprender el verbo ir y el futuro próximo",
                "explicacion": "Ir（去）完全不规则：yo voy，tú vas，él va，nosotros vamos，ellos van。用于：1. 去某地（Voy al mercado），2. 将来时ir + a + infinitivo（Voy a estudiar）。注意ir + a：Voy a + lugar（去某地），Voy a + infinitivo（将要...）。Preguntar：¿Adónde vas?你去哪里？¿Vas a...?你将要...？",
                "puntos": [
                    "voy, vas, va, vamos, van",
                    "Ir a + lugar: Voy al cine.",
                    "Ir a + infinitivo: Voy a comer.",
                    "¿Adónde vas? — 你去哪里？",
                ],
                "ejemplos": [
                    {"frase": "Voy a la biblioteca a estudiar.", "traduccion": "我去图书馆学习。", "analisis": ["Voy = ir (yo)", "a la biblioteca = 去图书馆"]},
                    {"frase": "Mañana vamos a viajar a Madrid.", "traduccion": "明天我们要去马德里旅行。", "analisis": ["Vamos a + viajar = 将要旅行", "futuro próximo"]},
                ],
                "ejercicio": {
                    "frase": "¿Adónde ____ (ir/tú)? — ____ (ir/yo) al supermercado.",
                    "traduccion": "你去哪里？我去超市。",
                    "solucion": "¿Adónde vas? — Voy al supermercado.",
                    "analisis": ["tú→vas", "yo→voy", "al = a + el"],
                },
            },
            {
                "slug": "050-poder-querer",
                "tema": "Los verbos PODER y QUERER",
                "objetivo": "Aprender los verbos modales poder y querer",
                "explicacion": "Poder（能/可以）和querer（想要）是stem-changing动词（o→ue）。Poder：puedo, puedes, puede, podemos, pueden。Querer：quiero, quieres, quiere, queremos, quieren。Poder + infinitivo = 能够做某事。Querer + infinitivo = 想要做某事。Puedo hablar español（我能说西班牙语）。Quiero comer（我想吃）。注意poder的nosotros形式不变（podemos）。",
                "puntos": [
                    "Poder: puedo, puedes, puede, podemos, pueden",
                    "Querer: quiero, quieres, quiere, queremos, quieren",
                    "Poder + inf: Puedo ayudarte.",
                    "Querer + inf: Quiero viajar.",
                ],
                "ejemplos": [
                    {"frase": "¿Puedes ayudarme, por favor?", "traduccion": "你能帮我吗？", "analisis": ["Puedes = poder (tú)", "ayudarme = 帮我"]},
                    {"frase": "Quiero aprender español muy bien.", "traduccion": "我想学好西班牙语。", "analisis": ["Quiero = querer (yo)", "muy bien = 很好"]},
                ],
                "ejercicio": {
                    "frase": "Yo no ____ (poder) ir. Ellos ____ (querer) comer.",
                    "traduccion": "我不能去。他们想吃。",
                    "solucion": "Yo no puedo ir. Ellos quieren comer.",
                    "analisis": ["poder→puedo (o→ue)", "querer→quieren (e→ie)"],
                },
            },
            {
                "slug": "051-repaso-irregulares",
                "tema": "Repaso: verbos irregulares",
                "objetivo": "Repasar tener, hacer, ir, poder, querer",
                "explicacion": "复习五个不规则动词：tener（tengo/tienes/tiene），hacer（hago/haces/hace），ir（voy/vas/va），poder（puedo/puedes/puede），querer（quiero/quieres/quiere）。",
                "puntos": [
                    "Tener: tengo, tienes, tiene, tenemos, tienen",
                    "Hacer: hago, haces, hace, hacemos, hacen",
                    "Ir: voy, vas, va, vamos, van",
                    "Poder: puedo, puedes, puede, podemos, pueden",
                    "Querer: quiero, quieres, quiere, queremos, quieren",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Conjuga: Yo ____ (tener) que ____ (ir) a clase.",
                    "traduccion": "变位：我必须去上课。",
                    "solucion": "Yo tengo que ir a clase.",
                    "analisis": ["tener que = 必须", "ir = 去"],
                },
                "es_repaso": True,
            },
        ],
    },
]
