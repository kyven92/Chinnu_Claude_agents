"""Interactive conflict resolution prompt."""


def prompt_conflict(file: str, action_choices: list, default: str, yes: bool = False) -> str:
    if yes:
        return default

    labels = "/".join(
        f"[{c[0]}]{c[1:]}" if c else c for c in action_choices
    )
    print(f"\nConflict: {file}")
    print(f"  Options: {labels}  (default: {default})")

    while True:
        raw = input("  Choice: ").strip().lower()
        if not raw:
            return default
        for choice in action_choices:
            if raw == choice[0] or raw == choice:
                return choice
        print(f"  Invalid — enter one of: {', '.join(action_choices)}")
