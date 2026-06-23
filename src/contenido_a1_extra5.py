"""
Extensiones A1 — Módulos 23 a 26
"""
EXTRA5 = [
    # ═══════════════════════════════════════════
    # MÓDULO 23: LA CASA
    # ═══════════════════════════════════════════
    {
        "titulo": "La casa y los muebles",
        "slug": "23_la_casa",
        "lecciones": [
            {
                "slug": "084-partes-casa",
                "tema": "Las partes de la casa",
                "objetivo": "Aprender el vocabulario de la casa",
                "explicacion": "房间和部分：cocina厨房，comedor餐厅，sala/salón客厅，dormitorio/habitación卧室，baño洗手间，pasillo走廊，escaleras楼梯，garaje车库，jardín花园，balcón阳台，terraza露台。表达：Vivo en un piso/casa（我住公寓/房子）。Mi casa tiene...（我家有...）。En la planta baja / primer piso（在底层/一楼）。",
                "puntos": [
                    "Cocina / Comedor / Salón / Dormitorio / Baño",
                    "Pasillo / Escaleras / Garaje / Jardín / Balcón",
                    "Vivo en... / Mi casa tiene...",
                ],
                "ejemplos": [
                    {"frase": "Mi casa tiene tres dormitorios y dos baños.", "traduccion": "我家有三间卧室和两个卫生间。", "analisis": ["tres dormitorios = 三间卧室", "dos baños = 两个卫生间"]},
                    {"frase": "La cocina es grande y el salón es muy bonito.", "traduccion": "厨房很大，客厅很漂亮。", "analisis": ["cocina = 厨房", "salón = 客厅"]},
                ],
                "ejercicio": {
                    "frase": "¿Dónde? Cocinas → ____. Duermes → ____. Te duchas → ____.",
                    "traduccion": "在哪里？做饭→___。睡觉→___。洗澡→___。",
                    "solucion": "cocina, dormitorio, baño",
                    "analisis": ["cocinar→cocina", "dormir→dormitorio", "ducharse→baño"],
                },
            },
            {
                "slug": "085-muebles",
                "tema": "Los muebles y objetos",
                "objetivo": "Aprender el vocabulario de muebles",
                "explicacion": "家具和物品：cama床，mesa桌子，silla椅子，sofá沙发，estantería书架，armario衣柜，cajón抽屉，lámpara灯，espejo镜子，cortina窗帘，alfombra地毯，cuadro画，televisión电视，nevera/refrigerador冰箱，lavadora洗衣机，horno烤箱，microondas微波炉。注意：los muebles（家具，复数）。描述位置：está en / hay en。",
                "puntos": [
                    "Cama / Mesa / Silla / Sofá / Armario / Estantería",
                    "Lámpara / Espejo / Cortina / Alfombra / Cuadro",
                    "Nevera / Lavadora / Horno / Microondas",
                ],
                "ejemplos": [
                    {"frase": "En mi dormitorio hay una cama, un armario y una mesa.", "traduccion": "我的卧室里有一张床、一个衣柜和一张桌子。", "analisis": ["Hay = 有", "un/una = 不定冠词"]},
                    {"frase": "El sofá está en el salón, delante de la televisión.", "traduccion": "沙发在客厅里，电视前面。", "analisis": ["delante de = 在...前面", "salón = 客厅"]},
                ],
                "ejercicio": {
                    "frase": "¿Dónde pones...? la ropa → ____ (armario/cama). los libros → ____ (nevera/estantería).",
                    "traduccion": "衣服放哪里？书放哪里？",
                    "solucion": "armario, estantería",
                    "analisis": ["ropa→armario", "libros→estantería"],
                },
            },
            {
                "slug": "086-repaso-casa",
                "tema": "Repaso: la casa",
                "objetivo": "Repasar el vocabulario de la casa",
                "explicacion": "复习房间和家具词汇，能够描述你的家。",
                "puntos": [
                    "Partes: cocina, dormitorio, baño, salón...",
                    "Muebles: cama, mesa, silla, sofá...",
                    "Describir: Mi casa tiene...",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Describe tu casa o tu habitación (3 frases).", "traduccion": "描述你的家或房间",
                    "solucion": "Mi habitación es pequeña pero bonita. Hay una cama, una mesa y un armario. La ventana es grande.",
                    "analisis": ["usa hay/está", "usa vocabulario de muebles"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 24: LA CIUDAD
    # ═══════════════════════════════════════════
    {
        "titulo": "La ciudad y las direcciones",
        "slug": "24_la_ciudad",
        "lecciones": [
            {
                "slug": "087-lugares-ciudad",
                "tema": "Lugares en la ciudad",
                "objetivo": "Aprender nombres de lugares en la ciudad",
                "explicacion": "城市地点：banco银行，supermercado超市，farmacia药店，hospital医院，escuela学校，universidad大学，biblioteca图书馆，museo博物馆，parque公园，cine电影院，teatro剧院，restaurante餐厅，cafetería咖啡馆，hotel酒店，estación车站，aeropuerto机场，correos邮局，comisaría警察局，iglesia教堂。用hay存在，estar问位置。",
                "puntos": [
                    "Banco, supermercado, farmacia, hospital",
                    "Escuela, biblioteca, museo, parque",
                    "Cine, teatro, restaurante, cafetería",
                    "Hotel, estación, aeropuerto, correos",
                ],
                "ejemplos": [
                    {"frase": "— Perdón, ¿hay un banco por aquí? — Sí, hay uno en la calle principal.", "traduccion": "打扰一下，附近有银行吗？有，主街上就有一家。", "analisis": ["Perdón = 打扰一下", "por aquí = 在这附近"]},
                    {"frase": "La biblioteca está entre el parque y el museo.", "traduccion": "图书馆在公园和博物馆之间。", "analisis": ["entre...y... = 在...和...之间", "biblioteca = 图书馆"]},
                ],
                "ejercicio": {
                    "frase": "Une: comprar medicina → ____. ver películas → ____. tomar café → ____.",
                    "traduccion": "连一连：买药→___。看电影→___。喝咖啡→___。",
                    "solucion": "farmacia, cine, cafetería",
                    "analisis": ["medicina→farmacia", "películas→cine", "café→cafetería"],
                },
            },
            {
                "slug": "088-dar-direcciones",
                "tema": "Dar direcciones",
                "objetivo": "Aprender a dar y pedir direcciones",
                "explicacion": "问路和指路：¿Dónde está...?（...在哪里？）¿Cómo llego a...?（怎样去...？）¿Está lejos/cerca?（远/近吗？）。指路：Sigue recto（直走），Gira a la derecha/izquierda（右/左转），Toma la primera/segunda calle（走第一/二条街），Está al final de la calle（在街的尽头），Está a la derecha/izquierda（在右边/左边），Está en la esquina（在拐角处），Está enfrente de / al lado de（在...对面/旁边）。",
                "puntos": [
                    "Sigue recto — 直走",
                    "Gira a la derecha/izquierda — 右/左转",
                    "Está al lado de / enfrente de / en la esquina",
                    "¿Está lejos? — No, está muy cerca.",
                ],
                "ejemplos": [
                    {"frase": "— ¿Cómo llego al museo? — Sigue recto y gira a la derecha.", "traduccion": "去博物馆怎么走？直走然后右转。", "analisis": ["Cómo llego a = 怎么到", "gira = 转（tú imperativo）"]},
                    {"frase": "La farmacia está enfrente del banco.", "traduccion": "药店在银行对面。", "analisis": ["enfrente de = 在...对面", "del = de + el"]},
                ],
                "ejercicio": {
                    "frase": "Ordena: gira a la derecha, sigue recto, está a la izquierda",
                    "traduccion": "排序：直走，右转，它在左边",
                    "solucion": "sigue recto → gira a la derecha → está a la izquierda",
                    "analisis": ["顺序：直走→转弯→位置"],
                },
            },
            {
                "slug": "089-medios-transporte",
                "tema": "Medios de transporte",
                "objetivo": "Vocabulario de transporte y cómo moverse",
                "explicacion": "交通工具：coche汽车，autobús公交车，metro地铁，tren火车，avión飞机，barco船，bicicleta自行车，moto摩托车，taxi出租车。Ir en + medio（乘...去）：Voy en coche / en autobús / en metro。Ir a pie（步行）。¿Cómo vas al trabajo?（你怎么去上班？）。Coger/Tomar el autobús（坐公交车）。El billete（车票），el andén（站台），la parada（站点），la estación（车站）。",
                "puntos": [
                    "Coche / Autobús / Metro / Tren / Avión / Barco",
                    "Ir en + medio / Ir a pie",
                    "Coger el autobús / el metro",
                    "La parada / La estación / El billete",
                ],
                "ejemplos": [
                    {"frase": "Voy al trabajo en metro. Tardo 20 minutos.", "traduccion": "我坐地铁上班。需要20分钟。", "analisis": ["en metro = 坐地铁", "tardo = 花时间（tardar）"]},
                    {"frase": "— ¿Cómo vas a la escuela? — Voy a pie.", "traduccion": "你怎么去学校？我步行去。", "analisis": ["¿Cómo vas? = 你怎么去？", "a pie = 步行"]},
                ],
                "ejercicio": {
                    "frase": "Completa con en/a: Voy ____ tren. Voy ____ pie.",
                    "traduccion": "用en或a填空",
                    "solucion": "en tren, a pie",
                    "analisis": ["en + vehículo", "a pie (excepción)"],
                },
            },
            {
                "slug": "090-repaso-ciudad",
                "tema": "Repaso: ciudad y transporte",
                "objetivo": "Repasar lugares, direcciones y transporte",
                "explicacion": "复习城市地点、问路指路和交通工具。",
                "puntos": [
                    "Lugares: banco, museo, parque...",
                    "Direcciones: sigue recto, gira...",
                    "Transporte: en coche, en metro, a pie",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Un turista pregunta: ¿Cómo llego al museo desde aquí?", "traduccion": "一个游客问：从这里怎么去博物馆？",
                    "solucion": "Sigue recto dos calles, gira a la izquierda y el museo está a la derecha, enfrente del parque.",
                    "analisis": ["sigue recto = 直走", "gira a la izquierda = 左转", "enfrente de = 在...对面"],
                },
                "es_repaso": True,
            },
        ],
    },

    # ═══════════════════════════════════════════
    # MÓDULO 25: REPASO GENERAL A1
    # ═══════════════════════════════════════════
    {
        "titulo": "Repaso general A1",
        "slug": "25_repaso_general",
        "lecciones": [
            {
                "slug": "091-repaso-gramatica",
                "tema": "Repaso de gramática A1",
                "objetivo": "Repasar la gramática más importante del nivel A1",
                "explicacion": "A1语法复习：1. 名词的阴阳性和单复数，2. 冠词el/la/un/una，3. 形容词配合，4. 现在时变位（-ar, -er, -ir），5. 不规则动词（ser, estar, tener, ir, hacer, poder, querer），6. Ser vs Estar，7. Gustar，8. Posesivos mi/mío，9. Demostrativos este/ese/aquel。",
                "puntos": [
                    "Género y número de sustantivos",
                    "Artículos: el/la/un/una + al/del",
                    "Presente regular e irregular",
                    "Ser vs Estar",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Corrige: Yo es estudiante. Ella está china. El libro están en mesa.",
                    "traduccion": "改错：",
                    "solucion": "Yo soy estudiante. Ella es china. El libro está en la mesa.",
                    "analisis": ["ser: yo→soy, ella→es", "estar: libro→está", "falta artículo 'la'"],
                },
                "es_repaso": True,
            },
            {
                "slug": "092-repaso-vocabulario",
                "tema": "Repaso de vocabulario A1",
                "objetivo": "Repasar el vocabulario esencial del nivel A1",
                "explicacion": "A1词汇复习：家庭、颜色、数字、日期、时间、食物、城市、房子、日常活动。",
                "puntos": [
                    "Familia, colores, números, fechas y hora",
                    "Comida, casa, ciudad, transporte",
                    "Rutina diaria y frecuencia",
                ],
                "ejemplos": [],
                "ejercicio": {
                    "frase": "Di en español: 我每天七点起床，洗澡，吃早餐，然后坐地铁去学校。",
                    "traduccion": "翻译",
                    "solucion": "Todos los días me levanto a las siete, me ducho, desayuno y luego voy a la escuela en metro.",
                    "analisis": ["todos los días = 每天", "me levanto = 起床", "en metro = 坐地铁"],
                },
                "es_repaso": True,
            },
        ],
    },
]
