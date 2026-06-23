#!/bin/bash
# esegue i chunk mancanti di p=40 finché restano <230s di budget
BUDGET=230
START=$(date +%s)
DONE=$(wc -l < gamma40.log)
for i in $(seq $DONE 15); do
  NOW=$(date +%s); ELAPSED=$((NOW-START))
  if [ $ELAPSED -gt 120 ]; then echo "budget esaurito, fatti $i/16"; exit 0; fi
  ./gamma_enum part 40 4 $i | tail -1 >> gamma40.log
  echo "chunk $i ok"
done
echo "p=40 COMPLETO"
