def get_lines(filename):
    return [line.strip() for line in open(filename, "r")]


def get_input(filename):
    with open(filename, "r") as file:
        return file.read()
