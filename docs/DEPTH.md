# 深度登记 证券除权复权与持仓对账

- 规模：中型
- 使用者与工作流：券商数据校验员，归一公司行动与成交持仓文件，复算除权因子和股数现金。
- 核心规则：除权参考价=(前收盘-每股现金+配股价×配股比例)/(1+送转比例+配股比例)，按登记日判定权益，零碎股单列。

## 功能模块

| 模块 | 使用者动作 | 入口 | 核心文件 | 测试 |
|---|---|---|---|---|
| M1 行动接收 | 运行行动接收并复核证据 | `POST /api/m1`；`/work/1` | `app/modules/m1_receiving/rules.py` | `tests/test_m1.py` |
| M2 证券映射 | 运行证券映射并复核证据 | `POST /api/m2`；`/work/2` | `app/modules/m2_mapping/rules.py` | `tests/test_m2.py` |
| M3 权益登记 | 运行权益登记并复核证据 | `POST /api/m3`；`/work/3` | `app/modules/m3_registry/rules.py` | `tests/test_m3.py` |
| M4 除权因子 | 运行除权因子并复核证据 | `POST /api/m4`；`/work/4` | `app/modules/m4_factors/rules.py` | `tests/test_m4.py` |
| M5 持仓重算 | 运行持仓重算并复核证据 | `POST /api/m5`；`/work/5` | `app/modules/m5_holdings/rules.py` | `tests/test_m5.py` |
| M6 现金对账 | 运行现金对账并复核证据 | `POST /api/m6`；`/work/6` | `app/modules/m6_cash/rules.py` | `tests/test_m6.py` |
| M7 修订回放 | 运行修订回放并复核证据 | `POST /api/m7`；`/work/7` | `app/modules/m7_revisions/rules.py` | `tests/test_m7.py` |

## 陷阱登记

| TRAP | 现象 | 朴素实现会怎样 | 本项目处理 | 处理位置 | 测试 |
|---|---|---|---|---|---|
| TRAP-02 | BOM | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m1_receiving/rules.py` | `tests/test_m1.py::test_bom_header` |
| TRAP-06 | 全角千分位 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m2_mapping/rules.py` | `tests/test_m2.py::test_fullwidth_decimal` |
| TRAP-08 | 证券前导零 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m2_mapping/rules.py` | `tests/test_m2.py::test_security_leading_zero` |
| TRAP-09 | 大整数保形 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m2_mapping/rules.py` | `tests/test_m2.py::test_large_id_unchanged` |
| TRAP-10 | Decimal除权因子 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m4_factors/rules.py` | `tests/test_m4.py::test_factor_precise` |
| TRAP-14 | 行动定义冲突 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m2_mapping/rules.py` | `tests/test_m2.py::test_conflicting_action_removed` |
| TRAP-24 | 现金尾差 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m5_holdings/rules.py` | `tests/test_m5.py::test_largest_remainder_conservation` |
| TRAP-25 | 行动版本选择 | 静默覆盖或误计 | 显式裁决并保留证据 | `app/modules/m2_mapping/rules.py` | `tests/test_m2.py::test_latest_action_chosen` |

## 对账规则

输入记录 = 采信记录 + 隔离记录 + 相同行重复。重复表头与空行单独记数。业务合计按阶段中的守恒或差值列复核。运行清单有原文SHA256、规则版本与耗时；相同规则版本下同文重复提交复用批次。

## 已知不覆盖

部署为本地单用户工具，不连接外部上游系统。CSV单文件5MB及一万条业务记录上限；不推断未提供的未知数据。
