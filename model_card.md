# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Music Fairy 1.0** — a small, rule-based music recommender that matches songs to
a listener's stated taste.

---

## 2. Intended Use  

Music Fairy takes a listener's taste profile — a favorite genre, a mood, a target
energy level, and whether they prefer acoustic or produced sound — and returns the
top 5 songs from a small catalog, each with a short explanation of why it was
picked. It assumes the user can describe their taste in those four fields, and that
those fields are a good enough stand-in for what they actually want to hear. This
is a **classroom exploration project**, not a product for real users: the catalog
is tiny and the scoring is intentionally simple so the behavior is easy to inspect
and reason about.

---

## 3. How the Model Works  

Music Fairy gives every song a score by asking four questions and adding up points:

- **Does the genre match?** If yes, the song earns some points.
- **Does the mood match?** If yes, it earns a few more.
- **How close is the song's energy to what the listener wants?** The closer it is,
  the more points it gets; a big mismatch earns almost none.
- **Does the sound (acoustic vs. produced) match the listener's preference?** Songs
  that lean the right way earn points here too.

It adds those four pieces into one number, sorts every song from highest to lowest,
and hands back the top five with a plain-language reason for each.

The one change I made from the starter logic was **reweighting**: I doubled how
much energy matters and halved how much genre matters. So compared with the
original, Music Fairy now cares more about a song *feeling* like the right
intensity and a little less about it being the exact genre the listener named.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

The catalog is a single CSV of **18 songs**. Each song has a genre, a mood, and
numeric features (energy, tempo, valence, danceability, acousticness). It covers
**15 genres** — lofi, pop, rock, edm, metal, hip hop, jazz, classical, ambient,
folk, country, reggae, r&b, synthwave, and indie pop — and a range of moods
(happy, chill, intense, relaxed, focused, energetic, melancholy, angry, romantic,
nostalgic, hopeful, confident, moody).

I did **not** add or remove any songs; I used the catalog as provided. The
representation is uneven — lofi has 3 songs and pop has 2, while every other genre
has only 1 — which means niche tastes have very few possible matches. A lot of
real musical taste is also missing: there are no lyrics or language, no artist or
release-year information, and no sense of subgenres or how songs blend styles — a
song is forced into exactly one genre and one mood.

---

## 5. Strengths  

Music Fairy works well for **clear, consistent profiles** — a listener whose
genre, mood, and energy all point the same direction. For all three realistic
profiles I tested (High-Energy Pop, Chill Lofi, Deep Intense Rock), the #1 pick was
exactly the song that matched on every axis, which matched my intuition.

It also separates **opposite tastes** cleanly: the Pop and Lofi lists share no
songs at all, because one wants loud/produced music and the other wants
calm/acoustic music. That tells me the energy and acoustic terms are doing real
work, not just noise. The plain-language explanations are a strength too — every
recommendation says *why* it was chosen, so the results are easy to sanity-check.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Exact-match genre/mood plus greedy top-K just echoes a user's taste back — a
filter bubble with no discovery. Acousticness is tied to genre, so a
"produced-sound" or high-energy preference quietly favors pop/electronic and
buries acoustic genres. The catalog is uneven (lofi 3, pop 2, most genres 1), so
niche tastes get thin results. Mid-range songs are penalized, ties break by CSV
order, and unknown genres/moods silently score 0.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles I tested.** I ran three realistic profiles plus two adversarial ones:

- **High-Energy Pop** — pop, happy, energy 0.9, non-acoustic
- **Chill Lofi** — lofi, chill, energy 0.35, acoustic
- **Deep Intense Rock** — rock, intense, energy 0.85, non-acoustic
- **Conflicting Sad High-Energy** — pop, "sad", energy 0.9 (contradictory + a mood not in the data)
- **Out-of-Range Energy** — rock, intense, energy 5.0 (invalid input)

For each I looked at the top 5 songs, their scores, and the "why" explanations to
check the results matched the stated taste. Comparing profiles *in pairs* was the
most useful test, because the differences show whether each preference actually
drives the output.

**Pop vs. Lofi (opposite tastes).** The two lists share *no* songs. Pop returns
all high-energy, produced tracks (Sunrise City, Gym Hero); Lofi returns all
low-energy, acoustic ones (Library Rain, Midnight Coding). This makes sense
because they differ on every axis — energy (0.9 vs 0.35) and acoustic preference
flip — so the recommender cleanly separates them. This is a strong sign the output
is valid.

**Pop vs. Rock (same energy, different genre/mood).** These two *overlap* a lot —
Gym Hero, Storm Runner, Warehouse Pulse, and Sunrise City appear in both top 5s.
That makes sense: both want high energy and non-acoustic sound, and energy is the
heaviest term, so both pull from the same high-energy pool. The difference is only
at the top: Pop ranks Sunrise City #1 (genre+mood match) while Rock ranks Storm
Runner #1. So the genre/mood signal still decides the winner, but energy blurs the
middle of the list — a valid but revealing result about how much energy dominates.

**Lofi vs. Rock (near opposites).** Zero overlap again, like Pop vs. Lofi — one
list is calm and acoustic, the other loud and produced. This confirms the energy
and acoustic terms are doing real work and the two tastes don't bleed together.

**What surprised me.** The adversarial pair exposed silent failures rather than
different music: "sad" is not a real mood, so it scored 0 and the contradiction
was invisible; and energy 5.0 pushed every score negative because nothing clamps
the input. Both told me the *rankings* look valid for normal profiles, but the
scorer does no input validation, so a bad profile fails quietly instead of loudly.

---

## 8. Future Work  

- **Validate user input.** Reject or warn on unknown genres/moods and clamp energy
  to a 0–1 range, so bad profiles fail loudly instead of silently scoring 0 or
  going negative (both of which I found in testing).
- **Understand similar labels.** Treat related genres (pop ≈ indie pop) and moods
  (chill ≈ relaxed) as partial matches, instead of requiring exact strings, so the
  system can suggest music *near* a taste and not just echo it.
- **Add a diversity term.** Reward variety among the top 5 so the list isn't five
  near-identical songs — this would soften the filter-bubble effect.
- **Handle richer tastes.** Let users list more than one genre or mood, and add a
  "neutral" acoustic option so listeners who don't care aren't forced to pick a side.

---

## 9. Personal Reflection  

Building Music Fairy showed me that a recommender is really just a scoring formula
plus a sort, and that the *weights* in that formula quietly decide what a listener
sees. When I doubled the energy weight, the top picks barely moved but the middle
of every list shifted toward high-energy songs — a small tuning change that could
meaningfully steer someone's listening.

The most eye-opening part was how easy it is to hide bias in an "objective" number.
An audio feature like acousticness turned out to be tied to genre, so a simple
"produced sound" preference quietly favored some genres and buried others. And my
adversarial tests failed *silently* — a misspelled mood just scored zero with no
warning. It made me realize that real music apps make these same choices at huge
scale, and that the fairness of a recommender lives in the details of its scoring,
not in any single obvious rule.
