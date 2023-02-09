@ECHO off

IF NOT "%~1"=="" (
	GOTO CONTENT
) ELSE (
	GOTO ERRORS
)

:CONTENT
IF /I "%1"=="-e" (
	IF "%~2"=="" GOTO ERRORS
	curl -X POST localhost:5000/evaluate -H "Content-Type: application/json" -d "{\"expression\":\"%2\"}"
) ELSE IF /I "%1"=="-h" (
	curl localhost:5000/history
) ELSE (
	GOTO ERRORS
)
GOTO :EOF

:ERRORS
ECHO Unrecognized operation
ECHO Evaluate: interface -e ^<expression^>
ECHO History: interface -h