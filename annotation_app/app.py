import json
from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:index>", methods=["GET", "POST"])
def annotate(index=0):
    #resp_types = [None] * 100

    # Load the corresponding JSON data for the image
    #data = load_json(image_name)

    # If the form is submitted, update the labels
    if request.method == "POST":
        true = request.form.getlist(f'prob_true_{index}')
        false = request.form.getlist(f'prob_false_{index}')

        print(true, false)

        prob_present = False
        if true == ['True']:
            prob_present = True
        elif false is None:
            raise ValueError("THIS SHOULDN'T HAPPEN")
        else: 
            prob_present = False

        text.loc[index, 'Prob_Included_Human'] = prob_present
        
        text.to_csv('annotation.csv')
        # TODO: 
        # Redirect to the next statement
        return redirect(url_for("annotate", index=index + 1))

    # Progress calculation
    progress = (index + 1) / text.shape[0] * 100

    # Find next unlabeled item
    next_unlabeled_index = index + 1#find_next_unlabeled_item(index, image_text_pairs)
    previous_index = index - 1 if index > 0 else None


    # Serve the current image and claims
    return render_template(
        "index.html",
        index=index,
        text=text,
        total=text.shape[0],
        progress=progress,
        next_unlabeled_index=next_unlabeled_index,
        previous_index=previous_index,
    )

if __name__ == "__main__":
    
    # Path to the directories containing images and text files
    text = pd.read_csv('annotation.csv', index_col=0)
    if 'Prob_Included_Human' not in text.columns.values.tolist():
        text['Prob_Included_Human'] = None

    app.run(debug=True)
