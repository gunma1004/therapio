import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Therapio Platform")

os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

REGIONS = {
    "seoul": {
        "name": "서울특별시",
        "description": "강남, 서초, 송파, 마포, 영등포 등 서울 전지역 25분 내 신속 방문 출장마사지 홈케어",
        "districts": {
            "gangnam": {
                "name": "강남구",
                "dongs": {"yeoksam": "역삼동", "nonhyeon": "논현동", "samseong": "삼성동", "cheongdam": "청담동", "daechi": "대치동"}
            },
            "seocho": {
                "name": "서초구",
                "dongs": {"seocho-dong": "서초동", "banpo": "반포동", "bangbae": "방배동", "yangjae": "양재동", "jamwon": "잠원동"}
            },
            "songpa": {
                "name": "송파구",
                "dongs": {"jamsil": "잠실동", "garak": "가락동", "bangi": "방이동", "munjeong": "문정동", "sincheon": "신천동"}
            },
            "mapo": {
                "name": "마포구",
                "dongs": {"seogyo": "서교동", "hapjeong": "합정동", "sangam": "상암동", "gongdeok": "공덕동", "yeonnam": "연남동"}
            },
            "yeongdeungpo": {
                "name": "영등포구",
                "dongs": {"yeouido": "여의도동", "yeongdeungpo-dong": "영등포동", "dangsan": "당산동", "mullae": "문래동"}
            }
        }
    },
    "gyeonggi": {
        "name": "경기도",
        "description": "수원, 성남/분당, 고양/일산, 용인, 부천 등 경기 전지역 출장마사지 방문 테라피",
        "districts": {
            "suwon": {
                "name": "수원시",
                "dongs": {"ingye": "인계동", "yeongtong": "영통동", "gwanggyo": "광교동", "maetan": "매탄동", "gwonseon": "권선동"}
            },
            "seongnam": {
                "name": "성남시 (분당/판교)",
                "dongs": {"seohyeon": "서현동", "jeongja": "정자동", "pangyo": "판교동", "yatap": "야탑동", "baekhyeon": "백현동"}
            },
            "goyang": {
                "name": "고양시 (일산)",
                "dongs": {"janghang": "장항동", "baekseok": "백석동", "daehwa": "대화동", "madu": "마두동", "tangehyeon": "탄현동"}
            },
            "yongin": {
                "name": "용인시",
                "dongs": {"pungdeok": "풍덕천동", "giheung": "기흥동", "jukjeon": "죽전동", "dongcheon": "동천동"}
            },
            "bucheon": {
                "name": "부천시",
                "dongs": {"jungdong": "중동", "sangdong": "상동", "simgok": "심곡동", "wonmi": "원미동"}
            }
        }
    },
    "incheon": {
        "name": "인천광역시",
        "description": "송도, 청라, 부평, 구월 등 인천 전지역 출장마사지 안심 후불제 바디케어",
        "districts": {
            "yeonsu": {
                "name": "연수구 (송도)",
                "dongs": {"songdo": "송도동", "yeonsu-dong": "연수동", "dongchun": "동춘동", "cheonghak": "청학동"}
            },
            "namdong": {
                "name": "남동구 (구월)",
                "dongs": {"guwol": "구월동", "ganseok": "간석동", "mansu": "만수동", "nonhyeon-in": "논현동"}
            },
            "bupyeong": {
                "name": "부평구",
                "dongs": {"bupyeong-dong": "부평동", "sangok": "산곡동", "samsan": "삼산동", "cheongcheon": "청천동"}
            },
            "seo": {
                "name": "서구 (청라/검단)",
                "dongs": {"cheongna": "청라동", "yeonhui": "연희동", "geomdan": "검단동", "wondang": "원당동"}
            }
        }
    }
}

# 직접 만든 로컬 이미지 경로 적용 (실패 시 기본 고화질 이미지 백업)
SHOPS = [
    {
        "id": 1,
        "name": "한국미인테라피",
        "badge": "추천 1위",
        "rating": "5.0",
        "review_count": 254,
        "desc": "수도권 전지역 25분 내 신속 방문! 고품격 힐링 & 타이·아로마 프로그램",
        "price": "100,000",
        "phone": "0507-1280-3172",
        "image": "/static/images/shop1.jpg",
        "fallback_image": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": 2,
        "name": "주주테라피",
        "badge": "힐링 추천",
        "rating": "4.9",
        "review_count": 198,
        "desc": "품격 있는 힐링을 선사하는 최고급 유기농 오일 프라이빗 방문 테라피 서비스",
        "price": "60,000",
        "phone": "0507-1280-3174",
        "image": "/static/images/shop2.jpg",
        "fallback_image": "https://images.unsplash.com/photo-1600334089648-b0d9d3028eb2?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": 3,
        "name": "한국골든테라피",
        "badge": "재방문 1위",
        "rating": "4.9",
        "review_count": 215,
        "desc": "재방문율 1위! 칼도착 25분 보장, 철저한 위생 관리와 럭셔리 감성 바디케어",
        "price": "60,000",
        "phone": "0507-1280-3361",
        "image": "/static/images/shop3.jpg",
        "fallback_image": "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": 4,
        "name": "오늘밤테라피",
        "badge": "20대 프리미엄",
        "rating": "5.0",
        "review_count": 182,
        "desc": "전문 힐러들의 맞춤형 VIP 피로회복 특화 프로그램! 1:1 집중 힐링 케어 진행 중",
        "price": "60,000",
        "phone": "0507-1280-3126",
        "image": "/static/images/shop4.jpg",
        "fallback_image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": 5,
        "name": "퀸즈홈테라피",
        "badge": "안심 후불제",
        "rating": "4.9",
        "review_count": 310,
        "desc": "선입금 없는 100% 후불제! 수도권 전지역 평균 25분 내 실시간 도착 안심 케어",
        "price": "60,000",
        "phone": "0507-1280-3128",
        "image": "/static/images/shop5.jpg",
        "fallback_image": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=400&q=80"
    }
]

REVIEWS = [
    {"author": "서울 강남 이용자", "rating": "5.0", "tag": "한국미인테라피", "content": "역삼동인데 20분 만에 오셨어요. 어깨 결림이 심했는데 압도 적당하고 시간 꽉 채워주셔서 개운합니다. 후불제라 정말 안심돼요!"},
    {"author": "경기 수원 직장인", "rating": "5.0", "tag": "퀸즈홈테라피", "content": "선입금 없는 후불제라 부담없이 이용할 수 있어서 만족합니다. 매니저분 마인드와 실력 모두 최고였어요."},
    {"author": "인천 송도 거주자", "rating": "5.0", "tag": "오늘밤테라피", "content": "스웨디시 코스로 받았는데 오일 향도 고급스럽고 피로가 싹 풀렸네요. 주말마다 자주 찾게 될 것 같습니다."},
    {"author": "경기 분당 이용자", "rating": "5.0", "tag": "한국골든테라피", "content": "시간 약속 칼같이 맞춰오시고 친절하셨어요. 뭉친 등과 목이 가벼워져서 숙면 취했습니다."}
]

COURSE_INFO = [
    {"name": "타이 테라피 (건식)", "tag": "스트레칭 & 뭉친 근육 이완", "desc": "오일 없이 지압과 스트레칭을 결합하여 만성 피로와 굳은 관절을 시원하게 풀어주는 정통 프로그램입니다."},
    {"name": "아로마 테라피 (습식)", "tag": "천연 에센셜 오일 & 릴랙스", "desc": "피부 보습과 혈액순환에 탁월한 최고급 천연 아로마 오일을 사용해 부드럽고 편안한 이완감을 제공합니다."},
    {"name": "스웨디시 바디케어", "tag": "감성 힐링 & 림프 순환", "desc": "따뜻한 오일로 림프절을 자극하여 노폐물 배출과 극상의 릴랙싱 감성을 전달하는 VIP 프리미엄 코스입니다."}
]

def get_rotated_shops(page_seed: str = "") -> list:
    if not page_seed:
        return SHOPS
    offset = sum(ord(c) for c in page_seed) % len(SHOPS)
    return SHOPS[offset:] + SHOPS[:offset]

def render_layout(title: str, description: str, keywords: str, body_content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; background-color: #050505; color: #f3f4f6; }}
        .brand-gradient {{ background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .card-border {{ border: 1px solid rgba(245, 158, 11, 0.2); }}
        .card-border:hover {{ border-color: rgba(245, 158, 11, 0.6); }}
    </style>
</head>
<body class="min-h-screen flex flex-col">
    <header class="sticky top-0 z-50 bg-[#050505]/90 backdrop-blur-xl border-b border-amber-500/20 px-4 py-3 shadow-[0_4px_20px_rgba(245,158,11,0.1)]">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
            <a href="/" class="flex items-center gap-2.5">
                <span class="text-xl font-black tracking-wider brand-gradient">테라피오 (Therapio)</span>
            </a>
            <nav class="hidden md:flex items-center gap-6 text-xs font-bold text-gray-300">
                <a href="/seoul" class="hover:text-amber-400 transition-colors">서울</a>
                <a href="/gyeonggi" class="hover:text-amber-400 transition-colors">경기</a>
                <a href="/incheon" class="hover:text-amber-400 transition-colors">인천</a>
            </nav>
            <a href="tel:0507-1280-3344" class="bg-gradient-to-r from-amber-500 to-yellow-400 text-black font-extrabold text-xs px-3.5 py-2 rounded-xl shadow transition-all active:scale-95">
                📞 빠른 문의
            </a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 w-full flex-1 space-y-12">
        {body_content}
    </main>
    <footer class="bg-[#030303] border-t border-white/10 py-10 text-center text-gray-500 text-xs mt-auto">
        <div class="max-w-4xl mx-auto px-4 space-y-4">
            <div>
                <a href="tel:0507-1280-3344" class="inline-flex items-center gap-1.5 bg-neutral-900 hover:bg-neutral-800 text-amber-400 font-bold px-4 py-2 rounded-xl border border-amber-500/30 text-xs shadow-md">
                    🤝 제휴문의 (0507-1280-3344)
                </a>
            </div>
            <p class="text-gray-400 font-bold">테라피오는 건전하고 안전한 제휴 마사지 정보 플랫폼입니다.</p>
            <p class="text-[11px] text-gray-600">COPYRIGHT © THERAPIO ALL RIGHTS RESERVED.</p>
        </div>
    </footer>
</body>
</html>"""

def render_shop_cards(shops: list, is_chuljang: bool = False, location_text: str = "") -> str:
    cards = []
    for s in shops:
        desc_text = s['desc']
        if is_chuljang and location_text:
            desc_text = f"{location_text} 전지역 25분 내 빠른 신속 출장마사지! 정성 가득 힐링 케어"
        card = f"""
        <div class="bg-[#121214] card-border rounded-2xl p-4 flex gap-4 items-center shadow-md transition-all group">
            <img src="{s['image']}" onerror="this.onerror=null; this.src='{s['fallback_image']}';" alt="{s['name']}" class="w-20 h-20 md:w-24 md:h-24 rounded-xl object-cover border border-white/10 group-hover:scale-105 transition-transform bg-gray-900">
            <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                    <span class="text-[10px] text-amber-400 font-bold bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">{s['badge']}</span>
                    <span class="text-xs text-yellow-400 font-bold">★ {s['rating']} <span class="text-gray-500 text-[10px]">({s['review_count']})</span></span>
                </div>
                <h3 class="font-extrabold text-sm md:text-base text-white truncate group-hover:text-amber-400 transition-colors mt-1">{s['name']}</h3>
                <p class="text-[11px] text-gray-400 mt-0.5 line-clamp-2">{desc_text}</p>
                <div class="mt-2.5 flex items-center justify-between">
                    <span class="text-xs font-black text-amber-400">{s['price']}원부터~</span>
                    <a href="tel:{s['phone']}" class="bg-amber-500 hover:bg-amber-400 text-black font-extrabold text-xs px-3.5 py-1.5 rounded-xl shadow transition-colors">
                        전화연결
                    </a>
                </div>
            </div>
        </div>
        """
        cards.append(card)
    return "".join(cards)

def render_course_info() -> str:
    cards = []
    for c in COURSE_INFO:
        card = f"""
        <div class="bg-[#121214] border border-white/10 p-5 rounded-2xl space-y-1.5">
            <span class="text-[10px] text-amber-400 font-bold bg-amber-500/10 px-2 py-0.5 rounded">{c['tag']}</span>
            <h4 class="font-bold text-white text-sm">{c['name']}</h4>
            <p class="text-xs text-gray-400 leading-relaxed">{c['desc']}</p>
        </div>
        """
        cards.append(card)
    return f"""
    <section class="space-y-4">
        <div class="text-center">
            <span class="text-amber-400 text-xs font-bold tracking-widest uppercase">MASSAGE GUIDE</span>
            <h3 class="text-xl font-black text-white mt-1">💆 테라피 기본 코스 안내</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">{"".join(cards)}</div>
    </section>
    """

def render_qa_section(location_name: str, is_chuljang: bool = False) -> str:
    subject = "출장마사지" if is_chuljang else "방문 테라피"
    qa_list = [
        {"q": f"{location_name} {subject} 방문 시간은 얼마나 걸리나요?", "a": f"{location_name} 전지역 요청 후 평균 20~25분 내 신속하게 방문합니다."},
        {"q": "선입금이나 예약금 사기 위험은 없나요?", "a": "테라피오는 100% 후불제로만 운영됩니다. 선입금을 요구하는 행위는 일체 없습니다."},
        {"q": f"{location_name} 원하시는 장소에서 이용 가능한가요?", "a": "자택, 오피스텔, 호텔, 모텔 등 고객님이 편안하게 계신 장소 어디든 방문 케어가 가능합니다."}
    ]
    cards = []
    for item in qa_list:
        card = f"""
        <div class="bg-black/60 rounded-2xl border border-white/5 p-4 space-y-1">
            <div class="font-bold text-sm text-gray-200 flex items-center gap-2">
                <span class="text-amber-400 font-black">Q.</span> {item['q']}
            </div>
            <div class="text-xs text-gray-400 pl-5 leading-relaxed">{item['a']}</div>
        </div>
        """
        cards.append(card)
    return f"""
    <section class="space-y-4">
        <div class="text-center">
            <span class="text-amber-400 text-xs font-bold tracking-widest uppercase">Q&A GUIDE</span>
            <h3 class="text-xl font-black text-white mt-1">❓ {location_name} {subject} 자주 묻는 질문</h3>
        </div>
        <div class="space-y-3">{"".join(cards)}</div>
    </section>
    """

def render_map_widget(query_name: str) -> str:
    map_url = f"https://map.kakao.com/?q={query_name}+출장마사지"
    return f"""
    <section class="bg-gradient-to-r from-[#18181b] to-[#101012] border border-amber-500/30 p-6 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-4 shadow-lg">
        <div class="space-y-1 text-center sm:text-left">
            <span class="text-xs text-amber-400 font-bold">📍 실시간 위치 및 주변 안내</span>
            <h4 class="text-base font-black text-white">{query_name} 출장마사지 지도 확인</h4>
            <p class="text-xs text-gray-400">카카오맵을 통해 현재 {query_name} 주변 위치 및 교통 현황을 확인하세요.</p>
        </div>
        <a href="{map_url}" target="_blank" rel="noopener noreferrer" class="bg-yellow-400 hover:bg-yellow-300 text-black font-extrabold text-xs px-4 py-2.5 rounded-xl shadow transition-transform active:scale-95 whitespace-nowrap flex items-center gap-1.5">
            🗺️ {query_name} 지도 바로가기
        </a>
    </section>
    """

@app.get("/", response_class=HTMLResponse)
async def index_page():
    region_blocks = []
    for key, reg in REGIONS.items():
        sub_links = "".join([f'<a href="/{key}/{g_key}" class="text-xs bg-[#18181b] hover:bg-amber-500/20 hover:text-amber-300 text-gray-300 px-2.5 py-1.5 rounded-lg border border-white/5 transition-colors">{g["name"]}</a>' for g_key, g in reg["districts"].items()])
        region_blocks.append(f"""
        <div class="bg-[#0d0d0f] border border-amber-500/20 p-5 rounded-2xl">
            <h3 class="text-base font-black text-white"><a href="/{key}" class="hover:text-amber-400">{reg['name']} →</a></h3>
            <p class="text-[11px] text-gray-400 mt-1 mb-3">{reg['description']}</p>
            <div class="flex flex-wrap gap-1.5">{sub_links}</div>
        </div>
        """)
    reviews_html = "".join([f"""
    <div class="bg-[#0f0f12] p-5 rounded-2xl border border-white/5 space-y-2">
        <div class="flex justify-between items-center">
            <span class="text-amber-400 font-black text-sm">★★★★★ {r['rating']} <span class="text-xs text-gray-400 font-normal">| {r['tag']}</span></span>
            <span class="text-[11px] text-gray-500">{r['author']}</span>
        </div>
        <p class="text-xs text-gray-300 leading-relaxed">"{r['content']}"</p>
    </div>
    """ for r in REVIEWS])
    content = f"""
    <!-- 메인 배너: 직접 올린 banner.jpg 우선 표시 -->
    <section class="text-center my-2">
        <div class="overflow-hidden rounded-3xl border border-amber-500/30 p-8 md:p-14 relative text-center space-y-3 shadow-2xl bg-cover bg-center" style="background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.85)), url('/static/images/banner.jpg'), url('https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80');">
            <span class="inline-block px-4 py-1 rounded-full bg-amber-500 text-black font-extrabold text-xs tracking-widest shadow-lg">
                ✨ 100% 후불제 안심 보장 시스템
            </span>
            <h1 class="text-3xl md:text-5xl font-black text-white tracking-tight drop-shadow">
                서울·경기·인천 <span class="brand-gradient">25분 내 신속 방문 케어</span>
            </h1>
            <p class="text-gray-200 text-xs md:text-sm font-medium max-w-lg mx-auto leading-relaxed drop-shadow">
                엄선된 최고급 베테랑 관리사의 프라이빗 피로회복 프로그램! 지금 바로 내 주변 제휴업체를 만나보세요.
            </p>
        </div>
    </section>
    <section class="space-y-6">
        <div class="text-center">
            <p class="text-xs text-amber-400 font-bold tracking-widest uppercase">BEST RECOMMENDED SHOPS</p>
            <h2 class="text-xl md:text-2xl font-black text-white mt-1">🏆 테라피오 최고의 추천 제휴업체 (5곳)</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{render_shop_cards(get_rotated_shops("index"))}</div>
    </section>
    <section class="space-y-4 pt-4 border-t border-white/10">
        <div class="text-center">
            <span class="text-amber-400 text-xs font-bold tracking-widest">REGIONS</span>
            <h3 class="text-xl font-black text-white mt-1">📍 서비스 지역 바로가기</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">{"".join(region_blocks)}</div>
    </section>
    {render_course_info()}
    <section class="space-y-4">
        <div class="text-center">
            <span class="text-amber-400 text-xs font-bold tracking-widest uppercase">REAL REVIEWS</span>
            <h3 class="text-xl font-black text-white mt-1">실제 이용 고객 후기</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{reviews_html}</div>
    </section>
    {render_qa_section("서울·경기·인천", is_chuljang=False)}
    """
    return HTMLResponse(content=render_layout("테라피오 | 서울·경기·인천 24시 방문 홈케어 & 힐링 테라피 안내", "선입금 없는 100% 후불 안심 케어!", "방문 홈케어, 홈타이, 스웨디시, 아로마 마사지", content), media_type="text/html; charset=utf-8")

@app.get("/{sido}", response_class=HTMLResponse)
async def sido_page(sido: str):
    if sido not in REGIONS:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
    reg = REGIONS[sido]
    rotated_shops = get_rotated_shops(sido)
    gugun_links = "".join([f'<a href="/{sido}/{gk}" class="bg-[#121214] hover:bg-amber-500/20 hover:text-amber-300 text-gray-200 text-xs font-bold p-3 rounded-xl border border-white/5 text-center transition-all">{gv["name"]}</a>' for gk, gv in reg["districts"].items()])
    content = f"""
    <div class="space-y-2">
        <div class="text-xs text-gray-400"><a href="/" class="hover:underline">홈</a> &gt; <span class="text-white font-bold">{reg['name']}</span></div>
        <h1 class="text-2xl md:text-3xl font-black text-white">{reg['name']} 24시 출장마사지 & 방문 홈케어</h1>
        <p class="text-xs text-amber-400">{reg['name']} 전지역 25분 신속 배차 · 선입금 없는 100% 안심 후불제 출장마사지</p>
    </div>
    {render_map_widget(reg['name'])}
    <section class="bg-[#0d0d0f] border border-white/10 p-5 rounded-2xl">
        <h2 class="text-xs font-bold text-amber-400 mb-3 uppercase tracking-wider">{reg['name']} 세부 구·시 출장마사지 선택</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5">{gugun_links}</div>
    </section>
    <section class="space-y-4">
        <h2 class="text-lg font-bold text-white">🏆 {reg['name']} 추천 출장마사지 제휴업체 (5곳)</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{render_shop_cards(rotated_shops, is_chuljang=True, location_text=reg['name'])}</div>
    </section>
    {render_course_info()}
    {render_qa_section(reg['name'], is_chuljang=True)}
    """
    return HTMLResponse(content=render_layout(f"{reg['name']} 출장마사지·홈타이 추천 24시 안내 | 테라피오", reg['description'], f"{reg['name']} 출장마사지, {reg['name']} 홈타이", content), media_type="text/html; charset=utf-8")

@app.get("/{sido}/{gugun}", response_class=HTMLResponse)
async def gugun_page(sido: str, gugun: str):
    if sido not in REGIONS or gugun not in REGIONS[sido]["districts"]:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
    sido_name = REGIONS[sido]["name"]
    gugun_info = REGIONS[sido]["districts"][gugun]
    rotated_shops = get_rotated_shops(f"{sido}_{gugun}")
    dong_links = "".join([f'<a href="/{sido}/{gugun}/{dk}" class="bg-[#121214] hover:bg-amber-500/20 hover:text-amber-300 text-gray-200 text-xs font-semibold px-3 py-2 rounded-xl border border-white/5 transition-all">{dn}</a>' for dk, dn in gugun_info["dongs"].items()])
    full_loc_name = f"{sido_name} {gugun_info['name']}"
    content = f"""
    <div class="space-y-2">
        <div class="text-xs text-gray-400"><a href="/" class="hover:underline">홈</a> &gt; <a href="/{sido}" class="hover:underline">{sido_name}</a> &gt; <span class="text-white font-bold">{gugun_info['name']}</span></div>
        <h1 class="text-2xl md:text-3xl font-black text-white">{full_loc_name} 출장마사지 & 홈타이 24시</h1>
        <p class="text-xs text-amber-400">{gugun_info['name']} 전지역 25분 내 실시간 방문 · 100% 안심 후불제 출장마사지</p>
    </div>
    {render_map_widget(full_loc_name)}
    <section class="bg-[#0d0d0f] border border-white/10 p-5 rounded-2xl">
        <h2 class="text-xs font-bold text-amber-400 mb-3 uppercase tracking-wider">{gugun_info['name']} 동별 출장마사지 바로가기</h2>
        <div class="flex flex-wrap gap-2">{dong_links}</div>
    </section>
    <section class="space-y-4">
        <h2 class="text-lg font-bold text-white">🏆 {gugun_info['name']} 추천 출장마사지 제휴업체 (5곳)</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{render_shop_cards(rotated_shops, is_chuljang=True, location_text=gugun_info['name'])}</div>
    </section>
    {render_course_info()}
    {render_qa_section(gugun_info['name'], is_chuljang=True)}
    """
    return HTMLResponse(content=render_layout(f"{full_loc_name} 출장마사지·홈타이 24시 실시간 방문 | 테라피오", f"{gugun_info['name']} 25분 내 빠른 방문", f"{gugun_info['name']} 출장마사지, {full_loc_name} 출장안마", content), media_type="text/html; charset=utf-8")

@app.get("/{sido}/{gugun}/{dong}", response_class=HTMLResponse)
async def dong_page(sido: str, gugun: str, dong: str):
    if (sido not in REGIONS or 
        gugun not in REGIONS[sido]["districts"] or 
        dong not in REGIONS[sido]["districts"][gugun]["dongs"]):
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
    sido_name = REGIONS[sido]["name"]
    gugun_name = REGIONS[sido]["districts"][gugun]["name"]
    dong_name = REGIONS[sido]["districts"][gugun]["dongs"][dong]
    rotated_shops = get_rotated_shops(f"{sido}_{gugun}_{dong}")
    full_dong_name = f"{gugun_name} {dong_name}"
    content = f"""
    <div class="space-y-2">
        <div class="text-xs text-gray-400"><a href="/" class="hover:underline">홈</a> &gt; <a href="/{sido}" class="hover:underline">{sido_name}</a> &gt; <a href="/{sido}/{gugun}" class="hover:underline">{gugun_name}</a> &gt; <span class="text-white font-bold">{dong_name}</span></div>
        <h1 class="text-2xl md:text-3xl font-black text-white">{full_dong_name} 출장마사지 24시 신속 방문</h1>
        <p class="text-xs text-amber-400 font-semibold">{dong_name} 인근 평균 25분 내 도착 보장 · 100% 안심 후불제 출장마사지</p>
    </div>
    {render_map_widget(full_dong_name)}
    <section class="space-y-4">
        <h2 class="text-lg font-bold text-white">🏆 {dong_name} 추천 출장마사지 제휴업체 (5곳)</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{render_shop_cards(rotated_shops, is_chuljang=True, location_text=dong_name)}</div>
    </section>
    {render_course_info()}
    {render_qa_section(dong_name, is_chuljang=True)}
    """
    return HTMLResponse(content=render_layout(f"{full_dong_name} 출장마사지·홈타이 24시 신속방문 | 테라피오", f"{dong_name} 20~25분 내 실시간 방문", f"{dong_name} 출장마사지, {full_dong_name} 출장안마", content), media_type="text/html; charset=utf-8")

if __name__ == "__main__":
    print("Therapio server ready")
    uvicorn.run(app, host="0.0.0.0", port=8001)
