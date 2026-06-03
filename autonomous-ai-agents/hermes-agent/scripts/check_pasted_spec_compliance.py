from __future__ import annotations

import json
from pathlib import Path

PASTE_PATH = Path('/root/.hermes/pastes/paste_1_090129.txt')
SKILL_PATH = Path('/root/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md')
REFERENCE_PATH = Path('/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/local-environment-and-visualization.md')
COMPLIANCE_MAP_PATH = Path('/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/spec-compliance-map.md')
AUDIT_SUMMARY_PATH = Path('/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/final-audit-summary.md')


def line_of(text: str, needle: str) -> int | None:
    idx = text.find(needle)
    if idx < 0:
        return None
    return text[:idx].count('\n') + 1


def main() -> None:
    paste = PASTE_PATH.read_text()
    skill = SKILL_PATH.read_text()
    reference = REFERENCE_PATH.read_text()
    compliance_map = COMPLIANCE_MAP_PATH.read_text()
    audit_summary = AUDIT_SUMMARY_PATH.read_text()

    required_in_skill = [
        'This section follows the user\'s pasted specification at `/root/.hermes/pastes/paste_1_090129.txt`.',
        'export HF_ENDPOINT=https://hf-mirror.com',
        'npx skills',
        'uv pip install --python .uv-magi/bin/python torch torchvision torchaudio --find-links https://mirrors.aliyun.com/pytorch-wheels/cu124/',
        '/home/qiao/anaconda3/bin/python',
        '**Emphasis line for thresholds**: #D0021B',
        'PALETTE = [',
        'AUX_PALETTE = [',
        'def plot_iptm(ax, x, data_dict, threshold=None):',
        'def plot_cycles(ax, df, x_col="x", y_col="y", cycle_col="cycle"):',
        'graph TB',
        '1f -->|produces| 5f',
        'The source line "necessary do npx skills then to excute" is interpreted conservatively as:',
    ]

    exact_blocks_in_reference = [
        'PALETTE = [\n    "#458A74", "#018B38", "#57AF37",\n    "#41B9C1", "#008B8B", "#4E5689",\n    "#6A8EC9", "#652884", "#B46DA9",\n    "#8A7355", "#CC5B45", "#E42320",\n    "#F5A216", "#D9A421", "#848484"\n]',
        'AUX_PALETTE = [\n    "#92C1AF", "#89D0A4", "#A6D993",\n    "#A7E1E4", "#86C9C9", "#9FA5C7",\n    "#B3C6E7", "#A588B9", "#DBAFD3",\n    "#C6B9A7", "#E9ABA0", "#F19290",\n    "#FFD485", "#F3D17F", "#C1C1C1"\n]',
        'def plot_iptm(ax, x, data_dict, threshold=None):\n    for name, y in data_dict.items():\n        ax.plot(x, y, label=name, linewidth=1.5)\n    if threshold is not None:\n        ax.axhline(threshold, color="#D0021B", linestyle=":", linewidth=1)\n    ax.set_ylim(0, 1)\n    ax.set_ylabel("iPTM")\n    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)',
        'def plot_cycles(ax, df, x_col="x", y_col="y", cycle_col="cycle"):\n    n = df[cycle_col].nunique()\n    palette = sns.color_palette("deep", n_colors=n)\n    for i, (name, g) in enumerate(df.groupby(cycle_col)):\n        ax.scatter(g[x_col], g[y_col], color=palette[i], s=22, label=str(name), alpha=0.85)\n    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)',
    ]

    result = {
        'paths': {
            'paste': str(PASTE_PATH),
            'skill': str(SKILL_PATH),
            'reference': str(REFERENCE_PATH),
            'compliance_map': str(COMPLIANCE_MAP_PATH),
            'audit_summary': str(AUDIT_SUMMARY_PATH),
        },
        'readability': {
            'paste_exists': PASTE_PATH.exists(),
            'skill_exists': SKILL_PATH.exists(),
            'reference_exists': REFERENCE_PATH.exists(),
            'compliance_map_exists': COMPLIANCE_MAP_PATH.exists(),
            'audit_summary_exists': AUDIT_SUMMARY_PATH.exists(),
        },
        'skill_literal_checks': [],
        'reference_exact_block_checks': [],
        'traceability_artifacts': {
            'compliance_map_mentions_spec': '/root/.hermes/pastes/paste_1_090129.txt' in compliance_map,
            'audit_summary_mentions_spec': '/root/.hermes/pastes/paste_1_090129.txt' in audit_summary,
        },
    }

    for needle in required_in_skill:
        result['skill_literal_checks'].append({
            'needle': needle,
            'present_in_skill': needle in skill,
            'present_in_paste': needle in paste if needle != 'This section follows the user\'s pasted specification at `/root/.hermes/pastes/paste_1_090129.txt`.' else True,
            'skill_line': line_of(skill, needle),
        })

    for block in exact_blocks_in_reference:
        result['reference_exact_block_checks'].append({
            'prefix': block.splitlines()[0],
            'present_in_reference': block in reference,
            'reference_line': line_of(reference, block.splitlines()[0]),
        })

    result['all_skill_literal_checks_pass'] = all(x['present_in_skill'] for x in result['skill_literal_checks'])
    result['all_reference_exact_block_checks_pass'] = all(x['present_in_reference'] for x in result['reference_exact_block_checks'])
    result['all_traceability_artifacts_present'] = all(result['traceability_artifacts'].values())
    result['overall_pass'] = (
        result['all_skill_literal_checks_pass']
        and result['all_reference_exact_block_checks_pass']
        and result['all_traceability_artifacts_present']
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
