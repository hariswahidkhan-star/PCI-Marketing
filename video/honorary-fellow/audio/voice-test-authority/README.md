# Narrator test — "more authoritative"

Three voices reading the same two opening scenes of the authority cut, on
`eleven_v3`, so the choice is made by ear. All three are stock library voices —
**none is a clone of any real person.**

| File | Voice | `voice_id` | Character |
|---|---|---|---|
| `A-Holden-directed-deep.mp3` | Holden Pro Voice — the brief's named narrator, directed `[deep, slow, commanding]` | `UudLhsL2DlHkDK0vGwl3` | American, Midwestern; the current narrator, pushed harder toward gravitas |
| `B-Jim-Executive-british.mp3` | Jim Executive — Authoritative, British and Warm | `tXxkePQsw0G69D8VeDzp` | British C-suite baritone; **already the narrator of PCI's other three films** |
| `C-Leo-broadcast-american.mp3` | Leo — Narration, Commercial & Social Media | `cOHUo8FosWk7BqQhx8nk` | American, four decades of broadcast; deep and controlled |

**Recommendation: B.** It is the only one of the three whose library descriptor
*is* "authoritative", it carries the institutional register the film needs, and
it keeps one narrator across the whole PCI set. The authority cut is produced on
B unless PCI says otherwise; switching is one re-generation (~$0.60).

Cost of this test: ~820 credits (~$0.15), one take each.

**Outcome:** PCI listened to all three and chose **A — Holden**. The authority
cut is produced on Holden. PCI then asked for it a little faster and more
human, then for maximum emotion, so the shipped takes (`../vo-01.mp3` … `../vo-13.mp3`)
carry phrase-level emotional direction (`../../src/v3-emotion.json`). The
`[deep, slow, commanding]` read is in `../holden-commanding/` and the
`[warm, confident, natural pace]` read in `../holden-warm/`. The full Jim Executive read of the same
script, made before PCI's choice, is kept in `../jim-executive-authority/`; the
previous cut's Holden takes are in `../old-paced-holden/`.
