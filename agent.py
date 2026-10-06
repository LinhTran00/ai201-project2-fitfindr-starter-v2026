"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import json

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import generate, ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """

    #       1. Start a session with new_session().
    session = new_session(query, wardrobe)

    #       2. Count the times round the loop, and call trace.check_iterations(count)
    #          on each one before you go again. It raises when the count passes
    #          MAX_ITERATIONS in config.py — see trace.py.
    count = 0
    trace.check_iterations(count)

    #       3. Parse the query into a description, a size, and a max_price. Regex,
    #          string splitting, or asking the model are all fine — say which you
    #          chose in your README. Put the result in session["parsed"].
    count += 1
    trace.check_iterations(count)
    session["parsed"] = parse_query(session["query"])

    #       4. Call search_listings() with what you parsed.
    #          Put the results in session["search_results"].
    count += 1
    trace.check_iterations(count)
    parsed = session["parsed"]
    session["search_results"] = search_listings(
        parsed["description"], parsed["size"], parsed["max_price"]
    )

    #          ⚠️ THIS IS THE BRANCH. If nothing came back:
    #               - put a message in session["error"] saying what the user could
    #                 change — "No results" is not that message
    #               - return the session
    #               - do NOT call suggest_outfit with nothing
    if not session["search_results"]:
        session["error"] = _no_results_message(session["parsed"])
        return session

    #       5. Choose an item — the first result is fine. Put it in
    #          session["selected_item"].
    session["selected_item"] = session["search_results"][0]

    #       6. Call suggest_outfit() with the selected item and the wardrobe.
    #          Put the result in session["outfit_suggestion"].
    count += 1
    trace.check_iterations(count)
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"], session["wardrobe"]
    )

    #       7. Call create_fit_card() with the outfit and the item.
    #          Put the result in session["fit_card"].
    count += 1
    trace.check_iterations(count)
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"], session["selected_item"]
    )

    #       8. Return the session.
    return session


# ── query parsing ─────────────────────────────────────────────────────────────

def parse_query(query: str) -> dict:
    """
    Ask the model to pull a description, size, and max_price out of the query.

    "vintage graphic tee under $30, size M" ->
        {"description": "vintage graphic tee", "size": "M", "max_price": 30.0}

    If the model's answer isn't usable JSON, the whole query becomes the
    description and the filters are skipped, so the search still runs.
    """
    prompt = (
        "Pull the shopping details out of this request.\n"
        f"Request: {query}\n\n"
        "Reply with only a JSON object with these keys:\n"
        '  "description": the item they want, as a few keywords (no size or price)\n'
        '  "size": the size they asked for as written, like "M" or "W30", or null\n'
        '  "max_price": the most they will pay as a number, or null'
    )
    # Temperature 0 because parsing should give the same answer every time.
    reply = generate(prompt, temperature=0.0)

    try:
        # The model sometimes wraps JSON in ```json fences. Take what's between the braces.
        data = json.loads(reply[reply.index("{"): reply.rindex("}") + 1])
        max_price = data.get("max_price")
        return {
            "description": str(data.get("description") or query),
            "size": data.get("size") or None,
            "max_price": float(max_price) if max_price is not None else None,
        }
    except (ValueError, TypeError):
        return {"description": query, "size": None, "max_price": None}


def _no_results_message(parsed: dict) -> str:
    """Say what was searched for and what the user could change."""
    searched = f"'{parsed['description']}'"
    tips = ["use different keywords"]
    if parsed["size"]:
        searched += f" in size {parsed['size']}"
        tips.append("pick another size")
    if parsed["max_price"] is not None:
        searched += f" under ${parsed['max_price']:.0f}"
        tips.append("raise your max price")
    if len(tips) > 1:
        tips[-1] = "or " + tips[-1]
    return f"Nothing matched {searched}. Try to {', '.join(tips)}."


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   \n{session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look the same,\nthe branch isn't doing anything yet."
    )
