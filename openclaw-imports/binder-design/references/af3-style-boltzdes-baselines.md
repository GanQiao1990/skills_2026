# AF3-style / BoltzDes transcript baselines and concise Chinese framing

Use this reference when the user asks what HalluDesign, ProteinHunter, or the broader Double Hallucination pipeline is being compared against in the project review materials, especially the file:
`[English (auto-generated)] How AF3-Style Structure Prediction Models Can Be Used for Design BoltzDes.txt`

## What the transcript is actually benchmarking

Important nuance: in that BoltzDes transcript, HalluDesign is not the main benchmark object by name. The direct baselines discussed there are mainly:

1. `binding-trap` / backpropagation-based design
   - framed as computationally heavy because many backward passes are needed
   - ProteinHunter is introduced as a faster alternative

2. `RFdiffusion all-atom`
   - described as the only existing all-atom diffusion comparison at the time
   - also discussed as a `single diffusion trajectory` style baseline

3. `single-cycle` / `zero-cycle` AF3-style artificial Boltz method
   - contrasted with iterative multi-step optimization
   - the iterative route is presented as giving better solutions than a single zero-cycle pass

4. `AF2 vs AF3`
   - appears as background comparison for prediction behavior, not the cleanest direct HalluDesign baseline for binder-design claims

## Safe Chinese interpretation for user-facing answers

When the user asks "HalluDesign 对比模型是什么", do not overclaim that the transcript contains a single explicit HalluDesign-vs-X benchmark if it does not. Prefer wording like:

- `在这份 BoltzDes 里，HalluDesign 不是单独被命名 benchmark 的核心对象；更直接的 baseline 是 binding-trap/backprop、RFdiffusion all-atom，以及 single-cycle/zero-cycle 的 AF3-style artificial Boltz method。`

## Concise comparison phrases

### HalluDesign short line
- `HalluDesign 序列结构闭合、局部界面精修，提高可表达可折叠性与界面合理性；依赖前序seed质量，搜索范围偏局部，仍需正交验证排除模型偏差。`

### If the user wants a shorter grant-style clause
- `HalluDesign 强于序列结构闭合与局部精修，但依赖前序拓扑种子，广域探索能力有限。`

## Usage note

In short proposal-style comparisons, keep the role split explicit:
- ProteinHunter = broad exploration / cheap proxy first
- HalluDesign = sequence-structure closure / local refinement
- Chai-1 = orthogonal audit / go-no-go validation
