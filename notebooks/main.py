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
def _(selected_path_0, selected_path_180):
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
    low_res_img_180_flipped = np.fliplr(low_res_img_180)

    x_axis = np.linspace(0, img_0.shape[1], new_shape[1])
    y_axis = np.linspace(0, img_0.shape[0], new_shape[0])

    import plotly.express as px

    # Blend the two images: average of 0° and flipped 180°
    blended = (low_res_img_0.astype(np.float32) + low_res_img_180_flipped.astype(np.float32)) / 2.0

    fig = px.imshow(blended, x=x_axis, y=y_axis, color_continuous_scale="gray", binary_string=True, origin="upper")
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=True)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=True,
                      scaleanchor="x", scaleratio=1)
    fig.update_layout(
        height=900,
        width=1600,
        title_text="0° and 180° (flipped) overlay",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    fig
    return


if __name__ == "__main__":
    app.run()
