import os
import io
import time
import tempfile
import tracemalloc
import cProfile
import pstats

import numpy as np
import pandas as pd
from cleaningbox import cleaningbox


# ---------------------------
# Data generation
# ---------------------------
def make_data(n=100_000, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "age": rng.normal(35, 10, n),
        "salary": rng.lognormal(11, 0.5, n),
        "dept": rng.choice(["HR", "Mkt", "Fin", "Eng"], n),
        "remote": rng.choice(["yes", "no"], n),
    })
    mask = rng.random(n) < 0.10
    df.loc[mask, "age"] = np.nan
    df.loc[mask, "dept"] = None
    return df


def write_tmp_csv(df) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    df.to_csv(tmp.name, index=False)
    tmp_path = tmp.name
    tmp.close()
    return tmp_path


# ---------------------------
# Pipelines (read from same CSV)
# ---------------------------
def cb_pipeline_from_path(path: str) -> pd.DataFrame:
    cb = cleaningbox()
    cb.load_data(dataset=path)
    cb.imputation()
    cb.normalization(method="minmax")
    cb.one_hot_encoding(columns=["dept"])
    cb.outlier(method="zscore", action="detect")
    return cb.get_data()


def pandas_pipeline_from_path(path: str) -> pd.DataFrame:
    out = pd.read_csv(path)
    # impute numeric: median
    out["age"] = out["age"].fillna(out["age"].median())
    # impute categorical: mode
    out["dept"] = out["dept"].fillna(out["dept"].mode(dropna=True).iloc[0])
    # normalization (min-max) for numeric
    for c in ["age", "salary"]:
        col_min = out[c].min()
        col_max = out[c].max()
        # guard against zero range
        out[c] = 0.0 if col_max == col_min else (out[c] - col_min) / (col_max - col_min)
    out = pd.get_dummies(out, columns=["dept"], drop_first=True)
    _z = (out["salary"] - out["salary"].mean()) / out["salary"].std(ddof=0)
    _detected = out[abs(_z) > 3]
    return out


# ---------------------------
# Timing helpers
# ---------------------------
def timeit(fn, *args, **kwargs):
    """Return (seconds, peak_MB) for a single call."""
    tracemalloc.start()
    t0 = time.perf_counter()
    _ = fn(*args, **kwargs)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return (t1 - t0), peak / (1024 ** 2)


def bench_once(path: str):
    t_cb, m_cb = timeit(cb_pipeline_from_path, path)
    t_pd, m_pd = timeit(pandas_pipeline_from_path, path)
    return t_cb, m_cb, t_pd, m_pd


def bench_sizes(sizes=(10_000, 50_000, 100_000), repeats=5, seed=0):
    for n in sizes:
        df = make_data(n=n, seed=seed)
        path = write_tmp_csv(df)
        try:
            sum_cb = sum_pd = 0.0
            peak_cb = peak_pd = 0.0
            for _ in range(repeats):
                t_cb, m_cb, t_pd, m_pd = bench_once(path)
                sum_cb += t_cb
                sum_pd += t_pd
                peak_cb = max(peak_cb, m_cb)
                peak_pd = max(peak_pd, m_pd)
            avg_cb = sum_cb / repeats
            avg_pd = sum_pd / repeats
            speedup_pct = (avg_pd - avg_cb) / avg_pd * 100
            print(f"{n:>6} rows | CB: {avg_cb:.3f}s {peak_cb:.1f}MB | "
                  f"Pandas: {avg_pd:.3f}s {peak_pd:.1f}MB | Δspeed: {speedup_pct:+.1f}% (avg of {repeats})")
        finally:
            try:
                os.remove(path)
            except PermissionError:
                pass


# ---------------------------
# Optional: cProfile for CleaningBox
# ---------------------------
def profile_cb(path: str, sort="cumtime", top=25):
    pr = cProfile.Profile()
    pr.enable()
    _ = cb_pipeline_from_path(path)
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats(sort).print_stats(top)
    print("\n=== cProfile (CleaningBox) — top by", sort, "===")
    print(s.getvalue())


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    bench_sizes(sizes=(10_000, 50_000, 100_000), repeats=5, seed=0)

'''
Code was run locally via the Windows Command Prompt (CMD), executing this script as a standalone file. 
The benchmark was repeated 10 times independently.

Outputs:
Benchmark 1
 10000 rows | CB: 0.034s 1.4MB | Pandas: 0.018s 1.3MB | Δspeed: -86.7% (avg of 5)
 50000 rows | CB: 0.084s 6.9MB | Pandas: 0.052s 6.5MB | Δspeed: -63.3% (avg of 5)
100000 rows | CB: 0.139s 13.9MB | Pandas: 0.090s 13.0MB | Δspeed: -55.5% (avg of 5)

Benchmark 2
 10000 rows | CB: 0.034s 1.4MB | Pandas: 0.018s 1.3MB | Δspeed: -88.6% (avg of 5)
 50000 rows | CB: 0.082s 6.9MB | Pandas: 0.051s 6.5MB | Δspeed: -62.1% (avg of 5)
100000 rows | CB: 0.142s 13.9MB | Pandas: 0.090s 13.0MB | Δspeed: -57.0% (avg of 5)

Benchmark 3
 10000 rows | CB: 0.034s 1.4MB | Pandas: 0.018s 1.3MB | Δspeed: -88.6% (avg of 5)
 50000 rows | CB: 0.081s 6.9MB | Pandas: 0.051s 6.5MB | Δspeed: -58.7% (avg of 5)
100000 rows | CB: 0.139s 13.9MB | Pandas: 0.089s 13.0MB | Δspeed: -55.2% (avg of 5)

Benchmark 4
 10000 rows | CB: 0.034s 1.4MB | Pandas: 0.019s 1.3MB | Δspeed: -79.5% (avg of 5)
 50000 rows | CB: 0.080s 6.9MB | Pandas: 0.051s 6.5MB | Δspeed: -57.1% (avg of 5)
100000 rows | CB: 0.140s 13.9MB | Pandas: 0.090s 13.0MB | Δspeed: -55.5% (avg of 5)

Benchmark 5
 10000 rows | CB: 0.035s 1.4MB | Pandas: 0.019s 1.3MB | Δspeed: -84.3% (avg of 5)
 50000 rows | CB: 0.082s 6.9MB | Pandas: 0.051s 6.5MB | Δspeed: -60.7% (avg of 5)
100000 rows | CB: 0.141s 13.9MB | Pandas: 0.090s 13.0MB | Δspeed: -56.7% (avg of 5)

Benchmark 6
 10000 rows | CB: 0.038s 1.4MB | Pandas: 0.020s 1.3MB | Δspeed: -92.2% (avg of 5)
 50000 rows | CB: 0.083s 6.9MB | Pandas: 0.053s 6.5MB | Δspeed: -54.9% (avg of 5)
100000 rows | CB: 0.143s 13.9MB | Pandas: 0.091s 13.0MB | Δspeed: -57.6% (avg of 5)

Benchmark 7
 10000 rows | CB: 0.035s 1.4MB | Pandas: 0.019s 1.3MB | Δspeed: -84.3% (avg of 5)
 50000 rows | CB: 0.080s 6.9MB | Pandas: 0.052s 6.5MB | Δspeed: -54.2% (avg of 5)
100000 rows | CB: 0.144s 13.9MB | Pandas: 0.090s 13.0MB | Δspeed: -59.4% (avg of 5)

Benchmark 8
 10000 rows | CB: 0.036s 1.4MB | Pandas: 0.019s 1.3MB | Δspeed: -86.3% (avg of 5)
 50000 rows | CB: 0.081s 6.9MB | Pandas: 0.052s 6.5MB | Δspeed: -57.9% (avg of 5)
100000 rows | CB: 0.144s 13.9MB | Pandas: 0.092s 13.0MB | Δspeed: -55.5% (avg of 5)

Benchmark 9
 10000 rows | CB: 0.037s 1.4MB | Pandas: 0.020s 1.3MB | Δspeed: -81.7% (avg of 5)
 50000 rows | CB: 0.081s 6.9MB | Pandas: 0.052s 6.5MB | Δspeed: -53.6% (avg of 5)
100000 rows | CB: 0.139s 13.9MB | Pandas: 0.092s 13.0MB | Δspeed: -52.3% (avg of 5)

Benchmark 10
 10000 rows | CB: 0.034s 1.4MB | Pandas: 0.019s 1.3MB | Δspeed: -81.3% (avg of 5)
 50000 rows | CB: 0.081s 6.9MB | Pandas: 0.052s 6.5MB | Δspeed: -56.3% (avg of 5)
100000 rows | CB: 0.142s 13.9MB | Pandas: 0.091s 13.0MB | Δspeed: -55.5% (avg of 5)
'''
