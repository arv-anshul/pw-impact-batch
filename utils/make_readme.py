from pathlib import Path
from typing import IO

from PyPDF2 import PdfReader


def extract_text_from_pdf(
    pdf_file: Path,
    n_page: int = 1,
    absent_txt_to: str = "Assignment",
) -> list[str]:
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (Path): Path to the PDF file.
        n_page (int, optional): Number of pages to extract text from. Defaults to 1.
        absent_txt_to (str, optional): Text to use when PDF text is absent. Defaults to 'Assignment'.

    Returns:
        list[str]: Extracted text from the PDF file.
    """
    with open(pdf_file, "rb") as pdf:
        reader = PdfReader(pdf, strict=False)
        pdf_text = [
            page.extract_text() or absent_txt_to for page in reader.pages[:n_page]
        ]
    return pdf_text


def get_month_dir_path(root_path: Path, month: str) -> Path:
    """
    Finds the directory for a specific month.

    Args:
        root_path (Path): Root directory path.
        month (str): Name of the month.

    Returns:
        Path: Path to the month's directory.
    """
    months_dir = [i for i in root_path.iterdir() if i.name == month]
    if not months_dir:
        raise FileNotFoundError(f"Required month dir not found: {month}")
    return months_dir[0]


def get_pdf_paths(root_path: Path, month: str) -> list[Path]:
    """
    Gets paths of PDF files in a specific month's directory.

    Args:
        root_path (Path): Root directory path.
        month (str): Name of the month.

    Returns:
        list[Path]: List of paths to PDF files.
    """
    month_dir = get_month_dir_path(root_path, month)
    dates_dir = [date for date in month_dir.iterdir() if date.is_dir()]
    pdf_paths = [f for date in dates_dir for f in date.iterdir() if f.suffix == ".pdf"]
    return sorted(pdf_paths, key=lambda x: int(x.name[:2]))


def write_bullet_points(file_obj: IO, pdf_paths: list[Path], month: str):
    """
    Writes bullet points to the given file object.

    Args:
        file_obj (IO): File object to write to.
        pdf_paths (list[Path]): List of paths to PDF files.
        month (str): Name of the month.
    """
    for pdf_path in pdf_paths:
        date = pdf_path.name[:2]
        txt = extract_text_from_pdf(pdf_path)
        assignment_name = (
            txt[0].replace("Assignment Questions", "").replace("\n", "").strip()
        )
        parent_path = f"<{pdf_path.parent.name}>"
        bullet = f"- **{date} {month} :** [**`{assignment_name}`**]({parent_path})\n"
        file_obj.write(bullet)


def generate_readme(month: str, root_path: Path = Path(".")):
    """
    Generates a README file for a specified month.

    Args:
        month (str): Name of the month.
        root_path (Path, optional): Root directory path. Defaults to current directory.
    """
    readme_path = root_path / month / "README.md"
    with open(readme_path, "w") as f:
        f.write(f"# 🗂️ Assignments of {month}\n\n")
        write_bullet_points(f, get_pdf_paths(root_path, month), month)


def main():
    generate_readme("February")


if __name__ == "__main__":
    main()
