from calendar import month_name
from dataclasses import dataclass
from pathlib import Path
from typing import IO

from PyPDF2 import PdfReader


def extract_text_from_pdf(
    pdf_file: Path | str,
    n_page: int = 1,
    absent_txt_to: str = 'Assignment',
) -> list[str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PdfReader(pdf, strict=False)
        pdf_text = []

        for page in reader.pages[:n_page]:
            txt = page.extract_text()
            if txt:
                pdf_text.append(txt)
            else:
                pdf_text.append(absent_txt_to)

    return pdf_text


@dataclass
class PathParser:
    root_path: Path
    month: str

    def __post_init__(self):
        # Validate month name
        if self.month not in month_name:
            raise ValueError(f"'month' must be in {month_name}")

    def month_dir_path(self, path: Path) -> Path:
        for i in path.iterdir():
            if i.name == self.month:
                return i
        else:
            raise FileNotFoundError(
                f'Required month dir not found on {path.name!r}.'
            )

    def date_dirs(self, month_dir: Path) -> list[Path]:
        return [date for date in month_dir.iterdir() if date.is_dir()]

    def pdf_paths(self) -> list[Path]:
        months_dir = self.month_dir_path(self.root_path)
        dates_dir = self.date_dirs(months_dir)
        pdf_paths = [f for date in dates_dir
                     for f in date.iterdir()
                     if f.suffix == '.pdf']
        return pdf_paths


@dataclass
class ReadmeWriter:
    file_obj: IO

    def write_header(self, month: str):
        lines = [
            f'# 🗂️ Assignments of {month}\n',
            '\n',
        ]
        self.file_obj.writelines(lines)

    def write_bullet_points(
        self,
        pdf_paths: list[Path],
        month: str
    ) -> None:
        """ Write the unordered list points in passed readme file. """
        pdf_paths = sorted(pdf_paths, key=lambda x: int(x.name[:2]))
        dates = [i.name[:2] for i in pdf_paths]

        # Get the assignments_name from all pdf
        assignments_name = []
        for pdf_path in pdf_paths:
            txt = extract_text_from_pdf(pdf_path)
            assignments_name.append(
                txt[0].replace('Assignment Questions', '')
                .replace('\n', '')
                .strip()
            )

        # Create markdown bullet points
        lines = []
        for date, name, pdf_path in zip(dates, assignments_name, pdf_paths):
            parent_path = pdf_path.parent.name.replace(' ', '%20')
            bullet = f'- **{date} {month} :** [**`{name}`**]({parent_path})\n'
            lines.append(bullet)

        self.file_obj.writelines(lines)


@dataclass
class Readme:
    root_path: Path
    month: str

    def __post_init__(self):
        self.path_parser = PathParser(self.root_path, self.month)

    @property
    def readme_path(self) -> Path:
        return self.root_path / self.month / 'README.md'

    def write(self) -> None:
        with open(self.readme_path, 'w') as f:
            readme_parser = ReadmeWriter(f)
            readme_parser.write_header(self.month)
            readme_parser.write_bullet_points(
                self.path_parser.pdf_paths(),
                self.month
            )
