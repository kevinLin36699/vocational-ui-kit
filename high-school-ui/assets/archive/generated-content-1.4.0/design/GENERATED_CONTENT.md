# 多类型生成内容工作区 v1.4.0

## 本次依据与范围
此前只有固定教学大纲文本框。本次实际检查高职教原代码中的产品生成、课程包、课程目录、作业考试、独立实训、求职、升学、证书、竞赛及管理端工作区，提取 22 个代表性成果配方，归并为 14 种内容渲染结构。逐项来源、行号、摘录和处理结论见 data/generated-content-index.json。本次没有重新扫描或重置旧平台历史快照，不声称穷尽所有业务分支。

## 选择结构而非套用文本框
| 渲染标识 | 适用内容 | 预览与编辑 |
| --- | --- | --- |
| document | 教学大纲、项目报告、培养方案、招生文案 | 分节阅读，逐节修改标题和正文 |
| slides | PPT课件 | 切换页面、正文与讲者备注；逐项编辑及调整页序 |
| interactive | 互动HTML课堂 | 问题选择与反馈；编辑活动、选项及答案 |
| video | 视频分镜 | 镜头、画面、讲稿与时长；没有成片就显示分镜，不提供假播放器 |
| graph | 知识／能力图谱 | 点选节点、查看前置关系；编辑标识和说明，校验循环与失效引用 |
| questions | 作业、课程考试 | 核对题干、选项、答案和解析；不创建学生作答记录 |
| course | 课程方案 | 单元目录、内容与学时，普通课程与独立实训分开 |
| practice | 独立实训任务 | 目标、输入输出、交付材料与评价要求 |
| package | 课程包 | 成员成果与查看入口，关联同一集合中的内容；保存快照含成员正文 |
| report | 学情、质量、模拟练习报告 | 同一数据驱动指标、对比条和明细；数值可为0 |
| plan | 成长、证书备考计划 | 阶段行动、日期与完成记录 |
| checklist | 升学材料、认定核对 | 事项、依据、完成记录；不自动决定资格或认定结果 |
| resume | 简历 | 独立简历版式及分节编辑；虚构个人信息 |
| workflow | 智能体配置 | 节点、输入输出与后续关系；不表示模型或工具已执行 |

## 公共外壳与数据
- 工作区名称统一“生成内容”，具体成果使用业务名称。当前任务的多份成果使用选择器切换，按业务组组织，不将全目录当成一次生成结果。
- 预览、编辑、内部滚动、独立版本、收起／恢复、导出和按类型的后续动作使用同一公共外壳。
- props.contents 未传时，独立 workspace 展示虚构类型目录；明确空数组表示暂无内容，绝不回退到全量。真实页面必须由业务方传入当前任务的成果集合。
- 每项数据：`{id,kind,title,group?,summary?,action?,status?,items:[]}`。id 在集合内唯一；kind 对应上表；items 的字段可查询 `VocContentWorkspace.kinds[kind].fields`，配方见 data/generated-content-examples.json。
- `status` 为 ready／waiting／generating／failed。未完成内容不能保存为完成版本；失败提供 voc:content retry 事件，业务方重试后 setContents 或 setValue 更新，组件不伪造成功。
- action 为 archive／package／review／plan／course。archive 仅保存与导出；其他类型打开目标及说明表单，记录本地请求。真实资源广场、审核、计划采纳与课程绑定由业务接入；不以只弹 Toast 代替流程，也不声称已写入后台。

## 使用
```js
const outputs = VocContentWorkspace.samples(['outline','slides','knowledge','homework','package']);
VocUI.mount(document.querySelector('#target'),'workspace',{contents:outputs,activeId:'slides'});
// 聊天组件的本地示例每轮返回指定集合，不从提示词猜测真正业务结果。
VocUI.mount(document.querySelector('#chat'),'chat',{contents:outputs});
```

按 data/library.json 顺序引用 runtime；新增 content-data.js 和 content-workspace.js 位于 voc-ui.js 前。data/generated-content-examples.json 是虚构示例唯一数据源；scripts/build_content.py 生成离线 content-data.js，不手改副本。

## 草稿与版本
- 每份成果分别保留编辑草稿，切换成果、内容视图及收放不丢失。编辑不覆盖其他成果。
- 保存首版1.0，后续1.1、1.2…；保存版本只读，返回“当前草稿”后继续编辑和另存版本。不会将修改写回历史版本。
- 保存课程包时，成员内容随该版一起快照；后续修改成员不改变旧课程包快照。成员尚未独立保存时如实记录“未保存草稿快照”，不伪造已保存版本。
- 版本仅在当前页面；刷新重置。并非资源广场的真实持久化，权限由调用方提供 readonly 和当前允许的目录，示例业务组不是角色权限。
- AI 会话每条已完成回答保存各自内容集合与状态；查看旧回答后编辑不会写入新回答。会话切换不将内容混在一起。

## API 与事件
- `VocContentWorkspace.samples(ids?)` 取得虚构配方副本；传入 id数组精确选择，空数组为空。
- `getValue(root)` 返回当前状态快照；`setValue(root,state)` 恢复同一工作区状态；`setContents(root,contents,{readonly?,activeId?})` 替换本任务内容。root 是 `[data-content-workspace]`，不是外层展示容器。
- `voc:content` 冒泡 detail：`{action,contentId,simulated:true,...}`。action 为 change／select／save／request／retry／export；save 含 version,snapshot，request 含 request,snapshot。真实任务处理应依据接口返回状态更新，不能仅凭本地事件显示业务成功。
- 文本及结构数据都按文本转义，不执行任意HTML、脚本、模型或节点配置。图谱为关系阅读与节点编辑，不是原平台专业画布。

## 输出边界
文档、简历、实训可导出 Markdown；其他类型导出 JSON 结构数据。按钮明确文件格式，不把JSON下载命名为PPTX、MP4或已运行的HTML。完整PPT画布与文件导出、任意互动HTML沙箱、视频制作与播放器、考试发布和作答隔离、真实简历投递等沿用原平台专用实现。组件库提供可复用容器和类型交互，不重写整个业务系统。

## 页面生成要求
1. 先根据业务任务选择产物结构并提供真实当前集合，不把所有结果放进textarea。
2. 读取索引来源与 gaps，专业编辑场景复用目标项目既有编辑器，通过局部适配嵌入公共外壳。
3. 生成、审核、保存版本、资源归档、课程绑定和正式发布分别表达，按原业务控制器执行。
4. 至少验证一种非文本成果、跨成果草稿隔离、只读历史、当前任务状态和真实可用的后续动作。
