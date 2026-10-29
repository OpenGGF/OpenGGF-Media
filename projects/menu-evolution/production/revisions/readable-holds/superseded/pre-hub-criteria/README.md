# Superseded draft: readable-holds before the hub criteria follow-up (pre-hub-criteria)

The first render of the readable-holds cut (2026-10-29, Claude Opus 5.5), kept as an external record. It is
superseded by `../../final/` because its last criteria row showed the finish-pass A1 Hub row at `d823ce643`
(spacing and icons 8.5, line "9 OVERALL. SPACING AND ICONS STILL 8.5.") and its delivered wall used the
`d823ce643` moving hub take. The user then asked for those criteria to be earned, the engine follow-up
(`ca3d04a1d`, `55d9fec81`; audit at `56c9aed13`) raised A1 spacing and icons to 9, and the final cut shows that
row and the follow-up's hub still. Everything before the criteria row (frame 2826) is pixel-identical between
the two renders and the audio is bit-identical.

| File (renamed on supersession) | Original name | Bytes | SHA-256 |
|---|---|---|---|
| `final/menu-evolution-readable-holds-pre-hub-criteria.mp4` | `final/menu-evolution-readable-holds.mp4` | 18892757 | `f298adff92c8842e3be6eedd9f96d21c1ce33bfef514bd833718523e0f4d0965` |
| `final/menu-evolution-readable-holds-pre-hub-criteria-master.mkv` | `final/menu-evolution-readable-holds-master.mkv` | 942022906 | `d0d1cc2094c67ad362df34fd964a49e42892aea2e8faaea0214999e7ed3cde4d` |

`sources/promo/` and `provenance/` are byte copies of that render's edit, result row, reading holds, lists and
provenance (their paths inside still name the original file names); `review/` holds its review images. To
rebuild it, copy `sources/promo/` over a copy of the revision's `sources/promo/` (the edit finds the production
root by relative depth).
