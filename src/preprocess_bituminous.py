"""
src/preprocess_bituminous.py
Specialized preprocessing pipeline for ASTM D388 Bituminous Coal.
Filters bituminous rank coal, enforces zero target leakage, and calculates proximate mass balance.
"""

import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def main():
    print("Loading raw coal laboratory dataset for Bituminous filtering...")
    raw_path = 'CQ20261065053.CSV'
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"{raw_path} not found.")

    df = pd.read_csv(raw_path, low_memory=False)
    df.columns = df.columns.str.strip()

    cols = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Btu', 'Btu Moist MMF', 'VM Dry MMF', 'Fixed C Dry MMF']
    df = df[cols].copy()

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Target GCV must be available
    df.dropna(subset=['Btu'], inplace=True)
    df['GCV'] = df['Btu'] / 1.8
    df.drop(columns=['Btu'], inplace=True)

    # ASTM D388 Standard Classification for Bituminous Coal:
    # Moist MMF Btu >= 10,500 Btu/lb, Dry MMF Volatile Matter >= 14%, Dry MMF Fixed Carbon < 86%
    bituminous_cond = (
        (df['Btu Moist MMF'] >= 10500) &
        (df['VM Dry MMF'] >= 14.0) &
        (df['Fixed C Dry MMF'] < 86.0)
    )
    df = df[bituminous_cond].copy()
    print(f"Identified {len(df)} samples matching ASTM D388 Bituminous rank.")

    # Domain physical limits for bituminous coal
    cond = (
        (df['GCV'] >= 2500) & (df['GCV'] <= 9000) &
        (df['Standard Ash'].isna() | ((df['Standard Ash'] >= 0) & (df['Standard Ash'] <= 50))) &
        (df['Moisture'].isna() | ((df['Moisture'] >= 0) & (df['Moisture'] <= 30))) &
        (df['Volatile Matter'].isna() | ((df['Volatile Matter'] >= 14) & (df['Volatile Matter'] <= 55)))
    )
    df = df[cond].copy()

    # Zero-Target-Leakage Feature Imputation
    feature_cols = ['Moisture', 'Volatile Matter', 'Standard Ash']
    imputer = KNNImputer(n_neighbors=5)
    df[feature_cols] = imputer.fit_transform(df[feature_cols])

    # Outlier filtering with IQR
    def remove_outliers_iqr(df_in, col_name):
        q1 = df_in[col_name].quantile(0.25)
        q3 = df_in[col_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return df_in[(df_in[col_name] >= lower_bound) & (df_in[col_name] <= upper_bound)]

    for col in ['Moisture', 'Volatile Matter', 'Standard Ash', 'GCV']:
        df = remove_outliers_iqr(df, col)

    # Mass balance and feature engineering
    df['Fixed Carbon'] = 100.0 - (df['Standard Ash'] + df['Moisture'] + df['Volatile Matter'])
    df = df[df['Fixed Carbon'] > 0].copy()
    df['Fuel_Ratio'] = df['Fixed Carbon'] / df['Volatile Matter']

    out_cols = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio', 'GCV']
    df = df[out_cols].copy()

    os.makedirs('data', exist_ok=True)
    out_path = 'data/processed_coal_bituminous.csv'
    df.to_csv(out_path, index=False)
    print(f"Preprocessed {len(df)} clean Bituminous coal samples saved to: {out_path}")

if __name__ == '__main__':
    main()
