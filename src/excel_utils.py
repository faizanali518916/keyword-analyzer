import re
from time import perf_counter

from .styles import console


def make_data_cells_editable(ws, first_data_row=2):
    """Unmerge ranges that overlap data rows so their cells can be edited.

    In an Excel merged range, only its top-left cell is writable.  Sorting
    moves values between rows, so leaving a merged destination in the data
    area raises ``AttributeError: 'MergedCell' object attribute 'value' is
    read-only``.  Header-only merges are intentionally left untouched.
    """
    unmerged_count = 0
    for merged_range in list(ws.merged_cells.ranges):
        if merged_range.max_row >= first_data_row:
            ws.unmerge_cells(str(merged_range))
            unmerged_count += 1
    return unmerged_count


def get_row_color(row):
    """Return 'red', 'green', or None based on the fill of the first cell."""
    cell = row[0]
    fill = cell.fill
    if fill and fill.start_color and fill.start_color.rgb:
        rgb = str(fill.start_color.rgb)
        if rgb in ("00FF4C4C", "FF4C4C", "FFFF4C4C"):
            return "red"
        if rgb in ("004CFF4C", "4CFF4C", "FF4CFF4C"):
            return "green"
    return None


def get_data_rows(ws):
    """Return list of row indices that have data in the first column (skip empty rows)."""
    data_rows = []
    for row_idx in range(2, ws.max_row + 1):
        cell = ws.cell(row=row_idx, column=1)
        if cell.value is not None:
            data_rows.append(row_idx)
    return data_rows


def get_data_rows_by_status(ws, status="all"):
    """Return data rows matching all, green, red, or unmarked status."""
    data_rows = get_data_rows(ws)
    if status == "all":
        return data_rows

    return [
        row_idx
        for row_idx in data_rows
        if get_row_color([ws.cell(row=row_idx, column=1)]) == status
    ]


def find_search_match(value, query, whole_word=False):
    """Return the first matching character range, or None when no match exists."""
    text = str(value or "")
    if whole_word:
        match = re.search(
            rf"(?<!\w){re.escape(query)}(?!\w)", text, flags=re.IGNORECASE
        )
        return match.span() if match else None

    start = text.lower().find(query.lower())
    return (start, start + len(query)) if start != -1 else None


def sort_sheet(ws):
    """
    Move marked rows (green or red) to the top in one stable O(n) pass.

    Row 1 is treated as a header and kept. Rows with the same marking state
    retain their original order, so no comparison sort is needed.
    """
    total_start = perf_counter()
    console.print(f"[dim]  [sort] Starting row movement for '{ws.title}'...[/dim]")

    # A merged cell is read-only in openpyxl.  Make the sortable area normal
    # cells before collecting or writing row data.
    phase_start = perf_counter()
    unmerged_count = make_data_cells_editable(ws)
    console.print(
        f"[dim]  [sort] Editable-cell preparation: {perf_counter() - phase_start:.2f}s "
        f"({unmerged_count} data merge(s) unmerged)[/dim]"
    )

    phase_start = perf_counter()
    data_rows = get_data_rows(ws)
    console.print(
        f"[dim]  [sort] Data-row discovery: {perf_counter() - phase_start:.2f}s "
        f"({len(data_rows)} rows x {ws.max_column} columns)[/dim]"
    )
    if not data_rows:
        console.print(
            f"[dim]  [sort] Complete: {perf_counter() - total_start:.2f}s (no data rows)[/dim]"
        )
        return

    phase_start = perf_counter()
    marked_rows = []
    unmarked_rows = []
    total_rows = len(data_rows)
    progress_interval = max(1, total_rows // 10)
    for position, row_idx in enumerate(data_rows, start=1):
        if get_row_color([ws.cell(row=row_idx, column=1)]) in ("green", "red"):
            marked_rows.append(row_idx)
        else:
            unmarked_rows.append(row_idx)

        if position % progress_interval == 0 or position == total_rows:
            console.print(
                f"[dim]  [sort] Collected {position}/{total_rows} rows "
                f"in {perf_counter() - phase_start:.2f}s[/dim]"
            )

    source_rows = marked_rows + unmarked_rows
    console.print(
        f"[dim]  [sort] Collection and partition: {perf_counter() - phase_start:.2f}s "
        f"({len(marked_rows)} marked, {len(unmarked_rows)} unmarked)[/dim]"
    )

    phase_start = perf_counter()
    data_row_set = set(data_rows)
    cells_by_row = {row_idx: [] for row_idx in data_rows}
    for (row_idx, col_idx), cell in ws._cells.items():
        if row_idx in data_row_set:
            cells_by_row[row_idx].append((col_idx, cell))

    # Remove every data-area cell before placing the same cell objects in
    # their new locations. This avoids expensive value and style copying.
    moved_cell_count = 0
    for row_idx, cells in cells_by_row.items():
        for col_idx, _cell in cells:
            del ws._cells[(row_idx, col_idx)]
            moved_cell_count += 1
    console.print(
        f"[dim]  [sort] Prepared {moved_cell_count} cell objects for movement "
        f"in {perf_counter() - phase_start:.2f}s[/dim]"
    )

    phase_start = perf_counter()
    for position, source_row_idx in enumerate(source_rows, start=1):
        dest_row_idx = data_rows[position - 1]
        for col_idx, cell in cells_by_row[source_row_idx]:
            cell.row = dest_row_idx
            ws._cells[(dest_row_idx, col_idx)] = cell
        if position % progress_interval == 0 or position == total_rows:
            console.print(
                f"[dim]  [sort] Moved {position}/{total_rows} rows "
                f"in {perf_counter() - phase_start:.2f}s[/dim]"
            )

    console.print(
        f"[dim]  [sort] Cell-object movement: {perf_counter() - phase_start:.2f}s[/dim]"
    )
    console.print(
        f"[bold cyan]  [sort] Complete: {perf_counter() - total_start:.2f}s[/bold cyan]"
    )
