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

## 生成内容容器
workspace的title/subtitle/state/statusText/actions仅配置外壳；通过VocContentWorkspace.getSlot或setContent接入业务模块。可选动作使用voc:workspace-action；聊天入口使用voc:workspace-open。详见design/GENERATED_CONTENT.md与data/workspace-contract.json。

## v2.0.0公共适配
组件render/mount及既有参数保持；Tabs视觉改为分段，不改变tab/tabpanel语义。反馈voc:feedback增加reason/comment字段，点踩确认后才更新；编辑提问保留本轮附件、资源与技能；重新生成只替换点击的回答。select(label,options,value,props)的options可携带disabled/reason，禁用理由可见。

## AI添加内容与文件引用
composer/chat 的 files 为当前可见我的文件目录；＋菜单提供上传、我的文件及高职教引用扩展。附件ID与版本通过ai-send的attachments传递；不代表已上传或解析。线上受阻范围、文件字段和交互依据见REFERENCE_ALIGNMENT.md。

## 教学关联Agent预览
composer/chat/conversation支持agentOptions与selectedAgents；[]隐藏整组，参数/事件/快照见TEACHING_AGENTS.md。发送事件增加agents；本地示例未连接真实服务。
