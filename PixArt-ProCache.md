## PixArt-alpha-ProCache

### 1. Prepare Environment

```bash
cd PixArt-alpha-ProCache
conda env create -f environment-pixart.yml
```

### 2. Download Checkpoints

Follow the official documentation to download the required model checkpoints.

### 3. Sample Patterns

Run the pattern sampling script:

```bash
python CASS.py
```

Copy the generated patterns into `diffusion\model\cache_functions\global_force_fresh.py`.


### 4. Proxy Evaluation

For each candidate pattern, run DDP inference on a small sample set:

```bash
torchrun --nproc_per_node=1 scripts/inference_ddp.py --image_size 256 --bs 100 --txt_file your_proxy_prompts.txt
```

Use `clip_score.py` to compute the metrics.


### 5. Full Evaluation

Select the best-performing pattern, replace it with the `injected` version, then run the full evaluation:

```bash
torchrun --nproc_per_node=1 scripts/inference_ddp.py --image_size 256 --bs 100 --txt_file COCO_caption_prompts_30k.txt
```