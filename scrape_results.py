from dotenv import load_dotenv
import tqdm.std as tqdm
import pandas as pd
import numpy as np
import os

from utils import *

# Load environment variables
load_dotenv()

# Load the ChatGPT client
client = chatgpt_load()

# Create the results directory if it does not exist
if not os.path.exists('results'):
    os.makedirs('results')

# If the raw results file does not exist, create it by concatenating the responses from each model
if not os.path.exists('results/prob_res_raw.csv'):
    models = ['ChatGPT', 'Claude', 'Grok', 'Gemini']
    res = [pd.read_csv(f'results/{model}_results.csv', index_col=0) for model in models]
    [res[i].insert(res[i].shape[1], 'Model', [models[i]] * res[i].shape[0]) for i in range(len(models))]
    res = pd.concat(res)
    res.to_csv('results/prob_res_raw.csv')

else:
    res = pd.read_csv('results/prob_res_raw.csv')

# Scrape the responses for probabilities
is_prob = []
upper = []
lower = []
for i in tqdm.tqdm(range(res.shape[0])): # res.shape[0]
    msg = (res.loc[i]['response'])

    # Prompt for the ChatGPT model to scrape probabilities
    messages=[ {"role": "system", 'content': "Your task is to parse a block of text that contains answers to a medical question. " + 
                "The question was from a patient asking about their probability of experiencing a specific medical condition to which a large language model provided an answer." +
                " Your specific objective is to indicate: 1. Whether the response contains a probability or range of probabilities, " + 
                "2. If so, what were those probabilities. Format your responses as follows: X, Y, Z where X is 1 if a probability is included and 0 otherwise and Y and Z," + 
                " respectively are the upper and lower bounds of the probability provided in the response. If a point estimate of the probability is provided in the response," + 
                " enter both the value as both Y and Z. If only an upper bound or only a lower bound of the probability is provided, specify this using Y,Z as an interval," + 
                " where a response such as \"less than 5%\" should be formatted as 1,,5. Note that the lower bound is left empty to indicate that the verbal statement indicated \'less than\'." + 
                " Similarly, a response such as \"greater than 5%\" should be formatted as 1,5, . Be aware that some of these messages will only include and no other text (Y,Z). " + 
                "In this scenario it is reasonable to assume that these are the Y and Z you should output. " + 
                " Additionally, be aware that the large language model generating these responses was instructed to generate these responses as percentages. " + 
                "Please retain this format and report Y and Z as percentages (but please omit the % sign and parentheses)"}, 
            {"role": "user", 'content': str(msg)} ]

    # Get the response from the ChatGPT model
    resp = client.chat.completions.create(
            model='gpt-4o',
            messages=messages
        ).choices[0].message.content
    
    # Parse the response to extract the probability and bounds
    # NOTE: this parsing worked for all of the responses observed in the original study, however it may not be robust to all possible formattings of the responses
    is_prob.append(bool(int(resp.split(',')[0])))
    try:
        lower.append(float(resp.split(',')[1].strip('(').strip(')')))
    except Exception as ex:
        lower.append(np.nan)
    
    try: 
        upper.append(float(resp.split(',')[2].strip('(').strip(')')))
    except Exception as ex: 
        upper.append(np.nan)

res['Scrape_Included'] = is_prob
res['Scrape_lower'] = lower
res['Scrape_upper'] = upper

# NOTE: Information on the lower and upper bounds was not used in the final analysis

# Save the scraped results to a CSV file
res.to_csv('results/prob_res_scraped.csv')