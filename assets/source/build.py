"""Erzeugt Banner und Schaubild für lawful-good als SVG.

  python build.py <ausgabe> <font-ordner> <logo-ordner>
  EMBED_FONTS=0 python build.py ...   # SVG ohne eingebettete Schrift (Satoshi muss installiert sein)
  node render.js <svg-ordner> <png-ordner>   # PNG in 2x (Social Preview 1x), braucht Playwright

Schrift: Satoshi 500/700/900 von fontshare.com (satoshi-<gewicht>.woff2).
Logos: DECAID_Logo_weiß.svg und DECAID_Logo_schwarz.svg aus dem DECAID-Brand-Ordner.
Texte stehen in TXT, Farben (CI V3, Theme D) in THEME.
"""
import base64, math, sys
from pathlib import Path

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
FONTS = Path(sys.argv[2]); LOGOS = Path(sys.argv[3])

def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
import os
FONTCSS = "" if os.environ.get("EMBED_FONTS") == "0" else "".join(
    f"@font-face{{font-family:'Satoshi';font-weight:{w};font-style:normal;"
    f"src:url(data:font/woff2;base64,{b64(FONTS/f'satoshi-{w}.woff2')}) format('woff2');}}"
    for w in (500, 700, 900))
LOGO = {"weiss": b64(LOGOS/"DECAID_Logo_weiß.svg"), "schwarz": b64(LOGOS/"DECAID_Logo_schwarz.svg")}
# Wortbildmarke: viewBox 5000 x 1250 (4:1)

def head(w, h, title):
    return (f'<!-- decaid-profil: web -->\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n<style>{FONTCSS}text{{font-family:Satoshi,sans-serif;}}</style>\n')

def logo(x, y, h, variant):
    return (f'<image x="{x}" y="{y}" height="{h}" width="{h*4}" '
            f'href="data:image/svg+xml;base64,{LOGO[variant]}" xlink:href="data:image/svg+xml;base64,{LOGO[variant]}"/>\n')

def d20(cx, cy, r, uid):
    """Ikosaeder in Frontansicht als Milchglas-Schichten: Sechseck, mittleres Dreieck, Kanten."""
    hexa = [(cx + r*math.cos(math.radians(90 + 60*i)), cy - r*math.sin(math.radians(90 + 60*i))) for i in range(6)]
    tri = [(cx + 0.58*r*math.cos(math.radians(90 + 120*i)), cy - 0.58*r*math.sin(math.radians(90 + 120*i))) for i in range(3)]
    P = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s = [f'<defs><radialGradient id="glow{uid}" cx="50%" cy="50%" r="50%">'
         f'<stop offset="0" stop-color="#2a81bb" stop-opacity=".55"/>'
         f'<stop offset=".55" stop-color="#ecb4d8" stop-opacity=".18"/>'
         f'<stop offset="1" stop-color="#ecb4d8" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="fc{uid}" x1="0" y1="0" x2="1" y2="1">'
         f'<stop offset="0" stop-color="#ffffff" stop-opacity=".16"/>'
         f'<stop offset="1" stop-color="#ffffff" stop-opacity=".03"/></linearGradient></defs>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*1.55:.0f}" fill="url(#glow{uid})"/>',
         f'<polygon points="{P(hexa)}" fill="url(#fc{uid})" stroke="#ffffff" stroke-opacity=".35" stroke-width="1.5"/>']
    # Außenfacetten: jede Dreieckskante mit dem gegenüberliegenden Sechseckpunkt, Ecken mit Nachbarn
    faces = []
    for i in range(3):
        a, b = tri[i], tri[(i+1) % 3]
        faces.append([a, b, hexa[(2*i+1) % 6]])          # Facette zwischen zwei Dreiecksecken
        faces.append([a, hexa[(2*i) % 6], hexa[(2*i+1) % 6]])
        faces.append([b, hexa[(2*i+1) % 6], hexa[(2*i+2) % 6]])
    for k, f in enumerate(faces):
        op = (.05, .10, .03)[k % 3]
        s.append(f'<polygon points="{P(f)}" fill="#ffffff" fill-opacity="{op}" stroke="#ffffff" stroke-opacity=".28" stroke-width="1.2"/>')
    s.append(f'<polygon points="{P(tri)}" fill="#2a81bb" fill-opacity=".30" stroke="#ffffff" stroke-opacity=".55" stroke-width="1.5"/>')
    return "\n".join(s) + "\n"

def banner(w, h, name, flat):
    s = [head(w, h, "lawful-good: Open, machine-readable AI governance by DECAID"),
         f'<rect width="{w}" height="{h}" fill="#020203"/>\n']
    if flat:
        s.append(d20(w - 250, h/2, 118, name))
        s.append(logo(64, 52, 30, "weiss"))
        s.append(f'<text x="62" y="186" font-weight="900" font-size="96" letter-spacing="-3.8" fill="#ffffff">lawful-good</text>\n')
        s.append(f'<text x="64" y="236" font-weight="500" font-size="27" fill="#f0efe8">Open, machine-readable AI governance.</text>\n')
        s.append(f'<text x="64" y="272" font-weight="500" font-size="27" fill="#999999">Governance mit KI, nicht nur für KI.</text>\n')
    else:
        s.append(d20(w - 300, h/2 + 10, 190, name))
        s.append(logo(80, 80, 44, "weiss"))
        s.append(f'<text x="76" y="352" font-weight="900" font-size="132" letter-spacing="-5.3" fill="#ffffff">lawful-good</text>\n')
        s.append(f'<text x="80" y="418" font-weight="500" font-size="34" fill="#f0efe8">Open, machine-readable AI governance.</text>\n')
        s.append(f'<text x="80" y="462" font-weight="500" font-size="34" fill="#999999">Governance mit KI, nicht nur für KI.</text>\n')
        s.append(f'<text x="80" y="566" font-weight="500" font-size="22" fill="#999999">Open source · Code MIT · Inhalte CC BY 4.0 · github.com/decaid-studio/lawful-good</text>\n')
    s.append('</svg>\n')
    (OUT/f"{name}.svg").write_text("".join(s), "utf-8")

# ---------------- Schaubild ----------------
TXT = {
 "de": dict(
   title="So läuft ein Use Case durch lawful-good",
   steps=[("Use Case", ["kommt rein: Zweck,", "Nutzer, System"]),
          ("Vorprüfung", ["Entscheidungsbaum", "zum EU AI Act"]),
          ("Prüfkatalog", ["Gates G0 bis G5 mit", "Nachweisen"]),
          ("Mensch|entscheidet", ["Freigabe, Auflagen", "oder Nachbesserung"]),
          ("Trigger", ["halten den Fall", "aktuell"])],
   stop_t="Stopp",
   stop=["Verbotsverdacht, Hochrisiko", "oder unklar: rechtliche Prüfung,", "dann entscheidet ein Mensch."],
   loop="Änderung an Zweck, Modell oder Nutzern: erneut prüfen",
   base_label="Das Fundament",
   base=[("Richtlinie", "Wozu wir uns verpflichten", "Vorlage, jede Regel verknüpft"),
         ("Agentic Framework", "Wie Agenten es umsetzen", "8 Level · 7 Kontrollen · 6 Praktiken"),
         ("Prüfkatalog", "Ob es wirkt", "36 Prüfpunkte in 6 Gates")],
   legend="Hier entscheidet ein Mensch",
   motto="Automatisieren bis zur Abwägung, dann entscheidet ein Mensch.",
   foot="Orientierung, keine Rechtsberatung · lawful-good by DECAID, CC BY 4.0"),
 "en": dict(
   title="How a use case runs through lawful-good",
   steps=[("Use case", ["comes in: purpose,", "users, system"]),
          ("Triage", ["decision tree for", "the EU AI Act"]),
          ("Assessment", ["gates G0 to G5", "with evidence"]),
          ("A person|decides", ["approval, conditions", "or rework"]),
          ("Triggers", ["keep the case", "up to date"])],
   stop_t="Stop",
   stop=["Possibly prohibited, high-risk", "or unclear: legal review,", "then a person decides."],
   loop="Change of purpose, model or users: assess again",
   base_label="The foundation",
   base=[("Policy", "What we commit to", "Template, every rule linked"),
         ("Agentic Framework", "How agents enforce it", "8 levels · 7 controls · 6 practices"),
         ("Assessment catalog", "Whether it works", "36 check items in 6 gates")],
   legend="A person decides here",
   motto="Automate up to the judgement call, then a human decides.",
   foot="Orientation, not legal advice · lawful-good by DECAID, CC BY 4.0"),
}
THEME = {
 "light": dict(bg="#ffffff", card="#f7f5fa", line="#0d0d0d", text="#121212", sub="#3a3a3a", mute="#6b6b6b",
               accent="#1d6091", accent_fill="#2a81bb", on_accent="#ffffff", stop="#ff3b30", stop_bg="#ffffff",
               base="#ede8f4", logo="schwarz", line_op=".14"),
 "dark":  dict(bg="#020203", card="#1d1d1f", line="#ffffff", text="#ffffff", sub="#f0efe8", mute="#999999",
               accent="#2a81bb", accent_fill="#2a81bb", on_accent="#ffffff", stop="#ff3b30", stop_bg="#1d1d1f",
               base="#2d2d2f", logo="weiss", line_op=".18"),
}

def person(x, y, c, scale=1.0):
    r = 7*scale
    return (f'<g fill="{c}"><circle cx="{x}" cy="{y - 6*scale:.1f}" r="{r:.1f}"/>'
            f'<path d="M{x-13*scale:.1f},{y+15*scale:.1f} a{13*scale:.1f},{12*scale:.1f} 0 0 1 {26*scale:.1f},0 z"/></g>')

def diagram(lang, theme):
    T, C = TXT[lang], THEME[theme]
    W, H = 1600, 1000
    s = [head(W, H, T["title"]), f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>\n',
         f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{C["mute"]}"/></marker>'
         f'<marker id="arS" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{C["stop"]}"/></marker></defs>\n']
    s.append(f'<text x="80" y="104" font-weight="700" font-size="40" letter-spacing="-1" fill="{C["text"]}">{T["title"]}</text>\n')
    s.append(logo(W - 80 - 128, 76, 32, C["logo"]))
    # Legende
    s.append(person(92, 152, C["accent_fill"], .8))
    s.append(f'<text x="112" y="158" font-weight="500" font-size="19" fill="{C["mute"]}">{T["legend"]}</text>\n')

    cw, gap, top, ch = 248, 50, 270, 236
    xs = [80 + i*(cw + gap) for i in range(5)]
    for i, (t, lines) in enumerate(T["steps"]):
        x = xs[i]; human = (i == 3)
        fill = C["accent_fill"] if human else C["card"]
        tc = C["on_accent"] if human else C["text"]; sc = C["on_accent"] if human else C["sub"]
        s.append(f'<rect x="{x}" y="{top}" width="{cw}" height="{ch}" rx="18" fill="{fill}"'
                 + ('' if human else f' stroke="{C["line"]}" stroke-opacity="{C["line_op"]}"') + '/>\n')
        num_c = C["on_accent"] if human else C["accent"]
        s.append(f'<text x="{x+24}" y="{top+46}" font-weight="700" font-size="20" fill="{num_c}" fill-opacity="{".8" if human else "1"}">{i+1}</text>\n')
        if human: s.append(person(x + cw - 34, top + 38, C["on_accent"], 1.0))
        tl = t.split("|")
        for k, part in enumerate(tl):
            s.append(f'<text x="{x+24}" y="{top+96+k*32}" font-weight="700" font-size="27" letter-spacing="-.4" fill="{tc}">{part}</text>\n')
        dy = top + 96 + (len(tl)-1)*32 + 40
        for k, l in enumerate(lines):
            s.append(f'<text x="{x+24}" y="{dy+k*28}" font-weight="500" font-size="20" fill="{sc}">{l}</text>\n')
        if i < 4:
            s.append(f'<line x1="{x+cw+8}" y1="{top+ch/2}" x2="{x+cw+gap-8}" y2="{top+ch/2}" stroke="{C["mute"]}" stroke-width="2.5" marker-end="url(#ar)"/>\n')
    # Rückkopplung Trigger -> Prüfkatalog (oben)
    x3, x5 = xs[2] + cw/2, xs[4] + cw/2
    s.append(f'<path d="M{x5},{top-8} C{x5},{top-70} {x3},{top-70} {x3},{top-12}" fill="none" stroke="{C["mute"]}" '
             f'stroke-width="2.5" stroke-dasharray="7 7" marker-end="url(#ar)"/>\n')
    s.append(f'<text x="{(x3+x5)/2}" y="{top-66}" text-anchor="middle" font-weight="500" font-size="18" fill="{C["mute"]}">{T["loop"]}</text>\n')
    # Stopp-Zweig unter der Vorprüfung
    x2 = xs[1]; sy = top + ch + 70
    s.append(f'<line x1="{x2+cw/2}" y1="{top+ch+8}" x2="{x2+cw/2}" y2="{sy-8}" stroke="{C["stop"]}" stroke-width="2.5" marker-end="url(#arS)"/>\n')
    sw = 420; sx = x2 + cw/2 - 60
    s.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="150" rx="18" fill="{C["stop_bg"]}" stroke="{C["stop"]}" stroke-width="2"/>\n')
    s.append(f'<text x="{sx+24}" y="{sy+44}" font-weight="700" font-size="24" fill="{C["stop"]}">{T["stop_t"]}</text>\n')
    s.append(person(sx + sw - 34, sy + 36, C["accent_fill"], 1.0))
    for k, l in enumerate(T["stop"]):
        s.append(f'<text x="{sx+24}" y="{sy+80+k*26}" font-weight="500" font-size="19" fill="{C["sub"]}">{l}</text>\n')
    # Leitsatz rechts neben dem Stopp
    s.append(f'<text x="{xs[3]}" y="{sy+70}" font-weight="700" font-size="24" letter-spacing="-.3" fill="{C["accent"]}">'
             + T["motto"].split(", ")[0] + ',</text>\n')
    s.append(f'<text x="{xs[3]}" y="{sy+102}" font-weight="700" font-size="24" letter-spacing="-.3" fill="{C["accent"]}">'
             + T["motto"].split(", ")[1] + '</text>\n')
    # Fundament
    by = 790
    s.append(f'<text x="80" y="{by-22}" font-weight="700" font-size="18" letter-spacing="1.6" fill="{C["mute"]}">{T["base_label"].upper()}</text>\n')
    bw = (1440 - 2*24)/3
    for i, (t, q, d) in enumerate(T["base"]):
        x = 80 + i*(bw + 24)
        s.append(f'<rect x="{x}" y="{by}" width="{bw}" height="128" rx="18" fill="{C["base"]}"/>\n')
        s.append(f'<text x="{x+24}" y="{by+44}" font-weight="700" font-size="25" fill="{C["text"]}">{t}</text>\n')
        s.append(f'<text x="{x+24}" y="{by+76}" font-weight="500" font-size="20" fill="{C["accent"]}">{q}</text>\n')
        s.append(f'<text x="{x+24}" y="{by+106}" font-weight="500" font-size="18" fill="{C["mute"]}">{d}</text>\n')
    s.append(f'<text x="80" y="{H-30}" font-weight="500" font-size="16" fill="{C["mute"]}">{T["foot"]}</text>\n')
    s.append('</svg>\n')
    (OUT/f"schaubild-{lang}-{theme}.svg").write_text("".join(s), "utf-8")

# Banner: see banner/ (Prismatic renders). The vector banner functions above are kept for reference.
for lang in ("de", "en"):
    for th in ("light", "dark"):
        diagram(lang, th)
print("ok")
