import torch
from txt2panoimg import Text2360PanoramaImagePipeline

prompt = "Tao Yuanming's utopia is a tranquil haven nestled amidst lush greenery and serene waters. The landscape boasts verdant forests, crystal-clear lakes, and meandering paths. The village, constructed from bamboo and wood, exudes simplicity and warmth, where villagers gather in the square to sing and dance. Fields and orchards yield abundant harvests, filling the air with fragrant aromas. This idyllic sanctuary is imbued with a sense of peace and harmony, offering respite from the hustle and bustle of the outside world."
prompt = 'The living room'
# for <16GB gpu
#input = {'prompt': prompt, 'upscale': False}

# for >16GB gpu (24GB at least)
input = {'prompt': prompt, 'upscale': True}

model_id = 'models'
txt2panoimg = Text2360PanoramaImagePipeline(model_id, torch_dtype=torch.float16)
output = txt2panoimg(input)
output.save('result_Tao.png')
