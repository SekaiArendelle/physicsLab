# -*- coding: utf-8 -*-
from __future__ import annotations

import ctypes
import os
import platform
from dataclasses import dataclass
from pathlib import Path

from physicsLab import errors
from physicsLab._core import _Experiment
from physicsLab._typing import Dict, List, Optional, Tuple, Union
from physicsLab.enums import ExperimentType
from physicsLab.savTemplate import Generate


class PhyEngineNotAvailableError(RuntimeError):
    pass


class PhyEngineUnsupportedElementError(NotImplementedError):
    pass


class PhyEngineAnalyzeError(RuntimeError):
    pass


class _PhyEngineAnalyzeType:
    OP = 0
    DC = 1
    AC = 2
    ACOP = 3
    TR = 4
    TROP = 5


_ELEMENT_BRANCHES: Dict[int, int] = {
    4: 1,  # VDC
    5: 1,  # VAC
    6: 1,  # IDC (guess; not used by current mapping)
    7: 1,  # IAC (guess; not used by current mapping)
    12: 1,  # switch
    14: 2,  # transformer
    15: 2,  # coupled inductors
}

_ELEMENT_PROPS: Dict[int, int] = {
    0: 0,
    1: 1,  # R
    2: 1,  # C
    3: 1,  # L
    4: 1,  # VDC
    12: 1,  # switch
    14: 1,  # transformer n
    15: 3,  # coupled inductors L1 L2 k
    54: 0,
    200: 1,  # digital input state
    201: 0,
    202: 0,
    203: 0,
    204: 0,
    205: 0,
    206: 0,
    207: 0,
    208: 0,
    209: 0,
    211: 0,
    212: 0,
    220: 0,
    221: 0,
    222: 0,
    223: 0,
    224: 0,
    225: 0,
    226: 0,
    227: 0,
    228: 0,
}


def _default_phyengine_lib_names() -> List[str]:
    sysname = platform.system()
    if sysname == "Windows":
        return ["phyengine.dll"]
    if sysname == "Darwin":
        return ["libphyengine.dylib"]
    return ["libphyengine.so"]


def _default_phyengine_search_paths() -> List[Path]:
    # 1) packaged location: physicsLab/native
    here = Path(__file__).resolve()
    pkg_root = here.parents[1]  # .../physicsLab
    native_dir = pkg_root / "native"

    # 2) dev build locations
    repo_root = pkg_root.parent
    dev_builds = [
        repo_root / "third-parties" / "Phy-Engine" / "build",
        repo_root / "third-parties" / "Phy-Engine" / "src" / "build",
        repo_root / "third-parties" / "Phy-Engine" / "src" / "cmake-build-release",
        repo_root / "third-parties" / "Phy-Engine" / "src" / "cmake-build-debug",
    ]
    return [native_dir, *dev_builds]


def resolve_phyengine_library_path(explicit_path: Optional[Union[str, os.PathLike]] = None) -> Path:
    if explicit_path is not None:
        p = Path(explicit_path).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(str(p))
        return p

    env = os.environ.get("PHYSICSLAB_PHYENGINE_LIB")
    if env:
        p = Path(env).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"PHYSICSLAB_PHYENGINE_LIB points to missing file: {p}")
        return p

    names = _default_phyengine_lib_names()
    for base in _default_phyengine_search_paths():
        for name in names:
            candidate = base / name
            if candidate.exists():
                return candidate

    raise PhyEngineNotAvailableError(
        "Phy-Engine shared library not found. "
        "Set PHYSICSLAB_PHYENGINE_LIB to the full path of the built library, "
        "or install it under physicsLab/native/."
    )


class _PhyEngineCDLL:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.cdll = ctypes.CDLL(str(path))
        self._bind()

    def _bind(self) -> None:
        c_int_p = ctypes.POINTER(ctypes.c_int)
        c_size_t_p = ctypes.POINTER(ctypes.c_size_t)
        c_double_p = ctypes.POINTER(ctypes.c_double)
        c_bool_p = ctypes.POINTER(ctypes.c_bool)

        self.create_circuit = self.cdll.create_circuit
        self.create_circuit.argtypes = [
            c_int_p,
            ctypes.c_size_t,
            c_int_p,
            ctypes.c_size_t,
            c_double_p,
            ctypes.POINTER(c_size_t_p),
            ctypes.POINTER(c_size_t_p),
            c_size_t_p,
        ]
        self.create_circuit.restype = ctypes.c_void_p

        self.destroy_circuit = self.cdll.destroy_circuit
        self.destroy_circuit.argtypes = [ctypes.c_void_p, c_size_t_p, c_size_t_p]
        self.destroy_circuit.restype = None

        self.circuit_set_analyze_type = self.cdll.circuit_set_analyze_type
        self.circuit_set_analyze_type.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        self.circuit_set_analyze_type.restype = ctypes.c_int

        self.circuit_set_tr = self.cdll.circuit_set_tr
        self.circuit_set_tr.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
        self.circuit_set_tr.restype = ctypes.c_int

        self.circuit_set_ac_omega = self.cdll.circuit_set_ac_omega
        self.circuit_set_ac_omega.argtypes = [ctypes.c_void_p, ctypes.c_double]
        self.circuit_set_ac_omega.restype = ctypes.c_int

        self.circuit_analyze = self.cdll.circuit_analyze
        self.circuit_analyze.argtypes = [ctypes.c_void_p]
        self.circuit_analyze.restype = ctypes.c_int

        self.circuit_digital_clk = self.cdll.circuit_digital_clk
        self.circuit_digital_clk.argtypes = [ctypes.c_void_p]
        self.circuit_digital_clk.restype = ctypes.c_int

        self.circuit_sample = self.cdll.circuit_sample
        self.circuit_sample.argtypes = [
            ctypes.c_void_p,
            c_size_t_p,
            c_size_t_p,
            ctypes.c_size_t,
            c_double_p,
            c_size_t_p,
            c_double_p,
            c_size_t_p,
            c_bool_p,
            c_size_t_p,
        ]
        self.circuit_sample.restype = ctypes.c_int


def _get_required_float(element, key: str) -> float:
    if not hasattr(element, "properties"):
        raise TypeError(f"unsupported element type: {type(element).__name__}")
    v = element.properties.get(key)
    if v is None or v is Generate:
        raise ValueError(f"{element.data.get('ModelID', type(element).__name__)} missing property: {key}")
    if not isinstance(v, (int, float)):
        raise TypeError(f"{element.data.get('ModelID', type(element).__name__)} property {key} must be numeric, got {type(v).__name__}")
    return float(v)


def _get_required_int01(element, key: str) -> int:
    v = element.properties.get(key)
    if v is None or v is Generate:
        raise ValueError(f"{element.data.get('ModelID', type(element).__name__)} missing property: {key}")
    if not isinstance(v, (int, float)):
        raise TypeError(f"{element.data.get('ModelID', type(element).__name__)} property {key} must be numeric, got {type(v).__name__}")
    return 1 if float(v) != 0.0 else 0


def _to_phy_engine_element(element) -> Tuple[int, List[float]]:
    model_id = getattr(element, "data", {}).get("ModelID", type(element).__name__)

    # Ground is represented as code 0 (special-cased by the wiring algorithm).
    if model_id == "Ground Component":
        return 0, []

    # Linear / passive
    if model_id == "Resistor":
        return 1, [_get_required_float(element, "电阻")]
    if model_id == "Basic Capacitor":
        return 2, [_get_required_float(element, "电容")]
    if model_id == "Basic Inductor":
        return 3, [_get_required_float(element, "电感")]
    if model_id == "Battery Source":
        # Note: internal resistance is not modeled; use an explicit Resistor if needed.
        return 4, [_get_required_float(element, "电压")]

    # Controller
    if model_id in {"Simple Switch", "Push Switch", "Air Switch"}:
        return 12, [float(_get_required_int01(element, "开关"))]

    # Coupled devices
    if model_id == "Transformer":
        vp = _get_required_float(element, "输入电压")
        vs = _get_required_float(element, "输出电压")
        if vs == 0.0:
            raise ValueError("Transformer 输出电压 must be non-zero")
        return 14, [vp / vs]  # n = Vp/Vs
    if model_id == "Mutual Inductor":
        return 15, [
            _get_required_float(element, "电感1"),
            _get_required_float(element, "电感2"),
            _get_required_float(element, "耦合系数"),
        ]

    # Non-linear convenience blocks
    if model_id == "Rectifier":
        return 54, []

    # Digital (logic circuit)
    if model_id == "Logic Input":
        state = 1 if bool(_get_required_int01(element, "开关")) else 0
        return 200, [float(state)]
    if model_id == "Logic Output":
        return 201, []
    if model_id == "Or Gate":
        return 202, []
    if model_id == "Yes Gate":
        return 203, []
    if model_id == "And Gate":
        return 204, []
    if model_id == "No Gate":
        return 205, []
    if model_id == "Xor Gate":
        return 206, []
    if model_id == "Xnor Gate":
        return 207, []
    if model_id == "Nand Gate":
        return 208, []
    if model_id == "Nor Gate":
        return 209, []
    if model_id == "Imp Gate":
        return 211, []
    if model_id == "Nimp Gate":
        return 212, []
    if model_id == "Half Adder":
        return 220, []
    if model_id == "Full Adder":
        return 221, []
    if model_id == "Half Subtractor":
        return 222, []
    if model_id == "Full Subtractor":
        return 223, []
    if model_id == "Multiplier":
        return 224, []
    if model_id == "D Flipflop":
        return 225, []
    if model_id == "T Flipflop":
        return 226, []
    if model_id == "Real-T Flipflop":
        return 227, []
    if model_id == "JK Flipflop":
        return 228, []

    raise PhyEngineUnsupportedElementError(
        f"Phy-Engine backend does not support element ModelID={model_id!r} ({type(element).__name__})"
    )


def _analyze_type_value(analyze_type: Union[str, int]) -> int:
    if isinstance(analyze_type, int):
        return int(analyze_type)
    if not isinstance(analyze_type, str):
        raise TypeError("analyze_type must be str|int")
    s = analyze_type.strip().upper()
    if s == "OP":
        return _PhyEngineAnalyzeType.OP
    if s == "DC":
        return _PhyEngineAnalyzeType.DC
    if s == "AC":
        return _PhyEngineAnalyzeType.AC
    if s == "ACOP":
        return _PhyEngineAnalyzeType.ACOP
    if s == "TR":
        return _PhyEngineAnalyzeType.TR
    if s == "TROP":
        return _PhyEngineAnalyzeType.TROP
    raise ValueError(f"unknown analyze_type: {analyze_type!r}")


@dataclass(frozen=True)
class PhyEngineSample:
    elements: List[object]  # non-ground elements, in Phy-Engine component order
    pin_voltage: Dict[object, List[float]]
    pin_digital: Dict[object, List[bool]]
    branch_current: Dict[object, List[float]]


class PhyEngineCircuit:
    def __init__(
        self,
        experiment: _Experiment,
        *,
        lib_path: Optional[Union[str, os.PathLike]] = None,
    ) -> None:
        if not isinstance(experiment, _Experiment):
            raise TypeError("experiment must be an _Experiment")
        if experiment.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        self._experiment = experiment
        self._lib = _PhyEngineCDLL(resolve_phyengine_library_path(lib_path))

        self._circuit_ptr: Optional[int] = None
        self._vec_pos = ctypes.POINTER(ctypes.c_size_t)()
        self._chunk_pos = ctypes.POINTER(ctypes.c_size_t)()
        self._comp_size = ctypes.c_size_t(0)
        self._comp_elements: List[object] = []
        self._comp_codes: List[int] = []

        self._create()

    @property
    def lib_path(self) -> Path:
        return self._lib.path

    @property
    def comp_elements(self) -> List[object]:
        return list(self._comp_elements)

    def _create(self) -> None:
        elements = list(self._experiment.Elements)
        if not elements:
            raise ValueError("experiment has no elements")
        id2idx = {id(e): i for i, e in enumerate(elements)}

        # Build element codes + property stream.
        element_codes: List[int] = []
        properties: List[float] = []
        comp_elements: List[object] = []
        comp_codes: List[int] = []

        for e in elements:
            code, props = _to_phy_engine_element(e)
            element_codes.append(int(code))
            if code != 0:
                comp_elements.append(e)
                comp_codes.append(int(code))
                expected = _ELEMENT_PROPS.get(int(code))
                if expected is None:
                    raise PhyEngineAnalyzeError(f"unknown property arity for Phy-Engine element code: {code}")
                if len(props) != expected:
                    raise PhyEngineAnalyzeError(
                        f"element ModelID={getattr(e, 'data', {}).get('ModelID', type(e).__name__)} has wrong property count for code={code}: "
                        f"expected {expected}, got {len(props)}"
                    )
                properties.extend(props)

        # Build wire quads: (ele1, pin1, ele2, pin2)
        wires_flat: List[int] = []
        for w in self._experiment.Wires:
            s_idx = id2idx.get(id(w.Source.element_self))
            t_idx = id2idx.get(id(w.Target.element_self))
            if s_idx is None or t_idx is None:
                continue
            wires_flat.extend([int(s_idx), int(w.Source._pin_label), int(t_idx), int(w.Target._pin_label)])

        ele_arr = (ctypes.c_int * len(element_codes))(*element_codes)
        wire_arr = (ctypes.c_int * len(wires_flat))(*wires_flat) if wires_flat else None
        prop_arr = (ctypes.c_double * max(1, len(properties)))(*properties) if properties else (ctypes.c_double * 1)(0.0)

        vec_pos_ptr = ctypes.POINTER(ctypes.c_size_t)()
        chunk_pos_ptr = ctypes.POINTER(ctypes.c_size_t)()
        comp_size = ctypes.c_size_t(0)

        circuit_ptr = self._lib.create_circuit(
            ele_arr,
            ctypes.c_size_t(len(element_codes)),
            wire_arr,
            ctypes.c_size_t(len(wires_flat)),
            prop_arr,
            ctypes.byref(vec_pos_ptr),
            ctypes.byref(chunk_pos_ptr),
            ctypes.byref(comp_size),
        )
        if not circuit_ptr:
            raise PhyEngineAnalyzeError("Phy-Engine create_circuit() failed (returned NULL)")

        self._circuit_ptr = int(circuit_ptr)
        self._vec_pos = vec_pos_ptr
        self._chunk_pos = chunk_pos_ptr
        self._comp_size = comp_size
        self._comp_elements = comp_elements[: int(comp_size.value)]
        self._comp_codes = comp_codes[: int(comp_size.value)]

    def close(self) -> None:
        if self._circuit_ptr is None:
            return
        self._lib.destroy_circuit(self._circuit_ptr, self._vec_pos, self._chunk_pos)
        self._circuit_ptr = None

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self) -> "PhyEngineCircuit":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def analyze(
        self,
        *,
        analyze_type: Union[str, int] = "DC",
        tr_step: float = 1e-6,
        tr_stop: float = 1e-6,
        ac_omega: Optional[float] = None,
        digital_clk: bool = False,
    ) -> PhyEngineSample:
        if self._circuit_ptr is None:
            raise PhyEngineAnalyzeError("circuit is closed")

        at = _analyze_type_value(analyze_type)
        if self._lib.circuit_set_analyze_type(self._circuit_ptr, ctypes.c_uint32(at)) != 0:
            raise PhyEngineAnalyzeError("Phy-Engine circuit_set_analyze_type() failed")

        if at in (_PhyEngineAnalyzeType.TR, _PhyEngineAnalyzeType.TROP):
            if self._lib.circuit_set_tr(self._circuit_ptr, float(tr_step), float(tr_stop)) != 0:
                raise PhyEngineAnalyzeError("Phy-Engine circuit_set_tr() failed")

        if at in (_PhyEngineAnalyzeType.AC, _PhyEngineAnalyzeType.ACOP):
            if ac_omega is None:
                raise ValueError("ac_omega is required for AC/ACOP analysis")
            if self._lib.circuit_set_ac_omega(self._circuit_ptr, float(ac_omega)) != 0:
                raise PhyEngineAnalyzeError("Phy-Engine circuit_set_ac_omega() failed")

        if self._lib.circuit_analyze(self._circuit_ptr) != 0:
            raise PhyEngineAnalyzeError("Phy-Engine circuit_analyze() failed")

        if digital_clk:
            if self._lib.circuit_digital_clk(self._circuit_ptr) != 0:
                raise PhyEngineAnalyzeError("Phy-Engine circuit_digital_clk() failed")

        comp_size = int(self._comp_size.value)
        total_pins = 0
        for e in self._comp_elements:
            count_all_pins = getattr(type(e), "count_all_pins", None)
            if callable(count_all_pins):
                total_pins += int(count_all_pins())
            else:
                total_pins += sum(1 for _ in e.all_pins())

        total_branches = sum(int(_ELEMENT_BRANCHES.get(code, 0)) for code in self._comp_codes)
        total_branches = max(total_branches, total_pins)

        voltage = (ctypes.c_double * max(1, total_pins))()
        voltage_ord = (ctypes.c_size_t * (comp_size + 1))()
        current = (ctypes.c_double * max(1, total_branches))()
        current_ord = (ctypes.c_size_t * (comp_size + 1))()
        digital = (ctypes.c_bool * max(1, total_pins))()
        digital_ord = (ctypes.c_size_t * (comp_size + 1))()

        rc = self._lib.circuit_sample(
            self._circuit_ptr,
            self._vec_pos,
            self._chunk_pos,
            ctypes.c_size_t(comp_size),
            voltage,
            voltage_ord,
            current,
            current_ord,
            digital,
            digital_ord,
        )
        if rc != 0:
            raise PhyEngineAnalyzeError(f"Phy-Engine circuit_sample() failed (rc={rc})")

        pin_voltage: Dict[object, List[float]] = {}
        pin_digital: Dict[object, List[bool]] = {}
        branch_current: Dict[object, List[float]] = {}

        for i, e in enumerate(self._comp_elements):
            v0 = int(voltage_ord[i])
            v1 = int(voltage_ord[i + 1])
            d0 = int(digital_ord[i])
            d1 = int(digital_ord[i + 1])
            c0 = int(current_ord[i])
            c1 = int(current_ord[i + 1])

            pin_voltage[e] = [float(voltage[j]) for j in range(v0, v1)]
            pin_digital[e] = [bool(digital[j]) for j in range(d0, d1)]
            branch_current[e] = [float(current[j]) for j in range(c0, c1)]

        return PhyEngineSample(
            elements=list(self._comp_elements),
            pin_voltage=pin_voltage,
            pin_digital=pin_digital,
            branch_current=branch_current,
        )


def analyze_experiment_with_phy_engine(
    experiment: _Experiment,
    *,
    analyze_type: Union[str, int] = "DC",
    tr_step: float = 1e-6,
    tr_stop: float = 1e-6,
    ac_omega: Optional[float] = None,
    digital_clk: bool = False,
    lib_path: Optional[Union[str, os.PathLike]] = None,
) -> PhyEngineSample:
    with PhyEngineCircuit(experiment, lib_path=lib_path) as c:
        return c.analyze(
            analyze_type=analyze_type,
            tr_step=tr_step,
            tr_stop=tr_stop,
            ac_omega=ac_omega,
            digital_clk=digital_clk,
        )
