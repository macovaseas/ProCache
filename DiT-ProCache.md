## DiT-ProCache

### 1. Prepare Environment

```bash
cd DiT-ProCache
conda env create -f environment.yml
conda activate DiT
pip install flash-attention
```

### 2. Download Checkpoints

Follow the official documentation to download the required model checkpoints.

### 3. Sample Patterns

Run the pattern sampling script:

```bash
python CASS.py
```

Copy the generated patterns into `cache_functions/cal_type.py`:

```python
s_1 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
...
s_5 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] == (current['num_steps'] - 1))    
    step_index = current['step']
    is_cache_step = s[step_index]
    threshold = 21
    
    if first_step:
        current['type'] = 'full'
    else:
        if is_cache_step == 1:
            current['type'] = 'full'
        elif is_cache_step == 0:
            current['type'] = 'FORA'
        elif is_cache_step == 2:
            if current['layer'] < threshold:
                current['type'] = 'FORA'
            else:
                current['type'] = 'ToCa'
        else:
            current['type'] = 'FORA'
```

### 4. Proxy Evaluation

For each candidate pattern, run DDP inference on a small sample set:

```bash
torchrun --nnodes=1 --nproc_per_node=1 sample_ddp.py \
  --model DiT-XL/2 \
  --image-size 256 \
  --cfg-scale 1.5 \
  --ddim-sample \
  --num-sampling-steps 50 \
  --num-fid-samples 1000
```

This generates a sample folder and a `.npz` file. Use [ADM's TensorFlow evaluation suite](https://github.com/openai/guided-diffusion/tree/main/evaluations) to compute FID, Inception Score, and other metrics.

### 5. Full Evaluation

Select the best-performing pattern, replace it with the `injected` version: 

```python
s_1_injected = [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
```

Then run the full evaluation:

```bash
torchrun --nnodes=1 --nproc_per_node=1 sample_ddp.py \
  --model DiT-XL/2 \
  --image-size 256 \
  --cfg-scale 1.5 \
  --ddim-sample \
  --num-sampling-steps 50 \
  --num-fid-samples 50000
```
