import pandas as pd


def generate_subtables(table: pd.DataFrame, no_cols: int) -> list[pd.DataFrame]:
    """Split a 'wide' pandas dataframe into subtables based on a specified number of columns,
       with repeating rows.

    Args:
        table (pd.DataFrame): table to be split into subtables
        No_Cols (int): number of columns per subtable

    Returns:
        list[pd.DataFrame]: list of subtables as dataframes
    """
    # Divide Table up by No_Cols
    cols = len(table.columns)
    no_subtables, remainder = divmod(cols, no_cols)

    # Get Remainder Columns
    end_table = table.iloc[:, -remainder:]

    # Add SubTables to List
    subtables = []
    for x in range(no_subtables):
        subtables.append(table.iloc[:, x*no_cols:no_cols*(x+1)])
    subtables.append(end_table)

    return subtables


def latex_subtables(subtables: list[pd.DataFrame]) -> list[str]:
    """Convert list of subtables as pandas dataframes into LaTex strings.

    Args:
        subtables (list[pd.DataFrame]): list of subtables.

    Returns:
        list[str]: subtables converted into LaTeX strings.
    """
    return [st.to_latex() for st in subtables]


def wrap_table(latex_tables: list[str], container: str) -> list[str]:
    """Wraps each table in a begin and end statement.

    Args:
        latex_tables (list[str]): subtables as LaTeX strings.
        container (str): container to wrap e.g. landscape.

    Returns:
        list[str]: LaTeX subtables wrapped in a container.
    """
    return [f"\\begin{{{container}}}\n{lt}\\end{{{container}}}\n" for lt in latex_tables]


def insert_command(latex_tables: list[str], command: str, row: int) -> list[str]:
    """Inserts a command into a table at a given line.

    Args:
        latex_tables (list[str]): subtables as LaTeX strings.
        command (str): command to insert. e.g., \centering. For latex commands use double backslash.
        row (int): row of table to insert command. 0 is first row of table.

    Returns:
        list[str]: LaTeX subtables with command inserted.
    """
    latex_table_new = []
    for sub_table in latex_tables:
        row_split = sub_table.split("\n")  # split by row
        top_rule = [i for i in range(len(row_split)) if row_split[i] == "\\toprule"]  # find top of table
        row_split.insert((top_rule[0]+row), command)  # insert command
        st_new = "\n".join(row_split)  # reconstruct table
        latex_table_new.append(st_new)

    return latex_table_new


def combine_subtables(latex_tables: list[str]) -> str:
    """Join subtables in a list into a single string. Seperates each table by a \newpage command.

    Args:
        LatexTables (list[str]): LaTeX subtables.

    Returns:
        str: LaTeX subtables as a single string.
    """
    new_page = [f"\\newpage\n{lt}" for lt in latex_tables]
    joined = "".join(new_page)

    return joined


def wide_table(
    table: pd.DataFrame,
    no_cols: int,
    landscape=True,
    center=True,
    midrules=None) -> str:
    """Wrapper for functions to create a series of LaTeX subtables from a single wide table.

    Args:
        WideTable (pd.DataFrame): Wide table to split into subtables.
        No_Cols (int): Number of columns in a subtable.
        Landscape (bool, optional): Wrap each subtable in a landscape container. Defaults to True.
        MidRule (list[int], optional): row indexes to draw a midrule at. 0 is above the top row. Defaults to None.

    Returns:
        str: LaTeX code to create subtables.
    """
    subtables = generate_subtables(table, no_cols)

    latex_tables = latex_subtables(subtables)

    if center:
        latex_tables = wrap_table(latex_tables, "table")
        latex_tables = insert_command(latex_tables, "\\centering", 0)

    if landscape:
        latex_tables = wrap_table(latex_tables, "landscape")

    if midrules is None:
        midrules = []
    for count, mr in enumerate(midrules):
        latex_tables = insert_command(latex_tables, "\\midrule", mr+count)

    combined = combine_subtables(latex_tables)

    return combined
