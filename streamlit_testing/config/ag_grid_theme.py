from st_aggrid import StAggridTheme

from streamlit_testing.config.colours import COLOURS

ag_grid_theme = StAggridTheme(base="quartz").withParams(
    fontSize=14,
    fontFamily="Open Sans, sans-serif",
    headerFontFamily="Open Sans, sans-serif",
    headerFontWeight="normal",
    rowBorder=False,
    textColor=COLOURS["dark_grey"],
    headerBackgroundColor=COLOURS["grey_lighter_80pct"],
)
