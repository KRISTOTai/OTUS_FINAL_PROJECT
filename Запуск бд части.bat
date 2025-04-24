@echo off
docker run --rm --network host -v %cd%:/app final_project tests/test_db_opencart.py
pause