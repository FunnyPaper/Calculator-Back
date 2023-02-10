@ECHO off
setlocal ENABLEDELAYEDEXPANSION

IF NOT "%~1"=="" (
	GOTO CONTENT
) ELSE (
	GOTO ERRORS
)

:CONTENT
IF /I "%1"=="-e" (
	IF "%~2"=="" GOTO ERRORS
	IF "%~3"=="" GOTO ERRORS
	
	curl -X POST localhost:5000/evaluate -H "Content-Type: application/json" -d "{\"expression\":\"%2\",\"options\":{\"rad\": %3}}"
) ELSE IF /I "%1"=="-h" (
	curl localhost:5000/history
) ELSE (
	GOTO ERRORS
)
GOTO :EOF

:ERRORS
ECHO Unrecognized operation
ECHO Evaluate: interface -e ^<expression: string^> ^<radians: boolean^>
ECHO History: interface -h
