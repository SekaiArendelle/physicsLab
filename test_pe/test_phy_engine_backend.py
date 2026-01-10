# -*- coding: utf-8 -*-
import os
import unittest
from pathlib import Path
from typing import Optional

_IMPORT_ERROR: Optional[BaseException] = None
try:
    from physicsLab import Experiment, ExperimentType, OpenMode
    from physicsLab.circuit import Battery_Source, Ground_Component, Resistor, crt_wire
    from physicsLab.circuit.elements.logicCircuit import (
        And_Gate,
        Logic_Input,
        Logic_Output,
        Yes_Gate,
    )
    from physicsLab.circuit.phy_engine import (
        PhyEngineNotAvailableError,
        PhyEngineUnsupportedElementError,
        analyze_experiment_with_phy_engine,
        resolve_phyengine_library_path,
    )
except ModuleNotFoundError as e:
    # `physicsLab` depends on `typing_extensions` (and `requests`) at import time.
    _IMPORT_ERROR = e


def _try_get_lib_path() -> Optional[Path]:
    try:
        return resolve_phyengine_library_path()
    except PhyEngineNotAvailableError:
        return None


class TestPhyEngineBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if _IMPORT_ERROR is not None:
            name = getattr(_IMPORT_ERROR, "name", None)
            if name in {"typing_extensions", "requests"}:
                raise unittest.SkipTest(
                    f"Missing runtime dependency: {name}. Install deps or run via the repo venv."
                )
            raise _IMPORT_ERROR

    def test_dc_voltage_divider_like_loop(self):
        lib_path = _try_get_lib_path()
        if lib_path is None:
            self.skipTest("Phy-Engine dynamic library not available")

        with Experiment(
            OpenMode.crt,
            "__test_phyengine_dc__",
            ExperimentType.Circuit,
            force_crt=True,
        ) as expe:
            v = Battery_Source(0, 0, 0, voltage=5)
            r = Resistor(1, 0, 0, resistance=1000)
            g = Ground_Component(2, 0, 0)

            crt_wire(v.red, r.red)
            crt_wire(r.black, v.black)
            crt_wire(v.black, g.i)

            sample = analyze_experiment_with_phy_engine(expe, analyze_type="DC", lib_path=lib_path)

            # Resistor pins should be at ~5V and ~0V.
            self.assertIn(r, sample.pin_voltage)
            self.assertEqual(len(sample.pin_voltage[r]), 2)
            self.assertAlmostEqual(sample.pin_voltage[r][0], 5.0, places=6)
            self.assertAlmostEqual(sample.pin_voltage[r][1], 0.0, places=6)

            expe.close(delete=True)

    def test_env_var_override(self):
        lib_path = _try_get_lib_path()
        if lib_path is None:
            self.skipTest("Phy-Engine dynamic library not available")

        old = os.environ.get("PHYSICSLAB_PHYENGINE_LIB")
        try:
            os.environ["PHYSICSLAB_PHYENGINE_LIB"] = str(lib_path)

            with Experiment(
                OpenMode.crt,
                "__test_phyengine_env_override__",
                ExperimentType.Circuit,
                force_crt=True,
            ) as expe:
                v = Battery_Source(0, 0, 0, voltage=5)
                r = Resistor(1, 0, 0, resistance=1000)
                g = Ground_Component(2, 0, 0)

                crt_wire(v.red, r.red)
                crt_wire(r.black, v.black)
                crt_wire(v.black, g.i)

                sample = analyze_experiment_with_phy_engine(expe, analyze_type="DC")
                self.assertAlmostEqual(sample.pin_voltage[r][0], 5.0, places=6)
                self.assertAlmostEqual(sample.pin_voltage[r][1], 0.0, places=6)

                expe.close(delete=True)
        finally:
            if old is None:
                os.environ.pop("PHYSICSLAB_PHYENGINE_LIB", None)
            else:
                os.environ["PHYSICSLAB_PHYENGINE_LIB"] = old

    def test_two_vdc_series_one_resistor(self):
        lib_path = _try_get_lib_path()
        if lib_path is None:
            self.skipTest("Phy-Engine dynamic library not available")

        with Experiment(
            OpenMode.crt,
            "__test_phyengine_two_vdc_series__",
            ExperimentType.Circuit,
            force_crt=True,
        ) as expe:
            v1 = Battery_Source(0, 0, 0, voltage=5)
            v2 = Battery_Source(1, 0, 0, voltage=2)
            r = Resistor(2, 0, 0, resistance=1000)
            g = Ground_Component(3, 0, 0)

            # Series sources: GND --(v2 2V)--> mid --(v1 5V)--> top
            crt_wire(v2.black, g.i)
            crt_wire(v2.red, v1.black)
            crt_wire(v1.red, r.red)
            crt_wire(r.black, g.i)

            sample = analyze_experiment_with_phy_engine(expe, analyze_type="DC", lib_path=lib_path)

            self.assertAlmostEqual(sample.pin_voltage[v2][1], 0.0, places=6)  # v2 black
            self.assertAlmostEqual(sample.pin_voltage[v2][0], 2.0, places=6)  # v2 red
            self.assertAlmostEqual(sample.pin_voltage[v1][1], 2.0, places=6)  # v1 black (mid)
            self.assertAlmostEqual(sample.pin_voltage[v1][0], 7.0, places=6)  # v1 red (top)
            self.assertAlmostEqual(sample.pin_voltage[r][0], 7.0, places=6)
            self.assertAlmostEqual(sample.pin_voltage[r][1], 0.0, places=6)

            # Each VDC has 1 branch current (direction depends on implementation); check magnitude.
            self.assertEqual(len(sample.branch_current[v1]), 1)
            self.assertEqual(len(sample.branch_current[v2]), 1)
            self.assertAlmostEqual(abs(sample.branch_current[v1][0]), 0.007, places=6)
            self.assertAlmostEqual(abs(sample.branch_current[v2][0]), 0.007, places=6)

            expe.close(delete=True)

    def test_digital_yes_gate(self):
        lib_path = _try_get_lib_path()
        if lib_path is None:
            self.skipTest("Phy-Engine dynamic library not available")

        with Experiment(
            OpenMode.crt,
            "__test_phyengine_digital_yes__",
            ExperimentType.Circuit,
            force_crt=True,
        ) as expe:
            inp = Logic_Input(0, 0, 0, output_status=True)
            gate = Yes_Gate(1, 0, 0)
            out = Logic_Output(2, 0, 0)

            crt_wire(inp.o, gate.i)
            crt_wire(gate.o, out.i)

            sample = analyze_experiment_with_phy_engine(
                expe,
                analyze_type="DC",
                lib_path=lib_path,
                digital_clk=True,
            )
            self.assertEqual(sample.pin_digital[out], [True])
            expe.close(delete=True)

    def test_digital_and_gate_truth_table(self):
        lib_path = _try_get_lib_path()
        if lib_path is None:
            self.skipTest("Phy-Engine dynamic library not available")

        # Case 1: 1 AND 0 -> 0
        with Experiment(
            OpenMode.crt,
            "__test_phyengine_digital_and_10__",
            ExperimentType.Circuit,
            force_crt=True,
        ) as expe:
            a = Logic_Input(0, 0, 0, output_status=True)
            b = Logic_Input(0, 1, 0, output_status=False)
            g = And_Gate(1, 0, 0)
            o = Logic_Output(2, 0, 0)

            crt_wire(a.o, g.i_up)
            crt_wire(b.o, g.i_low)
            crt_wire(g.o, o.i)

            sample = analyze_experiment_with_phy_engine(expe, analyze_type="DC", lib_path=lib_path, digital_clk=True)
            self.assertEqual(sample.pin_digital[o], [False])
            expe.close(delete=True)

        # Case 2: 1 AND 1 -> 1
        with Experiment(
            OpenMode.crt,
            "__test_phyengine_digital_and_11__",
            ExperimentType.Circuit,
            force_crt=True,
        ) as expe:
            a = Logic_Input(0, 0, 0, output_status=True)
            b = Logic_Input(0, 1, 0, output_status=True)
            g = And_Gate(1, 0, 0)
            o = Logic_Output(2, 0, 0)

            crt_wire(a.o, g.i_up)
            crt_wire(b.o, g.i_low)
            crt_wire(g.o, o.i)

            sample = analyze_experiment_with_phy_engine(expe, analyze_type="DC", lib_path=lib_path, digital_clk=True)
            self.assertEqual(sample.pin_digital[o], [True])
            expe.close(delete=True)

    def test_unsupported_element_raises(self):
        lib_path = _try_get_lib_path()
        if lib_path is None:
            self.skipTest("Phy-Engine dynamic library not available")

        from physicsLab.circuit.elements.otherCircuit import Buzzer

        with Experiment(
            OpenMode.crt,
            "__test_phyengine_unsupported__",
            ExperimentType.Circuit,
            force_crt=True,
        ) as expe:
            Buzzer(0, 0, 0)
            with self.assertRaises(PhyEngineUnsupportedElementError):
                analyze_experiment_with_phy_engine(expe, analyze_type="DC", lib_path=lib_path)
            expe.close(delete=True)
