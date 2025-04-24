@echo off
docker run --rm --network host -v %cd%:/app final_project
pause