@echo off
echo Installing dependencies for Hotel Agent...

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install PyTorch first using the official method
echo Installing PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

REM Install other requirements
echo Installing other dependencies...
pip install streamlit pandas scikit-learn transformers

echo Installation complete!
echo To run the application, use: streamlit run app/main.py
pause
