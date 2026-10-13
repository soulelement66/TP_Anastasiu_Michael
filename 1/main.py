import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    if path.startswith("/"):
        path = path[1:]
        return "https://" + host + "/" + path
    else:
        return "https://" + host + "/" + path

    """Returnează o adresă completă, de exemplu https://example.com/login."""
print(build_url("example.com", "/login"))  # Returneaza "https://example.com/login"
print(build_url("example.com", "login"))   # Returneaza "https://example.com/login"

def is_https(url):
    if url.startswith("https://"):
        return True
    else:
        return False
    """Returnează True dacă adresa începe cu https://, altfel False."""
print(is_https("https://example.com"))  # Returneaza True
print(is_https("http://example.com"))   # Returneaza False



def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url, timeout=1)
    print(f"Status:" , r.status_code)
    print(f"Content-Type:" , r.headers.get("Content-Type"))

print(show_response("https://example.com")) 

def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""

    try:
        r = requests.get(url, timeout=5)
        return {"status": r.status_code,
                "content_type": r.headers.get("Content-Type"),
                "length": len(r.content),
                "server": r.headers.get("Server")}
    except:
        return {"status": None, "error": "nu raspunde"}

for url in SITES:
    print(url, " ---------- ", check_site(url))

def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []

    for url in SITES:
        rezultate.append((url, check_site(url)))

    merg = []
    for url, r in rezultate:
        if r.get("status") == 200:
            merg.append((url, r))

    merg.sort(key=lambda x: x[1]["length"], reverse=True)


    for url, r in merg:
        print(url, "---", r["status"], ",", r["length"], "octeti")

    print("Reusite:", len(merg), "| Esuate:", len(rezultate) - len(merg))
scan_sites()


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
    except:
        return {"status": None, "error": "nu raspunde"}

    chei = []
    for k in r.headers.keys():
        chei.append(k.lower())

    present = []
    missing = []

    for h in SECURITY_HEADERS:
        if h.lower() in chei:
            present.append(h)
        else:
            missing.append(h)

    score = int(len(present) / len(SECURITY_HEADERS) * 100)

    return {
        "present": present,
        "missing": missing,
        "score": score,
    }

print(check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY"))
print(check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print(check_headers("https://example.com"))
print(check_headers("http://this-site-does-not-exist.invalid"))
