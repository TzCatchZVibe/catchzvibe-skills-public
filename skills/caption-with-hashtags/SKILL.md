---
name: caption-with-hashtags
description: Generate platform-native captions + layered hashtag stacks for short-form video posts (TikTok primary; FB/IG/X variants). Encodes 5-tier hashtag strategy, caption-visual complementarity rules, and [CLIENT]/HG brand voice. Use when user posts a video and says "写caption", "加hashtag", "post this video", or pastes a shot list / final video for publishing. Also use proactively when running publish/iterate flows on CatchZVibe (project_id → caption needed before push).
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# Caption + Hashtag Skill

For CatchZVibe Studio publishing pipeline. Encodes everything learned about
caption-writing and hashtag layering so future runs are one-shot.

## Core Principles

### 1. Caption ≠ Voiceover
The video's audio already says what the video says. The caption must give
the viewer **the layer the video doesn't show**:
- Product name (when visual is tight on object, viewer wonders "what is this?")
- Audience callout ("moms watching this — ")
- Soft CTA (save/send/buy yourself one)
- Continuation thought (not repetition of speech)

If you can delete the caption and lose nothing, the caption is wrong.

### 2. The First Line Is The Hook
TikTok preview shows ~80 chars. First line must:
- Land a feeling or a fact in <12 words
- Lowercase, conversational
- No emoji on line 1 (algo deprioritizes emoji-led captions in 2025+)

### 3. Brand Voice Per Account
| Account | Voice | Caption Style |
|---|---|---|
| Main Account (主号) | philosophical, intimate, 32yo male monologue | story-fragment, soft CTA |
| Secondary Account (副号) | casual product-forward, snackable | product fact + sensory cue |
| HG (other clients) | match client brief; default warm-direct | — |

### 4. Format Rules ([CLIENT] non-negotiable, generalizes well)
- All lowercase
- Each line ≤6 words
- 2-4 short stanzas separated by blank line
- Hashtags **after** caption body, on their own block
- No "link in bio" / no "buy now" / no "catch you tomorrow"

---

## Hashtag Tier Model (THE deep playbook)

**Total tags: 4-8 per post.** Never stack 15+ — TikTok algo treats it as spam
since 2024 and dilutes per-tag relevance signal. Verified videos with 4-6
strategic tags consistently out-perform tag-stuffed posts.

### The 5 tiers (mix 1-2 from each, not all)

| Tier | Volume | Role | Example ([CLIENT]) |
|---|---|---|---|
| **T1 Branded** | <100K | Aggregate your own catalog · controlled | `#kozed` `#kozedgummy` `#peelablegummy` |
| **T2 Niche** | 100K-1M | High-intent discovery · low competition | `#asmrcandy` `#oddlysatisfying` `#candyreview` `#chewycandy` |
| **T3 Category** | 1M-50M | Mid-broad audience · entering vertical | `#candytok` `#snacktok` `#foodtok` |
| **T4 Mood/Trend/Audience** | varies | Contextual · TIME or PERSON locked | `#mothersday2026` `#momsoftiktok` `#tuesdayvibes` `#cozyvibes` `#povkid` |
| **T5 Discovery** | 100M+ | Broad reach · saturated · use sparingly | `#fyp` (pick ONE — never stack `#fyp #foryou #foryoupage`) |

### The composition recipe

**Default 6-tag stack:** `1×T1 + 2×T2 + 1×T3 + 1×T4 + 1×T5`

```
#kozed                        ← T1 branded
#peelablegummy                ← T2 niche (product)
#asmrcandy                    ← T2 niche (sensory match)
#candytok                     ← T3 category
#mothersday2026               ← T4 trend (TIME locked)
#fyp                          ← T5 discovery (one only)
```

### Per-account adjustments

- **Snacks (副号 / discovery):** push T2 niche to 3, drop T4 unless on-trend.
  Goal: get crawled into ASMR/snack discovery loops.
- **Choice (主号 / story):** push T4 to 2, lean audience/mood. Goal: hit
  emotionally-targeted FYPs (moms, dads, etc).
- **Holiday post:** T4 trend tag MUST be year-locked (`#mothersday2026` not
  `#mothersday` alone) — algo weighs current-year tag higher in window.
  Include both for evergreen surfacing post-holiday.

### Hard rules

1. **Tag what's IN the frame.** TikTok CV verifies. `#cooking` on a
   candy-eating video = relevance penalty.
2. **No double-stacking discovery.** ONE of `{fyp, foryou, foryoupage, viral}` max.
3. **No banned tags.** Avoid `#tiktok` (deprioritized), `#sex*`, `#weight*`
   (auto-flag), and any TikTok rotates as restricted that week.
4. **Don't repeat caption text as hashtag.** If caption already says "mother's day", `#mothersday2026` adds context — but `#momcalledtwice` (mirror of caption) wastes a slot.
5. **Branded tag every post.** Builds your aggregate page over time.
6. **No spaces, no emoji** inside hashtags.

---

## Workflow

### Inputs needed
1. Video script / shot list (or final video file)
2. Account → Choice / Snacks / other
3. Publish date (for trend-window detection)
4. Project UUID (if CatchZVibe pipeline)

### Steps

1. **Read shot list** — note: who's speaking, what's in frame, mood,
   product, voiceover key phrases.
2. **Identify the layer** — what does the visual NOT say that the viewer
   wants? (product name, CTA, audience hook)
3. **Draft 3 caption stanzas:**
   - Hook line (≤12 words, first-line punch)
   - Bridge / continuation (1-3 lines)
   - Soft CTA or close (1-2 lines)
4. **Layer hashtags** using 5-tier recipe. Account-tune.
5. **Self-check** with the validation checklist (below).
6. **Output** in this format:

```
<caption stanzas>

<hashtag block>
```

7. **Present to user for approval** before publishing. Captions are
   public + irreversible — never push without sign-off unless explicitly
   pre-authorized for a batch.

---

## Validation checklist (run before output)

- [ ] Caption does not paraphrase voiceover (different angle / continuation)
- [ ] First line ≤12 words, lowercase, no emoji
- [ ] Each line ≤6 words
- [ ] 4-8 hashtags total
- [ ] At least 1 branded tag (T1)
- [ ] At least 1 niche tag (T2)
- [ ] Max 1 discovery tag (T5)
- [ ] Trend tag year-locked if holiday/dated content
- [ ] No tag mismatches frame content
- [ ] No "buy now" / "link in bio" / "catch you tomorrow"

If any unchecked → revise.

---

## Examples (battle-tested 2026-05-10 [CLIENT] batch)

See `examples/` directory:
- `v1-two-layers-snacks.md` — philosophical product post on sub-account
- `v3-mothers-day-choice.md` — holiday emotional post on main
- `v6-mothers-day-tuesday-choice.md` — post-holiday audience-pivot

---

## Common mistakes (don't repeat)

| Mistake | Why it kills reach |
|---|---|
| 15+ hashtags | Algo treats as spam since 2024 |
| `#fyp #foryou #foryoupage` stack | Algo dedupes; signals desperation |
| Holiday tag without year | Loses current-window boost |
| Caption mirrors voiceover | Wastes the second channel |
| Emoji on line 1 | Engagement preview deprioritized |
| Untagged brand | No aggregate catalog over time |
| `#cooking` on candy video | CV mismatch → relevance penalty |

---

## Posting Time Strategy (MANDATORY · TZ rule 2026-05-10)

**Hard rule: NEVER instant-post. Always scheduled. Always confirm time with TZ first.**

When publishing is requested, the skill MUST:
1. Compute recommended posting time using the model below
2. Show TZ a time table (date + ET + PT + rationale)
3. Wait for confirmation
4. Output schedule-ready package (caption + hashtags + UTC timestamp)

### 2026 TikTok timing model (Sprout Social + Buffer 7M-post study)

| Day | Top slot (local) | Backup slots |
|---|---|---|
| Mon | 1 PM | 11 AM, 8 AM |
| Tue | 6 AM | 10 PM, 7 AM |
| Wed | 2-6 PM (best window of week) | 11 AM, 10 PM |
| Thu | 1 PM | 10 PM, 6 AM |
| Fri | 6 PM | 10 PM, 8 PM |
| Sat | 5 PM (Buffer's strongest day) | 4 PM, 3 PM |
| Sun | **9 AM (single strongest slot of entire week)** | 1 PM, 12 PM, 7 PM |

**Universal:** First 3 hours after post = algorithm's discovery window. Posting when audience is offline = lost momentum permanently.

### Tier-2 modifiers (apply ON TOP of day/time table)

| Modifier | Adjustment |
|---|---|
| **US English account, default audience** | Use ET (Eastern) as primary; most US active hours align ET |
| **Mom audience** | Push to evening 7-10 PM local — kids in bed, moms scroll wind-down |
| **ASMR / oddly-satisfying** | Afternoon-early evening 2-6 PM — scroll/break behavior peak |
| **Holiday content** | Post DURING holiday morning-afternoon, NOT day after; year-locked hashtag has ~24h window |
| **Post-holiday wind-down content** | Post within 24-48h post-holiday for emotional recency |
| **Multi-video same-day same-account** | Space ≥4h apart; algo deprioritizes back-to-back from same handle |
| **Multi-video same-day cross-account** | No penalty — different handles |

### Output format (mandatory before publishing)

```
| Video | Account | Date | Time (ET) | Time (PT) | Why this slot |
|---|---|---|---|---|---|
| V3 Mother's Day | choice | 5/10 Sun | 7:00 PM | 4:00 PM | Sunday evening = Buffer T2 slot · holiday emotion peaks late-day · matches sunset visual |
```

Then: "OK 就预约 → 我打包 caption + hashtag + 时间给你（你在 TikTok Studio 排一下，或我帮你跑预约 API）"

### Hard rule: never instant-post

Even "现在就发" requests get scheduled — if the optimal slot is in 30 min, schedule for 30 min. Only exception: time-sensitive trend hijack (<1h window of relevance), and even then ask TZ to confirm.

---

## Re-running the skill

When updated knowledge or a new account's voice is learned, append to:
- `templates/<scenario>.md` for new scenario patterns (holiday, ASMR, etc)
- `examples/` for canonical successes
- This SKILL.md only when a rule changes
