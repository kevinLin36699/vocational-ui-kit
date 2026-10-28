# 可配置控件与业务组合 · 2.2.0

使用 data/library.json 的 styles、runtime 顺序加载资源，再加载 patternsRuntime（需要页面模式时）。VocUI.render / mount / hydrate / destroy 保持；新增控件以数据配置，文本始终转义，不执行传入的 HTML。

## 2.2 组件家族与变体

本轮完整清单与独立类型见 [COMPLETENESS.md](COMPLETENESS.md)。新增 `temporal.js` / `extended-controls.js` / `extended-controls.css` 按 library.json 加载。date 保留旧 single/range 接口；新页面可按场景直接使用 date-picker/date-range、time-picker/time-range、datetime-picker/datetime-range、year-picker/year-range、month-picker/month-range、week-picker/quarter-picker/multi-date。新面板采用选择草稿后确认；只读/禁用及清空由公共组件处理。

通用基础组件参数以 [API.md](API.md) 当前矩阵为准；checkbox/radio/switch/tabs/steps/tree/chart 等已支持数据配置，替代旧固定演示约束。

## 日期与时间

`VocUI.mount(host,'date',{mode:'range',label:'教学日期',value:['2026-10-27','2026-11-03'],min:'2026-01-01',max:'2027-12-31',disabledDates:['2026-11-05']})`。

mode=single 时 value 为日期字符串或 null；默认 range 时 value 为两个日期字符串或 null。值均为 YYYY-MM-DD，不转成 UTC 时间戳。业务时区说明为 Asia/Shanghai，日期计算使用纯日历规则。

单外框内含两个文本端点、分隔、清空和日历按钮；宽容器双月、窄容器单月。第二个日期早于起点时重新选起点，同日允许；范围内禁选日期会阻止提交。只提交完整合法值。Esc 和外部关闭丢弃未完成选择；上次完整值保留。手动输入 Enter 提交；无效值保留并提示，Esc 恢复。上下左右、Home/End、PageUp/PageDown 移动日历焦点，Enter/Space 选择；向下键从输入框进入日历。

`voc:change` 的 date-change 含 `{action,value,name}`；清空 value=null。`name` 是开始或单日期隐藏表单字段，`endName` 是结束字段，默认 start/end（single 默认 date）。原生隐藏字段不承担必填验证，业务表单应验证控件值；内置课程表单已接入。

`time-picker` 使用 HH:mm，支持 value/name/min/max/step/disabled/readonly；step 为分钟面板步长。输入校验成功后发出 time-change，非法时间不作为有效值。

## 选择与组织

- select：options 为字符串或 `{value,label,disabled?,reason?}`，value 为稳定字符串；label/name/placeholder/disabled 可配置。
- multiselect：options 同上，values 为初始字符串 ID 数组；标签在框内显示，maxTagCount默认2并按实际宽度收纳，+N展开已选管理。移除按钮独立可达，长标签省略且保留title。
- tree-select：nodes 为 `{id,label,children?,disabled?}[]`，value 单个 ID；multiple=true 时为 ID 数组；leafOnly=true 限制叶节点。搜索包含祖先路径，已选项可移除。
- cascade：复用树选择，默认院系→专业，提交专业ID，不再用两个分离下拉展示同一层级。
- academic-term：terms 为 `{id,year,label}[]`；学期边界和目录由业务提供，示例不推定真实校历。
- person-picker：items 为 `{id,name,department?,disabled?}[]`，value 为 ID 数组。弹窗中的搜索、选择、取消都不改外部值；确认后发出 people-select。

`VocControls.getValue(element)` 获取已挂载控件当前值；选择器 select/multiselect 使用其隐藏 input 和 voc:change，表格使用独立 API。不向未声明参数传入伪回调或私有源码字段。

## 表格

```javascript
VocUI.mount(host,'table',{
  title:'教学资源',rowKey:'id',pageSize:10,editable:false,
  rows:[{id:'r1',name:'课程任务说明',owner:'林老师'}],
  columns:[{key:'name',label:'资源名称',sortable:true},
           {key:'owner',label:'负责人'}]
});
```

columns 支持 key/label/type（number/date/status）/sortable/align（end）/hidden/required/min/max/options/editable。内容按文本输出，不接收任意 HTML 渲染器；复杂单元格通过页面局部适配，不编造 render 参数。

filters 为 `{key,label,options}[]`；未传 rows 时才提供课程示例及其筛选，传入自定义 rows 默认无课程筛选、无编辑功能。editable=true 可启用本地通用增改删，不能当生产写入。每行 rowKey 唯一且非空；保留编号前导零。隐藏列至少留一列。

搜索、筛选、排序、分页、选择、导出共用同一数据集合。选择限定当前页，换页、修改筛选或排序时清空；取消勾选不会改变其他行。支持5/10/20/50每页；默认10。导出当前筛选或所选的可见列，CSV字段转义并防公式前缀。

`VocDataTable.getState(host)` 返回当前 rows/page/pageSize/query/selected/visible 副本；`setRows(host,rows)` 替换数据、校验ID并清空选择。相关 voc:change 为 table-render、table-save、table-delete、table-export；保存/删除只在明确确认后执行，带 simulated:true。

## 新增展示与反馈

- collapse：items `{id,title,content,disabled?}[]`、openKeys、accordion；content 为文本，内容 DOM 不因收起销毁。
- rate：label、labels、value、disabled、readonly；五级文字默认定义，可配置其他级数。左右方向键/Home/End 选择，不冒称专业评分量表。
- calendar：month=YYYY-MM、value=日期、events=`{id,date,title,type?}[]`；按日期显示事件，发出 calendar-select；没有排课冲突、拖拽调课或真实发布引擎。
- notification：items=`{id,title,description?,read?}[]`；本地已读和详情，发出 notification-open / notifications-read。
- image-preview：src、alt；模态大图、50%–300%缩放、旋转和加载失败反馈，不解析 Office/PDF。
- feedback-result：kind=success/error/forbidden/notfound，支持标题、描述、actionLabel；动作发出 result-action，由当前业务处理。
- empty：kind=empty/no-match/failed；首次创建可打开课程演示表单；自定义操作和恢复动作发出 empty-action，不能自动声称后台已恢复。
- confirm：模态与轻量气泡确认都先取消优先，确认后发出 confirm；调用方承担实际删除。
- resource：items=`{id,name,type?,size?,version?,description?}[]`、view=list/grid。目录搜索、详情与本地示例文本下载；不是实际文件读取服务。

## 名单导入

`batch-import` 及 import 页面模式：CSV/TSV/TXT或粘贴Excel，表头学号/姓名/班级，班级可选。单文件2MB、最多1000条。校验缺项、重复学号、已导入学号和字段长度。错误可定位回原始行、导出明细；修改内容使旧预览失效，重新校验后才能确认。全部通过且明确确认后加入当前页面名单。

voc:submit `{action:'roster-import',rows:[{id,name,className}],simulated:true}`。文件异步读取带实例与版本检查，卸载后不得写回。解析支持引号、引号转义、逗号和带引号换行；不支持真实Excel二进制解析或永久保存。

## 生命周期与业务边界

扩展控件由 VocUI.hydrate 激活，destroy 清理实例事件、弹层与观察器。AI资源、技能、Agent快照和空工作区沿用现有契约。不能从“UI能点击”推断服务、权限、查询来源或业务发布已经完成。

## 2.1.1交互细节
日期显示YYYY/MM/DD，公开事件与表单值仍为YYYY-MM-DD；框内多选、树多选、分页、图表明细和公共hover规则见INTERACTION_DETAILS.md。
