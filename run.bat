@echo off
echo 🏆 Let's Beat the STAPS! Preparing your environment...
python -m venv env
call env\Scripts\activate
pip install selenium requests
echo 🎉 Environment ready! Launching the YouTube runner.
python LetsBeatTheSTAPS.py
echo 🎬 Contest finished. Hope you enjoyed beating the STAPS!
pause
