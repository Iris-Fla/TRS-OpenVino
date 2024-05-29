import gradio as gr
# import run_seg
import run_stablediffusion
# demo = gr.Interface(
#     run_seg.run_grounding_sam,
#     [
#         gr.Image(),
#         gr.Dropdown(["det", "seg"], value="seg", label="task_type"),
#         gr.Textbox(value="bears", label="Text Prompt"),
#     ],
#     additional_inputs=[
#         box_threshold,
#         text_threshold,
#     ],
#     outputs=gr.Gallery(preview=True, object_fit="scale-down"),
#     examples=[
#         [f"{run_seg.ground_dino_dir}/.asset/demo2.jpg", "seg", "dog, forest"],
#         [f"{run_seg.ground_dino_dir}/.asset/demo7.jpg", "seg", "horses and clouds"],
#     ],
#     additional_inputs_accordion=advanced,
# )
def generate_from_text(text, negative_text, seed, num_steps, _=gr.Progress(track_tqdm=True)):
    result = run_stablediffusion.ov_pipe(text, negative_prompt=negative_text, num_inference_steps=num_steps, seed=seed)
    return result["sample"][0]

with gr.Blocks() as demo:
    with gr.Tab("Text-to-Image generation"):
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(lines=3, label="Positive prompt")
                negative_text_input = gr.Textbox(lines=3, label="Negative prompt")
                seed_input = gr.Slider(0, 10000000, value=751, label="Seed")
                steps_input = gr.Slider(1, 50, value=20, step=1, label="Steps")
            out = gr.Image(label="Result", type="pil")
        sample_text = (
            "futuristic synthwave city, retro sunset, crystals, spires, volumetric lighting, studio Ghibli style, rendered in unreal engine with clean details"
        )
        sample_text2 = "RAW studio photo of tiny cute happy  cat in a yellow raincoat in the woods, rain, a character portrait, soft lighting, high resolution, photo realistic, extremely detailed"
        negative_sample_text = ""
        negative_sample_text2 = "bad anatomy, blurry, noisy, jpeg artifacts, low quality, geometry, mutation, disgusting. ugly"
        btn = gr.Button()
        btn.click(
            generate_from_text,
            [text_input, negative_text_input, seed_input, steps_input],
            out,
        )
try:
    demo.queue().launch(debug=True)
except Exception:
    print("Exception")