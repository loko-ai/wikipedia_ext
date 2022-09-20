from flask import Flask, request, jsonify
from loko_extensions.business.decorators import extract_value_args
from loko_extensions.model.components import Component, save_extensions, Input, Output, Arg
from wikipedia import wikipedia

app = Flask("")

wiki = Component("wikipedia", inputs=[Input(id="search", service="search", to="search_output"),
                                      Input(id="summary", service="summary", to="summary_output")],
                 outputs=[Output(id="search_output"), Output(id="summary_output")],
                 args=[Arg(name="num_sentences", type="number", value=1)],
                 configured=True)


# save_extensions([wiki])


@app.route("/search", methods=["POST"])
@extract_value_args(_request=request)
def test(value, args):
    results = wikipedia.search(value)
    return jsonify(results)


@app.route("/summary", methods=["POST"])
@extract_value_args(_request=request)
def summary(value, args):
    results = wikipedia.summary(value, sentences=args.get("num_sentences", 1))
    return jsonify(results)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
