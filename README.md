# power-supply-system-model-lint


## Purpose

* 对供电系统模型进行合法性校验
* 提供命令行工具和python api两种使用方式
* 本项目仅为框架， 具体校验规则需要通过插件实现

## A sample application

```python
import pssmlint


try:
    # 创建抽象模型树(abstract model tree)
    amt = pssmlint.AbstractModelTree()
    # 逐条添加记录
    amt.add_connection(load="load_A", bus="bus_1", redundancy="2", ...)
    # 如果发现某汇流条下有同名负载
except pssmlint.errors.DuplicateLoad as e:
    print(e)

# 分别打印汇流条和负载
print(amt.buses)
print(amt.loads)

# 解除汇流条和负载的连接关系
amt.disconnect(load="load_A", bus="bus_1")
# 增加负载load_A的冗余度
amt.loads["load_A"].redundancy += 1

try: 
    # 负载冗余度等于实际挂载的汇流条数量
    rule = psslint.Rule("redudancy-match")
        .visit_connection(lambda load: load.redundancy == len(load.buses), 
            message="负载冗余度等于实际挂载的汇流条数量")
    pssmlint.Linter(rule).lint(amt)
except pssmlint.ValidationError as e:
    print(e.violations)
```

## 