## FLUX-ProCache

### 1. Prepare Environment

```bash
conda create -n flux python=3.10
conda activate flux
pip install -e ".[all]"
```

### 2. Download Checkpoints

Follow the official documentation to download the required model checkpoints.

### 3. Sample Patterns

Run the pattern sampling script:

```bash
python CASS.py
```

Copy the generated patterns into `src/flux/modules/cache_functions/cal_type.py`.


### 4. Proxy Evaluation

For each candidate pattern, run DDP inference on a small sample set:

```bash
python src/sample.py --prompt_file </path/to/your/proxy_prompt.txt> \
  --width 1024 --height 1024 --model_name flux-dev \
  --add_sampling_metadata --output_dir </path/to/your/generated/samples/folder> --num_steps 50
```

Use [ImageReward](https://github.com/zai-org/ImageReward) to compute the metrics.


### 5. Full Evaluation

Select the best-performing pattern, replace it with the `injected` version, then run the full evaluation:

```bash
python src/sample.py --prompt_file </path/to/your/full_prompt.txt> \
  --width 1024 --height 1024 --model_name flux-dev \
  --add_sampling_metadata --output_dir </path/to/your/generated/samples/folder> --num_steps 50
```

### 6. Sampling with FLUX-ProCache

Interactive Sampling (Should Download Extra NSFW Classifier)

```bash
python -m flux --name <name> --loop
```

Single Sample Generation (Should Download Extra NSFW Classifier)

```bash
python -m flux --name <name> \
  --height <height> --width <width> \
  --prompt "<prompt>"
```