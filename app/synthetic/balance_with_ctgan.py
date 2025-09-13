import argparse
import os
import pandas as pd
import numpy as np
from ctgan import CTGAN   # <-- THIS, not "from sdv.tabular import CTGAN"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, help="Path to imbalanced input CSV (must have sex,label,score)")
    p.add_argument("--out", required=True, help="Path to write balanced CSV")
    p.add_argument("--target_ratio", type=float, default=0.5, help="Target female ratio (default 0.5)")
    p.add_argument("--epochs", type=int, default=300, help="CTGAN training epochs (default 300)")
    p.add_argument("--seed", type=int, default=42, help="Random seed")
    args = p.parse_args()

    np.random.seed(args.seed)

    # 1) Load dataset
    df = pd.read_csv(args.csv, comment="#", on_bad_lines="skip", engine="python")

    required = {"sex", "label", "score"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Normalize sex values (M/F/O)
    df["sex"] = (
        df["sex"].astype(str).str.upper().str[0].map({"M": "M", "F": "F"}).fillna("O")
    )

    n = len(df)
    n_f = int((df["sex"] == "F").sum())
    n_m = int((df["sex"] == "M").sum())
    n_o = n - n_f - n_m
    current_ratio = n_f / n if n else 0.0
    print(f"[INFO] Current counts: M={n_m}, F={n_f}, O={n_o}  (female ratio={current_ratio:.3f})")

    # How many synthetic females do we need to hit target_ratio?
    target_f = int(round(args.target_ratio * n))
    needed_f = max(0, target_f - n_f)
    if needed_f == 0:
        print("[INFO] Already balanced. Writing copy to --out.")
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        df.to_csv(args.out, index=False)
        print(f"[OK] Wrote: {args.out}")
        return

    # 2) Train CTGAN on FEMALE subset only
    df_f = df[df["sex"] == "F"].copy()
    if df_f.empty:
        raise ValueError("No female rows available to learn from.")

    discrete_cols = ["sex", "label"]  # categorical columns
    print(f"[INFO] Training CTGAN on {len(df_f)} female rows for {args.epochs} epochs...")
    ctgan = CTGAN(epochs=args.epochs, verbose=True)

    ctgan.fit(df_f, discrete_columns=discrete_cols)

    # 3) Sample synthetic females
    print(f"[INFO] Sampling {needed_f} synthetic female rows...")
    syn_f = ctgan.sample(needed_f)

    # Force proper values
    syn_f["sex"] = "F"
    syn_f["label"] = syn_f["label"].round().clip(0, 1).astype(int)
    syn_f["score"] = syn_f["score"].clip(0.0, 1.0)

    # 4) Merge & save
    df_bal = pd.concat([df, syn_f], ignore_index=True)
    df_bal = df_bal.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)

    n_bal = len(df_bal)
    n_f_bal = int((df_bal["sex"] == "F").sum())
    ratio_bal = n_f_bal / n_bal if n_bal else 0
    print(f"[INFO] Balanced counts: total={n_bal}, female={n_f_bal} (ratio={ratio_bal:.3f})")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df_bal.to_csv(args.out, index=False)
    print(f"[OK] Wrote balanced CSV: {args.out}")

if __name__ == "__main__":
    main()
