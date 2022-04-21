# The repository

To clone the project, you must add **--recursive** at the end of the command.

# The environment 

You will find the environment info in the environment.yml file, you can directly create your environment by running : 
```bash
conda env create -f environment.yml
```

# Updating the documentation

First, if you haven't already, run:
```bash
cd ~/ParlAI; python setup.py develop
```
You might need to rebuild the vqa-maskrcnn-benchmark package as well : 
```bash
cd vqa-maskrcnn-benchmark; python setup.py develop
```

# Launch the script 

To run your script, use this command :

```bash
python parlai/scripts/safe_interactive.py -t blended_skill_talk -mf ${PATH_TO_YOUR_MODEL_FILE} --model projects.multimodal_blenderbot.agents:BiasAgent --image-mode faster_r_cnn_152_32x8d --delimiter $'\n' --beam-block-ngram 3 --beam-context-block-ngram 3 --beam-min-length 20 --beam-size 10 --inference beam --model-parallel False
```

The chatbot uses the bear2 image located in projects/multimodal_blenderbot, you can put another picture directly in the code by modifying the path at parlAI/agents/safe_local_human/safe_local_human.py line 116 
