import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def main():
    print("Loading raw coal laboratory dataset...")
    df = pd.read_csv('CQ20261065053.CSV', low_memory=False)
    
    # Clean whitespace in column headers
    df.columns = df.columns.str.strip()
    
    # Select proximate features and target
    cols = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Btu']
    df = df[cols].copy()
    
    print("Parsing numerical formats...")
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Drop rows without target (Btu)
    df.dropna(subset=['Btu'], inplace=True)
    
    print("Converting Units: Btu/lb -> GCV (Kcal/kg)...")
    df['GCV'] = df['Btu'] / 1.8
    df.drop(columns=['Btu'], inplace=True)
    
    print("Applying Domain-Specific Physical Validity Filtering...")
    # Realistic physical limits for coal combustion
    cond = (
        (df['GCV'] >= 2000) & (df['GCV'] <= 9000) &
        (df['Standard Ash'].isna() | ((df['Standard Ash'] >= 0) & (df['Standard Ash'] <= 55))) &
        (df['Moisture'].isna() | ((df['Moisture'] >= 0) & (df['Moisture'] <= 45))) &
        (df['Volatile Matter'].isna() | ((df['Volatile Matter'] >= 0) & (df['Volatile Matter'] <= 60)))
    )
    df = df[cond].copy()
    
    print("Applying Zero-Target-Leakage KNN Imputation (Features Only)...")
    # Impute missing feature values ONLY using other features, NEVER the target GCV
    feature_cols = ['Moisture', 'Volatile Matter', 'Standard Ash']
    imputer = KNNImputer(n_neighbors=5)
    df[feature_cols] = imputer.fit_transform(df[feature_cols])
    
    print("Removing Measurement Outliers (IQR)...")
    def remove_outliers_iqr(df_in, col_name):
        q1 = df_in[col_name].quantile(0.25)
        q3 = df_in[col_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return df_in[(df_in[col_name] >= lower_bound) & (df_in[col_name] <= upper_bound)]

    for col in ['Moisture', 'Volatile Matter', 'Standard Ash', 'GCV']:
        df = remove_outliers_iqr(df, col)
        
    print("Enforcing Mass Balance & Feature Engineering...")
    # Fixed Carbon = 100 - (Moisture + Volatile Matter + Standard Ash)
    df['Fixed Carbon'] = 100.0 - (df['Standard Ash'] + df['Moisture'] + df['Volatile Matter'])
    
    # Retain only physically valid mass balance (Fixed Carbon > 0)
    df = df[df['Fixed Carbon'] > 0].copy()
    
    # Fuel Ratio: Key coal ranking metric
    df['Fuel_Ratio'] = df['Fixed Carbon'] / df['Volatile Matter']
    
    print(f"Data preprocessing complete. Final dataset size: {len(df)} samples.")
    df.to_csv('data/processed_coal.csv', index=False)
    print("Saved clean, zero-leakage dataset to data/processed_coal.csv")

if __name__ == '__main__':
    main()
