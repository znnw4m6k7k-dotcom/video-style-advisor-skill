"""Build a compact style + audio index from a lemo-opuscar checkout.
usage: python3 -I build_index.py <lemo-opuscar dir> <out.json>"""
import json, re, sys, pathlib

lib, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

def section(md, num):
    m = re.search(rf"^## {num}\. .*?$(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip() if m else ""

def bullets(text):
    return [b.strip() for b in re.split(r"^- ", text, flags=re.M) if b.strip()]

def plain(s):
    return re.sub(r"[*`_]", "", re.sub(r"\s+", " ", s)).strip()

def clip(s, n):
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"

styles = []
for d in sorted((lib / "styles").iterdir()):
    sj, sm = d / "style.json", d / "STYLE.md"
    if d.name.startswith("_") or not sj.exists() or not sm.exists():
        continue
    meta, md = json.loads(sj.read_text()), sm.read_text()
    if meta.get("slug") != d.name:
        continue
    essence = plain(next((l[1:] for l in md.splitlines() if l.startswith(">")), ""))
    essence = clip(essence.split(" References")[0], 220)
    sound = bullets(section(md, 7))
    rest = [b for b in sound if not re.match(r"(\*\*)?(mix|voice|silence|foley)", b, re.I)]
    music = (next((b for b in rest if re.match(r"\*\*[^*]*(music|instrument|score|timbre|electronic|acoustic)", b, re.I)), None)
             or (rest[0] if rest else ""))
    fits = re.findall(r"Fits content like:\*?\s*(.*?)(?:\.|$)", section(md, 8), re.M)
    styles.append({
        "slug": d.name, "cn": meta["cn"], "en": meta["en"],
        "category": meta.get("category_cn", ""),
        "uses": meta.get("uses", []),
        "look": essence,
        "music": clip(plain(music), 260),
        "fits": [plain(f) for f in fits][:4],
    })

out.write_text(json.dumps({"source": "github.com/lemomo-ai/lemo-opuscar", "styles": styles}, ensure_ascii=False, indent=1))
print(len(styles), "styles ->", out)
