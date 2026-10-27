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
