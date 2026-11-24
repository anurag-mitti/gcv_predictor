import numpy as np
import pandas as pd

def compute_engineered_features(df):
    """
    Computes domain geochemical interaction terms from standard proximate analysis.
    Input df contains: 'Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio'.
    """
    df = df.copy()
    m = df['Moisture']
    vm = df['Volatile Matter']
    ash = df['Standard Ash']
    fc = df['Fixed Carbon']
    
    df['Combustible_Fraction'] = fc + vm
    df['Inert_Ballast'] = m + ash
    df['Ballast_Combustible_Ratio'] = (m + ash) / (fc + vm + 1e-4)
    df['FC_x_VM'] = fc * vm
    df['Ash_x_M'] = ash * m
    df['Volatile_in_Combustibles'] = vm / (fc + vm + 1e-4)
    df['Ash_FC_Ratio'] = ash / (fc + 1e-4)
    df['Thermal_Inert_Factor'] = (m * 2.26) + (ash * 0.84)
    
    return df

class MoEPipeline:
    def __init__(self, univ_stack, bit_stack, gating_clf, feature_cols):
        self.univ_stack = univ_stack
        self.bit_stack = bit_stack
        self.gating_clf = gating_clf
        self.feature_cols = feature_cols
        
    def predict_components(self, input_df_raw):
        X_eng = compute_engineered_features(input_df_raw)[self.feature_cols]
        
        # 1. Universal prediction
        u_oof = np.column_stack([m.predict(X_eng) for _, m in self.univ_stack['models']])
        pred_u = self.univ_stack['meta'].predict(u_oof)
        
        # 2. Bituminous prediction
        b_oof = np.column_stack([m.predict(X_eng) for _, m in self.bit_stack['models']])
        pred_b = self.bit_stack['meta'].predict(b_oof)
        
        # 3. Gating weight
        prob_bit = self.gating_clf.predict_proba(X_eng)[:, 1]
        
        # 4. MoE Blended prediction
        pred_moe = (prob_bit * pred_b) + ((1.0 - prob_bit) * pred_u)
        
        return {
            'pred_moe': pred_moe,
            'pred_u': pred_u,
            'pred_b': pred_b,
            'prob_bit': prob_bit
        }
        
    def predict(self, input_df_raw):
        return self.predict_components(input_df_raw)['pred_moe']
