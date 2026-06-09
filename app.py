import gradio as gr

from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide — ACC CS Professor Reviews")
    gr.Markdown(
        "Ask about teaching style, communication, workload, or exams. "
        "Answers come only from real student reviews."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Which professor doesn't respond to emails?",
    )
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
