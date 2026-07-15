# Keyword Helper

## Start Here (Windows)

Follow these steps if you are not familiar with programming. You only need to do the setup once.

### 1. Install Python

1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
2. Open the downloaded installer.
3. **Before clicking Install**, check the box that says **Add Python to PATH**.
4. Finish the installation.

### 2. Install Git

1. Download Git from [git-scm.com/downloads](https://git-scm.com/downloads).
2. Open the installer and accept the default options by clicking **Next** until installation finishes.

Git is the tool that copies this project from its online repository to your computer.

### 3. Download (clone) Keyword Helper

1. Open the project page in your browser.
2. Click the green **Code** button, copy the **HTTPS** link, and keep it handy.
3. Open **PowerShell** on Windows (search for "PowerShell" in the Start menu).
4. Move to the folder where you want to keep the project. For example:

   ```powershell
   cd "$HOME\Desktop"
   ```

5. Paste the following command, replacing the text in angle brackets with the HTTPS link you copied:

   ```powershell
   git clone <paste-the-HTTPS-link-here>
   ```

6. Open the new project folder. If the folder is named `keyword-helper`, run:

   ```powershell
   cd keyword-helper
   ```

### 4. Set up and run the app

In the project folder, double-click `setup.bat` once. This installs the app's required pieces automatically.

After setup finishes:

1. Put your Excel `.xlsx` files in the project's `input` folder.
2. Double-click `run.bat` to start Keyword Helper.
3. Follow the on-screen questions to choose a file and worksheet.

You can also run the files from PowerShell:

```powershell
.\setup.bat
.\run.bat
```

If Windows asks whether you want to run a batch file, choose **Run**. To start over with another workbook, place it in `input` and run the app again.

Keyword Helper is an interactive command-line tool for reviewing, marking, cleaning, and exporting keywords in Excel spreadsheets.

It is designed around a simple workflow:

1. Pick an `.xlsx` file from the `input/` folder.
2. Choose one worksheet or merge multiple worksheets.
3. Review the keywords, search for matches, mark them, export a clean sheet, or remove duplicates.
4. Save changes directly back into the same workbook.

## Features

- **Keyword review** - View all keywords in a table with status and statistics.
- **Case-insensitive search** - Find matching keywords by substring.
- **Bulk marking** - Mark search results as relevant, irrelevant, or neutral.
- **Multi-sheet mode** - Work across several worksheets as one merged view.
- **Clean export** - Create a new sheet containing only relevant and unmarked rows.
- **Duplicate removal** - Delete duplicate keywords from a single worksheet.
- **Automatic row movement** - Marked rows (relevant or irrelevant) move to the top while unmarked rows follow; the order within each group is preserved.
- **Auto-save** - Changes are written directly to the workbook.

## Files And Folders

Keyword Helper expects your Excel files to be placed in the `input/` folder. The tool only lists `.xlsx` files from that folder.

The main workbook is edited in place. When you mark rows, remove duplicates, or export a clean sheet, the changes are saved back to the same file.

## How The Scripts Work

The batch files now handle the routine setup and launch steps:

- `setup.bat` creates the local `venv` folder and installs the Python dependencies from `requirements.txt`.
- `run.bat` activates that environment and starts `main.py`.

If you want to run the project manually, you can still do that, but it is no longer required for normal use.

```bat
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Startup Flow

When the app launches, it follows this order:

1. Choose an `.xlsx` file from `input/`.
2. Choose whether to work with a single sheet or multiple sheets.
3. Use the main menu to inspect or modify the data.

If no `.xlsx` files are found, the app exits with a message telling you to add files to `input/`.

## Sheet Selection

You can work in one of two modes:

- **Single sheet** - Select one worksheet and perform actions on that sheet only.
- **Multiple sheets (merged)** - Select several worksheets and treat them as one merged working set for viewing, searching, and exporting.

In multi-sheet mode, matching keywords can be marked across all selected sheets at once.

## Main Menu

After file and sheet selection, the main menu shows these options:

- **View Data** - Show the current keywords and their status.
- **Keyword Search** - Search for a substring and optionally mark the results.
- **Export Clean Sheet (remove irrelevant)** - Create a new sheet without irrelevant rows.
- **Remove Duplicate Keywords** - Delete duplicate keywords from a single sheet.
- **Switch Worksheet(s)** - Pick a different sheet or sheet combination in the same workbook.
- **Switch File** - Load a different workbook from `input/`.
- **Help & Instructions** - Reopen the built-in usage guide.
- **Exit** - Close the tool.

## Detailed Actions

### View Data

This option displays the first column of the active sheet or merged sheet set in a Rich table.

What it shows:

- Keyword text.
- Row number.
- Status indicator.
- Summary statistics for total, relevant, irrelevant, and unmarked rows.

Status colors:

- **Green** means relevant.
- **Red** means irrelevant.
- **Unmarked** means no status color has been applied yet.

If there are more than 500 rows, the view is paginated and you can pick which page to open.

### Keyword Search

This option searches the first column for a case-insensitive substring match.

Search behavior:

- The query is trimmed and compared in lowercase.
- Matches are shown in a results table.
- The matching portion of each keyword is highlighted in the display.
- In single-sheet mode, results come from the active worksheet.
- In multi-sheet mode, results can come from any selected sheet.

After the results are shown, you can choose one of four actions:

- **Mark all as RELEVANT (green)** - Apply green fill to all matching rows.
- **Mark all as IRRELEVANT (red)** - Apply red fill to all matching rows.
- **Mark all as NEUTRAL (unmarked)** - Remove the marking color by applying a neutral fill.
- **Back to menu (no changes)** - Leave the workbook unchanged.

Protection rules:

- A row already marked relevant will not be changed to irrelevant.
- A row already marked irrelevant will not be changed to relevant.
- Neutral is allowed to override any existing mark.

After marking, marked rows are moved to the top and the workbook is saved.

### Export Clean Sheet

This option creates a new worksheet containing cleaned data.

Single-sheet mode:

- The new sheet is based on the active worksheet.
- The header row is copied.
- Relevant and unmarked rows are copied.
- Irrelevant rows are skipped.

Multi-sheet mode:

- The selected sheets are merged into one new sheet.
- The new sheet starts with a single `Keyword` header.
- Relevant and unmarked rows are copied from all selected sheets.
- Irrelevant rows are skipped.

The tool suggests a default sheet name such as `<sheet>_clean` or `merged_clean`, and you can accept it or type your own name.

### Remove Duplicate Keywords

This option is available only in single-sheet mode.

How it works:

- It checks the first column for duplicate keywords.
- Matching is case-insensitive.
- The first occurrence is kept.
- Later duplicates are deleted.

Before deletion, the tool asks for confirmation and shows how many duplicate rows were found.

### Switch Worksheet(s)

Use this to stay in the same file but change what data you are working with.

You can switch between:

- One worksheet.
- A different single worksheet.
- A different multi-sheet selection.

### Switch File

This reloads the file picker so you can open a different `.xlsx` workbook from `input/`.

### Help & Instructions

This reopens the built-in help screen from inside the app. It is useful if you forget the marking rules or need a quick reminder of the workflow.

## Marking Rules

The tool uses worksheet fill colors to store keyword status:

- **Green fill** means relevant.
- **Red fill** means irrelevant.
- **White fill** means neutral or unmarked.

When you mark rows, the tool applies the chosen fill across the entire row, not just the first cell.

Marked rows are then moved to the top so the workbook stays organized.

## Saving Behavior

There is no separate export-save step for the main workbook.

Changes are saved immediately after these actions:

- marking search results,
- exporting a clean sheet,
- removing duplicates.

Because of that, it is a good idea to keep a backup of your original workbook if you want to preserve the untouched version.

## Usage

```bash
run.bat
```

If you start the app manually, the initial workflow is the same:

1. Select your Excel file
2. Choose which sheets to work with
3. Use the menu to view, search, export, deduplicate, switch sheets, or switch files

## Requirements

- openpyxl
- rich
- questionary

## Notes

- The app reads only `.xlsx` files from `input/`.
- The first column is treated as the keyword column.
- Row 1 is treated as the header.
- Multi-sheet mode is best when you want one search or export operation across several worksheets.
