# video-style-advisor

给一段视频内容（文字描述或视频文件），推荐 3 种适合用 Claude Opus 5.5 制作的视频风格，每种配好音频风格和参考案例，再交给 [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) 制作或走实拍剪辑。

## 安装

把 `SKILL.md` 放到 `~/.claude/skills/video-style-advisor/`，或在 claude.ai 的 Skills 里上传。然后对 Claude 说："这个视频适合什么风格？"并附上视频或文字。

## 文件

| 文件 | 用途 |
| --- | --- |
| `SKILL.md` | skill 本体：流程 + 51 种风格索引 |
| `styles_index.json` | 风格索引完整版（画面描述、音乐方向、适配内容） |
| `scripts/build_index.py` | 上游更新后重新生成索引：`python3 -I scripts/build_index.py <lemo-opuscar 目录> styles_index.json` |
| `examples/开箱视频推荐.md` | 用一条护肤礼盒开箱视频的实测结果 |

## 数据来源

- 风格与声音：[lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)（MIT / CC BY 4.0）
- 参考案例：[yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)（MIT）、[joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts)（仅链接引用）
- 音频分析思路：[mexicat/pdoom-video](https://github.com/mexicat/pdoom-video)（MIT）
- 领域×风格统计：[athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos)（CC BY 4.0）
