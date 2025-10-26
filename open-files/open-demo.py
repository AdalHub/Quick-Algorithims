import os
FILE_NAME= "notes.txt"

def ensure_note():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            f.write("")


def write_note(message):
    with open(FILE_NAME, "a") as f:
        f.write(message)
        print(f"{message} appended successfully")


def read_note():
    char_to_read=10
    with open(FILE_NAME, "r") as f:
        content = f.read(char_to_read)
        while len(content) > 0:
            print(content, end="*")
            content= f.read(char_to_read)
def main():
    ensure_note()
    write_note("I like pie so much i ended up eating like 20 pies in one sitting lmao isnt that interesting would you like to know more about my pie eating habits")
    read_note()

if __name__ == "__main__":
    main()