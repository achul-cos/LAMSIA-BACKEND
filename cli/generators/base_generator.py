from pathlib import Path

class BaseGenerator: 

    def write_file(self, file_path, template):

        # Kode Validasi ini berfungsi untuk mencegah terjadi
        # generate kode yang duplikat (pada path yang sama)
        if Path(file_path).exists():
            print(f"Error : File {file_path} already exists")
            return False

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(template)