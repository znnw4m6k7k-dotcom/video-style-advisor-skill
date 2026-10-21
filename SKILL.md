---
name: video-style-advisor
description: 给视频内容（文字或视频文件）推荐 3 种适合 Opus 5.5 制作的视频风格和配套音频风格，附参考案例。Use when the user asks which video or music style fits their content.
---

# 视频风格顾问

用户只给内容，你给出 3 个视觉风格候选，每个都配好音频风格和参考案例。风格库来自 [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)（51 种，每种都有 STYLE.md 规定画面和声音），案例来自 [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) 和 [joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts)。用用户的语言回复（默认中文）。

先说清一件事：这些风格都是**用代码逐帧画出来的画面**，不生成写实镜头，也不剪辑已有素材。用户给的是实拍视频时，风格用在**包装层**（开场钩子、信息卡、转场、片尾）和**配乐**上，实拍主体按剪辑处理。

## 1. 读内容

**文字描述**：直接读。缺的信息（平台、时长、有无素材）按最常见的情况假设，并在结果里写明假设。

**视频文件**（`$V` 为路径，命令在临时目录里跑）：

```sh
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact "$V"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
# 12 帧拼成一张联系表，自己看这张图（Read 工具）。超过 3 分钟用 tile=4x4，或分段多出几张
ffmpeg -v error -y -i "$V" -vf "fps=12/$D,scale=480:-2,tile=4x3" -frames:v 1 sheet.jpg
# 切镜次数：0 = 一镜到底
ffmpeg -v error -i "$V" -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -c pts_time
# 整体响度和动态
ffmpeg -hide_banner -i "$V" -af ebur128=framelog=quiet -f null - 2>&1 | grep -E "I:|LRA:"
```

要文字稿时：`pip install faster-whisper` 后转写；装不上就读画面里的烧录字幕，或请用户提供文案。不要为此卡住。

## 2. 写内容画像

先给用户看一行画像，再推荐。字段：

- 领域与主体（如：美妆护肤，5 件套礼盒）
- 情绪基调（如：轻松、居家、亲切）
- 画面主色（从联系表看，如：奶油米色、薄荷蓝、金色）
- 素材类型：实拍 / 录屏 / 无素材（纯代码出片）
- 人声：有无讲解，是否已烧录字幕
- 目标平台与画幅、时长

## 3. 选 3 个视觉风格

在下方「风格索引」里按这几条选：

1. **适用内容**和领域对得上（索引里的 uses 列）。
2. **色彩和情绪**和素材协调。实拍素材的主色是硬条件：暖色居家画面配暗场科技风格会割裂，除非只用在某一个高光镜头上。
3. **条件满足**：「实证影像」类要求画面上每个数字都有实测或出处，没有真实数据就不选；需要录屏、扫描、卫星图的风格同理。
4. **三个方向拉开**：一个最稳妥、一个最贴调性、一个更大胆。用户之前定过调性（如"清新可爱"或"简约高级"）就按它排第一。
5. 参考常见做法：公开案例里广告/发布类 71.6% 用动态图形，游戏类 70% 用 3D，科普和故事类风格最分散（[athemeroy 统计](https://github.com/athemeroy/awesome-claude-5-5-videos)）。只作平局时的参考。

选定后，对每个候选读它的 STYLE.md（`https://raw.githubusercontent.com/lemomo-ai/lemo-opuscar/main/styles/<slug>/STYLE.md`），重点看 §1 画面本质、§7 声音、§8 Native moves 的 "Fits content like"，确认真的适合再推荐。

## 4. 配音频风格

音频风格直接取该风格 STYLE.md 的 §7 Sound palette，不要另配。翻成用户能用的说法：

- 曲风与主乐器（如：极简电子，玻璃铃、晶体颗粒音，不用钢琴弦乐）
- 节奏：给一个 BPM 区间，按内容情绪定（轻松种草 95–115，发布/卡点 115–128，抒情 70–90）
- 关键音效：§7 里的 foley 对应到这条内容的具体动作（如开盖、按压、拆封）
- 混音：人声出现时音乐压低多少 dB（§7 的 Mix 行），整体 -14 LUFS
- 实拍有人声时另加：人声响度统一、限幅防爆音、音乐自动避让

## 5. 附参考案例

```sh
curl -sL https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/data/videos.json -o videos.json
curl -sL https://raw.githubusercontent.com/joeseesun/opus-video-prompts/main/cases.json -o cases.json
python3 -I -c "
import json,re,sys
kw=sys.argv[1]
for x in json.load(open('videos.json')):
    if re.search(kw, x['prompt'], re.I): print(x['category'], x['post_url'], x['prompt'][:120].replace(chr(10),' '))
for x in json.load(open('cases.json')):
    if re.search(kw, x['title']+x['category']+x['how'], re.I): print(x['category'], x['url'], x['title'], x['how'])
" "product|launch|产品|广告"
```

关键词换成这条内容的领域。每个候选挑 1 个最像的案例，给链接和一句话说明它怎么做的。joeseesun 的仓库没有许可证，只给链接，不复制提示词全文。已有实拍素材时，优先参考 joeseesun 的「高端极简产品片」（接入真实素材、卡点）和「真人口播改线稿」两份提示词。

## 6. 输出格式

```
内容画像：<一行>

| | 视觉风格 | 为什么适合 | 音频风格 | 参考案例 |
| 1 稳妥 | 中文名 English (slug) | … | 曲风·乐器 / BPM / 音效 / 避让 dB | 链接 |
| 2 调性 | … |
| 3 大胆 | … |

用在哪：<纯代码出片：整片 / 实拍：开场、信息卡、片尾、转场>
不推荐：<一两个看起来相关但不合适的风格，和原因>
```

最后问一句用户选哪个，不要连问多个问题。

## 7. 交给制作

- **纯代码出片**：用 lemo-opuscar。未安装时：`claude plugin marketplace add lemomo-ai/lemo-opuscar && claude plugin install lemo-opuscar@lemolab`，然后对它说"用<风格中文名>风格做一支 <时长> 秒的片子，讲……"。一支片约 30–60 分钟，token 用量较大，开工前告诉用户。
- **实拍素材**：剪辑用 ffmpeg（节奏剪辑、推拉变焦、响度、配乐避让）；包装元素按选定风格的 STYLE.md 用代码渲染成带透明通道的片段再叠加。需要卡点时，参考 [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video) 的 analysis（节拍、下拍、段落检测）做音乐分析。配乐必须是可商用的，或按 §7 用代码合成。

## 风格索引

由 lemo-opuscar 各风格的 style.json 和 STYLE.md 自动生成（2026-10-21，51 种）。上游会更新：如果用户点名的风格不在表里，去 `https://raw.githubusercontent.com/lemomo-ai/lemo-opuscar/main/styles/README.md` 查最新列表。

| slug | 中文名 | 类别 | 适用内容 | 音乐方向（STYLE.md §7 开头） |
| --- | --- | --- | --- | --- |
| archive-lighttable | 档案灯台 | 实证影像 | Brand history & anniversaries; Documentary & archive explainers; Museum & collection stories | Music: restrained and small: a felt piano, a few strings, glass or bowed metal for the moments of seeing. Build by subdivision and register, not by… |
| art-deco | 装饰艺术 | 图形与排版 | Luxury & hospitality; Galas; Invitations | Symphonic jazz of the 1920s–30s, not a 60s big band. Options: stride or concert piano, clarinet (trill; a glissando by time-varying resampling of a… |
| ascii-crt | ASCII / CRT 终端 | 图形与排版 | Developer tools; Sci-fi; Tech brands | Music: an original analog-synth score, rendered in code (numpy / numba): PolyBLEP saw and square oscillators, a resonant 4-pole ladder filter with… |
| backrooms | 后室 / 新怪谈 | 电影与时代 | Horror; Mystery & ARG; Game teasers | No score. Only what the tape would have recorded. Music exists only inside the world (hold music, a radio through walls, a tinny PA jingle), filtered… |
| blueprint | 蓝图 / 工程制图 | 图形与排版 | Engineering; Hardware launches; Tech explainers | Contrapuntal, mechanical music: harpsichord, bassoon, strings spiccato, harp, celesta, music box, clavichord, a small wind ensemble. Imitative lines… |
| brick-toy | 积木玩具 | 材质与 3D | Toys & kids; Product builds; Space | Instruments: small, acoustic, playful (glockenspiel, toy piano, pizzicato, ukulele, whistling, claps, melodica); a brass or orchestral swell for… |
| briefing-board | 工程简报板 | 实证影像 | Engineering decisions; Option comparisons; Briefings & explainers | Room: an air-conditioning bed and traffic through the window, about 20 dB under the voice — audible, not a hiss; silences keep only this. |
| cel-anime-80s | 80 年代赛璐璐动画 | 卡通与动画 | Music videos; Game trailers; Nostalgia | Instruments (city pop, synth funk, anime-opening pop): saxophone or synth-brass lead, FM electric piano with a bell transient, slap bass, chorus-y… |
| crayon-book | 蜡笔儿童绘本 | 手绘与绘画 | Picture books; Bedtime stories; Kids' learning | Small wooden and metal-toothed instruments, no strings or grand piano: ukulele or nylon guitar, clarinet or bassoon (bass, humour), music box (can… |
| dark-keynote | 暗色科技发布 | 信息与发布 | Product launches; SaaS; Keynotes | Music as a visible process: options include phasing (two voices on one pattern, one drifting), additive build (one note per bar), subtractive process… |
| data-physical | 数据实物化 | 实证影像 | Annual reports & ESG; Investor communications; Energy & climate statistics | Score: mallets and air — marimba ostinato, bowed and struck vibraphone, harp, glass, a soft synth pad and a pulse bass with audible 2nd/3rd… |
| dataviz | 数据叙事 | 信息与发布 | Data journalism; Reports; Climate & science | Ambience follows the places the notes evoke (J-cuts in, L-cuts out). Foley is graphite, paper and wood: tick-and-paper taps, scratches for… |
| engraving | 铜版画 | 印刷与版画 | Museum labels; Science explainers; Brand heritage | Instruments (choose): harpsichord, string quartet, solo cello or viola da gamba, lute, chamber organ, glass harmonica for a cold subject. Plucked and… |
| game-show | 综艺节奏扁平 | 游戏 | Tech timelines; Year in review; Variety shows | All synthesized from the picture's events: a sine kick with soft saturation, band-passed noise snare and clap, hats, slap bass, detuned-saw brass… |
| glass-product | 玻璃质感产品 | 材质与 3D | Product launches; Consumer tech; Beauty | Minimal electronic, never piano-and-strings. Timbres, as options: bowed-glass or wet-finger tones, granular crystal clouds, glass bells and FM glass… |
| halftone-dossier | 复古半调案卷 | 印刷与版画 | Humour; Pet content; Social shorts | Synth pop-print toolkit: synth kick, snare, clap, hat; a square-ish 8th-note bass; triangle pad; a marimba-like pluck (fundamental + ~4× partial) for… |
| hd-2d | HD-2D | 游戏 | Game trailers; Fantasy; Story films | Music: chamber-fantasy or cinematic colours (harp, celesta, strings, horns, low choir, timpani) or small folk instruments (lute, recorder, hand… |
| hologram-hud | 科幻全息界面 | 信息与发布 | Product spec walkthroughs; Launch & crowdfunding videos; Trade-show screens | Music first, on a grid (a bar = one information beat); locks land on downbeats, checked against the score. |
| impasto | 油画厚涂 | 手绘与绘画 | Music videos; Art & culture; Emotional ads | Acoustic instruments with a hand-made grain: solo strings, accordion, pizzicato, harp arpeggios, glockenspiel or celesta for pops, piano, guitar,… |
| ink-wash | 中国水墨 | 手绘与绘画 | Wuxia; Cultural brands; Poetry | Guqin-led, not piano and strings: guqin (core/audio/pluck.py guqin: open and stopped strings, slides, vibrato, glassy harmonics, sweeps), a low… |
| iso-infographic | 等距信息图 | 信息与发布 | Process explainers; Supply chains; Annual reports | Music: acoustic and light: kalimba, marimba, nylon guitar, pizzicato, woodblock and hand percussion (shaker, bongo, cajon), upright or synth bass,… |
| lidar-survey | 点云测绘 | 实证影像 | Archaeology & heritage; Forestry & environment; Infrastructure & site surveys | Instrument sounds: FM pings, fine crackle as points arrive, noise sweeps tied to a front, ticks that divide (8ths → 16ths → 32nds) to accelerate, a… |
| living-screencast | 活体实机录屏 | 信息与发布 | Product tutorials; Feature launches; Onboarding | Two resolutions in the music: a hi-fi layer (piano, upright or electric bass, brushed or tight kit, glockenspiel, real samples) is the world; a… |
| lowpoly-island | 低多边形等距 | 材质与 3D | Game trailers; World building; Calm content | Music can be event-driven: growth events carry a note, and the score synthesizes each one at its exact time, so the picture writes the tune. Pitched… |
| microgame | 微游戏快闪（瓦里奥制造式） | 游戏 | Game trailers; Onboarding; Social shorts | Music first: a tempo grid and a cue table before any animation; every picture hit lands on a listed cue. |
| microscope | 显微叙事 | 实证影像 | Biomedicine & pathology; Materials & surface science; Skincare & cosmetic science | Instrument foley: the objective turret (a click, a detent, a small metal ring), a focus servo, pen on glass for each line drawn, a band-passed scan… |
| midcentury-toon | 50s 扁平卡通 | 卡通与动画 | Product set-up guides; Help-centre explainers; How-to steps | Music: an original West-Coast cool-jazz combo: flute or muted trumpet, vibraphone (chords, arpeggios, glissandi, tremolo), pizzicato walking bass,… |
| one-line | 一笔画 | 手绘与绘画 | Brand stories; Life milestones; Minimal ads | Music: one solo instrument, one unbroken melodic line, the sound equivalent of the drawing: a bowed or plucked string (cello, violin, viola, harp), a… |
| paper-lantern | 纸雕灯影 | 东方传统 | Festivals; Gift brands; Cultural stories | Instruments that sit like light behind paper: felt piano, music box, celesta, harp or plucked zithers, bamboo flutes, soft strings; a solo instrument… |
| paper-popup | 纸片立体书 | 材质与 3D | Children's books; Game trailers; Story films | Music: whimsical, acoustic or toy-like: music box, pizzicato strings, clarinet, glockenspiel, ukulele, toy piano, brushes. Options: a warmer cue for… |
| papercut-red | 红色窗花剪纸 | 东方传统 | Lunar New Year; Festive greetings; Folk tales | Instruments: a bright Chinese chamber ensemble, not piano and strings and not the opera percussion of shadow puppetry: pipa (tremolo on long notes),… |
| pictogram-motion | 象形运动图形 | 图形与排版 | Sports events; Visual identity; Event openers | Type and music can carry the film alone; a voice is optional, calm, one line per chapter at most. |
| pixel-rpg | 16-bit 像素 RPG | 游戏 | Game trailers; Recaps; Nostalgia | Chiptune voices: pulse waves at 12.5/25/50 % duty, 4-bit triangle bass, LFSR noise drums, wavetable leads, SNES-style echo (a few taps ~180–370 ms,… |
| risograph | Risograph 丝网印刷 | 印刷与版画 | Indie brands; Zines; Lifestyle | Instruments, as options: warm, dry, handmade, slightly lo-fi: upright or electric bass, vibraphone or marimba, nylon guitar, whistled or hummed… |
| rubber-hose | 1930s 橡皮管卡通 | 卡通与动画 | Food & drink; Retro ads; Kids | Mickey-mouse the score, as options: a band member "answering" a character (trombone raspberry, trumpet laugh); a stop (hard silence, reverb tails… |
| satellite-briefing | 卫星简报 | 实证影像 | Climate & environment; Investigations & news explainers; Geography & history | Telemetry: FM pings (a lock-on ping worth bringing back), dry ticks on the grid that divide to accelerate, noise scans (rising for a rewind, falling… |
| scifi-toon | 科幻情景喜剧卡通 | 卡通与动画 | Comedy; Tech brands; Social shorts | Synthesized score, no samples needed. A theremin-like lead (sine + a little 2nd/3rd harmonic, legato portamento ~70 ms, vibrato fading in ~150 ms… |
| shadow-puppet | 皮影戏 | 东方传统 | Myths & folklore; Heritage; Festivals | Percussion first, not piano and strings (gong-and-drum pattern thinking, 锣鼓经): low barrel drum, hard high clapper drum (woodblock), cymbals, small… |
| silent-film | 1920s 默片 | 电影与时代 | Comedy; Retro brands; Silent storytelling | The instrument is the sound design, as in a picture house: an upright piano (optionally a reed organ, theatre organ, violin or small ensemble) plays… |
| silkscreen-poster | 丝印旅行海报 | 印刷与版画 | Trail & destination guides; Tourism promos; Event posters | Acoustic, hand-played instruments: strummed guitar, slide guitar, harmonica, upright bass, cajon or brushes, banjo, fiddle, accordion, harmonium,… |
| spy-titles | 60s 间谍片头 | 图形与排版 | Title sequences; Event openers; Trailers | 1960s spy big band: stacked staccato trumpets and trombones in octaves with crash (the stab), surf guitar low-string twang through a spring reverb,… |
| stained-glass | 彩色玻璃窗 | 图形与排版 | Legends; Heritage; Holiday stories | Instruments: organ (pedal drone, soft stops, full), harp, hand chimes, tubular bells, recorder or a chant-like voice, water-glass notes, timpani;… |
| swiss-motion | 瑞士动态排版 | 图形与排版 | Brand identity; Events; Design education | Music with a grid of its own: a steady pulse whose subdivisions give snap durations. Options: motorik / krautrock kit and bass, minimal techno,… |
| teardown | 产品拆解 | 实证影像 | Hardware launches; E-commerce product pages; Technical marketing & spec explainers | Instruments: tuned mallets (marimba, vibraphone, glockenspiel, glass), a round bass, a short synthetic kick and small dry percussion. Precise and dry… |
| tilt-shift | 移轴微缩 | 材质与 3D | City promos; Real estate; Transport | Ensemble: tuned percussion carries the style (marimba, glockenspiel, vibraphone, woodblocks, kalimba, celesta), pulse-based and minimalist (Reich… |
| ukiyoe | 浮世绘 | 东方传统 | Travel; Japanese culture; Poetry | Japanese instruments, not piano and pads: shamisen (core/audio/pluck.py shamisen, with sawari buzz), shakuhachi, koto, taiko and shime-daiko,… |
| urban-sketch | 钢笔淡彩 | 手绘与绘画 | City & travel; Architecture; Lifestyle brands | Music families: a jazz waltz (walking bass in three, brushes, piano, clarinet or flute); a café accordion trio; solo nylon guitar; a string quartet… |
| watercolor | 水彩笔刷 | 手绘与绘画 | Nature documentary; Travel; Science explainers | Music: acoustic and gentle: felt piano, fingerpicked guitar, woodwinds, light strings, glockenspiel, kalimba, soft pads. A licensed track can be… |
| white-model | 白模投影 | 实证影像 | Urban planning & real estate; Exhibitions & showrooms; City data & history | The room: room tone, the projector fan (hum + filtered air) rising when the lamp strikes, relays for the house lights, a lamp strike (zap + thump),… |
| whiteboard | 白板讲解 | 手绘与绘画 | Explainers; Online courses; Science | Music options: a solo piano figure; a small jazz trio with brushes; plucked strings and kalimba; a synth arpeggio for tech topics; clockwork… |
| woodcut | 木刻版画 | 印刷与版画 | Folk tales; Craft brands; Book trailers | Instruments: low strings (contrabass, cellos; spiccato, pizzicato), wood and skin (log drum, woodblock, frame drum), gran cassa, timpani, one… |
