import marimo

__generated_with = "0.21.1"
app = marimo.App(width="full")
app._unparsable_config = {"output_max_bytes": 1_000_000_000}


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    file_browser = mo.ui.file_browser(
        initial_path="data",
        filetypes=[".tiff", ".tif"],
        label="Select the 0° TIFF image",
        multiple=False,
    )
    file_browser
    return (file_browser,)


@app.cell
def _(file_browser, mo):
    mo.stop(len(file_browser.value) == 0, mo.md("**Please select the 0° TIFF image above.**"))
    selected_path_0 = file_browser.value[0].path
    mo.md(f"Selected: `{selected_path_0}`")
    return (selected_path_0,)


@app.cell
def _(mo):
    file_browser_180 = mo.ui.file_browser(
        initial_path="data",
        filetypes=[".tiff", ".tif"],
        label="Select the 180° TIFF image",
        multiple=False,
    )
    file_browser_180
    return (file_browser_180,)


@app.cell
def _(file_browser_180, mo):
    mo.stop(len(file_browser_180.value) == 0, mo.md("**Please select the 180° TIFF image above.**"))
    selected_path_180 = file_browser_180.value[0].path
    mo.md(f"Selected: `{selected_path_180}`")
    return (selected_path_180,)


@app.cell
def _(mo, selected_path_0, selected_path_180):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from skimage.transform import resize
    import tifffile as tiff
    import numpy as np

    img_0 = tiff.imread(selected_path_0)
    img_180 = tiff.imread(selected_path_180)

    scale_factor = 0.25

    new_shape = (int(img_0.shape[0] * scale_factor), int(img_0.shape[1] * scale_factor))
    low_res_img_0 = resize(img_0, new_shape, 
                           anti_aliasing=True,
                           preserve_range=True).astype(img_0.dtype)
    low_res_img_180 = resize(img_180, new_shape, 
                             anti_aliasing=True,
                             preserve_range=True).astype(img_180.dtype)

    x_axis = np.linspace(0, img_0.shape[1], new_shape[1])
    y_axis = np.linspace(0, img_0.shape[0], new_shape[0])

    fig = make_subplots(rows=1, cols=2, subplot_titles=("0°", "180°"))
    fig.add_trace(go.Heatmap(z=low_res_img_0, x=x_axis, y=y_axis, colorscale="gray", showscale=False), row=1, col=1)
    fig.add_trace(go.Heatmap(z=low_res_img_180, x=x_axis, y=y_axis, colorscale="gray", showscale=False), row=1, col=2)
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=True)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=True)
    fig.update_yaxes(scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_yaxes(scaleanchor="x2", scaleratio=1, row=1, col=2)
    fig.update_layout(
        height=900,
        width=1600,
        title_text="0° and 180° Images",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig
    return (fig, img_0, img_180)


if __name__ == "__main__":
    app.run()
