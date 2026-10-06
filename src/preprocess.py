import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def main():
    print("Loading data...")
    # Load dataset
    df = pd.read_csv('CQ20261065053.CSV', low_memory=False)
    
    # Strip leading/trailing whitespaces from column names
    df.columns = df.columns.str.strip()
    
    # Select needed columns
    cols = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Btu']
    df = df[cols].copy()
    
    print("Converting to numeric...")
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Drop rows where target or key feature (VM) is missing, as we only impute Ash & Moisture
    df.dropna(subset=['Btu', 'Volatile Matter'], inplace=True)
    
    print("Applying Unit Conversion...")
    # Unit conversion: Btu to GCV (Kcal/kg)
    df['GCV'] = df['Btu'] / 1.8
    df.drop(columns=['Btu'], inplace=True)
    
    print("Applying Domain-Specific Filtering...")
    # Domain-Specific Filtering: Ash <= 50 and GCV >= 2000
    # Also considering NaNs in Ash for filtering logic: keep them for imputation
    cond_ash = (df['Standard Ash'] <= 50) | (df['Standard Ash'].isna())
    cond_gcv = (df['GCV'] >= 2000)
    df = df[cond_ash & cond_gcv].copy()
    
    print("Applying KNN Imputation...")
    
    # Imputation: KNN-Imputer for Moisture and Ash
    imputer = KNNImputer(n_neighbors=5)
    imputed_data = imputer.fit_transform(df[['Moisture', 'Volatile Matter', 'Standard Ash', 'GCV']])
    df[['Moisture', 'Volatile Matter', 'Standard Ash', 'GCV']] = imputed_data
    
    print("Removing Outliers using IQR...")

    # remove outliers using iqr
    def remove_outliers_iqr(df_in, col_name):
        q1 = df_in[col_name].quantile(0.25)
        q3 = df_in[col_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return df_in[(df_in[col_name] >= lower_bound) & (df_in[col_name] <= upper_bound)]

    for col in ['Moisture', 'Volatile Matter', 'Standard Ash', 'GCV']:
        df = remove_outliers_iqr(df, col)
        
    print("Enforcing Mass Balance & Engineering Features...")
    # Mass Balance Enforcement
    df['Fixed Carbon'] = 100 - (df['Standard Ash'] + df['Moisture'] + df['Volatile Matter'])
    
    # Keep only physically possible rows (e.g. Fixed Carbon > 0)
    df = df[df['Fixed Carbon'] > 0]
    
    # Feature Engineering
    df['Fuel_Ratio'] = df['Fixed Carbon'] / df['Volatile Matter']
    
    print(f"Data preprocessing complete. Final dataset size: {len(df)} rows.")
    df.to_csv('data/processed_coal.csv', index=False)
    print("Saved to data/processed_coal.csv")

if __name__ == '__main__':
    main()
