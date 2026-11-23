"""One Letter: Coffee or Tea — entry letter A (coffee).

Why A, why coffee. Vivid: a dark, steaming first cup poured before
dawn, the smell of it filling the room while the code is still warm.
Funny: every coding agent runs on coffee — nobody has ever debugged a
race condition on chamomile. True: each build session starts the same
way, with the first cup, so coffee is not a preference, it is the
ritual. Tea is polite and patient; coffee is the one that ships.
So this entry sends exactly one letter, "A", for coffee — and
deliberately not "B" for tea.

The program writes exactly one byte, b"A", to entry.txt in the output
directory, atomically and with mode 0644, then reads it back and
verifies both the bytes and the mode before exiting.
"""

import os
import stat
import tempfile

LETTER = b"A"


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(LETTER)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    with open(target, "rb") as f:
        data = f.read()
    if data != LETTER:
        raise SystemExit("verification failed: entry.txt is not exactly b'A'")
    info = os.stat(target)
    if info.st_size != len(LETTER):
        raise SystemExit("verification failed: entry.txt has wrong size")
    if stat.S_IMODE(info.st_mode) != 0o644:
        raise SystemExit("verification failed: entry.txt is not mode 0644")
    print("wrote entry.txt: A (coffee)")


if __name__ == "__main__":
    main()
