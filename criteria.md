# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** my search is a plain keyword match and some phrasings will miss
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** This path is decided by a plain if in run_agent, not by a model. When search_listings returns an empty list, the code stops before suggest_outfit, every time. Nothing random happens after the search, so anything less than 5 of 5 would mean the branch is broken.

<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->


---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

For 5 matching queries, the id of session["selected_item"] is the same as the id of the item passed into suggest_outfit, in 5 of 5 tries.

**Why this target:** Passing selected_item from the session into suggest_outfit is plain code with no model involved, so it should be the same item every time. If the ids ever differ, there's a bug in how the loop passes state. It wouldn't crash, though. It would quietly give an outfit for the wrong item, which is why it needs its own check. Anything less than 5 of 5 means the loop is passing state wrong. 



---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

For 5 different matching items, the fit card is 300 characters or fewer in at least 4 of 5 tries.

**Why this target:** The fit card is written by a model, so an exact length can't be promised, which is why it's 4 of 5 and not 5 of 5. The tool asks for 2 to 4 sentences, and short caption-style sentences add up to roughly 150–300 characters. Anything longer stops reading like a post and starts reading like a product description.



---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

When the model can't be reached, the agent returns a message in session["error"] instead of a stack trace, in 5 of 5 tries.

**Why this target:** Parsing, suggesting an outfit, and creating the fit card all call the model, so none of them can work when it's down. The run has to stop, and the only question is how. Catching ModelUnavailable and writing a message into session["error"] is plain code with no model involved, so it should work every time. Anything less than 5 of 5 means the error handling is broken.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
