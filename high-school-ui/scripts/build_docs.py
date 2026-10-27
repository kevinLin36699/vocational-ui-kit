#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate standalone docs, offline viewer data, and runnable composition templates."""
from pathlib import Path
import json, re, hashlib
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'data/components.json').read_text());A=json.loads((R/'data/source-audit.json').read_text())
D={}
def add(k,title,text):D[k]={'title':title,'content':text.strip()+'\n'}

add('START','开始使用',r'''
# 高职教 UI 组件库 v2.0.0

本次交付是参考AI-base设计、以HTML/CSS/JS独立实现的原型组件库，不是参考平台同一套源码组件；本次已按文档统一整库公共规范，并逐项记录适配依据；线上逐状态一致性仍受可用智能体限制。对齐、扩展和差异见REFERENCE_ALIGNMENT.md。

本次交付是无构建、无后端的 HTML 原型组件库。它可以用于设计评审、交互验证和后续页面生成，不是已经接入真实权限、数据库和模型的生产框架包。原始高职教平台未修改。

## 打开与运行
- 可直接打开 index.html。展示站通过相邻 JS 加载索引，无运行时 fetch，不依赖 CDN、远程字体或安装包。
- 推荐在组件库目录执行：python3 -m http.server 8788 --bind 127.0.0.1
- 然后打开 http://127.0.0.1:8788/ 。仅此示例中的文本资源下载，不用于验收原平台视频 Range 行为。
- 独立管理页：examples/management.html；独立 AI 协作页：examples/ai-workspace.html。
- 会话、表单和数据只保留于当前页面内存，刷新恢复初始示例。源项目和参考线上业务不发生写入。

## 最小接入
```html
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/components.css">
<div id="target"></div>
<script src="js/icons.js"></script>
<script src="js/resource-composer.js"></script>
<script src="js/skill-picker.js"></script>
<script src="js/content-workspace.js"></script>
<script src="js/voc-ui.js"></script>
<script>
  VocUI.mount(document.querySelector('#target'), 'table');
</script>
```

页面组合还需加载 js/patterns.js，然后调用 VocPatterns.mount(element, 'list')。框架页面需自行包装生命周期，组件卸载前调用 VocUI.destroy(element)。

## 目录
- css/tokens.css：唯一主题变量与 ui-* 旧变量兼容别名。
- css/components.css、js/voc-ui.js、js/icons.js：复用实现。
- data/tokens.json、components.json：机器可读标准与索引。
- data/source-manifest.json、source-audit.json：源码扫描范围和 SHA256。
- data/migration-map.json / csv：完整词法候选及未判定项。
- js/catalog.js、tokens.js、docs.js：上述数据的离线展示副本，由脚本生成。
- design/：规范、研究证据、迁移、API、页面生成和验收说明。
- examples/：14 类独立组合模板，复用同一套实现。
- scripts/：本次可复现的索引、变量、文档和静态验证工具。

## 更新
主题值在 scripts/build_tokens.py 维护，然后执行它生成 JSON/CSS/JS；不要只改 CSS 副本。组件分类与来源指示在 scripts/build_catalog.py 维护。日常顺序：build_tokens.py → build_docs.py → verify.py → build_report.py → build_docs.py。build_catalog.py是显式重新扫描工具，会更新来源快照；不要用它清除已记录的原平台变化。组件描述与对齐规则以当前data/components.json、data/component-alignment.json为准，重新扫描后需合并这些已审核元数据。

当前工作区绝对路径仅用于来源定位；运行组件库本身使用相对资源。迁移到其他工作区时应配置或修改扫描脚本的 SOURCE，而不是硬改业务页面。
''')

add('STANDARD','蓝白设计规范',r'''
# 设计标准与主题 v2.0.0

## 依据与主题
结构、密度、尺寸、排版和交互以参考 DESIGN.md 为准。蓝白主体、局部蓝紫 AI 强调是用户明确覆盖；纸纹、暖色赭石不引入高职教主题。保留文档的衬线标题层级和无衬线 UI，以本机字体回退实现，不加载远程字体。

品牌 --v-brand=#155cc3，画布 --v-background=#f5f7fb，卡片 --v-card=#ffffff；正文 --v-foreground=#20344f，辅助 --v-muted-foreground=#5e7088。成功、警告、危险使用各自语义色，状态同时有文字。全部颜色、阴影、动效通过 data/tokens.json 与 css/tokens.css 引用，122 个变量、21 个兼容别名。

## 排版（DESIGN.md §4）
- UI 默认14/20px；说明和标签13/18px；时间、计数等12/16px，数字等宽。
- 对话正文15px/1.75；输入正文15px/1.7。代码13/20px；宽表格与代码内部滚动。
- 页面标题28/36px衬线600，欢迎问候32/42px；弹窗标题19/26px；空状态17/24px；区块、卡片标题15/22px无衬线600。
- 仅400/500/600字重。系统字体栈和等宽字体按文档配置；标题可自然换行，不裁切业务名称。

## 控件、间距与形状（§5、6、10）
- 默认控件36px；紧凑按钮30px；大按钮44px；导航/菜单34px；Chip28px；徽标22px。
- 控件/代码块10px圆角；卡片/菜单/选择浮层14px；弹窗20px；舞台24px；Composer18px；发送键34px、11px圆角；消息操作8px。
- 普通卡片16px内边距、12px间距，静态轻影；可交互卡悬停抬升2px并使用浮起阴影。
- 输入内边距10px，标签13px；文本域最小64px。焦点为描边与3px品牌弱底光晕，错误使用危险色光晕。
- 通用焦点2px、偏移1px；禁用50%透明；加载70%透明、状态和重复提交受控。
- Checkbox16px、6px圆角；选中对勾与部分选中明确，保留语义和键盘操作。
- 分段Tabs采用底轨、30px触发器、白色滑块、320ms位置过渡，首次定位不动画；方向键、Home、End可用。内容导航不再使用44px下划线。
- 折叠内容保持挂载，200ms高度/透明变化；关闭区域inert且不可Tab进入。执行中过程锁定展开。

## 布局（§5、11）
- 业务Shell侧栏272px，折叠64px；头部56px。当前导航卡片底、品牌图标，34px导航行。
- 目录最大1040px；首页800px；欢迎区720px；对话阅读列46rem；侧面板360px、内边距14px。
- 1280px起工作区内嵌；更窄使用原生模态Sheet适配焦点与遮罩，内容节点保留。关闭区域inert，关闭返回入口。
- 管理表格等复杂高职教模式是公共变量及控件的组合；文档未定义专用业务API的部分不声称线上存在相同控件。
- 展示站有文档导航结构，但使用同一排版、形状、控件与密度体系。PC优先；窄屏降级不等同完成移动端生产适配。

## 按钮、浮层与反馈
主操作蓝底白字，soft浅蓝、outline白底轻影，ghost弱操作，link行内下划线。实体删除使用危险红色：行内垃圾桶和文字为红色，最终确认按钮红底白字；默认焦点取消，明确对象与后果。

Dialog宽420/560/720px、20px圆角，头部16px/20px边距、正文20px、底部8px动作间距；AlertDialog遮罩不取消。Sheet360px，首焦点收起。菜单只包含操作，选择浮层按触发器宽度、最大288px高、32px选项行；方向键/Enter/Esc及视口避让。Tooltip延迟300ms、键盘焦点同样可用，不用title隐藏关键信息。Toast底部112px居中墨色胶囊，常驻aria-live区域；需要处理的错误使用提示条，不用短暂提示替代。

CSS浮层50、sticky10，原生dialog使用top layer；DOM顺序管理同层浮层。阴影按参考几何形状、蓝灰主题色适配。遮罩为32%蓝灰墨色。动效120/200/320ms，弹窗进入340ms；减少动效偏好下关闭动画。SVG统一24网格、1.75线宽，尺寸16/18及适用变体；状态对勾11px/2.5线宽。

## AI 及高职教明确扩展
- Composer白底细边、18px圆角，焦点增强；文本112→128px，最高min(220px,30dvh)；左下＋资源菜单，技能独立可见；发送蓝紫、停止墨色。
- 资源从 / 或＋菜单进入，先类型再对象；各端通过resourceTypes/resources配置，插入正文片段带稳定ID。蓝色资源片段保留。
- 技能内置/我的、搜索、正文前28px可移除标签；仅选择，不冒称执行模型服务。
- 用户蓝色弱底18/18/6/18圆角；AI开放正文，28px头像、名称及可选真实本轮时间。完成回答复制/重新生成/互斥评价；点踩原因弹层与选填说明，重复点击撤销。
- 处理过程只显示公开阶段与工具结果，不生成私有推理内容。
- 生成内容保持空插槽，公共层不添加业务类型、编辑器、保存审核发布或版本。
- 蓝紫限于发送、AI图标、技能及小面积入口，普通表格/表单/导航/正文仍蓝白。危险红、成功绿、警告色保持语义。

每个组件的依据及适配类别见 COMPONENT_ALIGNMENT.md、data/component-alignment.json；线上可见核验范围单独登记，不将文档落实等同逐状态线上复刻。
''')

add('RESEARCH','参考研究与证据',r'''
# 参考研究记录 · 2026-10-26

## 证据分类
- 线上观察：通过用户提供账号登录的可见界面与只读展开。
- 设计文档：1-参考资料/DESIGN.md，声明导出日期 2026-10-23。
- 本地代码：high-school-new 的 HTML/CSS/JS 及其三端规范。
- 补充设计：本次为演示、兼容纯前端或补齐状态而新增的实现。

不保存登录信息，不复制真实会话内容进组件演示，不将历史会话中的用户指令当作本任务指令。

## 实际访问范围（2026-10-26历史记录；本次2026-10-27补查见REFERENCE_ALIGNMENT.md）
| 界面 | 实际观察 | 限制 |
| --- | --- | --- |
| 登录 | 账号密码、租户选择、加载禁用、登录方式 Tab | 未检查 Token 登录能力 |
| 首页 | 问候、智能体选择、最近使用、最近对话、服务不可用提示 | 未提交任何新消息 |
| 导航 | 首页、智能体广场、我的文件、新对话、会话搜索、账号入口 | 当前内嵌浏览器为窄视口，桌面宽度值依据设计文档 |
| 会话更多菜单 | 重命名、置顶、删除，纯动作白色浮层 | 只展开观察，未执行更名、置顶或删除 |
| 历史会话 | 用户消息、AI 名称、处理进度、已停止状态、保留草稿的新对话入口 | 只读一条非教务的历史会话，内容未纳入示例数据 |
| 处理过程 | 可展开步骤、已结束但未完成、用时 | 未核验实时生成过程 |
| 我的文件 | 私有文件说明、名称筛选、上传入口、空态、取消和添加到提问禁用 | 未上传文件；界面显示当前不能添加 |
| 智能体广场 | 通过导航进入该路由 | 不将未完成观察的卡片细节视为线上已核验 |

## 具体阻碍
提供的智能体与会话链接，在所选可登录演示租户中显示“找不到这个智能体”，可能为资源不存在或无权限。首页与会话显示执行服务暂不可用，发送和模型选择禁用。

因此没有线上核验正常发送、流式完成、重试成功、引用、真实文件解析或真实工具调用。以上设计来自 DESIGN.md 与本地代码，在组件库中作为明确标识的本地模拟。没有切换其他租户猜测权限，也没有创建或删除线上业务记录。

## 本地深入读取
实际读取了 DESIGN.md 的设计理念、接入、颜色、排版、尺寸、圆角、组件、AI 模式、无障碍、必须/禁止与代码附录相关内容；大文档按章节查阅。

本地重点：AGENTS.md、共同交互清单、三端专项的当前规则，以及 ui-tokens.css、design-system.css、ai-composer.css、ui-icons.js、ai-composer-ui.js、ai-process-ui.js、management.js、teacher-course-center.js、navigation-breadcrumbs.js 等。全量源码进行词法扫描，扫描不等同人工阅读每一行或运行所有页面。

用户已明确授权本组件库的运行、交互和布局验证；旧项目默认不自测规则不阻止本次独立组件库验收。本次未打开旧平台做批量验收或修改旧项目。
''')

add('DECISIONS','三方差异与决策',r'''
# AI-base → 高职教 → 统一标准 v2.0.0

| 项目 | 参考 | 高职教旧实现 | 最终规则 |
| --- | --- | --- | --- |
| 主题 | 暖纸赭石 | 蓝色且局部不统一 | 用户明确蓝白主体、少量AI蓝紫；语义色独立 |
| 标题 | 衬线28/36，UI14/20 | 无衬线24及多种字号 | 按参考排版，中文系统字体回退 |
| 控件 | 36/30/44、圆角10 | 36/32/44、圆角8 | 全库采用参考尺寸及焦点体系 |
| 卡片 | 圆角14、内边距16、间距12 | 多数内边距24 | 采用参考密度；业务组合保留语义 |
| Tabs | 分段底轨与滑块 | 下划线44 | 统一分段30与320ms滑块 |
| 弹窗 | 20圆角、420/560/720 | 16圆角及不同边距 | 参考外观与焦点规则，原生dialog适配 |
| 应用外壳 | 272/64侧栏、56头部 | 232/64及64头部 | 采用参考几何；展示站文档导航独立结构 |
| 对话 | 46rem、15/1.75、头像元信息 | 更宽、14px、无元信息 | 统一开放正文、头像与消息动作 |
| 过程 | 细线、30px折叠行 | 大卡片时间线 | 公开处理阶段，始终挂载、关闭inert |
| 引用资源 | 线上未取得可用智能体 | 教学对象联动 | 按用户要求：/类型→对象、稳定ID与归属 |
| 技能 | 线上未核验此面板 | 横排简单入口 | 内置/我的、搜索、正文前标签可移除 |
| 生成内容 | 来源文件侧面板 | 曾内置多种业务编辑器 | 用户明确只留容器与空插槽 |
| 技术 | React/Tailwind/Radix/lucide | 独立HTML原型 | 保持HTML/CSS/JS复用，采用同类视觉与交互规则；不宣称同一源码包 |

三方材料不一致时，以本次要求为最高优先，再采用 DESIGN.md 的公共标准。旧平台只保留业务语义和必要流程，不用旧差异覆盖新规范。未定义专用样式的高职教业务组件使用统一公共控件组合，详见逐组件映射。
''')

rows='\n'.join('| '+c['id']+' | '+c['name']+' | '+c['category']+' | '+c['rule']+' | '+(c['evidence'][0]['file']+':'+str(c['evidence'][0]['line']) if c['evidence'] else '建议扩展')+' |' for c in C)
add('INVENTORY','盘点与覆盖',f'''
# 材料盘点与组件覆盖

扫描 {A['fileCount']} 个文本材料文件，其中业务 HTML/CSS/JS {A['sourceCount']} 个；静态资源文本和设计说明单独计入材料。提取 {A['classCount']} 个类名、{A['importantCount']} 条 !important。文件 SHA256、行数与路径见 data/source-manifest.json。

扫描采用词法提取，CSS .class 与 HTML/JS 中 class 属性包含动态字符串时可能存在漏提或误提；不解析完整 AST，不运行 eval。颜色和圆角统计为源声明频次，不是浏览器计算样式。源码位置为扫描当时行号。

## 核心问题
- 已有共享 ui-tokens 与 design-system，却并存大量角色/页面适配层与高优先级选择器。
- 标题旧变量28px与当前规则24px并存；按钮、卡片、输入存在历史尺寸和色值。
- 多个专用业务直接拼接 HTML 和局部样式，不能靠一次全局样式覆盖安全迁移。
- 普通过程、生成内容、输入及头像规则已有当前正文，早期页面仍需逐项对齐。
- 现有组件 API 依附全局控制器；本次独立实现可复用外观和交互，正式替换时必须保留事件及权限。

## 60 类组件
| 标识 | 名称 | 分类 | 规则 | 本地来源示例 |
| --- | --- | --- | --- | --- |
{rows}

每类完整来源片段、适用状态及 API 见 data/components.json，展示站可查看对应来源。

## 覆盖与未覆盖
已建立上述60类的可运行原型实现与14类组合模板。该结论不表示每个旧页面已迁移，或每个状态都已浏览器验收。验收另见 VALIDATION.md。

词法映射中的未判断类名全部列为 review-required；画布/考试/媒体候选列为 specialized-preserve，不把它们勉强塞入基础组件。复合动态模板、业务权限和真实异步数据的逐页覆盖仍待后续整改。
''')

add('MIGRATION','旧组件整改路线',f'''
# 整改映射与实施路线

data/migration-map.json / csv 登记全部 {A['classCount']} 条词法类名记录，包含来源、候选组件、处置理由、优先级与 verifiedMigration=false。

| 处置 | 数量 | 含义 |
| --- | --- | --- |
| candidate-mapped | {A['mappingSummary']['candidate-mapped']} | 名称或结构指示有候选，实施时复核；不是可直接全局替换的选择器映射 |
| specialized-preserve | {A['mappingSummary']['specialized-preserve']} | 媒体、画布、考试、编辑器等专用类，保留原控制器与内容主题 |
| review-required | {A['mappingSummary']['review-required']} | 其余类未作自动语义结论，必须逐页核对 |

## 人工确认的迁移方向
| 现有结构 | 新组件 | 替换要点 | 优先级 |
| --- | --- | --- | --- |
| mg-btn / prep-button / upload-button | voc-button | 统一尺寸与层级，保留事件、权限和状态 | P0 |
| ui-icon / UIIcons.render | voc-icon | 复用路径；补齐可访问按钮名 | P0 |
| mg-field / mg-filters | voc-input / select / form | 规范错误和依赖；正式字段由业务控制器绑定 | P0 |
| mg-table | voc-table | 筛选排序分页口径一致，选择范围与真实导出一致 | P0 |
| data-ai-composer / composer | voc-composer | 保留草稿、输入法、原上传范围，不能重建控制节点破坏绑定 | P0 |
| message-bubble / message.assistant | voc-message / prose | 用户浅蓝；AI开放正文；历史文本安全转义 | P0 |
| AIProcessUI / ai-process-card | voc-process | 真实阶段由业务传入；本库计时不得替代真实执行状态 | P0 |
| history-actions / 协作记录 | voc-conversation | 稳定ID、草稿隔离、恢复与归档语义沿原数据 | P1 |
| modal / dialog / mg-modal | voc-dialog / confirm | 保留现有提交协议，关闭恢复焦点，确认对象与后果 | P1 |
| program-course-card | voc-course-card | 保留课程入口与16:9资源封面，分离次级操作 | P1 |
| 大纲与生成内容工作区 | voc-workspace / result | 不混淆生成、审核、保存、分发；版本与角色仍由业务提供 | P1 |
| PPT/视频/图谱/考试控件 | 专项外壳 + 原实现 | 不替换编辑引擎、画布主题、考试计分或媒体跳转 | P2 |

## 迁移步骤
1. 对目标页面记录角色、稳定对象、入口、状态、数据和权限契约。
2. 根据组件索引确定结构和变量，先在副本中替换公共外壳与低风险基础组件。
3. 给原控制器绑定适配层，保留旧节点所需 ID、事件、草稿、生成生命周期与权限。
4. 通过空/错/加载/只读/停止等适用状态检查；比较原有行为与新组件行为。
5. 有证据后将该页面映射改为已实施与已验证，记录实际覆盖范围。

本库 ui-* 变量别名仅是视觉接入辅助，不能替代迁移过程或直接覆盖原平台全部样式。
''')

add('API','API 与参数支持',r'''
# API v2.0.0

## 公共入口
```javascript
VocUI.render('input', { label: '课程名称', state: 'invalid' });
VocUI.mount(document.querySelector('#target'), 'table', { state: 'failed' });
VocUI.hydrate(document.querySelector('#already-rendered'));
VocUI.destroy(document.querySelector('#target'));
VocPatterns.mount(document.querySelector('#page'), 'list');
```

render 返回 HTML 字符串；mount 先清理旧组件异步任务，再插入和激活复合组件。只调用 render 后插入复杂组件，必须调用 hydrate。hydrate 对已有表格、会话实例不重复初始化。所有 public key 可查 VocUI.supportedComponents。

## 参数支持矩阵
除下表外，其余组件在本版本是固定数据的可操作配方，props 不提供完整业务配置 API；不要把共同字段误认为所有组件均支持。生产接入应建立适配层，不直接将本地示例控制器作为业务数据层。

| key | 已支持参数 | 边界 |
| --- | --- | --- |
| input | label,value,type,name,placeholder,required,disabled,readonly,invalid,min,max,help,state | state 支持 disabled/readonly/invalid；仅 input 示例最长80字 |
| textarea | label,value,disabled | 固定示例最小高度，文字转义 |
| button | label,disabled,state | state=disabled；各操作固定示例，不支持任意回调参数 |
| select | label,disabled,state | 固定学院选项；通用可配置选择使用 VocUI.select |
| table | state | default/empty/no-match/failed/loading，固定17条示例数据；不是业务数据源 API |
| form | value | 用于初始课程名，其余演示字段固定；提交从 voc:submit 取得 values |
| process | state | waiting/running/completed/failed/stopped；运行中为静态状态样例，真实可终止流程见 chat |
| composer | value,placeholder,disabled,id,resources,resourceTypes,segments,skills,selectedSkill | 独立输入只接收演示需求；完整流式用 chat |
| chat | history,mode,resources,resourceTypes,skills,selectedSkill | history=false 隐藏会话栏；mode=success/failure 指定模拟结果；实际生成可停止 |
| conversation | 无 | 内置带会话栏的 chat 配方 |
| workspace | title/subtitle/state/statusText/actions | 空内容插槽，预览编辑、版本与业务动作由调用方接入 |

VocUI.input(label, props)、VocUI.select(label, options, value, props) 返回 HTML。select 的 options 可为字符串数组或 {label,value} 数组，props 支持 name / disabled / placeholder / multi。选项值应为稳定字符串 ID。

## 事件
均为冒泡 CustomEvent。只在实现中明确的相应动作触发，普通静态组件不会自动产生所有事件。

| 事件 | 实际场景 | detail |
| --- | --- | --- |
| voc:change | 选择器、多选、开关、树、文件、表格更新 | component, action（部分控件）, value/checked/selected 等 |
| voc:selection | 单选选择器内部协调事件 | value；复合表格和级联用它更新依赖 |
| voc:submit | 表单保存、AI发送/完成、示例分发 | component, form/values 或 action/threadId/prompt，simulated=true |
| voc:action | 未被演示控制器消费的 data-v-action | component, action；已消费动作不重复广播 |

```javascript
document.querySelector('#target').addEventListener('voc:submit', event => {
  if (event.detail.form === 'course') {
    console.log(event.detail.values); // 仅示例；正式接入自行调用真实服务
  }
});
```

## 限制与集成
- 表格示例的增改查删、排序、分页、选择及 CSV 都使用相同本地集合；更新后不入库。
- 选择器选项与参数按文本转义。公共 input 的 extra 参数仅供受信任的内部属性拼装，不得传入用户输入；建议业务方不用该内部逃生参数。
- Markdown 为受控子集：标题、段落、列表、代码、表格、引用、粗体和行内代码；不执行 HTML，不支持完整 CommonMark、任意外链和语法高亮。
- 模态使用原生 dialog；搜索选择使用原生 JS 浮层；没有 React、Vue、Radix 或 Tailwind 运行依赖。
- 组件为轻 DOM / 全局 v-* 命名空间，基础 reset 会影响宿主。正式嵌入旧平台前应隔离或限定作用域，不能直接全局覆盖。
- 不含真正后端权限、网络重连、流式API、文档解析、跨页同步或永久版本库。

## 正文资源输入扩展（v2.0.0）
composer 新增 resources、segments，chat 新增 resources；不新增 rows/messages 等业务接口。运行资产增加 js/resource-composer.js，按 manifest 顺序加载。voc:resource-change 和 ai-send 中的 segments/resources、恢复与校验 API 见 [INLINE_RESOURCES.md](INLINE_RESOURCES.md)。可见消息输入改为 .v-resource-editor，隐藏 textarea[data-ai-input] 仅为旧值适配，不应供用户聚焦。

## 新增配置与事件
composer 与 chat 支持 resourceTypes、skills、selectedSkill；资源两级选择见 INLINE_RESOURCES.md，技能 API、voc:skill-change 与 voc:feedback 见 SKILLS.md。voc:submit(ai-send) 增加 skill 快照；不改变既有 prompt/segments/resources。
''')

add('AI','AI 交互与状态',r'''
# AI 交互与状态 v2.0.0

## 输入与状态
阅读列46rem，Composer白色18px圆角、15px/1.7正文、112→128px焦点高度；＋上传/我的文件/引用资源，独立技能入口。引用资源按类型→对象，目录由调用方按端提供，资源ID/版本/归属须服务端再次校验。技能标签在所有正文之前、可X移除，不直接执行真实技能。

发送只在非空且资源/技能有效时可用；Enter发送、Shift+Enter换行、输入法组字不发送。执行时草稿可继续编辑。停止清除本地定时器并保留部分结果；失败、停止、完成后重试替换当前回答，不重复提问。生成中先停止再切换会话，避免旧回调写入新会话。会话草稿、附件、资源和技能分别保留，重试沿用本轮快照。

## 消息与过程
用户蓝色弱底气泡18/18/6/18，悬停或聚焦可复制和编辑回草稿；覆盖现有草稿前确认，重新发送由用户主动触发。AI回复开放正文，28px方圆头像、名称、本轮产生的可选时间及正在生成状态；15px/1.75正文、段间10px、标题20/17/15/14px，代码/表格内部滚动。

过程是细线归组与30px折叠行；运行时展开且不可收起，失败展开，完成/停止可切换。折叠子内容保留挂载、关闭inert。只展示公开阶段、工具输入摘要与可公开结果，不展示或编造内部推理。示例处理记录明确来自本地。

完成回答可复制、重新生成、点赞/点踩。两种评价互斥且再次点击撤销；点踩打开原因选择和最多500字说明，确认后提交本地状态，取消不改变已有评价。反馈事件含messageId/value/reason/comment/simulated；未连接真实收集服务。

## 侧面板与空插槽
结果卡只是通用工作区入口；工作区默认只显示“内容展示区”占位。业务内容、编辑器、数据、保存、审核、发布和版本由业务页面接入。组件不预设大纲/PPT/题库等类型，也不生成业务表单。

1280px起360px内嵌面板，更窄使用原生dialog Sheet：遮罩、焦点限制、首焦点收起、关闭返回入口；相同内容DOM节点保留。关闭inert。切换messageId由activate管理独立插槽，不混合历史内容。容器具体API见GENERATED_CONTENT.md。

## 本地模拟与文件
每个阶段约1秒，流式文字可以停止，失败可重试恢复；标题栏演示控制只配置本地模式，不混入真实输入工具。示例无模型、后端、真实检索、上传或解析。

通用上传示例10MB，AI输入示例20MB，支持类型是演示配置，不代表正式三端限额。我的文件选择提供名称筛选、版本、更新时间、选择、取消、添加到提问，使用虚构目录，选中确认只添加附件引用不发送。ID去重，不可用项显示原因。

## 可访问状态和滚动
回合间30px、轮内16px；底部时跟随新内容，阅读历史不强制回底，显示回到最新消息。输入与过程更新不反复抢焦点。停止/失败/完成通过状态文字适度播报，逐字生成不逐字播报。原型仅当前页面内存，刷新重置。

完整资源、技能和空插槽规则按需读取INLINE_RESOURCES.md、SKILLS.md、GENERATED_CONTENT.md。线上当前无可用智能体，发送/停止/生成等未在线操作，不将本地模拟标成线上通过。
''')

pattern_rows=[('home','平台首页','教师示例','agent / composer / card'),('list','管理列表','管理示例','toolbar / table / form'),('detail','普通详情','当前课程','breadcrumb / tabs / description / chat'),('edit','编辑表单','教师课程草稿','form'),('selection','选择关联','当前草稿','cascade / multiselect / person-picker'),('analytics','统计分析','17门示例课程','stat / chart'),('history','协作记录','当前页面会话','conversation'),('chat','AI主协作','虚构教师任务','chat'),('assistant','内嵌助手','当前课程','description / chat'),('workspace','长文工作区','教学大纲草稿','workspace'),('learning','学习作答','虚构学生作业','radio / alert / composer'),('approval','审核分发','本地演示对象','approval'),('files','资源文件','本次文件选择','upload / resource'),('settings','个人配置','虚构教师','input / switch / avatar')]
add('PATTERNS','页面契约与模板',r'''
# 页面组合契约

所有示例是独立模板，不是对旧业务页面的批量修改。examples 中每个 HTML 都加载同一套 tokens、组件和模式实现，没有另建近似样式。

## 必填页面契约
1. CON01：身份、稳定对象、实际权限与入口容器。模板角色只是虚构示例，不实现认证。
2. CON02：标题与操作、模板、组件和滚动归属。普通内容主区域滚动；对话、工作区和长浮层内部独立。
3. CON03：数据来源、筛选范围、字段格式、附件能力、默认/空/错等适用状态。
4. CON04：动作前置、确认、成功/失败、防重与留存。示例只保留当前页面内存，刷新重置。
5. CON05：适用规则、角色专项、覆盖证据与未确定项。原有权限和正式考试规则不从模板推断。

## 已交付模式
| 标识 | 模式 | 示例身份/对象 | 复用组件 |
| --- | --- | --- | --- |
'''+ '\n'.join('| '+' | '.join(x)+' |' for x in pattern_rows)+r'''

## 代表性管理页面
examples/management.html 使用 list 模式。17条虚构课程统一参与筛选、学时排序、5项分页、页内三态选择和导出。翻页/筛选清除选择并明确提示。创建/编辑需校验课程名、学时和日期；删除确认具体对象；CSV 可实际下载。

## 代表性 AI 页面
examples/ai-workspace.html 使用 chat 模式。新建/搜索/重命名/置顶/删除会话、会话草稿隔离、模拟发送/停止/失败/重试、来源和结果工作区共用组件实现。没有真实模型或上传服务。

## 状态适用性
- 列表：默认、筛选、空/无匹配、失败、选择、排序、编辑提交适用；真实权限过期由业务补充。
- 表单：草稿、字段错误、提交、防重、取消保护适用；真实冲突和幂等由业务补充。
- AI：等待、生成、停止、失败、重试、完成和工作区收放适用；真实网络恢复不适用。
- 学习：确认开始作业后禁用当前助手；提交一题计算本地分数并恢复。它不等于正式考试、教师批阅和跨页面防绕过机制。
- 分析：数据同源与明细可读；不做无依据的学习成效推断。
- 审批：本地展示流程，不模拟所有角色权限与后台审批成功。

## 必须保留的专项
课程与实训分离，课程不绑定学期；学生当前作业期间AI限制；学生/教师评价草稿差异；正式考试的中断计分与离开；师生课程详情助手默认显隐差异；教师大纲审核直接编辑；分发明确课程/单元；作品主题与应用界面独立。
''')

add('GENERATION','后续页面生成标准',r'''
# 页面生成约束 · 供后续 Skill 使用

本文件是可引用的页面生成标准，不是 Skill。后续 vocational-page-builder 应读取本文件、组件索引和实际源码，不把此前聊天中的方案当成已存在的组件API。

## 输入和版本
记录本次需求、角色、目标页面、组件库根目录及版本。先读取 data/components.json 和 data/tokens.json，再按需加载对应组件与模式。不得假设尚未实现的 props 或真实接口。

优先级：用户本次明确要求 → 指定版本组件库 → 页面/角色专项 → 旧页面实现 → 补充设计。用户未要求改业务时保留原权限、数据、事件和状态。业务专项只约束业务语义和权限，不以旧样式覆盖组件库公共视觉。

## 生成流程
1. 判断新建、整改或局部修改，建立CON01～05契约。
2. 从14类页面模式选择骨架，列出需求到具体组件标识的映射。
3. 使用现有渲染入口或从受控实现提取组件；引用主题变量，不再手画另一套近似控件。
4. 为真实任务补齐相关交互和数据适配。原型使用明示的虚构数据；实际系统沿真实接口，不用示例数据冒充。
5. 检查适用状态、长内容、错误恢复、键盘、焦点和内容溢出。
6. 输出文件、组件库版本、复用组件、局部扩展、检查结果和未覆盖事项。

## 必须遵守
- 标题28/36px衬线600，UI14/20px，控件36/30px、10px圆角，卡片14px/16px内边距，弹窗20px；AI专项优先。
- 主操作蓝底白字；颜色、间距、尺寸、阴影和动效引用变量。
- 内容Tabs与互斥选择均使用分段底轨，保留不同语义；表格口径、选择、排序、分页和导出一致。
- AI预填不自动发送；停止、失败、重试和草稿保留有实际行为。
- 禁止只靠Toast、空链接、“开发中”代替任务核心功能。
- 课程不绑定学期，不合并课程与独立实训。
- 不覆盖PPT、视频、图谱或考试的专用内容主题与行为。
- 不把生成、保存、审核、分发和发布混为一个状态。
- 用户输入必须转义；示例文件名不进入可执行HTML。
- 不私自改变组件库公共API或主题；按任务输出局部扩展说明。

## 缺口处理
先查组件变体，再组合已有组件。确需扩展时沿现有变量和规则设计，标明新增理由、状态、API、适用范围及是否应回收至公共库。没有真实能力的按钮应移除或明确禁用原因，不能伪装成功。

## 技术边界
当前是HTML原型库，table/chat等复杂组件使用内置示例数据。接入生产前必须将数据、权限、网络请求、版本和业务操作连接到真实控制器。框架项目优先包装或实现适配，不假装此目录已经提供Vue/React包。

## 完成标准
入口可运行；实际使用指定组件版本；关键业务路径可操作；适用异常有出口；已检查范围有证据；未检查不标通过。局部修改不重写无关页面，不静默修改公共库标准。

## AI 输入的资源能力
高职教页面的 AI 输入默认复用 voc-composer 的 `/` 资源选择和正文片段；按需读取 [INLINE_RESOURCES.md](INLINE_RESOURCES.md) 及 data/composer-resources.json。提供当前业务可见资源、稳定 ID 和父子关系，保留草稿及所选引用，不仅复制外观。该能力不代表已实现真实检索或课程绑定。

## 蓝白主体与蓝紫 AI 强调
普通管理页面继续引用品牌蓝色。只有 AI 发送、智能体图标、技能、AI 入口及输入框描边使用 ai-* 语义变量；AI 正文、卡片和工作区仍为白／浅灰蓝表面。聚焦增强、禁用退为中性色。删除与错误继续危险红色，不能把全站主色统一替换成紫色或在业务页面自行生成另一套渐变。

## 资源、技能与回答反馈
AI 输入必须先选资源类型再选对象；resourceTypes/resources 与 skills 由当前身份业务提供，不写死三端能力。技能使用内置／我的面板与正文前的可移除标签。完成消息提供按条保存的点赞／点踩。按需读取 INLINE_RESOURCES.md、SKILLS.md 及对应机器契约，不把 UI 选择视为真实执行或权限校验。
''')

add('LIMITATIONS','缺口与后续维护',r'''
# 交付成熟度与待补充项

## 已实现范围
60类HTML原型组件、14种组合模式、122个设计变量、21个旧变量别名，以及源码证据、词法映射和文档。所有演示数据虚构，未连接真实模型和业务服务。

## 明确未完成
- 原平台逐页整改和全平台回归；旧代码没有被修改。
- 线上指定智能体与执行服务的正常生成验收；当前访问受限。
- Vue/React组件包、生产权限、后端数据、真实审批、真实发布、跨页状态同步与永久版本保存。
- Office/PDF解析、真实语音、图片理解、知识库检索和模型接入；上传只显示元数据。
- 深色主题、移动端全量交互、旧浏览器和完整WCAG认证。
- PPT/图谱/视频编辑器引擎及正式考试控制；只提供外壳和保留边界。
- 教师四方向关联、三端上传限额、不同角色助手默认显隐等业务适配。
- 完整CommonMark解析、语法高亮、虚拟滚动、拖拽排序、可拖分栏、树复杂父子联选和复杂评分量表。

## 扫描边界
类名候选基于词法，未匹配类保留人工判断，不能把统计数量当成已规范化组件数量。后续每页迁移必须核对源选择器、事件和角色规则。候选映射全部 verifiedMigration=false。

## 依赖和资源
无新增运行依赖、远程字体、CDN或后台。图标几何复用当前本地项目UIIcons并补充少量同风格路径；未复制第三方编辑器或其依赖。原平台第三方库及许可证留在原处，不被本次删除或改写。

## 维护
版本是组件库交付版本，不是旧平台迁移进度。修改公共变量和组件API后，应复查代表性管理页、AI页及相关状态，更新规范与机器索引。仅在实际验证后登记通过。

资源选择器只使用提供给当前页面的目录；客户端资源有效性检查不能替代真实服务端权限、版本和归属校验。内置目录为虚构例子，不宣称读取真实资源内容。
''')

validation=R/'data/validation.json'
if validation.exists():
    v=json.loads(validation.read_text()); text='# 验证结果\n\n'+v.get('summary','')+'\n\n| 检查项 | 验证版本 | 结果 | 证据 |\n| --- | --- | --- | --- |\n'+'\n'.join('| '+x['name']+' | '+x.get('validatedVersion','未记录')+' | '+x['status']+' | '+str(x.get('evidence','')).replace('|','／')+' |' for x in v.get('checks',[]))+'\n\n'+v.get('limitations','')
else:text='# 验证结果\n\n实现正在验证，当前不宣称浏览器验收已完成。静态检查和实际交互检查分别登记。\n'
add('VALIDATION','验收与验证结果',text)

add('INLINE_RESOURCES','正文内资源选择',r'''
# 正文内资源选择 · v2.0.0

## 流程与来源
按用户最新修订，新插入资源必须先选类型，再选对象。`/` 与“引用资源”均进入类型层，不混排全部对象。现有 `js/programs.js` 的课程／单元内联槽位提供结构参考，通用类型层、专业、课时及端配置是用户本次明确要求的扩展。原平台控制器未改。

1. 第一层显示当前端允许的类型，例如课程、专业、课时、模板、教学资料；旧 unit 单元保留兼容。
2. 选择类型只进入第二层，不插入资源、不发送。第二层仅搜索此类对象，提供“返回资源类型”。Escape／关闭保持草稿；工具按钮打开后取消不插入斜杠，直接键入的 / 查询则保留。
3. 选对象后在原光标位置形成可替换片段，保留前后正文。点击已有片段直接换同类对象；不会跨类型替换原槽位。
4. 方向键选择，Enter 先进入类型或确认对象，不能误发。搜索支持无结果、不可用原因及返回上层。输入法组词期间不提交。资源与技能浮层在当前 dialog top layer 内使用。

## 各端配置
不在共享组件中写死教师／学生／管理端权限。业务方提供 `resourceTypes` 与已过滤的 `resources`，两个参数共同决定可展示的类型和对象。空数组表示不提供该能力，不回退到全量目录；未传时仅使用内置虚构目录。示例页的三端切换是配置演示，不等同正式权限清单。

resourceTypes 项：`{id,label,icon?,parentType?,multiple?}`，id 为稳定类型标识。支持业务自定义类型。内置默认 course课程、major专业、lesson课时、template模板、resource教学资料、unit单元。课时是可选择的教学内容对象，不是学时数值，不将 lesson 与 unit 按名称互相改写。

resources 项：`{id,type,label,parentId?,available?,reason?}`，id 全局唯一且稳定。只保留当前 resourceTypes 中存在的类型；名称不代替 ID。父子约束由 parentType 配置，示例中的课时／单元属于课程。删除或更换父引用清理不匹配下级引用，保留其余正文，不自动绑定新的子对象。multiple=true 可重复引用，提交 resources 按 ID 去重，segments 保留位置和顺序。

```javascript
VocUI.mount(container,'composer',{
 resourceTypes:[{id:'course',label:'课程'},{id:'lesson',label:'课时',parentType:'course'}],
 resources:[{id:'c1',type:'course',label:'人工智能导论'},
            {id:'l1',type:'lesson',label:'认识人工智能',parentId:'c1'}],
 segments:[{type:'text',text:'请为 '},{type:'resource',id:'c1'},{type:'text',text:' 整理学习要点。'}]
});
```

## 状态与边界
正文纯文本粘贴，默认上限8000字；片段可键盘更换或删除，仅移除引用，不删除源对象。禁用输入不可选择；失效、当前不可见和父子上下文不符均在发送／重试前再次校验，错误保留草稿。角色改变时销毁旧组件，用当前身份目录重建并隔离草稿，不能沿用其他身份引用。真实权限、版本和查询仍由业务服务复核。

## 实际 API
manifest runtime 顺序含 icons.js、resource-composer.js、skill-picker.js、voc-ui.js；页面组合额外加载 patterns.js。
`VocResourceComposer.getValue(element)` 返回 `{value,segments,resources}`；`setValue(element,value,segments?)` 安全恢复草稿；`setResources(element,resources)` 更新当前类型范围内的目录；`validate(element,snapshot?)` 校验当前或原轮引用；`openPicker(element)` 在当前光标打开类型层，无光标时追加到正文尾部；`sync(element)` 同步原生值适配器，通常由 VocUI 内部调用。

选择／编辑冒泡 `voc:resource-change`，包含 action,value,segments,resources。`voc:submit` 的 ai-send 包含 prompt,segments,resources,skill,simulated=true。隐藏 textarea[data-ai-input] 仅为旧值适配器，可见输入为 .v-resource-editor。

新建与切换会话分别保存正文、引用和技能；原轮重试使用原轮快照，不混入新草稿。会话与文件仅在当前页面，不提供真实检索、解析、入库或模型服务。状态验证以本次 data/picker-feedback-validation.json 为准，旧记录保留其原版本。
''')

add('SKILLS','技能选择与回答反馈',r'''
# 技能选择与回答反馈 · v2.0.0

## 技能面板
按用户截图，“添加技能”打开搜索面板，提供内置技能／我的技能两个页签及当前目录数量；支持说明、已选状态、无结果／空列表、禁用原因、键盘和关闭。按钮显示短文字“技能”（无障碍名称“添加技能”），选择不重命名按钮、不自动发送或覆盖正文。

选中项在白色输入面板内部、所有正文之前显示浅蓝紫标签；标签名称可重新选择，右侧 X 只移除技能，正文、附件和资源保持。当前实现单选；更换会替换原标签，不追加重复标签。技能随当前会话保留，发送后仍保持，用户 X 取消；新会话为空。每条提问记录自己的技能快照，原轮重试不借用新草稿选项。

`skills` 是当前身份可见目录：`{id,source:'builtin'|'my',name,description?,available?,reason?}`。`selectedSkill` 可初始化为 ID 或含 id 的记录。内置／我的只表示来源，不能当作执行权限。未传为虚构示例；空数组为空，不回退全量。需要更换身份时销毁旧组件并重新提供当前目录，不能把示例三端配置当权限规则。

`VocSkillPicker.getValue(element)` 返回当前记录或 null；`setValue(element,skillOrIdOrNull)` 恢复／取消；`setSkills(element,skills)` 更新目录；`validate(element,candidate?)` 校验当前或原轮技能。`VocUI.destroy` 清理浮层。组件只选择与携带 ID，不安装或执行真实 Codex Skill、不调用后台。

`voc:skill-change` 冒泡 detail `{action,skill}`；ai-send 的 `voc:submit` 包含 skill。真实业务方接收事件后按架构授权执行，不能把本地选择标签称为能力已运行。无效或当前不可见技能阻止发送并保留草稿。

## 回答点赞与点踩
完成的 AI 回答操作栏提供复制、重新生成、点赞、点踩。两者互斥，再点同项取消；按消息独立保存，切换会话后可恢复，不影响输入草稿。生成中、停止或失败不对未完成内容显示评价。重新生成产生新回答时反馈为空。

使用30px、8px圆角的纯图标按钮、可访问名称和 aria-pressed；选中浅蓝，点踩不复用危险红色，错误与删除语义仍独立。显示本次已点赞／已点踩／取消反馈，不伪造累计人数或后台收集成功。

`voc:feedback` 冒泡 detail `{messageId,value:'up'|'down'|null,simulated:true}`；真实反馈服务由业务接入。独立 message 示例使用本地生成标识，会话使用当前消息 ID；没有跨刷新持久化或评价统计。
''')

add('GENERATED_CONTENT','生成内容容器与插槽',"# 生成内容容器与业务插槽 v2.0.0\n\n## 当前边界\n用户2026-10-27明确收敛：通用组件库仅提供生成内容区域的外壳和预留插槽，不负责每一种业务内容。默认是空白占位，不再内置教学大纲、PPT、图谱、试题、简历等类型目录、编辑器、版本或业务动作。\n\n公共层负责：标题、收起／重新展开、可选工具栏、内部滚动、空／加载／就绪／错误状态，以及可选操作栏的外观和事件。\n\n业务层负责：具体预览与编辑器、业务字段、生成数据、校验、权限、版本、保存、审核、发布及资源关联。已有业务内容优先复用项目原有模块，组件库不要求重新实现，也不要求把所有内容转成某种统一数据结构。\n\n## 默认用法\n```js\nVocUI.mount(document.querySelector('#target'), 'workspace');\n// 默认仅显示内容展示区，无保存、分发、发布等业务操作。\n```\n\nprops：title（默认生成内容）、subtitle（可选）、state（empty/loading/ready/error）、statusText（可选状态文字）、actions（可选操作元数据，默认空）。显示ready时，业务方应已提供内容；组件不假称已生成、保存或审核。\n\n## 接入业务内容\n```js\nconst wrapper = document.querySelector('#target');\nVocUI.mount(wrapper, 'workspace', {title:'生成内容'});\nconst panel = wrapper.querySelector('[data-content-workspace]');\nconst editor = document.createElement('div');\n// 在editor上挂载业务项目现有的预览或编辑器。\nVocContentWorkspace.setContent(panel, editor);\n// 也可先取得插槽再挂载框架组件，随后声明就绪：\nconst slot = VocContentWorkspace.getSlot(panel);\nVocContentWorkspace.setState(panel, 'ready');\n```\n\nsetContent 接受DOM节点或纯文本；字符串始终作为文本，不执行HTML。框架页面在getSlot返回的节点上挂载已有组件并管理其卸载。组件库不检查或改写业务内容，不接管其内部状态。\n\n## 可选工具和动作\n`setToolbar(panel, node)` 挂载业务工具栏，传null隐藏。`setActions(panel, [{id,label,variant?,disabled?}])` 配置操作按钮，空数组隐藏整个操作栏。组件不自动添加保存／分发按钮。\n\n点击触发 `voc:workspace-action`，detail为 `{actionId,contentId}`。业务监听事件后完成自己的实际流程。错误状态的retry只是请求事件，业务处理后调用setState，组件不伪造重试成功。\n\n## 收放与会话\n收放只改变容器可见性，不重新渲染或销毁插槽中的业务DOM，输入和事件监听保持。内部滚动区域独立。\n\nAI会话展示一个通用工作区入口。自动打开或点击回答入口时发出 `voc:workspace-open`，detail含messageId，业务方据此关联该轮实际成果。`activate(panel, messageId)`按内容标识切换独立插槽节点，避免旧回答内容显示在新回答中；组件只缓存DOM和滚动位置，不设计业务数据、版本或保存规则。\n\nAPI还包括getState(panel)，返回 `{contentId,state,statusText}`。VocUI.destroy负责释放容器自身监听；业务订阅、框架实例、播放器、外部资源等仍需业务方按原架构卸载。所有示例仅在当前页面。\n\n## 后续页面生成规范\n1. 需要右侧生成区时，先复用workspace外壳，再挂载当前业务的内容模块。\n2. 不要求组件库穷举业务问题，不恢复默认全类型目录，不把某个示例编辑器升级为所有页面强制标准。\n3. 不因复用容器而改变原业务流程、权限、数据或版本逻辑。\n4. 验证插槽可挂载、收放不丢状态、加载错误反馈、滚动及实际业务关键流程。\n\n## 历史方案\nv1.4.0多类型示例已移入assets/archive/generated-content-1.4.0，仅作历史追溯，不再加载进当前运行时、索引或页面生成默认规范。历史验证记录保留其原版本，不能用于宣称当前版本已通过那些业务测试。\n")
D['GENERATION']['content']+='\n## 生成内容区域边界（v2.0.0）\n生成区仅复用容器和插槽，具体内容、预览编辑器、数据和业务流程由当前页面负责；参见design/GENERATED_CONTENT.md。不得默认加载全类型业务目录，也不要求所有业务采用内置编辑结构。\n'
D['API']['content']+='\n## 生成内容容器\nworkspace的title/subtitle/state/statusText/actions仅配置外壳；通过VocContentWorkspace.getSlot或setContent接入业务模块。可选动作使用voc:workspace-action；聊天入口使用voc:workspace-open。详见design/GENERATED_CONTENT.md与data/workspace-contract.json。\n'

alignment=json.loads((R/'data/reference-alignment.json').read_text())
add('REFERENCE_ALIGNMENT','参考一致性审计',alignment['documentation'])
items=json.loads((R/'data/component-alignment.json').read_text())['components']
add('COMPONENT_ALIGNMENT','60项组件对照','# 逐组件对照 v2.0.0\n\n60项均已映射到参考条款或公共控件组合；implemented表示已实施，不等于线上逐状态复刻。线上实测范围见参考一致性审计。\n\n| 标识 | 组件 | 依据 | 统一后的实现 |\n| --- | --- | --- | --- |\n'+'\n'.join('| '+x['id']+' | '+x['name']+' | '+x['reference']+' | '+x['implementation']+' |' for x in items)+'\n')
D['GENERATION']['content']+='\n## v2.0.0参考统一要求\n先读取data/library.json与data/component-alignment.json，按指定版本使用公共组件、变量和模板。常规按钮36/30px、10px圆角；卡片14px圆角/16px内边距；弹窗20px；Tabs分段；对话15px开放正文与头像元信息。不得恢复旧尺寸、下划线Tabs或无元信息回答。资源类型→对象、技能前置标签、局部蓝紫、危险删除和空生成插槽保持。文档未定义的业务能力通过公共组件组合，局部扩展要注明，不静默改标准。参考线上核验与文档实施分开，见REFERENCE_ALIGNMENT.md。\n'
D['SKILLS']['content']+='\n## v2.0.0反馈细节\n点踩先打开原因Popover（单选原因可不选、说明选填最多500字），确认后更新本地评价；取消保留旧值。点赞/点踩互斥且重复点击撤销。技能来源采用同一分段底轨和白色滑块；标签28px胶囊、移除22px按钮，保持正文之前。\n'
D['API']['content']+='\n## v2.0.0公共适配\n组件render/mount及既有参数保持；Tabs视觉改为分段，不改变tab/tabpanel语义。反馈voc:feedback增加reason/comment字段，点踩确认后才更新；编辑提问保留本轮附件、资源与技能；重新生成只替换点击的回答。select(label,options,value,props)的options可携带disabled/reason，禁用理由可见。\n'
D['API']['content']+='\n## AI添加内容与文件引用\ncomposer/chat 的 files 为当前可见我的文件目录；＋菜单提供上传、我的文件及高职教引用扩展。附件ID与版本通过ai-send的attachments传递；不代表已上传或解析。线上受阻范围、文件字段和交互依据见REFERENCE_ALIGNMENT.md。\n'

add('TEACHING_AGENTS','教师输入与关联Agent',(R/'design/TEACHING_AGENTS.md').read_text())
D['API']['content']+='\n## 教学关联Agent预览\ncomposer/chat/conversation支持agentOptions与selectedAgents；[]隐藏整组，参数/事件/快照见TEACHING_AGENTS.md。发送事件增加agents；本地示例未连接真实服务。\n'
D['GENERATION']['content']+='\n## 教师输入的教学关联\n教师场景按需读取TEACHING_AGENTS.md及data/teaching-agents.json。资源正文片段、技能前置标签、关联Agent多选分开；底栏入口统一资源/技能短文字。Agent目录与后台绑定由业务提供，学生/其他场景明确传agentOptions:[]隐藏。生成中锁定本轮，重试沿用原轮快照；不得把示例AgentID当真实服务。生成内容仍为空插槽。\n'
D['AI']['content']+='\n## 教学关联Agent\n按需使用可多选的教学关联，目录由当前业务提供。选择只改草稿，发送时携带agents；生成中锁定、按会话隔离、按原轮重试。详见TEACHING_AGENTS.md。\n'
for k,v in D.items():(R/'design'/f'{k}.md').write_text(v['content'])
(R/'js/docs.js').write_text('window.VocDocs='+json.dumps(D,ensure_ascii=False)+';\n')
(R/'data/page-patterns.json').write_text(json.dumps([dict(id=i,name=n,context=c,components=cs.split(' / '),version='2.0.0',contract={'identity':'虚构示例角色；真实权限待适配','data':'本地虚构示例','retention':'本次页面内存，刷新重置','source':'js/patterns.js','maturity':'HTML 交互原型'}) for i,n,c,cs in pattern_rows],ensure_ascii=False,indent=2)+'\n')

for ident,name,_,_ in pattern_rows:
    filename='management' if ident=='list' else 'ai-workspace' if ident=='chat' else ident
    html=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} · 高职教 UI 示例</title><link rel="stylesheet" href="../css/tokens.css"><link rel="stylesheet" href="../css/components.css"><link rel="stylesheet" href="../css/showcase.css"></head><body><header class="site-header" style="position:relative"><a href="../index.html#/patterns" style="text-decoration:none;font-size:13px">← 返回组件库</a><span class="v-caption">高职教 UI 2.0.0 · 虚构数据 · 仅本地演示</span></header><main style="max-width:var(--v-page-max);margin:0 auto;padding:32px clamp(24px,2vw,40px) 48px"><div id="page"></div></main><script src="../js/icons.js"></script><script src="../js/resource-composer.js"></script><script src="../js/skill-picker.js"></script><script src="../js/content-workspace.js"></script><script src="../js/voc-ui.js"></script><script src="../js/patterns.js"></script><script>VocPatterns.mount(document.querySelector('#page'),'{ident}');</script></body></html>'''
    (R/'examples'/f'{filename}.html').write_text(html)
for entry in [R/'index.html',*list((R/'examples').glob('*.html'))]:
    def fingerprint(m):
        attr,ref=m[1],m[2].split('?')[0]
        f=entry.parent/ref
        return attr+'="'+ref+'?v='+hashlib.sha256(f.read_bytes()).hexdigest()[:10]+'"' if f.is_file() and f.suffix in {'.css','.js'} else m[0]
    entry.write_text(re.sub(r'(href|src)="([^"#]+\.(?:css|js)(?:\?[^\"]*)?)"',fingerprint,entry.read_text()))
print('Generated',len(D),'documents and',len(pattern_rows),'standalone templates')
