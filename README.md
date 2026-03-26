# File Mover & Organizer

A Python-based desktop application that automatically sorts files from a source folder (like Downloads) into categorized directories (Documents, Images, Music, Videos) based on file type and age.

## How to Use
### For Users (No Python needed)
If you just want to use the tool, download the latest version from the **[Releases](https://github.com/Cabralv0309/file-mover/releases/tag/v1.0.0)** section.
1. Download `file_mover.exe`.
2. Run the application (Windows may show a "SmartScreen" warning; click 'More Info' -> 'Run Anyway').

### For Developers
If you have Python installed:
1. Clone this repository.
2. Run `python file_mover.py`.

### DEBUG
Should you wish to practice or safely test the script without affecting your real files, use the included utility scripts:

1. Set `DEBUG = True` in `file_mover.py`.
2. Run `folder_populator.py` to generate a set of dummy test files.
3. Run `file_mover.py` to see the sorting in action.
4. Run `folder_cleaner.py` to reset the environment for the next test.

## Features
* **Smart Sorting:** Categorizes files using `mimetypes` and custom extension backups.
* **Time Filtering:** Only moves files created within a specific number of Days or Hours.
* **GUI Interface:** Built with `tkinter` for a simple, user-friendly experience.

## Handled Extensions
* ***Documents:** .pdf, .docx, .txt, .pptx |
* **Images:** .jpg, .png, .gif, .bmp |
* **Audio/Video:** .mp3, .wav, .mp4, .mkv |

## Built With
* Python 3.13.5
* PyInstaller (for executable generation)

## Author
**Victor Cabral** - *March 2026*