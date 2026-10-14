# Archive scope and maintenance

This repository preserves the production materials used for OpenGGF-related
promo films, highlights, release reels and their retained revisions. The initial
import was made on 2026-10-14 from the local OpenGGF media directories and the
identified promo task directories. See `catalog/import.json` for the engine
reference used during discovery, totals and exclusion categories. The source
commit for each capture belongs to its original provenance; the discovery
reference is not a substitute for it.

Included: available plans/blueprints, assembly and capture programs, historical
Java drivers, controller scripts/logs, preference recipes, edit lists, chapters,
provenance, retained review conclusions and seven Resolve editing databases.
Original files retain their original wording, including superseded approaches
and incomplete work. A directory's presence or a filename containing `final`
does not certify a finished or published film.

External: recordings, finished videos, extracted ROM art/music, image sequences,
fonts, packaged mods, bulk state/observer dumps and other large dependencies.
They are catalogued where discovered, without uploading their bytes. Individual
large image sequences/review sets are summarized by directory or wildcard.

Excluded from the source import: installed environments, compiled/build trees,
temporary render work, consumed logs, process/session coordination metadata,
machine-local emulator configuration, general save data and unrelated projects.
This is an inventory of the media roots found on this machine, not a claim to
have recovered every historical source from every computer or deleted task.
Original release projects retain old media references, some outside the scanned
roots. Those references are listed separately; their availability is unverified.

## Adding work

1. Give each production a stable `projects/` directory and a short index. Preserve
   earlier revisions and identify unfinished/rejected takes honestly.
2. Add original source files without secrets or installed dependencies. Keep
   original paths and source commits in provenance; explain required relocation.
3. Extend the root map and the external asset catalog. Avoid committing footage,
   ROMs, decoded ROM assets, temporary logs or bulk diagnostic dumps.
4. Update `catalog/sources.json` with each preserved file's relative path, original
   root/path, size and SHA-256. Run `python3 tools/catalog.py verify` and relevant
   source syntax checks. Re-render only when changing an edit or validating it.
5. Every AI-assisted commit ends with the contributing model/version co-author
   trailer, e.g. `Co-authored-by: OpenAI Codex GPT-6.1 <noreply@openai.com>`.

For the Chaos card-gallery follow-up, [the scoped import helper](../tools/import_chaos_gallery.py)
accepts its frozen `revision-3` directory. The default invocation inventories
bounded production text and external asset sets without changing the archive;
`--write` copies that text and refreshes the matching catalogs. It verifies all
earlier Chaos source hashes, rejects unclassified files and detects source edits
during its snapshot. Review the resulting project index, source syntax, links
and public exposure, then run the ordinary catalog verifier before committing.
An import does not render or certify the movie.

## Rights

OpenGGF is an independent fan project and is not affiliated with Sega. OpenGGF
engine-derived code retains its GPL-3.0 terms; a copy is provided in `LICENSE`.
This archive does not grant additional rights to footage, Sega characters,
ROM-derived assets, third-party fonts/music, or other separately owned material.
Original notices remain applicable. Supply your own lawfully obtained ROMs and
respect the terms of external dependencies.
