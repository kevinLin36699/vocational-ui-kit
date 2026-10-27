# 教师输入与教学关联 Agent · 交互预览

本次是高职教输入区的优化预览。蓝白主体、技能浅蓝紫标签、资源类型→对象和空生成插槽继续保留。示例：examples/teacher-input.html。

## 三类选择
- 资源：引用课程、专业、课时、模板等对象，在正文内显示蓝色片段，保留稳定ID。
- 技能：当前单选，内置/我的面板；选中后在所有正文前显示标签，可X取消。
- 教学关联：底栏的产业、就业、政策、技术等可独立多选，不替换技能、不修改正文；名称和实际Agent绑定由业务提供。

## 工具栏
「＋ 资源」「技能」统一为图标+短文字，30px高、13px字、相同内边距；资源使用浅蓝底和品牌蓝字，技能使用浅蓝紫底和AI紫字，悬停/展开时同色细边加强。两入口间距6px。「资源」保留上传文件/我的文件/引用资源菜单。

四个关联选项不显示“教学关联”标题，保留组的无障碍名称；与操作入口以细竖线分组，28px浅中性底圆角选项；选中浅蓝底和勾，重复点击取消，宽度不因勾出现而跳动。空间不足时左侧内容自然换行，字数和发送固定在右下侧，不把发送挤出容器。资源类型图标名称同行和编辑区单层焦点的修正保留。

## 配置
composer、chat、conversation新增：
- agentOptions: [{id,label,agentId,available?,reason?}]，当前身份可见且允许选择的关联目录。
- selectedAgents: string[]，初始选中的关联id；默认未选。

显式agentOptions:[]隐藏整组，不显示空分隔线。组件展示配方缺省展示四项教师虚构示例；学生学习模板及三端配置示例明确传空数组。真实页面必须按角色和业务提供目录，不能用示例目录充当权限控制。demo-agent-*仅为演示标识，不代表真实后台Agent。

```js
VocUI.mount(document.querySelector('#input'), 'composer', {
  agentOptions: [
    {id:'industry', label:'产业', agentId:actualIndustryAgentId},
    {id:'policy', label:'政策', agentId:actualPolicyAgentId}
  ],
  selectedAgents: []
});
```

VocUI.getSelectedAgents(element)返回当前选中记录；setSelectedAgents(element, idsOrRecords)用于恢复当前目录中的选择。需要更换角色/目录时重新挂载组件，清理旧身份状态。输入保留、版本和真实权限由当前业务控制。

## 发送与执行
点击关联仅触发voc:change，detail.action='teaching-agents'，detail.agents为当前选择；不发送、不调用真实服务。主动发送后的voc:submit（action='ai-send'）增加agents数组，每项含id/label/agentId/available/reason；skill、resources、segments、attachments仍分别保留。

业务接收事件后由服务端核验Agent标识、权限和任务上下文并调度。前端不能仅凭available=true声明服务可调用，不把本地步骤显示称作真实检索成功。

chat在每条提问和回答上保存本轮选择快照，处理过程按所选关联插入明确标为「本地模拟」的Agent步骤。生成中禁止修改关联；停止后可调整下一轮。重试沿用被重试轮次的快照，不读取新草稿选择；目录中对应标识不可用或绑定变化时阻止重试并保留输入。

同一会话继续沿用所选项；新会话为空；切换会话恢复各自选择。编辑历史提问同时恢复对应的资源、技能、附件和关联。未传入的Agent不显示为已执行，不生成虚构来源。

当前原型只有本地模拟，未连接真实Agent/模型/检索服务；生成内容保持通用空插槽。真实调用和每个Agent的服务失败恢复由生产项目的接口及架构接入。

## 关联项外观
默认态使用浅中性底色、6px圆角与居中文字，不预留勾选空位；选中后显示蓝底、蓝字和勾。短标签最小宽度60px，切换时不挤动相邻选项。

输入正文区域默认最小高度112px，聚焦时128px；内容继续自然增高，达到现有上限后内部滚动。工具栏和技能前置区域另计高度。
