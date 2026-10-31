# Complexes inventory: OURS vs TAKANO

Src: `outputs/{III,II,I,CMS,MS}.json` vs `tests/fixtures/takano-{III,II,I,CMS,MS,MSIC}.json`. Complex = slot movement contains `+`; seq `[zone,[r1,r2]]` per-side reps. Lift share = complex lifts / all lifts.

## 1. Inventory + share (slots, lift-share)

| Prog | OURS complexes (slots / lift-share) | TAK complexes (slots / lift-share) |
|---|---|---|
| III (nov) | OthCl+OthJ 13/8.2%, OthCl+J 12/8.2%, Cl+J 4/2.3% — **total 18.8%** | Cl+J 6/6.4%, OthCl+OthJ 3/3.7%, OthCl+J 2/1.5%, OthSn+OthSq 1/1.3%, Pull+Sn 1/0.9% — **total 13.7%** |
| II | same trio 13/8.3% + 12/8.3% + 4/2.3% — **18.8%** | Cl+J 11/9.8%, OthCl+OthJ 5/6.1%, OthCl+J 4/3.1%, OthSn+OthSq 2/3.3% — **22.4%** |
| I | OthCl+OthJ 23/9.9%, Pull+Sn 21/9.1%, Cl+J 13/7.8%, Pull+OthSn 10/6.0%, Pull+OthCl 5/1.3%, Cl+OthJ 2/1.2%, OthCl+J 2/1.4% — **36.7%** | Cl+J 19/10.9%, OthCl+OthJ 11/6.7%, OthCl+J 6/3.2%, OthSn+OthSq 4/2.7%, Pull+Sn 2/1.1%, Pull+Cl 2/1.1%, OthSn+Press 1/0.7% — **26.3%** |
| CMS | same 7 types: 21/9.0% + 19/7.9% + 14/8.5% + 11/6.7% + 6/1.8% + 2/1.2% + 2/1.4% — **36.6%** | Cl+J 26/12.5%, OthCl+OthJ 18/9.7%, OthSn+OthSq 6/3.8%, OthCl+J 4/2.0%, rest ≤1% — **30.0%** |
| MS | OthCl+OthJ 52/15.1%, Pull+OthSn 29/13.6%, Pull+Sn 19/5.8%, Cl+J 18/9.4%, OthCl+J 2/0.9%, Pull+OthCl 2/0.6% — **45.4%** | Cl+J 30/9.3%, OthCl+OthJ 18/6.3%, others ≤2.8% ea — **23.3%** (MSIC: Cl+J 55/14.1%, total 25.1%) |
| Pairs that exist | 7: Cl+J, OthCl+J, OthCl+OthJ, Cl+OthJ, Pull+Sn, Pull+OthSn, Pull+OthCl | 7: Cl+J, OthCl+J, OthCl+OthJ, Pull+Sn, Pull+Cl, OthSn+OthSq, OthSn+Press |
| Never paired | **OthSn+OthSq, OthSn+Press, Pull+Cl never occur in ours** | **Pull+OthSn, Pull+OthCl, Cl+OthJ never occur in Takano** |

## 2. Per-type habits (modal reps, zones, sets/slot, position)

- **Clean+Jerk (the shared one):** ours modal **[2,3]** (I/CMS/MS: 70/70/107 hits; heavies [2,1] second) @ zones 60/70/80/90 spread, **7–12 sets/slot**, middle/first. Takano modal **[2,1] then [1,1]** (MSIC: 127/105; CMS 47/41), zones peak 80, **5–7 sets/slot**, always middle (MS/MSIC sometimes last). Ours does volume triples; Takano does singles.
- **Other Clean+Other Jerk:** ours modal [2,1]/[3,1] (III/II) shifting to [2,1]/[1,1] (MS: [1,1]=115, [2,2]=107), zones 60–90, **7–9 sets**, middle. Takano modal **[2,2]/[3,3]/[1,1]** (light symmetric doubles/triples), zones **60–70 only** (CMS 32/55 @60/70, ~0 @80+), **5–6 sets**, middle→last.
- **SnPull+Snatch:** ours modal [2,3]/[1,2]/[1,3], zones 60–90, ~7 sets, **always first slot**. Takano modal **[3,1] fixed** (all 5–7-set slots identical), zones 60–80, middle/first, rare (1–3 slots/program).
- **Ours-only Pull+OtherSnatch** (I/CMS/MS first-slot staple, 10–29 slots): modal **[1,2]/[1,3]** (MS: 96/99), ~12 sets, zones 60–90. **Takano-only OthSn+OthSq** (first-slot, 1–6 slots): modal [3,3]/[4,4], ~5 sets, 60–70 only.
- Position rule both sides: pull+snatch variants = **first**; clean+jerk variants = **middle** (Takano OthCl+OthJ drifts **last** in MS/MSIC: 10/18, 5/9).

## 3. Oddballs

- **OTHER-member complexes:** ours 5 of 7 types contain Other (I/CMS: 41/76 complex slots; MS: 83/122). Takano 3–4 of 7 (MSIC 30/92). Not a bug per se — but ours puts variant complexes under load (see below).
- **Triples (3-leg): none on either side.** No split-leg complexes anywhere.
- **Complexes at 90%+ (sets): OURS — nearly all of them.** MS: OthCl+OthJ 79, Pull+OthSn 55, Cl+J 40; I/CMS: every complex type has 3–23 sets ≥90 (Cl+J 18/23, OthCl+OthJ 18/19, Pull+Sn 12/14). **TAK — only Cl+J and OthCl+J ever touch 90** (MSIC Cl+J 89, OthCl+J 15; III/II/CMS: OthCl+OthJ **0 sets ≥90**, OthSn+* 0). Severity-ranked: (1) OthCl+OthJ @90 ×79 in MS — Takano never loads this above 70; (2) Pull+OthSnatch @90 ×55 — a Takano-nonexistent pair done heavy; (3) Cl+J [2,3]×~70 @80–90 — competition lift done as volume triples.

## 4. Biggest structural difference (role, not texture)

**Ours uses complexes as the volume engine; Takano uses them as the competition test.** In ours (MS 45%, I/CMS 37% of all lifts) the complex *replaces* the primary slot: first-slot Pull+Snatch/Pull+OthSnatch with 7–12 sets of [1–2,2–3], middle-slot Cl+J [2,3] triples across 60–90. In Takano (14–30%) singles stand alone, Cl+J is [1,1]/[2,1] heavy singles peaking at 80–90 in 4–7 sets while variant complexes are quarantined to light 60–70 technique work (OthCl+OthJ, OthSn+Sq/Press never exceed 70–80). Net: ours trains *through* the complex, Takano trains *up to* it.
