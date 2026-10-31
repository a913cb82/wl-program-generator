# Adversarial volume audit (outputs/*.json parsed directly, pair-slots split)
Method: lifts=sum(reps) per slot seq; `A+B` slots split tuple reps in order.
20-wk totals annualised x2.6; monthly=wkavgx4.33. Ours has no phase tags;
prep=m0-2, comp=m3-4 assumed. Roman bands p88; T11=p102 shares.
Ours 20-wk: III/II 4986, I/CMS 6712, MS 8438 (waves identical, scaled
1.0/1.348/1.691x — see 6).

## WRONG-NUMBERS
1. MS annual 21,939 = Roman MS year 18,000 +22% (+3,939). Prep-mo 2040
   inside 1500-2700 so months pass but year total breaks the book. Same
   mechanism: I/CMS 17,451 vs 15,000 +16%; III/II 12,964 vs ~12,000 +8%.
   Refit chased Takano MS ann (21,393, we match +2.5%) and overshot Roman
   years monotonically with level. Annualising a loaded 20-wk block with
   no rest month overstates; either cut peak meso or own the deviation.
2. III/II sit +40%/+25% above Takano ann (9,230/10,383) while CMS sits
   -6% below Takano (18,521). Refit pivoted the curve around CMS: bottom
   overshoots the sample, top (MS +2.5% vs Takano MS, no MSIC grid at all)
   undershoots Takano MSIC ann 26,652 by ~18%. No class is outside every
   band, but low classes left Roman-sample agreement worse, not better.
3. Missing Other-Squat at I+: ours 0.0% vs Roman ~6% prep I/CMS (≈100
   lifts/20wk, ≈260/yr) and large MS heavyweight volumes (p65: up to
   260/mo prep). SnP at MS 7.5% vs 8.5% (-1pp, ~-85/20wk) same gap.
   ~6pp silently redistributed (+0.6 Sn, +0.5 J, +Other). Add OSq or document.

## SHAPE-OFF
4. Peak:trough 4.11/4.10/4.09 identical all classes (peak 399/537/675,
   trough 97/131/165). Takano steepens with level (II 2.5, III 3.2, I 3.3,
   CMS 2.8, MS 5.1, MSIC 4.6); Roman Table-13 in-month ratio is ~2x.
   Single scaled template = the old "flat curve" bug moved from totals to shape.
5. Comp cut uniform 26.1% (m3-4 vs m0-2; last-meso 32.8%) every class —
   inside Roman 20-40%/avg 30%, but Roman grades by mass (52kg 27.5%,
   110+ 33.5%, beginners 17-18%) and Takano grades by level (prep->precomp
   mo: III -29%, II -36%, I -43%, CMS -49%, MS -48%). Ours should steepen;
   currently III cuts as hard as MS.
6. Final-week rule passes (meso3-wk4 12.0%, meso4-wk4 12.9-13.0% of meso;
   Roman 11-14%), but mid-prep trough (wk2: 170/228/287) gives 1.8-1.9x
   in-meso swings with no Table-13 variant justification. Trough weeks
   108/97 (III) back-load two deloads in 4 weeks.
7. III=II byte-identical totals (4986; groups differ by <=5 lifts) — zero
   gradient where Takano has +12% II>III. Refit kept the flat bottom.

## NIT (verified OK)
8. Zero pulls at III/II per Roman p61 verified, no bloat: Sn 10.0/10.0,
   Cl 7.5/9.8, J 7.5/3.5, Sq 26.7, OSq 14.9, Other 10.0 = T11 exact
   (classic Sn 50%, Cl 43-44%, J 68%). Takano does 7-9% pulls here —
   book-vs-sample conflict, we side with Roman; fine, note it.
9. I/CMS/MS classic shares exact (Sn 45/44/40, Cl 40/40/38, J 56/56/43
   vs T11 45/45/40, 40/40/38, 58/58/46). MS J classic 43% nails comp 43%.
10. Low-class large-day rule passes: max 1 L/wk (18L+11M+42S over 71
    sess). But distribution is bimodal (59% S, 15% M) vs Takano III
    (46% S, 50% M, 1L) — we use L where Takano uses M. I/CMS/MS weeks
    with 3 L-days (3/4/8 wks) have no book cap; MS p145 130-150d precedented.
