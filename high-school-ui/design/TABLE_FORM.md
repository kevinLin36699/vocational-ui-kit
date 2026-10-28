# 通用表格、表单与补充交互 · v2.3.0

预览入口：[表格、表单与补充交互](../examples/table-form.html)。23个表格/表单配置与6个补充交互直接挂载公共组件，可在「编辑配置」中替换JSON。资源、活动和设备等数据只是页面配置，不写死在组件控制器中。

## 依赖与公共入口

依次加载data/library.json中的styles/runtime。新增schema-form.js、advanced-table.js、common-extras.js与common-data.css。data-table.js保留旧版本源码，由advanced-table.js替换公开table/toolbar渲染器与VocDataTable控制器；业务只使用最终公共接口。手工render后必须hydrate，移除前destroy。

```javascript
VocUI.mount(host, 'form', {
  fields: [
    {name:'asset', label:'设备编号', type:'text', required:true},
    {name:'quantity', label:'数量', type:'number', min:0, unit:'台'}
  ],
  values: {asset:'EQ-001', quantity:0}
});
VocForm.setHandlers(host, {
  submit: async (values, {signal, requestId}) => {
    // 在这里接入当前业务，成功后返回ok:true；不要把演示反馈当真实入库。
    return {ok:true, message:'业务处理器已确认'};
  }
});
```

JSON配置不传入函数。异步校验、提交、加载和写入函数通过实例方法绑定；销毁和取消传递AbortSignal，旧请求回执不会覆盖新请求。

## 表格类型与数据

| 类型/交互 | 实际配置与行为 |
| --- | --- |
| 常规列表 | rows、columns、rowKey、filters；自定义rows不继承课程筛选或自动允许编辑 |
| 单元格 | text、number、status、tags、boolean/switch只读值、progress、link、image、date；null/空显示—，保留0与false |
| 选择 | selectable=false/single/默认复选；selectionScope=page/across；disabledRowKeys和行_selectionDisabled锁定选择 |
| 搜索/排序/分页 | 搜索与字段筛选使用同一数据集合；排序升序→降序→清除；页容量、页码、边界和直达页；中文输入法完成后查询 |
| 树形表 | tree:true，childrenKey默认children；默认不分页，显式pagination:true按根节点分页并保留子项；祖先路径保留、节点展开与选择独立 |
| 分组表 | groupBy指定字段，分组显示数量，可折叠 |
| 行详情 | expandable:{fields:[...]}，展开配置字段，不注入固定课程详情 |
| 多层表头 | columns含{label,children:[...]}；叶子key唯一，真实rowspan/colspan |
| 合并单元格 | 列merge:true按当前页相邻值纵向合并；mergeCells指定rowId、column、rowSpan、colSpan，覆盖格不重复渲染 |
| 汇总 | summary:true或文案；数字默认sum，列summary支持sum/avg/count/min/max；基于筛选结果，树形聚合叶子记录 |
| 固定与调整 | scrollY/height固定区域内表头；列fixed=left/right；fixedActions；resizable默认true，拖动或左右键按10px调整 |
| 顺序 | columnReorder拖动平铺列头，列面板提供显隐、固定和上下移动；rowReorder拖动手柄或Alt+上下键 |
| 单元格编辑 | editable:true、editMode:cell；双击或Enter进入，保存前校验，Esc取消，换页或排序保护未保存修改 |
| 表单编辑 | 默认弹窗编辑，复用同一schema表单和校验，不维护第二套固定字段 |
| 批量操作 | 本页/跨页已选数量明确；可选择全部本地筛选记录、导出、危险确认后删除；只读记录不被批量删除 |
| 大数据 | virtual:true固定行高窗口化；10,000条示例仅渲染可见记录，筛选排序仍基于完整集合 |
| 状态 | loading、empty、no-match、failed/retry、forbidden、readonly；失败保留查询参数，无权限不显示数据 |

全量参数在API.md。行_readonly禁止该行编辑/删除；删除树形父项也会检查只读后代。客户端这些规则是交互约束，真实权限仍由服务校验。

### 表格实例方法

- VocDataTable.getState(host)：rows/page/pageSize/query/filters/sort/selected/visible/order/widths/status/requestId的快照。
- setRows(host,rows,{keepPage?,preserveSelection?})：校验唯一ID后替换数据，默认清空选择和回到第一页。
- setState(host,status,message?)、setSelected(host,ids)、request(host)。
- setLoader(host,async(params,{signal,requestId})=>({rows,total}),{immediate?:true})：绑定真实查询或明确的模拟器。
- resolve(host,{requestId,rows,total,error?})：事件模式回执，只接受当前请求编号。
- setMutator(host,async(request,{signal,mutationId})=>({ok,message?,fieldErrors?}))：绑定新增/修改/删除处理器。
- resolveMutation(host,{mutationId,ok,message?,fieldErrors?})：事件模式写入回执。未确认时保持等待，不提前改远程记录或显示成功。
- exportCSV(host,selectedOnly?)：返回当前可导出CSV；导出按钮下载同一份内容。公式前导字符被转义。

remote模式的rows只表示当前平铺页，total为服务端总数。搜索、筛选、排序、翻页产生table-query，携带query/filters/sort/page/pageSize/requestId。可在业务控制器接收事件后调用resolve；或绑定loader。

远程写入产生table-create-request/table-update-request/table-delete-request，含mutationId和对应values/patch/ids。取消与卸载使本地等待失效；真实服务如何取消或回滚由业务定义。写入确认后重新查询数据。跨页导出有未加载ID时发出table-export-request，由业务提供真实完整导出，不把本页文件冒充全量。

## 表单字段配置

| 配置 | 含义 |
| --- | --- |
| name/label/type | name为作用域内唯一的字母/数字/下划线/短横线标识，type默认text；不接受原型链关键字 |
| defaultValue/values | 默认值与初始对象；支持0、false、数组；字段可任意替换 |
| 基础字段 | text/email/url/tel/password/textarea/number/hidden/display/richtext |
| 选择字段 | select/multiselect/radio/checkbox/switch/slider/rate/color |
| 时间字段 | date/date-range/time/time-range/datetime/datetime-range/month/year/quarter/week/multi-date |
| 组织与资源 | tree-select/cascade/person-picker/academic-term/upload；沿用已绑定组件的配置 |
| required/requiredWhen | 固定或条件必填；switch必填表示必须勾选同意 |
| min/max/step | 数字范围与步长；日期/时间透传对应限制 |
| minLength/maxLength/pattern | 数组或正文长度、正则格式；富文本按纯正文计算长度 |
| rules | {type:pattern/min/max/minLength/maxLength/sameAs,value?,field?,message?}[] |
| after/sameAs | 与关联字段比较日期顺序或值相同 |
| visibleWhen/disabledWhen | {field,equals?/notEquals?/in?/truthy?}或条件数组AND；重复项内优先同组字段，$root.name指定顶层 |
| optionsBy | {field,map:{来源值:选项数组}}，切换来源时清除不适用的选中值 |
| clearOnChange | 来源字段变化时清除指定关联字段 |
| computed | {operator:sum/multiply,fields:[...]}，显示只读计算结果 |
| span/help/optional | span:2跨两列，辅助说明、选填标记 |
| repeater | type:repeater、itemFields、minItems/maxItems、addLabel；值为对象数组，支持新增/移除/上下移动和逐项错误 |
| validator | 已通过setValidators注册的校验器名称；缺少校验器会明确报错，不绕过验证 |

layout支持vertical/horizontal/inline；columns=1/2；presentation支持standard/tabs/steps，sections将字段分区。下一步校验当前分区，最终提交校验所有有效字段。错误摘要可以切换到含错误的分区并定位输入。联动重绘保留输入焦点和光标。

条件隐藏与禁用字段默认不参与提交和校验，可用includeHidden/includeDisabled改变取值策略；只读字段仍参与提交值。上传只选择本地文件，getFiles获取当前真实File引用；没有文件上传服务或解析结果。隐藏字段不是授权机制。

### 表单实例方法与状态

- VocForm.getValues(host,{all?:false})：获取提交对象；all:true包含条件隐藏/禁用值。
- getState(host)：values/errors/status/dirty/section/requestId快照。
- setValues(host,patch,{replace?,baseline?})、setErrors(host,fieldErrors)、setState(host,status,message?)。
- validate(host,paths?)、submit(host)、cancel(host)、reset(host)。界面重置保护未提交修改，API reset直接恢复基线。
- setValidators(host,{名称:async(value,values,{signal,field})=>string|boolean})：空串/true通过，字符串为错误。中断和过期结果不覆盖新输入。
- setHandlers(host,{submit:async(values,{signal,requestId})=>({ok,message?,fieldErrors?})})：业务返回ok:true才确认成功；失败保留全部输入。
- resolveSubmit(host,{ok,message?,fieldErrors?},requestId)：事件模式回执，需匹配当前编号。没有处理器时voc:submit只通知，不自动显示成功。
- setLoader(host,async({signal,requestId})=>({values}),{immediate?:true})、load(host)、resolveLoad(host,{requestId,values,error?,forbidden?})：可控读取、失败重试与过期保护。
- getFiles(host,path)：当前本地File数组；重复项路径为members.0.file，排序时引用随项目移动。

表单区分default/dirty/invalid/validating/submitting/success/failed/loading/load-error/readonly/disabled/forbidden。提交或读取时锁定输入，防重复提交；取消保留草稿；卸载中断任务。上次成功提交后的值成为重置基线。

## 补充交互

- chart.interactive：区间起止、缩放、数值提示、data[].children下钻与返回；series支持柱/折线组合、独立左右轴和图例显隐，图形与明细共享区间。VocExtras.getChartState读取窗口/路径/系列。
- tree.checkStrategy：linked勾选可选叶节点，strict父子独立；inheritDisabled默认继承禁用。VocExtended.getCheckedKeys读取勾选ID；这些选择不替代权限服务。
- richtext：基础格式、标题、列表、链接、撤销/重做、清除格式、只读/禁用与正文计数。初始HTML与粘贴内容白名单清理，禁用脚本、事件、嵌入和危险链接。VocExtras.getHTML/setHTML提供清理后的HTML；不声称支持完整Word、Office、协同或媒体编辑。

## 已定义的组合边界

- 虚拟表格保持固定行高，不能叠加树形、分组、行展开、合并单元格或增高的单元格编辑；虚拟表可用弹窗编辑；不兼容配置明确报错。
- 合并单元格只在当前平铺页生效；树形、分组、行展开分别使用。多层表头暂不与固定列叠加，保留组结构，不支持跨组拖列。
- 行重排只在未筛选、未排序的本地平铺表生效；其他状态禁用手柄。远程总量与跨页记录由服务端提供。
- 重复字段组支持一层，复杂嵌套数据编辑应建立业务适配。动态字段配置不是低代码可视化搭建器。
- 图表支持分类轴、非负数值和左右两轴；不包含地理、3D、股票等专门图形。
- 真实上传、权限、审批、持久化、自动排课、PPT/Office/PDF/视频专用编辑器、生产框架包及全浏览器认证仍由对应业务实现。

## 验证

定向浏览器检查：examples/common-checks.html；既有全目录回归：examples/completeness-checks.html。报告和截图在data/common-2.3/。纯逻辑校验：scripts/test_common.mjs。构建成功、状态可切换和浏览器断言通过均不等同全部视觉或生产验收。
