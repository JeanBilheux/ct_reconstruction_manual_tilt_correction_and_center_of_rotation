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
    import plotly.express as px

    img_0 = np.flipud(tiff.imread(selected_path_0))
    img_180 = np.flipud(tiff.imread(selected_path_180))

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

# figure out the tilt by co-registering the two images and calculating the shift between them. This can be done using feature matching or phase correlation methods.
@app.cell
def _(low_res_img_0, low_res_img_180_flipped, np, px):
    from skimage import registration

    # Option A: cross-correlation to find shift automatically
    shift, error, _ = registration.phase_cross_correlation(low_res_img_0, low_res_img_180_flipped)
    print(f"Vertical shift (tilt indicator): {shift[0]:.3f} px")
    print(f"Horizontal shift (COR offset):   {shift[1]:.3f} px")

    # Option B: visual comparison

    from plotly.subplots import make_subplots

    diff = low_res_img_0 - low_res_img_180_flipped

    fig1 = make_subplots(rows=1, cols=3, subplot_titles=("0°", "180° flipped", "Difference"))
    fig1.add_trace(px.imshow(low_res_img_0, color_continuous_scale="gray", binary_string=True).data[0], row=1, col=1)
    fig1.add_trace(px.imshow(low_res_img_180_flipped, color_continuous_scale="gray", binary_string=True).data[0], row=1, col=2)
    fig1.add_trace(px.imshow(diff, color_continuous_scale="RdBu", binary_string=True).data[0], row=1, col=3)
    fig1.update_yaxes(scaleanchor="x", scaleratio=1, col=1)
    fig1.update_yaxes(scaleanchor="x2", scaleratio=1, col=2)
    fig1.update_yaxes(scaleanchor="x3", scaleratio=1, col=3)
    fig1.update_xaxes(matches="x")
    fig1.update_yaxes(matches="y")
    fig1.update_layout(height=400, width=1200, coloraxis_showscale=False)
    fig1




# @app.cell
# def _(blended, x_axis, y_axis, shift, new_shape, img_0, np, px):
#     # Center of rotation in original image coordinates
#     cor_pixel = new_shape[1] / 2 + shift[1]/2  # in low-res pixels
#     cor_x = np.interp(cor_pixel, np.arange(len(x_axis)), x_axis)

#     fig2 = px.imshow(blended, x=x_axis, y=y_axis, color_continuous_scale="gray", binary_string=True, origin="upper")
#     fig2.add_vline(
#         x=cor_x, line_color="red", line_width=2,
#         annotation_text=f"COR = {cor_x:.1f} px",
#         annotation_position="top left",
#         annotation_font_color="red",
#     )
#     fig2.update_xaxes(showgrid=False, zeroline=False, showticklabels=True)
#     fig2.update_yaxes(showgrid=False, zeroline=False, showticklabels=True,
#                       scaleanchor="x", scaleratio=1)
#     fig2.update_layout(
#         height=900,
#         width=1600,
#         title_text="0° and 180° (flipped) overlay with Center of Rotation",
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         coloraxis_showscale=False,
#     )
#     fig2


if __name__ == "__main__":
    app.run()
