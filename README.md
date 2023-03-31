<html><p><a href="https://loko-ai.com/" target="_blank" rel="noopener"> <img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /> </a></p>
<h1>Wikipedia</h1><br></html>

**Wikipedia** extension wraps the <a href="https://pypi.org/project/wikipedia/">wikipedia</a> api to search for 
Wikipedia's pages and summaries.

From the **Projects**'s tab, click on **Import from git** and copy and paste the URL of the current page 
(i.e. https://github.com/loko-ai/wikipedia_ext):
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229048981-e03d7b6f-6ef4-4064-8c0e-75052497744a.png" width="60%" /></p>
Once the project is downloaded, click and open it.  
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229051269-af6d7468-61b6-4663-85b8-02ea0ca7ddfb.png" width="80%" /></p>

In order to start the project remember to press the **play** button on the right of the project's name.

You'll find the Wikipedia extension on the bottom of blocks' list. The extension has 2 inputs and 2 outputs. 
The first one implements the *search* of Wikipedia pages, while the second one return a *summary* of a given topic.

Let's now see how to custom the extension. 

Click right on the project's name on *Open in editor* (configure your editor using the Loko's settings first):
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/229053415-a38b930c-9da3-4d28-beb8-87b882e620b9.png" width="80%" /></p>

Otherwise, you can open your project directly on the Loko's directory (i.e. `~/loko/projects/wikipedia_ext`).

First of all, create you **venv**, named venv, and install *requirements.lock*.

### Services

In `/wikipedia_ext/services/services.py` you'll find the wikipedia component:

```
wiki = Component("wikipedia", inputs=[Input(id="search", service="search", to="search_output"),
                                      Input(id="summary", service="summary", to="summary_output")],
                 outputs=[Output(id="search_output"), Output(id="summary_output")],
                 args=[Arg(name="num_sentences", type="number", value=1)],
                 configured=True)


save_extensions([wiki])
```

We are defining all the block's information: *inputs*, *outputs*, *args*. When you run the script, the component will be 
saved as a json into `/wikipedia_ext/services/services.py` and showed in your block's list. 
See more here https://loko-extensions.readthedocs.io/en/latest/.

The input **search** is linked to the service `/search`, while the input **summary** is linked to the service `/summary`:

```
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
```

Parameter *value* represents the input of the block, while *args* represents the configuration of the block 
(e.g. *num_sentences*).

### Dockerfile

Once you prepared your components and the services they are linked to, you have to configure the Dockerfile of your 
container:

```
FROM python:3.10-slim
EXPOSE 8080
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
CMD python services.py

```

When you **stop** your project and click again on the **play** button, Loko builds a new image, and you're ready to use 
your extension. 
