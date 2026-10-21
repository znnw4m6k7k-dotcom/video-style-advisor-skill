# 视频风格顾问 · video-style-advisor

**说出视频内容，就告诉你用哪种画面风格、配哪种音乐。**

这是一个 Claude skill。你给 Claude Opus 5.5 一段文字或一个视频文件，它会读懂内容，从 51 种代码出片风格里挑出最适合的 3 种，每种都配好音频风格和真实案例，选定后可以直接开始制作。

## 能做什么

- **读内容**：文字直接读；视频会自动抽帧、看切镜次数、测响度，判断领域、情绪、主色和素材类型。
- **推荐 3 种视觉风格**：一个稳妥、一个贴调性、一个大胆，并说明为什么适合、不推荐哪些。
- **配音频风格**：每种风格自带的曲风、乐器、BPM、关键音效和人声避让分贝。
- **附参考案例**：从 700 多个公开的 Opus 5.5 视频里找最像的案例。
- **交给制作**：纯代码出片交给 lemo-opuscar；实拍素材给出剪辑和包装方案。

## 怎么用

装好后，直接对 Claude 说：

> 这个视频适合做成什么风格？（附上视频文件）

> 我想做一支 30 秒的视频，讲我们家新开的咖啡店，推荐一下风格和配乐。

## 输出示例

用一条 70 秒的护肤礼盒开箱实拍视频测试，得到：

| | 视觉风格 | 音频风格 |
| --- | --- | --- |
| 稳妥 | 水彩笔刷 | 原声轻柔：钢琴、指弹吉他、卡林巴，100–110 BPM |
| 清新可爱 | Risograph 丝网印刷 | 温暖 lo-fi：马林巴、尼龙吉他、刷子鼓，100–115 BPM |
| 简约高级 | 玻璃质感产品（只用于开场 2 秒） | 极简电子：玻璃铃、晶体颗粒音，118–124 BPM 卡点 |

完整结果见 [examples/开箱视频推荐.md](examples/开箱视频推荐.md)。

## 安装

**claude.ai**：在设置的 Skills 页面上传本仓库的 `SKILL.md`。

**Claude Code**：

```sh
mkdir -p ~/.claude/skills/video-style-advisor
cp SKILL.md ~/.claude/skills/video-style-advisor/
```

分析视频需要本机有 ffmpeg。要正式出片，再装 lemo-opuscar：

```sh
claude plugin marketplace add lemomo-ai/lemo-opuscar
claude plugin install lemo-opuscar@lemolab
```

## 注意

- 这些风格都是 Opus 5.5 **写代码逐帧画出来的**，不生成写实镜头。实拍视频的风格只用在开场、信息卡、转场、片尾和配乐上。
- 推荐只需几分钟；用 lemo-opuscar 出一支片约 30–60 分钟，token 用量较大。
- 推荐的是音乐"风格"，不附带曲库。配乐要用可商用的音乐，或让 Claude 用代码合成。

## 仓库文件

| 文件 | 用途 |
| --- | --- |
| `SKILL.md` | skill 本体：推荐流程 + 51 种风格索引 |
| `styles_index.json` | 风格索引完整版（画面描述、音乐方向、适配内容） |
| `scripts/build_index.py` | 上游风格库更新后重新生成索引：`python3 -I scripts/build_index.py <lemo-opuscar 目录> styles_index.json` |
| `examples/` | 实测示例 |

## 致谢

- 风格与声音：[lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)（MIT / CC BY 4.0）
- 参考案例：[yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)（MIT）、[joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts)（仅链接引用）
- 音频分析思路：[mexicat/pdoom-video](https://github.com/mexicat/pdoom-video)（MIT）
- 领域与风格统计：[athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos)（CC BY 4.0）
