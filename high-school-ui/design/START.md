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
