# Amino Acid Production Strategy Analysis from Literature

Systematic approach to extracting gene regulation strategies and production results from PubMed literature.

## Workflow

### 1. Paper Filtering
Filter for amino acid production papers using keyword matching:
```python
aa_keywords = ['amino acid', 'threonine', 'lysine', 'valine', 'leucine', 'isoleucine',
               'phenylalanine', 'tryptophan', 'tyrosine', 'alanine', 'glutamate', 'glutamic',
               'aspartate', 'arginine', 'histidine', 'proline', 'serine', 'glycine', 
               'cysteine', 'methionine', 'glutamine', 'ornithine', 'citrulline']
```

### 2. Strategy Classification
Categorize papers by engineering strategy:
- **Metabolic Engineering**: pathway modifications, gene knockouts/overexpression
- **Fermentation**: fed-batch, batch, continuous culture optimization
- **Systems Engineering**: genome-scale models, omics integration
- **Transporter Engineering**: efflux pumps, import systems
- **Cofactor Engineering**: NADPH/ATP balance, redox optimization
- **Regulation**: transcription factors, dynamic control, biosensors
- **Tolerance**: stress resistance, product toxicity mitigation

### 3. Gene Extraction Patterns

#### Knockout/Deletion Genes
```python
knockout_patterns = {
    'ΔldhA': r'\bldhA\b.*\b(delet|knockout|deficien)\b',
    'Δpta-ackA': r'\bpta.ackA\b.*\b(delet|knockout)\b',
    'ΔadhE': r'\badhE\b.*\b(delet|knockout)\b',
    'ΔpflB': r'\bpflB\b.*\b(delet|knockout)\b',
}
```

#### Overexpression Genes
```python
overexpression_patterns = {
    'lysC': r'\blysC\b.*\boverexpress',
    'thrA': r'\bthrA\b.*\boverexpress',
    'aroG': r'\baroG\b.*\boverexpress',
}
```

### 4. Production Titer Extraction
```python
titer_pattern = re.compile(r'(\d+\.?\d*)\s*(g/L|g·L⁻¹|g l⁻¹)\b', re.IGNORECASE)
```

## Common Gene Targets by Amino Acid

### Lysine
- **Knockouts**: dapC, lysR, thrR
- **Overexpression**: lysC, asd, dapA, dapB, lysA
- **Transport**: lysE (exporter)

### Threonine
- **Knockouts**: thrR, ilvA
- **Overexpression**: thrA, thrB, thrC
- **Transport**: rhtA, rhtB, rhtC

### Aromatic AAs (Tyr, Phe, Trp)
- **Knockouts**: tyrR, trpR
- **Overexpression**: aroG, aroF, aroH, tyrA, pheA, trpE
- **Transport**: yddG

### Arginine
- **Knockouts**: argR
- **Overexpression**: argA-H (full pathway)

### Glutamate Family
- **Knockouts**: gltA (downregulate TCA)
- **Overexpression**: gdhA, glnA, gltB, proB, proA
- **Cofactor**: pntAB, zwf (NADPH)
