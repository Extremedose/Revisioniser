from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, time, date
from ics import Calendar, Event
from uuid import uuid4

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Full Surah metadata
surah_data = [
    {"number": 1, "name": "Al-Fatihah", "pages": 1},
    {"number": 2, "name": "Al-Baqarah", "pages": 48},
    {"number": 3, "name": "Ali 'Imran", "pages": 25},
    {"number": 4, "name": "An-Nisa'", "pages": 36},
    {"number": 5, "name": "Al-Ma'idah", "pages": 30},
    {"number": 6, "name": "Al-An'am", "pages": 20},
    {"number": 7, "name": "Al-A'raf", "pages": 24},
    {"number": 8, "name": "Al-Anfal", "pages": 10},
    {"number": 9, "name": "At-Tawbah", "pages": 16},
    {"number": 10, "name": "Yunus", "pages": 11},
    {"number": 11, "name": "Hud", "pages": 10},
    {"number": 12, "name": "Yusuf", "pages": 12},
    {"number": 13, "name": "Ar-Ra'd", "pages": 6},
    {"number": 14, "name": "Ibrahim", "pages": 7},
    {"number": 15, "name": "Al-Hijr", "pages": 6},
    {"number": 16, "name": "An-Nahl", "pages": 12},
    {"number": 17, "name": "Al-Isra'", "pages": 12},
    {"number": 18, "name": "Al-Kahf", "pages": 11},
    {"number": 19, "name": "Maryam", "pages": 6},
    {"number": 20, "name": "Ta-Ha", "pages": 8},
    {"number": 21, "name": "Al-Anbiya'", "pages": 10},
    {"number": 22, "name": "Al-Hajj", "pages": 10},
    {"number": 23, "name": "Al-Mu'minun", "pages": 9},
    {"number": 24, "name": "An-Nur", "pages": 8},
    {"number": 25, "name": "Al-Furqan", "pages": 9},
    {"number": 26, "name": "Ash-Shu'ara'", "pages": 11},
    {"number": 27, "name": "An-Naml", "pages": 7},
    {"number": 28, "name": "Al-Qasas", "pages": 9},
    {"number": 29, "name": "Al-Ankabut", "pages": 7},
    {"number": 30, "name": "Ar-Rum", "pages": 6},
    {"number": 31, "name": "Luqman", "pages": 4},
    {"number": 32, "name": "As-Sajda", "pages": 3},
    {"number": 33, "name": "Al-Ahzab", "pages": 9},
    {"number": 34, "name": "Saba'", "pages": 5},
    {"number": 35, "name": "Fatir", "pages": 5},
    {"number": 36, "name": "Ya-Sin", "pages": 5},
    {"number": 37, "name": "As-Saffat", "pages": 5},
    {"number": 38, "name": "Sad", "pages": 5},
    {"number": 39, "name": "Az-Zumar", "pages": 6},
    {"number": 40, "name": "Ghafir", "pages": 5},
    {"number": 41, "name": "Fussilat", "pages": 5},
    {"number": 42, "name": "Ash-Shura", "pages": 4},
    {"number": 43, "name": "Az-Zukhruf", "pages": 4},
    {"number": 44, "name": "Ad-Dukhan", "pages": 3},
    {"number": 45, "name": "Al-Jathiya", "pages": 3},
    {"number": 46, "name": "Al-Ahqaf", "pages": 3},
    {"number": 47, "name": "Muhammad", "pages": 3},
    {"number": 48, "name": "Al-Fath", "pages": 3},
    {"number": 49, "name": "Al-Hujurat", "pages": 2},
    {"number": 50, "name": "Qaf", "pages": 3},
    {"number": 51, "name": "Adh-Dhariyat", "pages": 3},
    {"number": 52, "name": "At-Tur", "pages": 3},
    {"number": 53, "name": "An-Najm", "pages": 3},
    {"number": 54, "name": "Al-Qamar", "pages": 3},
    {"number": 55, "name": "Ar-Rahman", "pages": 3},
    {"number": 56, "name": "Al-Waqia", "pages": 3},
    {"number": 57, "name": "Al-Hadid", "pages": 3},
    {"number": 58, "name": "Al-Mujadila", "pages": 3},
    {"number": 59, "name": "Al-Hashr", "pages": 3},
    {"number": 60, "name": "Al-Mumtahina", "pages": 2},
    {"number": 61, "name": "As-Saff", "pages": 2},
    {"number": 62, "name": "Al-Jumuʿa", "pages": 2},
    {"number": 63, "name": "Al-Munafiqun", "pages": 2},
    {"number": 64, "name": "At-Taghabun", "pages": 2},
    {"number": 65, "name": "At-Talaq", "pages": 2},
    {"number": 66, "name": "At-Tahrim", "pages": 2},
    {"number": 67, "name": "Al-Mulk", "pages": 2},
    {"number": 68, "name": "Al-Qalam", "pages": 2},
    {"number": 69, "name": "Al-Haqqa", "pages": 2},
    {"number": 70, "name": "Al-Ma'arij", "pages": 2},
    {"number": 71, "name": "Nuh", "pages": 2},
    {"number": 72, "name": "Al-Jinn", "pages": 2},
    {"number": 73, "name": "Al-Muzzammil", "pages": 2},
    {"number": 74, "name": "Al-Muddathir", "pages": 2},
    {"number": 75, "name": "Al-Qiyama", "pages": 2},
    {"number": 76, "name": "Al-Insan", "pages": 2},
    {"number": 77, "name": "Al-Mursalat", "pages": 2},
    {"number": 78, "name": "An-Naba'", "pages": 2},
    {"number": 79, "name": "An-Nazi'at", "pages": 2},
    {"number": 80, "name": "Abasa", "pages": 2},
    {"number": 81, "name": "At-Takwir", "pages": 2},
    {"number": 82, "name": "Al-Infitar", "pages": 2},
    {"number": 83, "name": "Al-Mutaffifin", "pages": 2},
    {"number": 84, "name": "Al-Inshiqaq", "pages": 2},
    {"number": 85, "name": "Al-Buruj", "pages": 2},
    {"number": 86, "name": "At-Tariq", "pages": 2},
    {"number": 87, "name": "Al-A'la", "pages": 2},
    {"number": 88, "name": "Al-Ghashiya", "pages": 2},
    {"number": 89, "name": "Al-Fajr", "pages": 2},
    {"number": 90, "name": "Al-Balad", "pages": 2},
    {"number": 91, "name": "Ash-Shams", "pages": 2},
    {"number": 92, "name": "Al-Lail", "pages": 2},
    {"number": 93, "name": "Ad-Duha", "pages": 2},
    {"number": 94, "name": "Ash-Sharh", "pages": 2},
    {"number": 95, "name": "At-Tin", "pages": 2},
    {"number": 96, "name": "Al-Alaq", "pages": 2},
    {"number": 97, "name": "Al-Qadr", "pages": 1},
    {"number": 98, "name": "Al-Bayyina", "pages": 2},
    {"number": 99, "name": "Az-Zalzala", "pages": 1},
    {"number": 100, "name": "Al-Adiyat", "pages": 1},
    {"number": 101, "name": "Al-Qaria", "pages": 1},
    {"number": 102, "name": "At-Takathur", "pages": 1},
    {"number": 103, "name": "Al-Asr", "pages": 1},
    {"number": 104, "name": "Al-Humaza", "pages": 1},
    {"number": 105, "name": "Al-Fil", "pages": 1},
    {"number": 106, "name": "Quraysh", "pages": 1},
    {"number": 107, "name": "Al-Ma'un", "pages": 1},
    {"number": 108, "name": "Al-Kawthar", "pages": 1},
    {"number": 109, "name": "Al-Kafirun", "pages": 1},
    {"number": 110, "name": "An-Nasr", "pages": 1},
    {"number": 111, "name": "Al-Masad", "pages": 1},
    {"number": 112, "name": "Al-Ikhlas", "pages": 1},
    {"number": 113, "name": "Al-Falaq", "pages": 1},
    {"number": 114, "name": "An-Nas", "pages": 1},
]

# User data
user_data = {
    "memorised": [],
    "max_pages_per_day": 6,
    "revision_pointer": {"surah_index": 0, "page_offset": 0}
}

def daily_plan(start_index=None, page_offset=None):
    memorised = user_data["memorised"]
    if not memorised:
        return []

    plan = []
    pages_used = 0
    max_pages = user_data["max_pages_per_day"]
    surah_index = start_index if start_index is not None else user_data["revision_pointer"]["surah_index"]
    page_offset = page_offset if page_offset is not None else user_data["revision_pointer"]["page_offset"]

    while pages_used < max_pages:
        surah_num = memorised[surah_index % len(memorised)]
        s = next((x for x in surah_data if x["number"] == surah_num), None)
        if not s:
            surah_index += 1
            page_offset = 0
            continue

        pages_remaining = s["pages"] - page_offset
        pages_to_take = min(max_pages - pages_used, pages_remaining)
        if pages_to_take <= 0:
            surah_index += 1
            page_offset = 0
            continue

        plan.append({
            "number": s["number"],
            "name": s["name"],
            "pages": pages_to_take,
            "start_page": page_offset + 1
        })

        pages_used += pages_to_take
        page_offset += pages_to_take
        if page_offset >= s["pages"]:
            surah_index += 1
            page_offset = 0

        if pages_used >= max_pages:
            break

    user_data["revision_pointer"]["surah_index"] = surah_index % len(memorised)
    user_data["revision_pointer"]["page_offset"] = page_offset

    return plan

@app.get("/revision.ics")
def revision_ics(ts: int = 0):
    cal = Calendar()
    today = datetime.utcnow().date()
    temp_pointer = dict(user_data["revision_pointer"])

    for day_offset in range(30):
        day = today + timedelta(days=day_offset)
        plan = daily_plan(temp_pointer["surah_index"], temp_pointer["page_offset"])
        if not plan:
            continue

        # Advance temp pointer
        temp_pointer["surah_index"] = user_data["revision_pointer"]["surah_index"]
        temp_pointer["page_offset"] = user_data["revision_pointer"]["page_offset"]

        title_parts = []
        description_parts = []
        for p in plan:
            if 1 < p["pages"] < 7:
                title_parts.append(f"{p['name']} (pages {p['start_page']}-{p['start_page'] + p['pages'] - 1})")
                description_parts.append(f"{p['name']} - pages {p['start_page']}-{p['start_page'] + p['pages'] - 1}")
            else:
                title_parts.append(f"{p['name']}")
                description_parts.append(f"{p['name']}")

        event = Event(
            name="Quran Revision: " + ", ".join(title_parts),
            description="\n".join(description_parts),
        )
        # All-day event by using date objects
        event.begin = day
        event.end = day + timedelta(days=1)
        event.uid = f"{uuid4()}@quran-revision"
        cal.events.add(event)

    return Response(content=str(cal), media_type="text/calendar",
                    headers={"Content-Disposition": f"attachment; filename=revision_{ts}.ics"})

@app.get("/add_surah/{num}")
@app.post("/add_surah/{num}")
def add_surah(num: int):
    if num not in user_data["memorised"]:
        user_data["memorised"].append(num)
    return {"memorised": user_data["memorised"]}

@app.get("/remove_surah/{num}")
@app.post("/remove_surah/{num}")
def remove_surah(num: int):
    if num in user_data["memorised"]:
        user_data["memorised"].remove(num)
        if user_data["memorised"]:
            user_data["revision_pointer"]["surah_index"] %= len(user_data["memorised"])
            user_data["revision_pointer"]["page_offset"] = 0
        else:
            user_data["revision_pointer"] = {"surah_index": 0, "page_offset": 0}
    return {"memorised": user_data["memorised"]}

@app.get("/status")
def status():
    memorised_list = [s for s in surah_data if s["number"] in user_data["memorised"]]
    return {"memorised": memorised_list}

@app.get("/ui")
def ui():
    html = """
    <html>
    <head><title>Quran Revision</title></head>
    <body>
    <h2>Quran Revision Manager</h2>
    <input type="text" id="search" placeholder="Search surah..." onkeyup="filterSurahs()">
    <ul id="surahList">
    """
    for s in surah_data:
        cls = "memorised" if s["number"] in user_data["memorised"] else ""
        html += f"""
        <li class="{cls}" data-name="{s['name'].lower()}" data-number="{s['number']}">
            {s['number']}. {s['name']}
            <button onclick="addSurah({s['number']})">Add</button>
            <button onclick="removeSurah({s['number']})">Remove</button>
        </li>
        """
    html += """
    </ul>
    <h3>Today's Revision:</h3>
    <ul id="todayPlan"></ul>
    <br><a id="calendarLink" href="/revision.ics?ts=0" target="_blank">Download Calendar</a>

    <script>
    function filterSurahs() {
        var input = document.getElementById('search').value.toLowerCase();
        var li = document.getElementById('surahList').getElementsByTagName('li');
        for (var i=0; i<li.length; i++) {
            var name = li[i].getAttribute('data-name');
            var number = li[i].getAttribute('data-number');
            li[i].style.display = (name.includes(input) || number.includes(input)) ? "" : "none";
        }
    }

    async function updateTodayPlan() {
        const res = await fetch('/status');
        const data = await res.json();
        const todayList = document.getElementById('todayPlan');
        todayList.innerHTML = '';
        data.memorised.forEach(s => {
            const li = document.createElement('li');
            li.textContent = s.number + '. ' + s.name + ' (' + s.pages + ' pages)';
            todayList.appendChild(li);
        });
    }

    async function addSurah(num) {
        await fetch('/add_surah/' + num);
        updateTodayPlan();
    }

    async function removeSurah(num) {
        await fetch('/remove_surah/' + num);
        updateTodayPlan();
    }

    updateTodayPlan();
    </script>
    </body>
    </html>
    """
    return Response(content=html, media_type="text/html")
