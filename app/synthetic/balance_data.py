import argparse
import os
import pandas as pd
import numpy as np

from ctgan import CTGAN
from imblearn.over_sampling import SMOTE

def balance_with_ctgan(df, target_ratio, epochs, seed):
    df_f = df[df["sex"] == "F"].copy()
    if df_f.empty:
        raise ValueError("No female rows available to learn from.")

    ctgan = CTGAN(epochs=epochs, verbose=True)
    ctgan.fit(df_f, discrete_columns=["sex", "label"])

    n = len(df)
    n_f = (df["sex"] == "F").sum()
    needed_f = int(round(target_ratio * n)) - n_f
    syn_f = ctgan.sample(needed_f)

    syn_f["sex"] = "F"
    syn_f["label"] = syn_f["label"].round().clip(0, 1).astype(int)
    syn_f["score"] = syn_f["score"].clip(0.0, 1.0)

    return pd.concat([df, syn_f], ignore_index=True)

def balance_with_smote(df):
    df_copy = df.copy()
    X = df_copy.drop(columns=["sex"])
    y = df_copy["sex"]

    smote = SMOTE()
    X_res, y_res = smote.fit_resample(X, y)

    df_bal = pd.DataFrame(X_res)
    df_bal["sex"] = y_res
    return df_bal

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--method", choices=["ctgan", "smote"], default="ctgan")
    p.add_argument("--target_ratio", type=float, default=0.5)
    p.add_argument("--epochs", type=int, default=300)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    np.random.seed(args.seed)
    df = pd.read_csv(args.csv, comment="#", on_bad_lines="skip", engine="python")
    df["sex"] = df["sex"].astype(str).str.upper().str[0].map({"M": "M", "F": "F"}).fillna("O")

    if args.method == "ctgan":
        df_bal = balance_with_ctgan(df, args.target_ratio, args.epochs, args.seed)
    elif args.method == "smote":
        df_bal = balance_with_smote(df)
    else:
        raise ValueError(f"Unsupported method: {args.method}")

    df_bal = df_bal.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df_bal.to_csv(args.out, index=False)
    print(f"[OK] Wrote balanced CSV to {args.out}")

if __name__ == "__main__":
    main()
