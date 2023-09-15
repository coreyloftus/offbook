import json
import os
import string


def welcome():
    print("*********************************************")
    print("I will teach you to...")
    print("LEARN YOUR LINES!!!")
    print("*********************************************")
    print("")


def load_scene_data(filename):
    with open(f"scenes/{filename}", "r") as file:
        return json.load(file)


def list_scenes():
    return [
        f
        for f in os.listdir("scenes")
        if os.path.isfile(os.path.join("scenes", f)) and f.endswith(".json")
    ]


def select_scene():
    scenes = list_scenes()
    print("Select a scene:")
    for index, scene in enumerate(scenes):
        print(f"{index+1}: {scene}")
    choice = int(input("Select scene by number: ")) - 1
    return scenes[choice]


def choose_character(data):
    print("Choose your character: ")
    for index, character in enumerate(data["meta"]["characters"]):
        print(f"{index+1}: {character}")
    choice = int(input("Choose your character by number: ")) - 1
    return data["meta"]["characters"][choice]


def display_scene(data):
    print(f"\n{data['meta']['name']} at {data['meta']['location']}")


def check_line(correct_line, user_line):
    correct_line = correct_line.lower().translate(
        str.maketrans("", "", string.punctuation)
    )
    user_line = user_line.lower().translate(str.maketrans("", "", string.punctuation))

    # Check for a perfect match
    if correct_line == user_line:
        return True

    correct_words = correct_line.split()
    user_words = user_line.split()

    for i, (correct_word, user_word) in enumerate(zip(correct_words, user_words)):
        if correct_word != user_word:
            corrected_part = " ".join(correct_words[: i + 1])
            next_word = correct_words[i + 1]
            return f"{corrected_part} {next_word}"


def run_lines(data, character):
    for line in data["lines"]:
        user_line = ""
        if line["speaker"] != character:
            if line["speaker"] == "Stage Directions":
                print(f"**** {line['text']}")
            else:
                print(f"{line['speaker']}: {line['text']}")
        else:
            while user_line != line["text"]:
                user_line = input(f"{line['speaker']}: ")
                if user_line == "quit":
                    break
                res = check_line(line["text"], user_line)
                if res is True:
                    continue
                else:
                    print(f">>>>>>{line['speaker']}: {res}")


def main():
    welcome()
    selected_file = select_scene()
    data = load_scene_data(selected_file)
    character = choose_character(data)
    display_scene(data)
    run_lines(data, character)


if __name__ == "__main__":
    main()
