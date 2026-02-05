import itertools

top = ["lhr", "lhh", "hhr", "hhh"]
middle = ["lpr", "lpp", "ppr"]
bottom = ["lfr", "lff", "ffr", "fff"]


# Combine all layout variations
# top-middle-bottom
# e.g. "lhr-lpr-lfr", "lhr-lpr-lff", etc.


# Mapping from abbreviations to full grid area names
area_map = {"l": "left", "h": "header", "p": "page", "f": "footer", "r": "right"}


def code_to_areas(code):
    """Convert a three-letter code to grid-template-areas string"""
    return " ".join(area_map[letter] for letter in code)


# Generate all possible combinations
combinations = list(itertools.product(top, middle, bottom))

# Format as strings with dashes
formatted_combinations = ["-".join(combo) for combo in combinations]

# Print all combinations
for combo in formatted_combinations:
    print(combo)

print(f"\nTotal combinations: {len(formatted_combinations)}")

# Generate SCSS for each combination
print("\n// SCSS Grid Template Areas:")
for combo in combinations:
    top_code, middle_code, bottom_code = combo
    combo_str = "-".join(combo)

    scss = f"""&.{combo_str} {{
  grid-template-areas:
    "{code_to_areas(top_code)}"
    "{code_to_areas(middle_code)}"
    "{code_to_areas(bottom_code)}";
}}"""
    print(scss)

# Each combination results in a grid-template-areas like:
# Example output:
#   &.lhr-lpr-lfr {
#     grid-template-areas:
#       "left header right"
#       "left page right"
#       "left footer right";
#   }
