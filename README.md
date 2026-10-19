# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps you shop secondhand. You describe what you want in plain words, like "vintage graphic tee under $30, size M", and it searches thrift listings from Depop, thredUp, and Poshmark for the best match. It then suggests one or two outfits that pair the find with clothes you already own, or gives general styling ideas if your wardrobe is empty, and writes a short caption you could post about it. If nothing matches, it stops and tells you what to change, like your keywords, size, or max price.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**  Searches the listings for items matching the user’s description, with optional size and maximum-price filters, and returns matching listings ranked by relevance.
- **Inputs:** `description` (str), `size` (str | None = None), `max_price` (float | None = none), <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:** `filteredListings` (list[dict]) of matching listing dictionaries ordered best match first, each with id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform 
- **When it has nothing:** search_listings returns an empty list 

### `suggest_outfit`

- **What it does:** Suggests one or two outfits using items from the user’s wardrobe that go with the new item they want.
- **Inputs:** `new_items` (dict), `wardrobe` (dict)
- **Returns:** `suggestions` (str) with outfit suggestions based on the new item and the user’s wardrobe.
- **When it has nothing:** returns general styling advice for the new item

### `create_fit_card`

- **What it does:**Write a short caption someone would actually post about the find.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** `caption` (str) with two to four sentences
- **When it has nothing:** return a descriptive message based on the new item

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in session["error"] that says what the user could change (keywords, size, or max price), and return the session without calling suggest_outfit. Otherwise, take the first result as session["selected_item"] and go to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** asking the model to pull the filtered information out which is a description, a size and a max price.

**What moves through the session:** query -> parsed -> search_results -> selected_item -> outfit_suggestion -> fit_card
error is only set if search_results is empty.
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'
```
***Output***

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Casual Streetwear**
Pair the baby tee with your baggy straight-leg jeans, dark wash. Layer your black cropped zip hoodie on top, and slip into your chunky white sneakers. Finish with your black crossbody bag for an easy, everyday look.

**Outfit 2: Y2K Contrast**
Tuck the butterfly tee into your wide-leg khaki trousers, cinched with your brown leather belt. Throw on your vintage black denim jacket and lace up your black combat boots to balance the sweet, girly print with some edge.

  Fit card: Found the ultimate Y2K butterfly baby tee and I’m obsessed. Snagged this baby on Depop for just $18 and it’s giving major sweet-meets-edgy energy. How are we styling this—casual streetwear with baggy denim or leaning into the contrast with combat boots?🦋✨

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
```
***Output***

le vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand':None, 'platform': 'depop'}]

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
```

***Output***

**Outfit 2: Edgy Streetwear**
Wear the jeans with the black cropped zip hoodie and layer the vintage black denim jacket on top. Lace up your black combat boots, put on the brown leather belt, and grab your black crossbody bag for a cool, all-black-and-denim vibe.

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
```

***Output***

Nothing beats a broken-in pair of vintage Levi's 501 jeans. Snagged these for just $38.00 on depop. Paired with crisp white sneakers, the streetwear vibe is effortless.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* Here are five acceptance criteria (paste in the five criterias) for a multi-tool agent. For each one, tell me exactly how you would test it using only what the sentence says. Don't suggest improvements — just tell me what you'd do
- *What came back:* A step-by-step test for each criterion: which query to use, how many runs, what to record, and when it passes. It also flagged places where my wording was unclear:
     - Criterion 1 says "a query," singular, so it would repeat one query 5 times instead of using 5 different ones.
     - Criterion 2's "names what the user could change" can only be checked by reading the message and making a judgment call.
     - Criterion 3 should take the item from what suggest_outfit actually received, not read it back from the session, or the check proves nothing.
     - Criterion 4's "why" mentions 2–4 sentences, but the criterion only sets a character limit, so it would only count characters.
     - Criterion 5 doesn't say which query to use, so any query would count.
- *What I changed:* didn't change anything in my criteria, because each test the AI described matched what I meant, and every criterion could be checked as written. The points it flagged were things I had already decided: repeating one query is fine for criterion 1, reading the message is a fair way to judge criterion 2, and characters are the only thing criterion 4 measures. The one thing I took from it was criterion 3: I'll check the item suggest_outfit actually received instead of reading it back from the session.

**Moment 2**

- *What I asked for*: I asked whether my criterion 5 was valid. It said: "For 5 out of 5 queries, if the model can't be reached, parsing will still occur and information still gets retrieved."
- *What came back*: It said the criterion wasn't valid yet, for three reasons. First, my README says I parse the query by asking the model, so parsing can't happen when the model is down. Second, "information still gets retrieved" is too vague to check. Third, suggest_outfit and create_fit_card also need the model, so the run can't finish anyway. It gave me two fixes: (A) check that the agent returns a friendly message in session["error"] instead of a stack trace, or (B) build a regex backup parser and check that it still fills in size and max price.
- *What I changed*: I chose option A and rewrote the criterion: "When the model can't be reached, the agent returns a message in session["error"] instead of a stack trace, in 5 of 5 tries." It kept my original idea of testing what happens when the model is down, but now it describes something my agent can actually do and something I can check. I skipped option B because building a second parser just for this test was more work than the criterion needed.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item reaches suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card stays under 300 characters | 4 of 5 | PASS (graphic tee, 248) | PASS (denim jacket, 267) | PASS (flannel shirt, 195) | PASS (slip dress, 228) | PASS (chelsea boots, 257) | MET (5/5) |
| 5. model down returns error message | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |


- **Criterion 3:** the run log prints `selected_item` but not the item that
  `suggest_outfit` received. I marked PASS because in every try the selected
  item was *Denim Jacket — Light Wash, Cropped ($42.0, poshmark)* and every
  outfit suggestion styles that same light-wash cropped denim jacket. It is
  not a direct id comparison.


**Real output from one try per criterion**, pasted as text. Every run was
recorded by `run_eval.py::main`, which calls `agent.py::run_agent`. Criteria
1–4 come from `results/run_2026-10-18_1745_before.md`; criterion 5 comes from
`results/run_2026-10-18_1751_before.md` (run with one character of the API
key changed).

**Criterion 1 — matching query completes** (try 1). Search by
`mcp_server.py::search_listings` (via `mcp_client.py::call_tool`), outfit by
`tools.py::suggest_outfit`, fit card by `tools.py::create_fit_card`:

```
### matching query completes
- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:
**Outfit 1: Casual Y2K Streetwear**
Pair the baby tee with your baggy straight-leg jeans, dark wash. Layer the black cropped zip hoodie right over top, and step into your chunky white sneakers. Finish the whole look with your black crossbody bag.

**Outfit 2: Soft Retro Contrast**
Tuck the butterfly tee into your wide-leg khaki trousers, and cinch the waist using your brown leather belt. Throw on your vintage black denim jacket as an extra layer, and tie the outfit together with your black combat boots.

Fit card:
Butterfly print Y2K baby tee for only $18? Grabbed this on Depop and I'm obsessed. Giving major early 2000s streetwear energy with baggy denim, or leaning into that soft retro contrast with khaki trousers. ✨
```

**Criterion 2 — impossible query stops early** (try 1). The stop happens in
`agent.py::run_agent`'s empty-results branch; the message is written by
`agent.py::_no_results_message`:

```
### impossible query stops early
- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**
- stopped early: yes — Nothing matched 'designer ballgown' in size XXS under $5. Try to use different keywords, pick another size, or raise your max price.
- selected_item: (none)
- search_results: 0
```

**Criterion 3 — selected item reaches suggest_outfit** (try 1).
`selected_item` is set in `agent.py::run_agent` and passed to
`tools.py::suggest_outfit`, which wrote the outfit below:

```
### selected item reaches suggested outfit
- Query: `denim jacket under $50`
- Wardrobe: example

**Try 1**
- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:
**Outfit 1: Double Denim**
Pair the Denim Jacket with your white ribbed tank top and baggy straight-leg jeans. Finish with chunky white sneakers and your black crossbody bag for an easy, casual weekend look.

**Outfit 2: High-Low Contrast**
Layer the Denim Jacket over your black cropped zip hoodie, and wear them with your wide-leg khaki trousers. Add your black combat boots and the black crossbody bag to give the classic jacket a cool, streetwear edge.
```

**Criterion 4 — fit card stays under 300 characters** (graphic tee, try 1).
Written by `tools.py::create_fit_card`:

```
### fit card length: graphic tee
- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Got this absolute dream of a Y2K butterfly baby tee for just $18 on Depop. Perfect for channeling total 2000s pop-princess energy with baggy jeans or balancing it out with chunky combat boots. Grab it before I change my mind and keep it forever! 🦋✨
```

**Criterion 5 — model down returns error message** (try 1, bad API key).
`generate.py::generate` raised `ModelUnavailable`, `agent.py::run_agent`
caught it, and `agent.py::_model_down_message` wrote the message:

```
### model down returns error message
- Query: `denim jacket under $50`
- Wardrobe: example

**Try 1**
- stopped early: yes — The model couldn't be reached, so I couldn't finish your request. Check your API key in .env and your internet connection.
Details: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: (none)
- search_results: 0
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | All 5 tries of `vintage graphic tee under $30` ended with `stopped early: no`, a selected item, an outfit, and a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | All 5 tries of `designer ballgown size XXS under $5` show `search_results: 0`, `selected_item: (none)`, and a message naming what to change (keywords, size, max price). No outfit or fit card was made. |
| 3 | The selected item is the item suggest_outfit receives | 5 of 5 | MET (5/5) | In all 5 tries `selected_item` was the light-wash cropped denim jacket, and every outfit suggestion styles that same jacket. The log doesn't print ids, so this is judged from the outfit text, not a direct id comparison. |
| 4 | Fit card is 300 characters or fewer | 4 of 5 | MET (5/5) | I took try 1 from each of the 5 different items and counted characters: 248, 267, 195, 228, 257. All under 300. All 25 cards in the run were under 300 (longest 269). |
| 5 | Model down returns a message, not a stack trace | 5 of 5 | MET (5/5) | With one character of the key changed, all 5 tries stopped with "The model couldn't be reached…" in `session["error"]`. No stack trace, no hang. |

**Diagnoses**

No criterion missed its target, so there's no failure to diagnose. Three
things the logs showed that are worth writing down anyway:

- **Criterion 3 is only checked indirectly.** The evidence is that the outfit text describes the selected item. That would catch a completely wrong item, but not two similar items being swapped. A stronger check would log the id that `suggest_outfit` actually received and compare it to `session["selected_item"]["id"]`.
- **Criterion 4 passed with room to spare.** The longest card was 269
  characters, and none came close to 300. The target held, but the fit cards run longer than a typical caption, between about 175 and 269 characters.
- **With the model down, every scenario fails the same way, even the
  impossible query.** In the bad-key run, `designer ballgown size XXS under $5`
  also stopped with the model error, not the "Nothing matched" message.
  That's because `agent.py::parse_query` calls the model before the search
  runs, so the loop never reaches the empty-results branch. The search itself
  (`search_listings`) doesn't need the model, but my loop depends on the
  model to parse the query first.



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
python app.py ask 'grey shirt under $20' --trace 

[1] search_listings
      in:  dict with keys: description, max_price, size
      out: 2 items: Vintage Polo Shirt — Forest Green, Vintage Band Tee — Faded Grey

  Found:    Vintage Polo Shirt — Forest Green — $18.0 on thredUp

  Outfit:   **Outfit 1: Casual Coffee Run**
Wear the vintage polo shirt tucked into your baggy straight-leg jeans, and add the brown leather belt. Layer the oversized grey crewneck sweatshirt loosely over your shoulders for a relaxed, preppy look. Finish with chunky white sneakers and your black crossbody bag.

**Outfit 2: Streetwear Edge**
Pair the vintage polo shirt unbuttoned over your white ribbed tank top with the wide-leg khaki trousers. Slip into your black combat boots and throw on the vintage black denim jacket over top. Accessorize with the black crossbody bag for an easy, high-low mix of sporty and tough.

  Fit card: Forest green Ralph Lauren polo for just $18 on thredUp? Yes please. Giving major vintage preppy vibes today. How are we styling it: coffee run comfy or total streetwear edge? ☕️🖤   
```

**Empty search**

```
python app.py ask 'designer ballgown size XXS under $5'

      in:  dict with keys: description, max_price, size
      out: [] (empty)

  Nothing matched 'designer ballgown' in size XXS under $5. Try to use different keywords, pick another size, or raise your max price.
```

**On the MCP move:** I moved `search_listings` behind an MCP server. Two files
changed:

- `mcp_server.py` — registered `search_listings` as an MCP tool with
  `@mcp.tool()`. It takes `description: str`, `size: str | None`, and
  `max_price: float | None`, and calls the real search in `tools.py`
  (imported as `_search_listings_impl` so the tool doesn't call itself).
- `agent.py::run_agent` — swapped the direct call
  `search_listings(description, size, max_price)` for
  `call_tool("search_listings", {"description": ..., "size": ..., "max_price": ...})`
  from `mcp_client.py`.

Nothing behaved differently afterwards. The matching query still selected
*Y2K Baby Tee — Butterfly Print ($18.0, depop)*, and the impossible query
still came back empty and stopped before `suggest_outfit`.

Two things broke along the way:

1. My first version of the server tool returned `{}` instead of calling the
   real search, and in `agent.py` I wrote `session["search_results"] = call_tool`
   without calling it. Fixed by returning `_search_listings_impl(description,
   size, max_price)` and calling `call_tool(...)` with the tool name and
   arguments.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** I added a second branch to the parse step in
`agent.py::run_agent`. Before, if the model couldn't be reached while
parsing the query, the run stopped right there. Now it catches
`ModelUnavailable` and falls back to a new function,
`agent.py::_parse_query_regex`, which pulls the size (`size XXS`) and max
price (`under $5`) out with regex and uses the leftover words as the
description. The search doesn't use the model, so it can run either way.

**Which failure it was meant to fix:** In my bad-key before run
(`results/run_2026-10-18_1751_before.md`), every scenario stopped at parsing
with `search_results: 0`, even though `search_listings` doesn't need the
model. Even the impossible query showed the general "model couldn't be
reached" error and never reached my empty-results branch, so the user wasn't
told what to change. My agent depended on the model for a step that didn't
need it.

### Run Log — After

Run with the same bad key, so the model was down for
every try.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5), model down |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item reaches suggest_outfit | 5 of 5 | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| 4. fit card stays under 300 characters | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5), model down |
| 5. model down returns error message | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

- **Criteria 1 and 4:** the search found items in every try, but
  `suggest_outfit` needs the model, so no run reached the fit card. These
  criteria assume a working model, and they missed in the bad-key before run
  too.
- **Criterion 3:** I judge this from the outfit text, and no outfit was
  written, so there's nothing to check.

**Did it help, and how do I know:** Yes, **for the part it was meant to fix.**

Before, the impossible query showed:

```
- stopped early: yes — The model couldn't be reached, so I couldn't finish your request. Check your API key in .env and your internet connection.
- search_results: 0
```

After, the same query with the same bad key showed:

```
[1] search_listings
      in:  dict with keys: description, max_price, size
      out: [] (empty)
  try 1: stopped early — Nothing matched 'designer ballgown' in size XXS under $5. Tr
```

The regex pulled out the same description, size, and price the model did,
so the message is the same one the user gets when the model works.

It didn't fix everything. Matching queries still stop at `suggest_outfit`
because outfits and fit cards still need the model (see What's Still Broken).

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

No criterion is still missed. All five met their targets. These are the
weak spots I know about:

- **The agent still depends on the model after the search.** The regex
  fallback means parsing and searching work without the model, but
  `suggest_outfit` and `create_fit_card` don't. With the model down, a
  matching query finds an item and then stops with the "model couldn't be
  reached" message. What I'd do next: maybe add a template fallback for each one,
  building outfits from the wardrobe items and a caption from the listing's
  title, price, and platform, so the run finishes with plainer results. I
  stopped at parsing because that's the step my diagnosis pointed at, and the
  other two need a separate design.
- **Criterion 3 is checked indirectly.** I judged it from the outfit text,
  not by comparing ids. What I'd do: log the id that `suggest_outfit`
  receives and compare it to `session["selected_item"]["id"]` in the run log.
- **The regex parser keeps filler words.** "looking for a vintage graphic
  tee under $30" becomes the description "looking for a vintage graphic
  tee". The size and price come out right, but the extra words could weaken
  the keyword search. What I'd do: strip common filler phrases before
  searching.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
