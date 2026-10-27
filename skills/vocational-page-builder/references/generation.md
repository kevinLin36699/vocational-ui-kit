# 页面实现与可移植交付

## 新建 HTML

scaffold_page.py 的 --pattern 指定真实页面模式，--output 为新的独立目录，--title 只控制页面文档标题。脚本生成可运行模板和来源记录，模板里的固定业务标题/字段不会自动因 title 改变。生成后按需求完成字段、数据、操作、状态及适配，不能直接把种子当成最终任务完成。

多文件输出只复制 manifest 中必要运行样式、脚本、图标及页面模式。依赖放在 assets/vocational-ui 下，page-provenance.json 记录库版本、每份源文件与哈希，页面不靠绝对路径在用户机器运行。copy 必须注明来源，升级不能悄悄覆盖已经定稿的旧页面。

对于当前基线，模板依赖少量局部布局样式。脚本提供独立页面所需布局，引用组件库变量，不复制展示站导航和营销外壳。

## 数据与 API

以 resolve_library.py 返回的 parameters 和真实源码为准。table 没有 rows/columns 参数、chat 没有任意 messages/真实流式接口。业务不同于演示时，复用 input/select/button/dialog 等基础能力和 v-* 结构，建立页面局部控制器；记录新增适配字段和事件，不能虚构公共 API。

render 返回 HTML，挂载复杂组件后 hydrate；替换/卸载前 destroy。用户文本和文件名转义；extra 等受信任属性逃生参数不能接受用户输入。自定义数据应有稳定 ID，选择、排序、分页、导出使用同一有效集合。

## 单文件

用户要求时运行 package_html.py，将已经完成并检查的本地页面中的样式与经典脚本内联到新输出文件，原多文件源保留。该工具不转换框架模块、远程依赖、媒体或任意构建项目；遇到这类情况先用项目构建方式再决定打包。

```bash
python3 "$SKILL_ROOT/scripts/package_html.py" /absolute/page/index.html --output /absolute/page-standalone.html
```

保留内嵌 provenance，包内资源哈希应与源一致。打包后重新检查相对资源和关键交互；单文件成立不代表跨机器媒体、上传解析或生产接口也可离线。

## 局部扩展

现有变体 → 组合 → 局部适配。适配使用主题变量，有真实行为、错误与恢复出口；名称和作用域避免污染公共组件。将扩展记录在任务交付说明而不是技能的公共规则。除非本次要求更新公共库，否则只提出回收建议。
