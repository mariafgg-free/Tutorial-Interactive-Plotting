
import anywidget
import traitlets
import pathlib
import pandas as pd
import numpy as np

class WellLogWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "index.js"
    options = traitlets.Dict().tag(sync=True)

    def set_complex_plot(self, df):
        # 1. Data Prep (Exact same logic as your snippet)
        df = df.sort_values(by='Depth')
        depth = df['Depth'].values
        
        # Calculate RHOB if missing (using your formula)
        if 'RHOB' not in df.columns and 'DENPHI' in df.columns:
             df['RHOB'] = df['DENPHI']/100*(1-2.65)+2.65
        
        # Mapping columns
        gr = df['GR'].values
        cali = df['CALI'].values
        rild = df['RT'].values # Deep
        rsfl = df['RS'].values # Shallow/Spherical
        rhob = df['RHOB'].values
        nphi = df['NPHI'].values / 100 # Convert to decimal 0.6 - 0
        dt = df['DT'].values

        nphi_on_rhob_scale = 2.65 + (nphi * -1.666667)
        
        
        # Helper to zip data [value, depth]
        def to_list(arr): return list(zip(arr.tolist(), depth.tolist()))

        self.options = {
            "animation": False,
            "dataZoom": [
                {"type": "inside", "yAxisIndex": [0,1,2,3], "start": 0, "end": 100},
                {"type": "slider", "yAxisIndex": [0,1,2,3], "left": "96%"}
            ],
            # --- LAYOUT (4 Tracks) ---
            "grid": [
                {"left": "2%", "width": "20%", "bottom": "2%", "top": 120, "containLabel": True}, # T1: GR/CALI
                {"left": "24%", "width": "20%", "bottom": "2%", "top": 120, "containLabel": True}, # T2: Resistivity
                {"left": "46%", "width": "20%", "bottom": "2%", "top": 120, "containLabel": True}, # T3: Density/Neutron
                {"left": "68%", "width": "20%", "bottom": "2%", "top": 120, "containLabel": True}  # T4: Sonic
            ],
            "yAxis": [
                {"gridIndex": 0, "inverse": True, "min": min(depth), "max": max(depth), "name": "Depth"},
                {"gridIndex": 1, "inverse": True, "min": min(depth), "max": max(depth), "show": False},
                {"gridIndex": 2, "inverse": True, "min": min(depth), "max": max(depth), "show": False},
                {"gridIndex": 3, "inverse": True, "min": min(depth), "max": max(depth), "show": False},
            ],
            "xAxis": [
                # --- TRACK 1 (GR & CALI) ---
                {
                    "gridIndex": 0, "position": "top", "min": 0, "max": 150,
                    "name": "GR", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "green"}}, "axisLabel": {"color": "green"},
                    "nameTextStyle": {"color": "green", "fontWeight": "bold"}
                },
                {
                    "gridIndex": 0, "position": "top", "min": 5, "max": 20, "offset": 40,
                    "name": "CALI", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "black"}}, "axisLabel": {"color": "black"},
                    "nameTextStyle": {"color": "black", "fontWeight": "bold"}
                },

                # --- TRACK 2 (Resistivity) ---
                {
                    "gridIndex": 1, "position": "top", "type": "log", "min": 0.2, "max": 200,
                    "name": "RILD", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "red"}}, "axisLabel": {"color": "red"},
                    "nameTextStyle": {"color": "red"}
                },
                {
                    "gridIndex": 1, "position": "top", "type": "log", "min": 0.2, "max": 200, "offset": 40,
                    "name": "RSFL", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "blue"}}, "axisLabel": {"color": "blue"},
                    "nameTextStyle": {"color": "blue"}
                },

                # --- TRACK 3 (Density / Neutron) ---
                {
                    "gridIndex": 2, "position": "top", "min": 1.65, "max": 2.65,
                    "name": "RHOB", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "red"}}, "axisLabel": {"color": "red"},
                    "nameTextStyle": {"color": "red"}
                },
                {
                    "gridIndex": 2, "position": "top", "min": -0.1, "max": 0.6, "inverse": True, "offset": 40,
                    "name": "NPHI", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "blue"}}, "axisLabel": {"color": "blue"},
                    "nameTextStyle": {"color": "blue"}
                },

                # --- TRACK 4 (Sonic) ---
                {
                    "gridIndex": 3, "position": "top", "min": 50, "max": 150, "inverse": True, # Reversed 150-50
                    "name": "DT", "nameLocation": "middle", "nameGap": 30,
                    "axisLine": {"lineStyle": {"color": "purple"}}, "axisLabel": {"color": "purple"},
                    "nameTextStyle": {"color": "purple"}
                }
            ],
            "series": [
                # T1
                {"name": "GR", "xAxisIndex": 0, "yAxisIndex": 0, "data": to_list(gr), "type": "line", "showSymbol": False, "lineStyle": {"color": "green"}},
                {"name": "CALI", "xAxisIndex": 1, "yAxisIndex": 0, "data": to_list(cali), "type": "line", "showSymbol": False, "lineStyle": {"color": "black", "type": "dashed"}},
                
                # T2
                {"name": "RILD", "xAxisIndex": 2, "yAxisIndex": 1, "data": to_list(rild), "type": "line", "showSymbol": False, "lineStyle": {"color": "red"}},
                {"name": "RSFL", "xAxisIndex": 3, "yAxisIndex": 1, "data": to_list(rsfl), "type": "line", "showSymbol": False, "lineStyle": {"color": "blue"}},
                
                # T3
                # Draw RHOB
                {"name": "RHOB", "xAxisIndex": 4, "yAxisIndex": 2, "data": to_list(rhob), "type": "line", "showSymbol": False, "lineStyle": {"color": "red"}},
                # Draw NPHI (on its own axis index 5)
                {"name": "NPHI", "xAxisIndex": 5, "yAxisIndex": 2, "data": to_list(nphi), "type": "line", "showSymbol": False, "lineStyle": {"color": "blue", "type": "dashed"}},
                
                # T4
                {"name": "DT", "xAxisIndex": 6, "yAxisIndex": 3, "data": to_list(dt), "type": "line", "showSymbol": False, "lineStyle": {"color": "purple"}}
            ]
        }
