# power-supply-system-model-lint


## Purpose

* 对供电系统模型进行合法性校验
* 提供命令行工具和python api两种使用方式
* 本项目仅为框架， 具体校验规则需要通过插件实现

## Quickstart

```python
import pssmlint

try: 
    pssmlint.Builder(...rules)
        .add_powser_supply(...)
        .add_load(...)
        .add_bus(...)
        .validate()
except pssmlint.ValidationError as e:
    print(e.violations)
```