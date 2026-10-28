# 生成内容容器与业务插槽 v2.7.1

## 当前边界
用户2026-10-27明确收敛：通用组件库仅提供生成内容区域的外壳和预留插槽，不负责每一种业务内容。默认是空白占位，不再内置教学大纲、PPT、图谱、试题、简历等类型目录、编辑器、版本或业务动作。

公共层负责：标题、收起／重新展开、可选工具栏、内部滚动、空／加载／就绪／错误状态，以及可选操作栏的外观和事件。

业务层负责：具体预览与编辑器、业务字段、生成数据、校验、权限、版本、保存、审核、发布及资源关联。已有业务内容优先复用项目原有模块，组件库不要求重新实现，也不要求把所有内容转成某种统一数据结构。

## 默认用法
```js
VocUI.mount(document.querySelector('#target'), 'workspace');
// 默认仅显示内容展示区，无保存、分发、发布等业务操作。
```

props：title（默认生成内容）、subtitle（可选）、state（empty/loading/ready/error）、statusText（可选状态文字）、actions（可选操作元数据，默认空）。显示ready时，业务方应已提供内容；组件不假称已生成、保存或审核。

## 接入业务内容
```js
const wrapper = document.querySelector('#target');
VocUI.mount(wrapper, 'workspace', {title:'生成内容'});
const panel = wrapper.querySelector('[data-content-workspace]');
const editor = document.createElement('div');
// 在editor上挂载业务项目现有的预览或编辑器。
VocContentWorkspace.setContent(panel, editor);
// 也可先取得插槽再挂载框架组件，随后声明就绪：
const slot = VocContentWorkspace.getSlot(panel);
VocContentWorkspace.setState(panel, 'ready');
```

setContent 接受DOM节点或纯文本；字符串始终作为文本，不执行HTML。框架页面在getSlot返回的节点上挂载已有组件并管理其卸载。组件库不检查或改写业务内容，不接管其内部状态。

## 可选工具和动作
`setToolbar(panel, node)` 挂载业务工具栏，传null隐藏。`setActions(panel, [{id,label,variant?,disabled?}])` 配置操作按钮，空数组隐藏整个操作栏。组件不自动添加保存／分发按钮。

点击触发 `voc:workspace-action`，detail为 `{actionId,contentId}`。业务监听事件后完成自己的实际流程。错误状态的retry只是请求事件，业务处理后调用setState，组件不伪造重试成功。

## 收放与会话
收放只改变容器可见性，不重新渲染或销毁插槽中的业务DOM，输入和事件监听保持。内部滚动区域独立。

AI会话展示一个通用工作区入口。自动打开或点击回答入口时发出 `voc:workspace-open`，detail含messageId，业务方据此关联该轮实际成果。`activate(panel, messageId)`按内容标识切换独立插槽节点，避免旧回答内容显示在新回答中；组件只缓存DOM和滚动位置，不设计业务数据、版本或保存规则。

API还包括getState(panel)，返回 `{contentId,state,statusText}`。VocUI.destroy负责释放容器自身监听；业务订阅、框架实例、播放器、外部资源等仍需业务方按原架构卸载。所有示例仅在当前页面。

## 后续页面生成规范
1. 需要右侧生成区时，先复用workspace外壳，再挂载当前业务的内容模块。
2. 不要求组件库穷举业务问题，不恢复默认全类型目录，不把某个示例编辑器升级为所有页面强制标准。
3. 不因复用容器而改变原业务流程、权限、数据或版本逻辑。
4. 验证插槽可挂载、收放不丢状态、加载错误反馈、滚动及实际业务关键流程。

## 历史方案
v1.4.0多类型示例已移入assets/archive/generated-content-1.4.0，仅作历史追溯，不再加载进当前运行时、索引或页面生成默认规范。历史验证记录保留其原版本，不能用于宣称当前版本已通过那些业务测试。
