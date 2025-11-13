# app.py
import json
import pickle
import io
import os
import traceback

import pandas as pd
import numpy as np
import gradio as gr
from pathlib import Path

ROOT = Path(__file__).parent

# Filenames (adjust if different)
MODEL_FILE = ROOT / "portfolio_risk_model (1).pkl"
PARAMS_FILE = ROOT / "model_parameters.json"
ANALYSIS_IMAGE = ROOT / "portfolio_risk_analysis.png"

# Load model (pickle)
def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_FILE}")
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    return model

# Load model parameter metadata (optional)
def load_params():
    if not PARAMS_FILE.exists():
        return {}
    with open(PARAMS_FILE, "r") as f:
        return json.load(f)

MODEL = None
PARAMS = {}
try:
    MODEL = load_model()
    PARAMS = load_params()
except Exception as e:
    # If something fails on import, we still want the app to start and show the error
    MODEL = None
    PARAMS = {"_load_error": str(e), "_trace": traceback.format_exc()}

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Try to select expected features if present in PARAMS.
    If no features listed in PARAMS, assume the dataframe columns match what model expects.
    """
    features = PARAMS.get("feature_names") or PARAMS.get("features") or []
    if features:
        missing = [c for c in features if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required feature columns in uploaded CSV: {missing}")
        return df[features]
    # if no feature list provided, return df as-is
    return df

def predict_from_csv(file_obj):
    if MODEL is None:
        return {"error": "Model failed to load. See logs."}
    try:
        # read CSV (supports file-like objects)
        df = pd.read_csv(file_obj)
        X = preprocess_dataframe(df)
        # if model expects 1D array for a single number, adapt accordingly
        preds = MODEL.predict(X)
        # attach probabilities if available
        proba = None
        if hasattr(MODEL, "predict_proba"):
            proba = MODEL.predict_proba(X).tolist()
        # build results
        results = {
            "predictions": preds.tolist() if hasattr(preds, "tolist") else list(preds),
            "probabilities": proba,
            "n_rows": len(X)
        }
        return results
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

def predict_from_manual(values_dict):
    """values_dict is a mapping feature->value from Gradio inputs"""
    if MODEL is None:
        return {"error": "Model failed to load. See logs."}
    try:
        # Build a single-row DataFrame in expected feature order
        features = PARAMS.get("feature_names") or PARAMS.get("features") or list(values_dict.keys())
        row = {k: float(values_dict.get(k, 0)) for k in features}
        X = pd.DataFrame([row], columns=features)
        preds = MODEL.predict(X)
        proba = None
        if hasattr(MODEL, "predict_proba"):
            proba = MODEL.predict_proba(X).tolist()
        return {
            "predictions": preds.tolist(),
            "probabilities": proba
        }
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

# Build Gradio UI
with gr.Blocks(title="Portfolio Risk Prediction") as demo:
    gr.Markdown("## Portfolio Risk Predictor\nUpload a CSV containing your features (column names must match) or enter a single sample manually.")
    with gr.Row():
        with gr.Column(scale=2):
            file_input = gr.File(label="Upload CSV", file_types=[".csv"])
            predict_btn = gr.Button("Predict from CSV")
            csv_output = gr.JSON(label="CSV Prediction Result")
            # Manual input section: create inputs for each feature if known in PARAMS
            gr.Markdown("### Manual input (single sample)")
            manual_inputs = []
            features = PARAMS.get("feature_names") or PARAMS.get("features") or []
            if features:
                for f in features:
                    manual_inputs.append(gr.Number(label=f, value=0.0))
            else:
                gr.Markdown("No feature list found in `model_parameters.json`. Provide a CSV instead or add `feature_names` to the JSON.")
            manual_predict_btn = gr.Button("Predict from Manual Input")
            manual_output = gr.JSON(label="Manual Prediction Result")
        with gr.Column(scale=1):
            if ANALYSIS_IMAGE.exists():
                gr.Image(str(ANALYSIS_IMAGE), label="Analysis image")
            else:
                gr.Markdown("_No analysis image found in repository_")
            if PARAMS.get("_load_error"):
                gr.Markdown("**Model load error:**")
                gr.Textbox(value=PARAMS["_load_error"], lines=6, interactive=False)
    # Hook up events
    predict_btn.click(fn=predict_from_csv, inputs=[file_input], outputs=[csv_output])
    if features:
        manual_predict_btn.click(
            fn=lambda *vals: predict_from_manual({features[i]: vals[i] for i in range(len(features))}),
            inputs=manual_inputs,
            outputs=manual_output,
        )

if __name__ == "__main__":
    demo.launch()
