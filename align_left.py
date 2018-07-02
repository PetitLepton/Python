def align_left(df, row_heading=False, columns=None):
    '''This function aligns the column headers to the left as well
    as the elements of the columns provided by columns_left or the
    index column.

    Args:
        df (pandas.DataFrame): the input DataFrame
        row_heading (bool, default False): if True, align left the
            index column
        columns_left (list, default None): list of columns to align left
    Returns:
        pandas.io.formats.style.Styler'''

    left_text = dict(props=[('text-align', 'left')])
    right_text = dict(props=[('text-align', 'right')])

    styles = [
        dict(selector='th.col_heading', **left_text),
        dict(selector='th.index_name', **left_text), ]
    if row_heading:
        styles.append(dict(selector='th.row_heading', **left_text))
    else:
        styles.append(dict(selector='th.row_heading', **right_text))
    if not columns:
        columns = []

    return df.style.set_table_styles(styles).applymap(
        lambda s: 'text-align: left', subset=columns)
