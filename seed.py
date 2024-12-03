from pathlib import Path

for i in range(25):
    part_1_py_path = Path(f"day{i+1}.py")
    part_2_py_path = Path(f"day{i+1}-2.py")
    input_path = Path("inputs") / f"{i+1}.txt"

    if not part_1_py_path.exists():
        print(f"Made {part_1_py_path}")
        part_1_py_path.touch()

    if not part_2_py_path.exists():
        print(f"Made {part_2_py_path}")
        part_2_py_path.touch()

    if not input_path.exists():
        print(f"Made {input_path}")
        input_path.touch()

    # append this to every part 1:
    """
    import fileinput
    lines = [line.strip() for line in fileinput.input(files="inputs/{i}.txt")]
    """
    with part_1_py_path.open("w") as part_1_py:
        part_1_py.writelines(
            [
                f"import fileinput\nlines = [line.strip() for line in fileinput.input(files='inputs/{i+1}.txt')]\n"
            ]
        )
