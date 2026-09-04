from pathlib import Path
import subprocess

simulation = "OFF"

def get_special_folder_path(name):
    result = subprocess.run(
        ["powershell", "-command", f"[Environment]::GetFolderPath('{name}')"],
        capture_output=True, text=True
    )
    return Path(result.stdout.strip())


documents_folder = get_special_folder_path("Personal")
documents_folder.mkdir(parents=True, exist_ok=True)  

pdf_folder = documents_folder / "PDF"
pdf_folder.mkdir(parents=True, exist_ok=True)

word_folder = documents_folder / "Word"
word_folder.mkdir(parents=True, exist_ok=True)

text_folder = documents_folder / "Text"
text_folder.mkdir(parents=True, exist_ok=True)

pictures_folder = get_special_folder_path("MyPictures")
pictures_folder.mkdir(parents=True, exist_ok = True)

screenshots_folder = pictures_folder / "Screenshots"
screenshots_folder.mkdir(parents=True, exist_ok = True)

images_folder = pictures_folder / "Images"
images_folder.mkdir(parents=True, exist_ok = True)

def Move_path(path : Path, destination : Path):
    if simulation == "OFF":
        path.rename(destination)
    elif simulation == "ON":
        print(f"Move {path} to {destination}")

def Delete_path(path : Path):
    if simulation == "OFF":
        path.unlink(missing_ok=True)
    elif simulation == "ON":
        print(f"Delete {path}")


RULES = {
    ".pdf": pdf_folder ,
    ".txt": text_folder,
    ".docx": word_folder,
}


for path in documents_folder.iterdir():
    destination_folder = RULES.get(path.suffix.lower())

    if destination_folder is None:
        continue  

    destination = destination_folder / path.name

    if destination.exists():
        Delete_path(path)
    else:
        Move_path(path, destination)
    

    if path.suffix.lower() == ".png" and ((screenshots_folder / path.name).exists() or (images_folder / path.name).exists()) == False: 
        if "Screenshot" in path.name:
            Move_path(path, screenshots_folder / path.name)
        else: Move_path(path, images_folder / path.name)

    elif path.suffix.lower() == ".png" and ((screenshots_folder / path.name).exists() or (images_folder / path.name).exists()) == True:
                Delete_path(path)











