# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "altair==6.2.2",
#     "marimo>=0.23.15",
#     "numpy==2.5.1",
#     "pandas==3.0.3",
# ]
# ///

import marimo

__generated_with = "0.23.15"
app = marimo.App(
    width="medium",
    layout_file="layouts/custom.slides.json",
    css_file="custom.css",
    auto_download=["html"],
)

with app.setup:
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt


@app.cell(hide_code=True)
def title():
    mo.md(r"""
    # 🎂 The Birthday Paradox

    ### How many people do you need in a room before **two of them share a birthday**?
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Take a guess 🤔

    - A year has **365 possible birthdays**.
    - So surely you'd need *a lot* of people for a collision...
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    - **50?**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    - **100?**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    - **183?** (half of 365)
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## **23 people!**

    With **23 people**, there is already a **> 50%** chance two share a birthday.

    With **57 people**, it's **> 99%**.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## Count the *pairs*, not the people

    You aren't comparing one person to everyone else, **every pair** is a chance for a match.

    $$\text{pairs} = \binom{n}{2} = \frac{n(n-1)}{2}$$

    - 23 people → **253 pairs**
    - That's a *lot* of chances for a collision.
    """)
    return


@app.cell
def math1():
    mo.md(r"""
    ### Step 1: probability of **no** shared birthday

    Add people one at a time; each new person must dodge every previous birthday:

    $$P(\text{no match}) = \frac{365}{365}\cdot\frac{364}{365}\cdots\frac{365-n+1}{365}$$
    """)
    return


@app.cell
def math2():
    mo.md(r"""
    ### Step 2: flip it around

    $$P(\text{match}) = 1 - P(\text{no match}) = 1 - \frac{365!}{(365-n)!\,\cdot\,365^{\,n}}$$

    Run the computation
    """)
    return


@app.function
def birthday_prob(n: int) -> float:
    """Exact probability that at least two of n people share a birthday."""
    if n < 2:
        return 0.0
    p_no_match = 1.0
    for _k in range(n):
        p_no_match *= (365 - _k) / 365
    return 1.0 - p_no_match


@app.cell
def _():
    n_people = mo.ui.slider(
        2, 80, value=23, label="People in the room", show_value=True
    )
    return (n_people,)


@app.cell
def live(n_people):
    mo.md(f"""
    {n_people}
    ### With **{n_people.value} people** in the room...

    chance of a shared birthday: **{birthday_prob(n_people.value):.1%}**
    """)
    return


@app.cell
def curve(n_people):
    _ns = np.arange(1, 81)
    _curve = pd.DataFrame(
        {"people": _ns, "probability": [birthday_prob(int(_n)) for _n in _ns]}
    )
    _line = (
        alt.Chart(_curve)
        .mark_line(color="#7c3aed", strokeWidth=3)
        .encode(
            x=alt.X("people:Q", title="Number of people"),
            y=alt.Y(
                "probability:Q",
                title="P(shared birthday)",
                axis=alt.Axis(format="%"),
            ),
        )
    )
    _rule = (
        alt.Chart(pd.DataFrame({"people": [n_people.value]}))
        .mark_rule(color="#ef4444", strokeDash=[6, 4])
        .encode(x="people:Q")
    )
    _dot = (
        alt.Chart(
            pd.DataFrame(
                {
                    "people": [n_people.value],
                    "probability": [birthday_prob(n_people.value)],
                }
            )
        )
        .mark_point(size=140, color="#ef4444", filled=True)
        .encode(x="people:Q", y="probability:Q")
    )
    birthday_chart = (_line + _rule + _dot).properties(
        width=640, height=360, title="Probability vs. room size"
    )
    birthday_chart
    return


@app.function
def simulate_birthday(n: int, trials: int = 5000, seed: int = 0) -> float:
    """Fraction of random rooms of n people that contain a shared birthday."""
    _rng = np.random.default_rng(seed)
    _bdays = _rng.integers(0, 365, size=(trials, n))
    _bdays.sort(axis=1)
    _has_match = (np.diff(_bdays, axis=1) == 0).any(axis=1)
    return float(_has_match.mean())


@app.cell
def _():
    slider = mo.ui.slider(1, 10000, value=5000)
    return


@app.cell
def sim_chart_cell():
    _ns2 = np.arange(2, 81, 2)
    trials = 2000
    _sim = pd.DataFrame(
        {
            "people": _ns2,
            "theory": [birthday_prob(int(_n)) for _n in _ns2],
            "simulation": [
                simulate_birthday(int(_n), trials=trials) for _n in _ns2
            ],
        }
    )
    _melt = _sim.melt("people", var_name="source", value_name="probability")
    sim_chart = (
        alt.Chart(_melt)
        .mark_line(point=True)
        .encode(
            x=alt.X("people:Q", title="Number of people"),
            y=alt.Y(
                "probability:Q",
                title="P(shared birthday)",
                axis=alt.Axis(format="%"),
            ),
            color=alt.Color("source:N", title=""),
        )
        .properties(
            width=640, height=360, title=f"Theory vs. {trials}-room simulation"
        )
    )

    sim_chart
    return


@app.cell
def takeaways():
    mo.md(r"""
    ## Takeaways 🎉

    - **23 people → > 50%**, **57 → > 99%** — collisions are cheap once you count *pairs*.
    - The "paradox" is really just $\binom{n}{2}$ growing fast.
    - The same math powers **hash collisions**, **cryptography**, and **load balancing**.
    """)
    return


if __name__ == "__main__":
    app.run()
