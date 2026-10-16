# Willow Consulting Group — Biographies (Web Page Format)

BUS 202 · Group Project Part 1, Deliverable 2. A scroll-driven 3D web page introducing Willow Consulting Group and its four members, prepared in response to the Old Strathcona Business Association RFP, *The Future of Whyte Ave*.

## Open it

Double-click `index.html` — it is one self-contained file (fonts embedded, no external requests, no libraries). Scroll, click the portal window, or use **Menu** to jump between sections. **Read full biography** opens each member's complete bio.

## Edit content

All text lives in the `STATES` array and `COMPANY_FULL` near the top of the `<script>` in `index.html`. Member bios are the members' own words; the company biography is a draft and should match the Document-format deliverable.

## Photos

Source photos live in `photos/` (full photo, 4:5 portrait crop and square avatar per member, plus `team.jpg`). They are embedded into `index.html` so the page stays one self-contained file. After replacing a photo, run:

```
python tools/embed_photos.py
```

Each member's portrait is the hero of their section, rendered as a floating 3D photo card (pointer tilt, gloss, shadow, flies through the portal), with their emblem spinning live in the panel slot beside it. The group photo is the hero of the Willow section and tops the company biography, captioned left to right. Without WebGL the photos fall back to plain images in the panel.

## Export the submission PDF

```
pip install playwright pillow && python -m playwright install chromium
python tools/export_pdf.py "Group 07"
```

Writes `Group 07_Biographies_2WEBPAGE.pdf` with one 1440×900 frame per section.

## How it works

- Raw WebGL renders the member photos as 3D cards plus five procedurally modelled emblems (willow, globe, book, microphone, film reel) with soft clay lighting, rim light and drifting particles.
- One gesture = one section: a wheel spin, trackpad swipe (inertia included), touch swipe or arrow/space key steps exactly one section, however hard or long. Each step eases to a tilting rounded "portal" window (stencil-masked, pointer-tilted) onto the next section, holds briefly, then dives through it to full screen.
- Willow strands, book pages and film strip sway harder as you scroll faster.
- Falls back to plain gradients without WebGL; respects reduced-motion; adapts render resolution if frames run slow.

Fonts: League Gothic and Inter (SIL Open Font License, see `fonts/`).

**Privacy:** this repo contains group members' biographies — keep it private unless everyone agrees to publish.
