# Github Repo for the paper tentatively titled "Large Language Models are Inconsistent Communicators of Medical Probabilities"


This repository contains the code needed to reproduce the results of the paper tentatively titled "Large Language Models are Inconsistent Communicators of Medical Probabilities". 

## Installation

First download and set up the repo

```sh
git clone https://github.com/nicholas-j-jackson/LLM-Medical-Prob.git
cd LLM_Medical_Probabilities
```

The [environment.yml](https://github.com/nicholas-j-jackson/fast-DiT/LLM-Medical-Prob/main/environment.yml) file can be used to create the conda environment used for this study.

```sh
conda env create -f environment.yml
conda activate llm_med_prob
```

## Running LLMs

1. Create a .env file that contains the API Keys for your OpenAI, Google AI, xAI, and anthropic accounts. 
2. Run main.py <model_name> <require_prob_only> where <model_name> is either ChatGPT, Gemini, Grok, or Claude and <require_prob_only> is 0 or 1, with 1 indicating you'd like to add a system prompt to require the LLM to answer only with a probability. To fully reproduce this study, the run the batch script experiment.sh.


## Analysis
1. After running the experiments with <require_prob_only> set to 0. Run the command: 

```sh
python scrape_results.py
```
Which uses GPT-4o to identify whether the LLM responses generated from main.py provided their answer in the form of a probability. Due to potential ambiguity in responses and the risk of hallucinations, this was then checked by two study authors in the "Manual Validation" section.


2. The notebook Analysis.ipynb:

- Aggregates all of the results files created from main.py with <require_prob_only> set to 0 and saves these as results_forced.csv
-  Computes basic readability measures and adds them to 'prob_res_scraped.csv', which is then saved as 'results_and_readability.csv'
- Samples 100 responses to be manually validated in the "Manual Validation" section.
- Produce the main figures and numbers used in the paper.

### NOTE: 
The results currently stored in the 'results' folder are those used in the study, but will be over-written if any of the above code is run.

## Manual Validation
To start the simple web app used for the manual annotation process, run: 

```sh
cd annotation_app
python app.py
```

Then go to http://127.0.0.1:5000 in any browser and follow the instructions. The results of this process will be stored in annotation_app/annotation.csv under the column "Scrape_Included"


## Authors

Nicholas Jackson | [Google Scholar](https://scholar.google.com/citations?user=ve19UQsAAAAJ&hl=en)

Katerina Andreadis | [Google Scholar](https://scholar.google.com/citations?hl=en&user=YOPCdI4AAAAJ&view_op=list_works&sortby=pubdate)

Jessica Ancker | [Website](https://www.vumc.org/dbmi/person/jessica-s-ancker-phd-mph-facmi) | [Google Scholar](https://scholar.google.com/citations?user=zW3gRmUAAAAJ&hl=en)

## Citation 

### TBD