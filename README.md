<div align=center>
  
# [AAAI 2026] *ProCache*: Constraint-Aware Feature Caching with Selective Computation for Diffusion Transformer Acceleration

[![arXiv](https://img.shields.io/badge/arXiv-2512.17298-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2512.17298)
[![AAAI](https://img.shields.io/badge/AAAI-Proceedings-00529b?logo=read-the-docs&logoColor=white)](https://ojs.aaai.org/index.php/AAAI/article/view/39069)

</div>

## Overview

**ProCache** speeds up Diffusion Transformers with *constraint-aware* feature caching and *selective* computation, trading redundant work for quality-preserving inference.

![ProCache](assets/poster.png) 

## 📣 News
* `2026/03/21` 📌 The code has been released.
* `2025/11/08` 💥💥 ProCache is honored to be accepted by AAAI 2026!

## Experiments

To run experiments with ProCache, follow the instructions in the model-specific markdown files in this repository (each backbone has its own guide):

- [DiT-ProCache.md](DiT-ProCache.md) — DiT
- [FLUX-ProCache.md](FLUX-ProCache.md) — FLUX
- [PixArt-ProCache.md](PixArt-ProCache.md) — PixArt-α

## TODO

- [ ] **HunyuanVideo:** We plan to add ProCache-style acceleration for **HunyuanVideo** (text-to-video) in a future release.

## Acknowledgement

ProCache is built upon the awesome [ToCa](https://github.com/Shenyi-Z/ToCa.git) and [TaylorSeer](https://github.com/Shenyi-Z/TaylorSeer.git). We are grateful to the authors for their open releases and for advancing feature caching in diffusion transformers.

## 📌 Citation

```bibtex
@inproceedings{cao2026procache,
  title={ProCache: Constraint-Aware Feature Caching with Selective Computation for Diffusion Transformer Acceleration},
  author={Cao, Fanpu and Chen, Yaofo and You, Zeng and Luo, Wei},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={40},
  number={24},
  pages={19862--19870},
  year={2026}
}
```

## :e-mail: Contact

If you have any questions, please email [`fanpucao@gmail.com`](mailto:fanpucao@gmail.com) or [`chenyaofo@scut.edu.cn`](mailto:chenyaofo@scut.edu.cn).
