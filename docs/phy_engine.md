# Phy-Engine（可选电路计算后端）

`physicsLab` 提供一个可选的第三方电路求解后端 `Phy-Engine`（通过动态库 + `ctypes` 调用）。该后端不会在 `import physicsLab` 时强制加载动态库；只有你显式调用相关 API 时才会尝试加载。

## 1. 获取源码（git submodule）

如果你是从父仓库克隆（并且 `Phy-Engine` 作为 submodule 管理）：

```bash
git clone --recurse-submodules <PHYSICSLAB_REPO_URL>
# 或者克隆后执行：
git submodule update --init --recursive
```

如果你要在当前 `physicsLab` 工作区添加 submodule：

```bash
git submodule add https://github.com/MacroModel/Phy-Engine.git third-parties/Phy-Engine
git submodule update --init --recursive
```

## 2. 本机编译动态库（native build）

`Phy-Engine` 的 C ABI 头文件：`third-parties/Phy-Engine/include/phy_engine/dll_api.h`  
动态库入口实现：`third-parties/Phy-Engine/src/dll_main.cpp`

### macOS / Linux

```bash
cmake -S third-parties/Phy-Engine/src -B third-parties/Phy-Engine/build -DCMAKE_BUILD_TYPE=Release
cmake --build third-parties/Phy-Engine/build -j
```

输出（常见）：
- macOS：`third-parties/Phy-Engine/build/libphyengine.dylib`
- Linux：`third-parties/Phy-Engine/build/libphyengine.so`

### Windows（MSVC）

```bat
cmake -S third-parties/Phy-Engine/src -B third-parties/Phy-Engine/build -G "Visual Studio 17 2022" -A x64
cmake --build third-parties/Phy-Engine/build --config Release
```

输出（常见）：
- `third-parties/Phy-Engine/build/Release/phyengine.dll`

## 3. 安装动态库（`physicsLab` 搜索路径）

`physicsLab` 查找 `Phy-Engine` 动态库的顺序：

1) 环境变量 `PHYSICSLAB_PHYENGINE_LIB`（动态库文件**完整路径**）
2) `physicsLab/native/`（推荐）
3) 若干开发期默认 build 目录（在 `third-parties/Phy-Engine/` 下）

推荐做法：拷贝到 `physicsLab/native/`：

- macOS：`physicsLab/native/libphyengine.dylib`
- Linux：`physicsLab/native/libphyengine.so`
- Windows：`physicsLab/native/phyengine.dll`

或者使用环境变量（示例）：

```bash
export PHYSICSLAB_PHYENGINE_LIB="$(pwd)/third-parties/Phy-Engine/build/libphyengine.dylib"  # macOS
export PHYSICSLAB_PHYENGINE_LIB="$(pwd)/third-parties/Phy-Engine/build/libphyengine.so"     # Linux
```

## 4. 在 Python 中调用

封装入口：`physicsLab/circuit/phy_engine.py`（已通过 `physicsLab.circuit` 暴露）。

### 4.1 一次性调用（推荐起步）

最简单的方式是直接调用 `analyze_experiment_with_phy_engine(...)`，它会在内部创建/销毁一次 `PhyEngineCircuit`。

```python
from pathlib import Path

from physicsLab import Experiment, OpenMode, ExperimentType
from physicsLab.circuit import (
    Battery_Source,
    Resistor,
    Ground_Component,
    crt_wire,
    analyze_experiment_with_phy_engine,
)

lib_path = Path("third-parties/Phy-Engine/build/libphyengine.dylib").resolve()  # macOS 示例

with Experiment(OpenMode.crt, "phyengine-demo", ExperimentType.Circuit, force_crt=True) as ex:
    v = Battery_Source(0, 0, 0, voltage=5)
    r = Resistor(1, 0, 0, resistance=1000)
    g = Ground_Component(2, 0, 0)

    crt_wire(v.red, r.red)
    crt_wire(r.black, v.black)
    crt_wire(v.black, g.i)

    sample = analyze_experiment_with_phy_engine(ex, analyze_type="DC", lib_path=lib_path)
    print(sample.pin_voltage[r])  # [5.0, 0.0]
```

数字电路（逻辑门）需要触发一次数字时钟更新，可传 `digital_clk=True`：

```python
sample = analyze_experiment_with_phy_engine(ex, analyze_type="DC", digital_clk=True)
```

### 4.2 复用同一电路对象（多次采样/多次分析）

如果你希望在同一个电路实例上重复调用（例如多次采样、或后续扩展为属性更新），可以显式使用 `PhyEngineCircuit`：

```python
from pathlib import Path
from physicsLab.circuit.phy_engine import PhyEngineCircuit

lib_path = Path("third-parties/Phy-Engine/build/libphyengine.dylib").resolve()

with PhyEngineCircuit(ex, lib_path=lib_path) as c:
    sample1 = c.analyze(analyze_type="DC")
    sample2 = c.analyze(analyze_type="DC", digital_clk=True)
```

### 4.3 API 参数（常用）

- `lib_path`：动态库路径（可选）。不传时按“搜索路径”自动查找。
- `analyze_type`：`"DC"|"AC"|"TR"|...`（也可传对应的整数枚举值）。
- `tr_step` / `tr_stop`：瞬态分析步长/终止时间（`TR/TROP` 时使用）。
- `ac_omega`：角频率（`AC/ACOP` 时需要传入）。
- `digital_clk`：是否在 `analyze()` 后额外调用一次 `circuit_digital_clk()` 更新数字电路（逻辑门、触发器等）。

### 4.4 返回结果（PhyEngineSample）

`analyze_experiment_with_phy_engine(...)` 返回 `PhyEngineSample`，包含：

- `elements`：参与求解的元件列表（按 Phy-Engine 组件顺序，**不包含**“接地占位元件”）。
- `pin_voltage[element] -> list[float]`：该元件各引脚电压（顺序与 `element.all_pins()`/`count_all_pins()`一致）。
- `pin_digital[element] -> list[bool]`：该元件各引脚数字状态（用于数字电路）。
- `branch_current[element] -> list[float]`：该元件各支路电流（并非所有元件都有支路电流；例如 `Resistor` 可能为空）。

### 4.5 常见异常

- `PhyEngineNotAvailableError`：未找到动态库（请设置 `PHYSICSLAB_PHYENGINE_LIB` 或拷贝到 `physicsLab/native/`）。
- `PhyEngineUnsupportedElementError`：电路中存在尚未映射到 Phy-Engine 的 `ModelID`。
- `PhyEngineAnalyzeError`：底层求解失败或 C API 返回错误码。

## 5. 运行测试（可选）

仓库包含一组后端集成测试：`test_pe/`。

如果你使用本仓库的 venv（推荐）：

```bash
./.venv/bin/python -m unittest -q test_pe.test_phy_engine_backend
```

如果你用系统 Python，请确保已安装依赖 `typing-extensions` 和 `requests`，否则会跳过该测试文件。

## 6. 支持范围说明

当前映射只覆盖部分常用元件；遇到未支持的 `ModelID` 会抛出 `PhyEngineUnsupportedElementError`。支持列表与示例请参考：
- `third-parties/Phy-Engine/README.physicsLab.zh_CN.md`
