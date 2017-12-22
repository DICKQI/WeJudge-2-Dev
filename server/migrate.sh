#!/bin/sh
echo "==== WeJudge Model Migration ====";
echo " PASS ANY KEY TO MAKE MIGRATIONS ";
echo "=================================";
read p;
python3 manage.py makemigrations
echo "\n ===== Done.";
echo "PASS ANY KEY TO APPLY YOUR CHANGED";
read p;
python3 manage.py migrate
echo "\n ===== ALL Done. Bye!";
