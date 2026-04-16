import os


def merge_files(output_name, num_parts):
    os.makedirs("downloads", exist_ok=True)

    output_path = f"downloads/{output_name}"

    with open(output_path, "wb") as final_file:
        for i in range(num_parts):
            part_path = f"temp/part{i}"

            with open(part_path, "rb") as part_file:
                final_file.write(part_file.read())

            os.remove(part_path)

    print("File merged successfully")
