"""The Funniest Excuse for Skipping a Meeting — make.fun entry.

Writes a single excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt: the
owner's laptop updated itself into a brick mid-morning, so the owner
is stuck negotiating with it in a language neither of them speaks —
and the meeting will have to carry on without them. Only the Python
standard library is used.
"""

import os
import sys

EXCUSE_LINE = "I can't make the meeting — my laptop updated itself into a brick, and I'm currently negotiating with it in a language I don't speak."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def validate_line(text):
    """Return the line once it passes the sealed gate, else raise.

    The gate counts UTF-8 characters, not bytes; the line must be a
    single line, not only whitespace, with no trailing newline in the
    output file and no control characters anywhere in it.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text or not text.strip():
        raise ValueError("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} gate"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def describe_line(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so a line with a wide
    character (like the em dash here) reads longer in bytes than in
    characters. Returns a one-line human-readable summary.
    """
    chars = len(text)
    byte_count = len(text.encode("utf-8"))
    words = len(text.split())
    return (
        f"{chars} characters, {byte_count} UTF-8 bytes, {words} words"
    )


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = validate_line(EXCUSE_LINE)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {path} ({describe_line(line)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
