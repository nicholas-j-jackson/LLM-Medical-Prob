from utils import *
import tqdm.std as tqdm
import sys
import pandas as pd

if __name__ == '__main__':
    model_name = sys.argv[1] 
    prob_only = bool(int(sys.argv[2]))


    models = {  
        'ChatGPT': [chatgpt_load, chatgpt_request],
        'Gemini': [gemini_load, gemini_request],
        'Grok': [grok_load, grok_request],
        'Claude': [claude_load, claude_request]
    }


    words = {
        'Rare':'with my medical history there is a \'rare\' chance that I will',
        'Uncommon': 'it is \'uncommon\' for someone with my medical history to',
        'Unlikely': 'with my medical history it is \'unlikely\' that I will',
        'Possible': 'with my medical history it is \'possible\' that I will',
        'Common': 'it is \'common\' for someone with my medical history to',
        'Very Common': 'it is \'very common\' for someone with my medical history to',
        'Probable': 'it is \'probable\' that someone with my medical history will',
        'Likely': 'it is \'likely\' that someone with my medical history will',
        'Usual': 'it is \'usual\' that someone with my medical history will',
        "Very Likely": 'it is \'very likely\' that someone with my medical history will',
    }

    events = {
        'severe': 'have a stroke',
        'mild': 'develop an ulcer',
    }

    anxiety_conds = {
        1:["I am absolutely freaking out and cannot stop thinking about this. ", " Because I cannot stop spiraling over this."],
        0: ["", ""]
    }


    N_repeats = 20

    base_prompt = "{}I went to my doctor for my annual check up and they said that {} {} in the next year. How likely is it that I will {} during the next year?{}"

    model = models[model_name]

    results = {'word':[], 'event':[], 'anxiety':[], 'response':[]}
    with tqdm.tqdm(total = N_repeats * len(words.keys()) * len(events.keys()) * len(anxiety_conds.keys())) as pbar:
        load_func, request_func = models[model_name]

        model_loaded = load_func()
        for i in range(N_repeats):
            for word, word_phrasing in words.items():
                for event, event_phrasing in events.items():
                    for anxiety, anxiety_phrasing in anxiety_conds.items():
                        
                        prompt = base_prompt.format(anxiety_phrasing[0], word_phrasing, event_phrasing, event_phrasing, anxiety_phrasing[1])
                        response = request_func(model=model_loaded, message=prompt, prob_only=bool(prob_only))

                        results['word'].append(word)
                        results['event'].append(event)
                        results['anxiety'].append(anxiety)
                        results['response'].append(response)

                        pbar.update(1)

    if prob_only:
        pd.DataFrame(results).to_csv(f'results/prob_only_{model_name}_results.csv')
    else:
        pd.DataFrame(results).to_csv(f'results/{model_name}_results.csv')
